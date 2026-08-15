"""Exact-content ingest dedup (Variant B).

A repeat of already-canonical content is a FREQUENCY sighting: it updates
occurrence metadata only. It never reinforces confidence, never changes
truth_status/ESM, and never promotes or duplicates a fact.
"""
import hashlib

from core import memory
from core.erasure import erase_fact
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


# ─── Legacy raw-id fallback / persistent normalized compatibility index ───────

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


def test_legacy_case_whitespace_variant_resolves_through_normalized_index():
    original = "Neon Glows   Orange-Red"
    legacy = _legacy_fact_id(original)
    norm = _fact_id(original)
    assert legacy != norm

    first = ingest(original, fact_id=legacy)
    assert first["accepted"] is True

    # The later text has a different raw legacy id but the same exact-normalized
    # identity. This is the gap left by the old byte-identical fallback.
    variant = "  neon glows orange-red  "
    assert _legacy_fact_id(variant) != legacy
    assert _fact_id(variant) == norm

    res = ingest(variant, source="repeat")
    assert res["accepted"] is True
    assert res["duplicate"] is True
    assert res["fact"]["fact_id"] == legacy
    assert res["occurrences"] == 2
    assert get_fact(norm) is None

    with memory._db() as conn:
        row = conn.execute(
            "SELECT normalized_id FROM normalized_ingest_index WHERE fact_id = ?",
            (legacy,),
        ).fetchone()
    assert row["normalized_id"] == norm


def test_existing_normalized_id_wins_over_older_legacy_collision():
    claim = "I prefer tea"
    normalized_id = _fact_id(claim)
    old_legacy = _legacy_fact_id("I Prefer   Tea")
    assert old_legacy != normalized_id

    ingest("I Prefer   Tea", fact_id=old_legacy)
    current = ingest(claim)  # creates the current normalized-id row
    assert current["accepted"] is True
    assert current["fact"]["fact_id"] == normalized_id

    duplicate = ingest("  I PREFER   TEA  ")
    assert duplicate["duplicate"] is True
    assert duplicate["fact"]["fact_id"] == normalized_id
    assert get_fact(old_legacy) is not None  # historical collision preserved


def test_multiple_legacy_collisions_are_preserved_and_oldest_routes_future_hits():
    text_a = "I Prefer   Tea"
    text_b = "  i prefer tea  "
    legacy_a = _legacy_fact_id(text_a)
    legacy_b = _legacy_fact_id(text_b)
    normalized_id = _fact_id("i prefer tea")
    assert len({legacy_a, legacy_b, normalized_id}) == 3

    ingest(text_a, fact_id=legacy_a)
    ingest(text_b, fact_id=legacy_b)

    # Freeze deterministic historical order independently of wall-clock timing.
    with memory._db() as conn:
        conn.execute(
            "UPDATE facts SET created_at = ? WHERE fact_id = ?",
            ("2020-01-01T00:00:00+00:00", legacy_a),
        )
        conn.execute(
            "UPDATE facts SET created_at = ? WHERE fact_id = ?",
            ("2021-01-01T00:00:00+00:00", legacy_b),
        )

    res = ingest("i prefer tea", source="future")
    assert res["duplicate"] is True
    assert res["fact"]["fact_id"] == legacy_a
    assert get_fact(legacy_a) is not None
    assert get_fact(legacy_b) is not None
    assert get_fact(normalized_id) is None
    assert get_fact(legacy_a)["metadata"]["occurrences"] == 2
    assert get_fact(legacy_b)["metadata"].get("occurrences") is None


def test_explicit_custom_fact_id_does_not_use_normalized_legacy_index():
    text = "I Prefer   Coffee"
    legacy = _legacy_fact_id(text)
    ingest(text, fact_id=legacy)

    explicit = ingest("i prefer coffee", fact_id="custom:coffee")
    assert explicit["accepted"] is True
    assert not explicit.get("duplicate")
    assert explicit["fact"]["fact_id"] == "custom:coffee"
    assert get_fact(legacy) is not None
    assert get_fact("custom:coffee") is not None


def test_non_validated_legacy_variant_is_not_duplicate_authority():
    original = "Pending   Legacy Claim"
    legacy = _legacy_fact_id(original)
    normalized_id = _fact_id(original)
    assert legacy != normalized_id

    store_fact({
        "fact_id": legacy,
        "claim": original,
        "source": "legacy",
        "confidence": 0.6,
        "epistemic_state": "Observed",
        "claim_type": "OPINION",
        "source_status": "USER_REPORTED",
    })

    res = ingest("pending legacy claim", claim_type="OPINION")
    assert res["accepted"] is True
    assert not res.get("duplicate")
    assert res["fact"]["fact_id"] == normalized_id
    assert get_fact(legacy)["epistemic_state"] == "Observed"


def test_full_erasure_removes_derived_normalized_mapping():
    original = "I Prefer   Erasure Tests"
    legacy = _legacy_fact_id(original)
    normalized_id = _fact_id(original)
    ingest(original, fact_id=legacy)

    # Cross-variant lookup lazily creates the derived compatibility mapping.
    assert ingest("i prefer erasure tests")["duplicate"] is True
    with memory._db() as conn:
        assert conn.execute(
            "SELECT COUNT(*) FROM normalized_ingest_index WHERE fact_id = ?",
            (legacy,),
        ).fetchone()[0] == 1

    receipt = erase_fact(legacy, reason="test")
    assert receipt["erased_now"] is True
    with memory._db() as conn:
        assert conn.execute(
            "SELECT COUNT(*) FROM normalized_ingest_index WHERE fact_id = ?",
            (legacy,),
        ).fetchone()[0] == 0
    assert get_fact(normalized_id) is None


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


def test_record_occurrence_drops_sighting_after_exhausting_retries_under_sustained_contention():
    """When every attempt loses the CAS race (persistent contention),
    record_occurrence() must drop the sighting and return the fact's actual
    current occurrence count — never a value that was silently never
    persisted."""
    from core import reconcile

    store_fact({"fact_id": "cas_ro2", "claim": "c", "source": "s", "confidence": 0.5})

    def always_fails(*args, **kwargs):
        return False

    original = reconcile.update_fact
    reconcile.update_fact = always_fails
    try:
        result = record_occurrence("cas_ro2")
    finally:
        reconcile.update_fact = original

    assert result == 1                                  # unchanged, not fabricated
    assert get_fact("cas_ro2")["metadata"].get("occurrences") is None


def test_record_occurrence_returns_none_if_fact_vanishes_during_exhausted_retries():
    """Extreme edge of the sustained-contention fallback: every retry attempt
    loses the CAS race AND the fact is concurrently erased right before the
    final fallback read. Must report None (matching the "fact does not
    exist" contract), not crash or fabricate a count."""
    from core import reconcile
    from core.memory import delete_fact_l1

    store_fact({"fact_id": "cas_ro3", "claim": "c", "source": "s", "confidence": 0.5})

    calls = {"n": 0}

    def always_fails_then_erase(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] >= reconcile._CAS_MAX_ATTEMPTS:
            delete_fact_l1("cas_ro3")
        return False

    original = reconcile.update_fact
    reconcile.update_fact = always_fails_then_erase
    try:
        result = record_occurrence("cas_ro3")
    finally:
        reconcile.update_fact = original

    assert result is None
    assert calls["n"] == reconcile._CAS_MAX_ATTEMPTS
