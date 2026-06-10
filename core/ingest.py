# core/ingest.py
# Velantrim ExoCortex — Ingestion Layer
# v8.4.0-sprint2
#
# Purpose: turn a user's utterance into a fact with the right modality
# (claim_type) and origin (source_status), run it through the same gates
# (Guardian → TruthGate) and write it into the L3 canon. This "brings to life" the subjective path:
# now EMOTION / OPINION / GOAL are born from live input, not only from the corpus.
#
# The classifier is heuristic (no LLM dependency): it catches markers of feeling,
# opinion, goal, preference, conjecture; otherwise — a claim about the world.
# Replacing it with an LLM classifier is a separate step (see the core/generation.py pattern).

import hashlib
import re
from typing import Dict, Any, Optional

from core.memory import store_fact, get_fact, transition_esm
from core.l3_graph import get_l3_graph
from core.embedding import assert_compatible_embedder
from core.pipeline import guardian, truth_gate, _truth_status_for, _l3_payload
from core.reconcile import reinforce, find_conflicts, REL_CONTRADICTS, _now
from core import metrics, adaptation, pii, contradiction, immune, neurogenesis

# Modality markers (RU + EN). Order matters: we check from specific to general.
_CLAIM_MARKERS = [
    ("EMOTION", [
        r"\bi\s+feel\b", r"\bi\s+felt\b", r"\bfeel(s|ing)?\b", r"\bafraid\b",
        r"\bя\s+чувству", r"\bя\s+почувствова", r"\bмне\s+(страшно|тревожно|больно|радостно)",
        r"\bчувству", r"\bтревог",
    ]),
    ("OPINION", [
        r"\bi\s+think\b", r"\bi\s+believe\b", r"\bin\s+my\s+opinion\b", r"\bimho\b",
        r"\bя\s+(думаю|считаю|полагаю)", r"\bпо-?моему\b", r"\bна\s+мой\s+взгляд\b",
    ]),
    ("GOAL", [
        r"\bi\s+want\b", r"\bi\s+need\b", r"\bmy\s+goal\b", r"\bi('?d| would)\s+like\b",
        r"\bя\s+хочу\b", r"\bмне\s+нужно\b", r"\bмоя\s+цель\b",
    ]),
    ("PREFERENCE", [
        r"\bi\s+prefer\b", r"\bi\s+like\b.*\bbetter\b", r"\bi\s+love\b",
        r"\bя\s+предпочита", r"\bмне\s+больше\s+нравится\b",
    ]),
    ("INTERPRETATION", [
        r"\bmaybe\b", r"\bprobably\b", r"\bperhaps\b", r"\bi\s+guess\b",
        r"\bseems?\s+(like|to)\b", r"\bit\s+looks\s+like\b",
        r"\bнаверное\b", r"\bвозможно\b", r"\bкажется\b", r"\bмне\s+кажется\b",
        r"\bпохоже\b",
    ]),
]


def classify_claim(utterance: str) -> tuple[str, str]:
    """
    (claim_type, source_status) for a user's utterance.
    An utterance is always USER_REPORTED; the type — by linguistic markers,
    otherwise WORLD_FACT (a claim about the world).
    """
    text = utterance.lower()
    for claim_type, patterns in _CLAIM_MARKERS:
        if any(re.search(p, text) for p in patterns):
            return claim_type, "USER_REPORTED"
    return "WORLD_FACT", "USER_REPORTED"


def _fact_id(utterance: str) -> str:
    return "ing:" + hashlib.md5(utterance.encode("utf-8")).hexdigest()[:12]


