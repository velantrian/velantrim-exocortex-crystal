# core/ingest.py
# Velantrim ExoCortex — Ingestion Layer
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
from core.queue import get_outbox_queue
from core.pipeline import guardian, truth_gate, _truth_status_for, _l3_payload
from core.reconcile import record_occurrence, find_conflicts, REL_CONTRADICTS, _now
from core.ingest_identity import normalize_claim, normalized_ingest_id
from core.normalized_ingest_index import resolve_validated_normalized_fact
from core import (metrics, adaptation, pii, contradiction, immune,
                  neurogenesis, salience, mosc)

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


def _regex_classify(utterance: str) -> str:
    """The historical marker-based claim_type (fallback when MOSC abstains)."""
    text = utterance.lower()
    for claim_type, patterns in _CLAIM_MARKERS:
        if any(re.search(p, text) for p in patterns):
            return claim_type
    return "WORLD_FACT"


def classify_claim(utterance: str) -> tuple[str, str]:
    """
    (claim_type, source_status) for a user's utterance.
    An utterance is always USER_REPORTED. The type: MOSC (core/mosc.py,
    weighted RU/EN keywords) suggests first; below its threshold it abstains
    (None) and the historical regex markers decide, otherwise WORLD_FACT.
    MOSC is advisory only — the suggestion faces the same gates as before.
    """
    suggested = mosc.classify(utterance)
    if suggested is not None:
        return suggested, "USER_REPORTED"
    return _regex_classify(utterance), "USER_REPORTED"


def _normalize(text: str) -> str:
    """Compatibility wrapper for the shared exact-normalization contract."""
    return normalize_claim(text)


def _fact_id(utterance: str) -> str:
    """Compatibility wrapper for the canonical normalized auto fact id."""
    return normalized_ingest_id(utterance)


def _legacy_fact_id(utterance: str) -> str:
    """The pre-normalization id (md5 of the RAW utterance). Kept only as a
    dedupe fallback so facts stored before normalization still match instead of
    spawning a second node for identical content."""
    return "ing:" + hashlib.md5(utterance.encode("utf-8"), usedforsecurity=False).hexdigest()[:12]


def _fingerprint(utterance: str) -> str:
    """Full sha256 of the normalized content, kept in occurrence metadata for
    audit/transparency (the 12-char fact_id is for identity, this is the proof)."""
    return hashlib.sha256(_normalize(utterance).encode("utf-8")).hexdigest()


def _resolve_auto_fact(
    utterance: str,
    *,
    persist_index: bool = True,
) -> tuple[str, Optional[Dict[str, Any]]]:
    """Resolve the fact id used by the auto-id ingest path.

    Resolution order is fail-safe and compatibility preserving:
      1. the current normalized id wins if a row already exists;
      2. otherwise the derived normalized legacy index may select an existing
         Validated ``ing:*`` row with exact normalized equality;
      3. finally the historical raw-text id fallback preserves byte-identical
         pre-normalization pending/validated rows.

    The index never creates identity by similarity and never merges historical
    rows. ``persist_index=False`` is used by dry-run prediction so it performs
    the same selection without writing the derived index.
    """
    fid = _fact_id(utterance)
    prior = get_fact(fid)
    if prior is not None:
        return fid, prior

    indexed = resolve_validated_normalized_fact(
        utterance, persist_index=persist_index
    )
    if indexed is not None:
        prior = get_fact(indexed)
        if prior is not None and prior.get("epistemic_state") == "Validated":
            return indexed, prior

    legacy = _legacy_fact_id(utterance)
    if legacy != fid:
        prior = get_fact(legacy)
        if prior is not None:
            return legacy, prior

    return fid, None


