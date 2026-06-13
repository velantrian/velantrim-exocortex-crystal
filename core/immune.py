# core/immune.py
# Velantrim ExoCortex — Immune / CRISPR Memory Guard (RFC0072)
#
# Bacterial CRISPR immunity in three moves: a cell records a fragment of an
# invading virus (a "spacer"), and on re-exposure recognises and cuts the matching
# sequence. This module is the same idea for memory: it keeps a persistent,
# adaptive record of known *threat patterns* (hallucination signatures, harmful
# or previously-refuted claims) and screens new claims against them BEFORE they
# can reach the canon — the automated verification + blocking layer of RFC0072.
#
# Design principles (kept faithful to the rest of the system):
#   - Truth-first, non-destructive by default. A heuristic must never silently
#     overwrite or auto-reject the canon. So blocking power comes from the
#     EXPLICIT, curated CRISPR memory (recorded threats); contradiction with the
#     canon is, by default, an advisory QUARANTINE signal — not a block. Hard
#     blocking on contradiction is opt-in (VELANTRIM_IMMUNE_STRICT).
#   - Deterministic & dependency-free. Pattern matching is normalized whole-token
#     containment (no NLI/LLM); contradiction reuse the high-precision classifier
#     in core/contradiction.py.
#   - Accountable. Every threat recorded/forgotten is appended to the
#     tamper-evident audit log (core/audit.py), content-hash only.
#   - Persistent & adaptive. The threat memory lives in the same SQLite store
#     (table immune_memory) and survives restarts; hit counters make the immune
#     response observable (immunity_report).
#
# Empty threat memory blocks nothing, so the guard is a no-op until something is
# recorded — turning it on does not change default ingest behaviour.

import os
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from core import memory, metrics, contradiction

# ─── Verdicts ─────────────────────────────────────────────────────────────────
ADMIT = "ADMIT"            # nothing matched — safe to gate/ingest normally
QUARANTINE = "QUARANTINE"  # advisory: contradicts the canon, surface for review
BLOCK = "BLOCK"            # matched the CRISPR memory (or strict contradiction)

_ENV_STRICT = "VELANTRIM_IMMUNE_STRICT"            # contradiction → BLOCK
_ENV_LEARN = "VELANTRIM_IMMUNE_LEARN"              # strict-blocked claim → record threat
_ENV_BLOCK_SEVERITY = "VELANTRIM_IMMUNE_BLOCK_SEVERITY"  # min severity to block (default 0.5)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize(text: str) -> str:
    """Canonical signature of a claim: lowercased content+function tokens joined
    by single spaces (reuses the contradiction tokenizer so the two layers agree
    on what 'the same wording' means)."""
    return " ".join(contradiction._tokens(text))


def _pattern_id(normalized: str) -> str:
    return "imm:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def _block_severity() -> float:
    try:
        return float(os.environ.get(_ENV_BLOCK_SEVERITY, "0.5"))
    except ValueError:
        return 0.5


def strict_mode() -> bool:
    """True if a claim contradicting the canon should be BLOCKED (not just flagged)."""
    return os.environ.get(_ENV_STRICT, "").lower() in ("1", "true", "yes", "on")


def learn_mode() -> bool:
    """True if a strict-blocked claim is recorded as a threat (adaptive immunity).

    Off by default and deliberately so: the system cannot know which side of a
    contradiction is the hallucination, so auto-learning a 'spacer' from a clash
    could immunise against a true correction. Enable only when new WORLD_FACTs are
    expected to be wrong-by-default (e.g. an untrusted feed behind manual review)."""
    return os.environ.get(_ENV_LEARN, "").lower() in ("1", "true", "yes", "on")


# ─── CRISPR threat memory (persistent, adaptive) ──────────────────────────────

def record_threat(
    pattern: str,
    *,
    threat_type: str = "manual",
    severity: float = 1.0,
    actor: str = "system",
) -> Dict[str, Any]:
    """
    Record a threat 'spacer' — a claim pattern to recognise and block on sight.

    Idempotent by normalized pattern: re-recording the same pattern refreshes its
    type/severity and keeps a single entry (and its accumulated hit count).
    Appends a content-free entry to the audit log for accountability.
    """
    normalized = _normalize(pattern)
    if not normalized:
        raise ValueError("record_threat: empty pattern")
    pid = _pattern_id(normalized)
    sev = max(0.0, min(1.0, float(severity)))
    now = _now()
    with memory._db() as conn:
        conn.execute(
            "INSERT INTO immune_memory "
            "(pattern_id, pattern, threat_type, severity, recorded_at, actor, hits) "
            "VALUES (?, ?, ?, ?, ?, ?, 0) "
            "ON CONFLICT(pattern_id) DO UPDATE SET "
            "threat_type = excluded.threat_type, severity = excluded.severity",
            (pid, normalized, threat_type, sev, now, actor),
        )
    metrics.incr("immune.threat_recorded")
    # Lazy import avoids a hard import cycle (audit → memory; immune → audit).
    from core import audit
    audit.append_event("immune_threat_recorded", None, {
        "pattern_id": pid, "threat_type": threat_type, "severity": sev, "actor": actor,
    })
    return {"pattern_id": pid, "pattern": normalized, "threat_type": threat_type,
            "severity": sev, "recorded_at": now, "actor": actor, "hits": 0}