def ingest(
    utterance: str,
    *,
    fact_id: Optional[str] = None,
    source: str = "user",
    confidence: float = 0.6,
    significance: float = 0.5,
    claim_type: Optional[str] = None,
    episode: Optional[Dict[str, Any]] = None,
    source_status: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Accept an utterance, classify it, run it through the gates, write it to L3.

    Returns a result: {accepted, fact, reason?}.
    - accepted=True  → the fact passed the TruthGate, transitioned to Validated, MERGE into L3.
    - accepted=False → blocked (reason). In SQLite it remains as Observed.

    claim_type can be set explicitly (bypassing the classifier). source_status
    defaults to the classifier's verdict (USER_REPORTED for a user's message); an
    external loader (RFC0063 knowledge ingestion) overrides it, e.g. EXTERNAL.
    """
    if not utterance or not utterance.strip():
        raise ValueError("ingest: empty utterance")

    # Data minimisation (GDPR Art. 5): optionally strip PII before anything is
    # stored. Off by default; enabled via VELANTRIM_REDACT_PII. The content-free
    # summary (types/counts, no values) is kept in metadata for accountability.
    pii_redacted = None
    if pii.redaction_enabled():
        utterance, _found = pii.redact(utterance)
        if _found:
            pii_redacted = pii.summary(_found)

    ct, classified_status = classify_claim(utterance)
    if claim_type is not None:
        ct = claim_type
    source_status = source_status or classified_status

    fid = fact_id or _fact_id(utterance)

    # An exact repeat of an already accepted fact (same content-hash id, Validated) —
    # this is independent evidence: we reinforce confidence rather than create a duplicate.
    metrics.incr("ingest.total")
    prior = get_fact(fid)
    if prior is not None and prior.get("epistemic_state") == "Validated":
        reinforce(fid)
        metrics.incr("ingest.reinforced")
        return {"accepted": True, "reinforced": True, "fact": get_fact(fid)}

    fact = {
        "fact_id": fid,
        "claim": utterance.strip(),
        "source": source,
        "confidence": confidence,
        "epistemic_state": "Observed",
        "claim_type": ct,
        "source_status": source_status,
        "significance": significance,
        "truth_status": "UNVERIFIED",
    }
    if pii_redacted:
        fact["metadata"] = {"pii_redacted": pii_redacted}

    # L0/L1: store as raw experience (pending), even if the gates reject it.
    store_fact(fact)

    # Immune pre-screen (RFC0072): block claims matching the CRISPR threat memory
    # — known hallucination / harmful / previously-refuted patterns — BEFORE the
    # gates. The threat memory is empty by default, so this is a no-op until a
    # curator (or adaptive learning) records something. The fact stays Observed in
    # L0/L1 (pending), never reaching the canon.
    pre = immune.screen(utterance, fact_id=fid, check_canon=False)
    if pre["verdict"] == immune.BLOCK:
        metrics.incr("ingest.immune_blocked")
        adaptation.record_block()
        return {"accepted": False, "reason": f"Immune: {pre['reason']}",
                "immune": pre, "fact": fact}

    facts_pack = {"facts": [fact], "query": utterance, "total": 1}
    trace = [{
        "fact_id": fid, "source": source, "origin": "ingestion",
        "epistemic_state": "Observed", "confidence": confidence,
    }]

    ok, reason = guardian(facts_pack, trace)
    if ok:
        ok, reason = truth_gate(facts_pack)
    if not ok:
        metrics.incr("ingest.blocked")
        adaptation.record_block()
        return {"accepted": False, "reason": reason, "fact": fact}

    # Immune contradiction check (RFC0072): WORLD_FACTs are checked against the
    # canon ONCE here (reused for the result below). By default a contradiction is
    # a non-destructive advisory — we still admit and link (see truth-first
    # principle). With VELANTRIM_IMMUNE_STRICT, a claim that contradicts the canon
    # is blocked outright (and, with VELANTRIM_IMMUNE_LEARN, recorded as a threat
    # so a repeat is caught pre-gate next time).
    conflicts = find_conflicts(utterance, fact_id=fid) if ct == "WORLD_FACT" else []
    contradictions = [c for c in conflicts
                      if c["kind"] == contradiction.CONTRADICTION]
    if contradictions and immune.strict_mode():
        metrics.incr("ingest.immune_blocked")
        adaptation.record_block()
        if immune.learn_mode():
            immune.record_threat(utterance, threat_type="contradiction",
                                 severity=1.0, actor="immune-auto")
        return {
            "accepted": False,
            "reason": f"Immune: contradicts {len(contradictions)} canonical "
                      f"fact(s) (strict mode)",
            "immune": {"verdict": immune.BLOCK, "contradictions": contradictions},
            "conflicts": conflicts, "fact": fact,
        }

    # Passed the gates → Validated, truth_status by modality, MERGE into the L3 canon.
    transition_esm(fid, "Validated")
    updated = get_fact(fid)
    if updated:
        fact["epistemic_state"] = updated["epistemic_state"]
    fact["truth_status"] = _truth_status_for(ct)

    graph = get_l3_graph()
    # Guard against mixing embedders: merge puts the claim's vector into the store.
    assert_compatible_embedder(graph)
    # We merge the persistent record (created_at/metadata) — otherwise SleepCycle
    # will not find a reference timestamp for decay (see pipeline._l3_payload).
    graph.merge_fact(_l3_payload(fact))

    metrics.incr("ingest.accepted")
    adaptation.record_success()
    result = {"accepted": True, "fact": fact}
    # Immune signal: for facts about the world we surface canon candidates that
    # are close-but-different, classified (CONTRADICTION/REFINEMENT/RELATED) above.
    # By default we only hand it off for a decision. With VELANTRIM_AUTO_CONTRADICT
    # set, a high-precision CONTRADICTION is also recorded as a CONTRADICTS edge
    # (new → prior) so the clash is queryable via fact_history — we LINK, we do
    # not deprecate either side (a heuristic must not silently overwrite canon).
    if conflicts:
        result["conflicts"] = conflicts
        if contradictions and _auto_contradict_enabled():
            graph_ = get_l3_graph()
            for c in contradictions:
                graph_.add_edge(fid, REL_CONTRADICTS, c["fact_id"],
                                {"at": _now(), "signal": c["signal"], "auto": True})
            result["auto_contradicted"] = [c["fact_id"] for c in contradictions]
            metrics.incr("ingest.contradiction_detected")
        # Neurogenesis pattern separation (RFC0073, opt-in): keep a vectorally
        # close but non-contradictory memory distinct via a SEPARATED_FROM edge,
        # rather than letting similar episodes blur together.
        if neurogenesis.separation_enabled():
            separated = neurogenesis.separate(fid, utterance, conflicts=conflicts)
            if separated:
                result["separated_from"] = separated
    return result


def _auto_contradict_enabled() -> bool:
    """True if VELANTRIM_AUTO_CONTRADICT turns on automatic CONTRADICTS linking."""
    import os
    return os.environ.get("VELANTRIM_AUTO_CONTRADICT", "").lower() in (
        "1", "true", "yes", "on")