def ingest(
    utterance: str,
    *,
    fact_id: Optional[str] = None,
    source: str = "user",
    confidence: float = 0.6,
    significance: Optional[float] = None,
    claim_type: Optional[str] = None,
    episode: Optional[Dict[str, Any]] = None,
    source_status: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Accept an utterance, classify it, run it through the gates, write it to L3.

    Returns a result: {accepted, fact, reason?}.
    - accepted=True  → the fact passed the TruthGate, transitioned to Validated, MERGE into L3.
    - accepted=False → blocked (reason). In SQLite it remains as Observed.

    claim_type can be set explicitly (bypassing the classifier). source_status
    defaults to the classifier's verdict (USER_REPORTED for a user's message); an
    external loader (RFC0063 knowledge ingestion) overrides it, e.g. EXTERNAL.

    significance: an explicit value always wins. When omitted (None) it is
    auto-derived from utterance salience (core/salience.py): ordinary text gets
    exactly the historical 0.5; CAPS/"!"/importance keywords lift it toward 1.0,
    with content-free explainability metadata (significance_source,
    salience_score, salience_markers — categories only, never raw phrases).
    Salience touches ranking only — never confidence/truth_status/ESM.
    """
    if not utterance or not utterance.strip():
        raise ValueError("ingest: empty utterance")

    pii_redacted = None
    if pii.redaction_enabled():
        utterance, _found = pii.redact(utterance)
        if _found:
            pii_redacted = pii.summary(_found)

    ct, classified_status = classify_claim(utterance)
    if claim_type is not None:
        ct = claim_type
    source_status = source_status or classified_status

    salience_meta = None
    if significance is None:
        sal = salience.analyze(utterance)
        significance = sal["significance"]
        if sal["markers"]:
            salience_meta = {
                "significance_source": "auto_salience",
                "salience_score": sal["salience"],
                "salience_markers": sal["markers"],
            }

    metrics.incr("ingest.total")
    if fact_id is None:
        fid, prior = _resolve_auto_fact(utterance)
    else:
        fid = fact_id
        prior = get_fact(fid)

    if prior is not None and prior.get("epistemic_state") == "Validated":
        occurrences = record_occurrence(fid, source=source,
                                        fingerprint=_fingerprint(utterance))
        metrics.incr("ingest.duplicate")
        return {"accepted": True, "duplicate": True,
                "occurrences": occurrences, "fact": get_fact(fid)}

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
    meta = dict(metadata or {})
    if pii_redacted:
        meta["pii_redacted"] = pii_redacted
    if salience_meta:
        meta.update(salience_meta)
    if meta:
        fact["metadata"] = meta

    store_fact(fact)

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

    if not transition_esm(fid, "Validated"):
        adaptation.record_block()
        return {
            "accepted": False,
            "reason": "ESM CAS conflict: fact state changed concurrently; not promoted",
            "conflicts": conflicts, "fact": fact,
        }
    updated = get_fact(fid)
    if updated:
        fact["epistemic_state"] = updated["epistemic_state"]
    fact["truth_status"] = _truth_status_for(ct, source_status)

    graph = get_l3_graph()
    assert_compatible_embedder(graph)
    try:
        graph.merge_fact(_l3_payload(fact))
    except Exception as exc:  # noqa: BLE001 — preserve post-gate recovery state
        get_outbox_queue().enqueue(fid)
        metrics.incr("ingest.blocked")
        adaptation.record_block()
        return {
            "accepted": False,
            "reason": f"L3 promotion failed: {exc}",
            "conflicts": conflicts,
            "fact": fact,
        }

    metrics.incr("ingest.accepted")
    adaptation.record_success()
    result = {"accepted": True, "fact": fact}
    if conflicts:
        result["conflicts"] = conflicts
        if contradictions and _auto_contradict_enabled():
            graph_ = get_l3_graph()
            for c in contradictions:
                graph_.add_edge(fid, REL_CONTRADICTS, c["fact_id"],
                                {"at": _now(), "signal": c["signal"], "auto": True})
            result["auto_contradicted"] = [c["fact_id"] for c in contradictions]
            metrics.incr("ingest.contradiction_detected")
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
