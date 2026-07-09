"""Exact-content ingest dedup (Variant B).

A repeat of already-canonical content is a FREQUENCY sighting: it updates
occurrence metadata only. It never reinforces confidence, never changes
truth_status/ESM, and never promotes or duplicates a fact.
"""
import hashlib

from core.ingest import (
    ingest, _fact_id, _legacy_fact_id, _normalize, _fingerprint,
)
from core.l3_graph import get_l3_graph
from core.memory import get_fact, store_fact
from core.reconcile import record_occurrence


# ─── Normalized exact dedup ───────────────────────────────────────────────────

def test_case_and_whitespace_variants_dedupe_to_one_fact():
    first = ingest("The Earth orbits the Sun")
    assert first["accepted"] and not first.get("duplicate")
    fid = first["fact"]["fact_id"]

    # Different casing + padding + doubled spaces → same normalized identity.
    again = ingest("  the   earth orbits the sun  ")
    assert again["duplicate"] is True
    assert again["fact"]["fact_id"] == fid           # one node, not two
    assert again["occurrences"] == 2
    assert get_fact(fid)["metadata"]["occurrences"] == 2


def test_duplicate_does_not_change_confidence_or_truth_fields():
    first = ingest("Helium is lighter than air")
    fid = first["fact"]["fact_id"]
    c1 = first["fact"]["confidence"]
    ts1 = get_l3_graph().get_fact(fid).get("truth_status")

    dup = ingest("Helium is lighter than air")
    assert dup["fact"]["confidence"] == c1                       # confidence frozen
    assert dup["fact"]["epistemic_state"] == "Validated"         # ESM frozen
    assert get_l3_graph().get_fact(fid).get("truth_status") == ts1  # truth frozen
    # The evidentiary observations counter is never touched by dedup.
    assert "observations" not in dup["fact"]["metadata"]


def test_fingerprint_and_sources_seen_recorded():
    ingest("Argon is a noble gas", source="alice")
    dup = ingest("argon is a noble gas", source="bob")   # different source label
    meta = dup["fact"]["metadata"]

    assert meta["fingerprint_sha256"] == _fingerprint("Argon is a noble gas")
    assert meta["fingerprint_sha256"] == hashlib.sha256(
        _normalize("Argon is a noble gas").encode("utf-8")).hexdigest()
    # sources_seen is a sorted list (JSON-serialisable), holding both labels.
    assert meta["sources_seen"] == ["alice", "bob"]
    assert isinstance(meta["sources_seen"], list)


# ─── Legacy raw-id fallback ───────────────────────────────────────────────────

def test_legacy_raw_id_fact_is_reused_not_duplicated():
    text = "Neon glows orange-red"
    legacy = _legacy_fact_id(text)
    norm = _fact_id(text)
    assert legacy != norm                            # raw vs normalized differ

    # Simulate a fact stored before normalization (raw-text id), Validated.
    ingest(text, fact_id=legacy)
    assert get_fact(legacy)["epistemic_state"] == "Validated"

    # Auto-id ingest of the same content must adopt the legacy node, not fork.
    res = ingest(text)
    assert res["duplicate"] is True
    assert res["fact"]["fact_id"] == legacy
    assert get_fact(norm) is None                    # no second node created


# ─── record_occurrence unit behaviour ─────────────────────────────────────────

def test_record_occurrence_missing_fact_returns_none():
    assert record_occurrence("ing:does-not-exist") is None


def test_record_occurrence_on_non_validated_fact_never_reaches_l3():
    store_fact({
        "fact_id": "obs1", "claim": "pending claim", "source": "s",
        "confidence": 0.6, "epistemic_state": "Observed",
        "claim_type": "WORLD_FACT", "source_status": "USER_REPORTED",
    })
    n = record_occurrence("obs1")                    # no source / fingerprint args
    assert n == 2
    assert get_fact("obs1")["metadata"]["occurrences"] == 2
    # Guardrail: a non-Validated fact is never merged into the L3 canon here.
    assert get_l3_graph().get_fact("obs1") is None


def test_record_occurrence_retries_on_cas_miss_and_eventually_succeeds(monkeypatch):
    """Regression for a Codex P1 finding (#244): record_occurrence() ignored
    update_fact()'s boolean return, so a CAS miss (lost race with a
    concurrent writer) made it report an occurrence count that was never
    actually persisted. It must retry against fresh state instead."""
    from core import reconcile

    store_fact({"fact_id": "cas_ro1", "claim": "c", "source": "s", "confidence": 0.5})

    real_update_fact = reconcile.update_fact
    calls = {"n": 0}

    def flaky_update_fact(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            return False  # simulate one lost CAS race
        return real_update_fact(*args, **kwargs)

    monkeypatch.setattr(reconcile, "update_fact", flaky_update_fact)

    result = record_occurrence("cas_ro1", source="s2")
    assert result == 2
    assert get_fact("cas_ro1")["metadata"]["occurrences"] == 2
    assert calls["n"] == 2  # first attempt lost the race, second succeeded