def forget_threat(pattern_id: str, *, actor: str = "system") -> bool:
    """Revoke a recorded threat (curator override). Returns True if one was removed."""
    with memory._db() as conn:
        cur = conn.execute(
            "DELETE FROM immune_memory WHERE pattern_id = ?", (pattern_id,))
        removed = cur.rowcount > 0
    if removed:
        metrics.incr("immune.threat_forgotten")
        from core import audit
        audit.append_event("immune_threat_forgotten", None,
                           {"pattern_id": pattern_id, "actor": actor})
    return removed


def list_threats() -> List[Dict[str, Any]]:
    """All recorded threats, most-recent first."""
    with memory._db() as conn:
        rows = conn.execute(
            "SELECT * FROM immune_memory ORDER BY recorded_at DESC, pattern_id"
        ).fetchall()
    return [dict(r) for r in rows]


def _register_hit(pattern_id: str) -> None:
    with memory._db() as conn:
        conn.execute(
            "UPDATE immune_memory SET hits = hits + 1, last_hit_at = ? "
            "WHERE pattern_id = ?", (_now(), pattern_id))


def match_threat(claim: str) -> Optional[Dict[str, Any]]:
    """
    Return the highest-severity recorded threat whose pattern is contained in the
    claim (whole-token match) and meets the block-severity floor — or None.

    Containment is on normalized, space-padded token strings, so a recorded
    spacer "the sky is green" matches "the sky is green because magic" but "car"
    never matches "scary".
    """
    haystack = f" {_normalize(claim)} "
    floor = _block_severity()
    best: Optional[Dict[str, Any]] = None
    for t in list_threats():
        if t["severity"] < floor:
            continue
        needle = f" {t['pattern']} "
        if needle in haystack:
            if best is None or t["severity"] > best["severity"]:
                best = t
    return best


# ─── Screening ─────────────────────────────────────────────────────────────────

def screen(
    claim: str,
    *,
    fact_id: Optional[str] = None,
    check_canon: bool = True,
) -> Dict[str, Any]:
    """
    Screen a claim before it reaches the canon.

    Returns:
      verdict        — ADMIT / QUARANTINE / BLOCK
      reason         — short human-readable explanation
      threat         — the matched CRISPR entry (on BLOCK by threat), else None
      contradictions — canon WORLD_FACTs this claim contradicts (kind=CONTRADICTION)

    BLOCK     — the claim matches the CRISPR threat memory, OR it contradicts the
                canon and strict mode is on.
    QUARANTINE— the claim contradicts the canon (advisory; not blocked).
    ADMIT     — nothing matched.
    """
    result: Dict[str, Any] = {
        "verdict": ADMIT, "reason": "no immune signal",
        "threat": None, "contradictions": [],
    }

    threat = match_threat(claim)
    if threat is not None:
        _register_hit(threat["pattern_id"])
        metrics.incr("immune.blocked")
        result.update(verdict=BLOCK, threat=threat,
                      reason=f"matches recorded threat ({threat['threat_type']}, "
                             f"severity {threat['severity']})")
        return result

    if check_canon:
        # Reuse the high-precision contradiction classifier via reconcile. Imported
        # lazily: reconcile → l3_graph/embedding, not needed for pure threat checks.
        from core.reconcile import find_conflicts
        contradictions = [
            c for c in find_conflicts(claim, fact_id=fact_id)
            if c["kind"] == contradiction.CONTRADICTION
        ]
        if contradictions:
            result["contradictions"] = contradictions
            if strict_mode():
                metrics.incr("immune.blocked")
                result.update(
                    verdict=BLOCK,
                    reason=f"contradicts {len(contradictions)} canonical fact(s) "
                           f"(strict mode)")
            else:
                metrics.incr("immune.quarantined")
                result.update(
                    verdict=QUARANTINE,
                    reason=f"contradicts {len(contradictions)} canonical fact(s)")
    return result


def immunity_report() -> Dict[str, Any]:
    """Observable state of the immune layer: threats, total hits, breakdown."""
    threats = list_threats()
    by_type: Dict[str, int] = {}
    total_hits = 0
    for t in threats:
        by_type[t["threat_type"]] = by_type.get(t["threat_type"], 0) + 1
        total_hits += int(t["hits"] or 0)
    return {
        "total_threats": len(threats),
        "total_hits": total_hits,
        "by_type": by_type,
        "recent": threats[:5],
    }
