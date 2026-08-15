"""Adversarial tests for the derived exact-normalized ingest compatibility index."""

from core import memory
from core.ingest import ingest, _fact_id, _legacy_fact_id
from core.ingest_identity import (
    normalized_claim_fingerprint,
    normalized_ingest_id,
)


def test_review_stage_index_schema_upgrades_and_backfills_full_fingerprint():
    """An earlier local review-stage table is upgraded without touching facts."""
    with memory._db() as conn:
        conn.execute(
            "CREATE TABLE normalized_ingest_index ("
            "fact_id TEXT PRIMARY KEY, "
            "normalized_id TEXT NOT NULL, "
            "fact_revision INTEGER NOT NULL)"
        )

    original = "I Prefer   Schema Upgrades"
    legacy = _legacy_fact_id(original)
    assert ingest(original, fact_id=legacy)["accepted"] is True

    duplicate = ingest("i prefer schema upgrades")
    assert duplicate["duplicate"] is True
    assert duplicate["fact"]["fact_id"] == legacy

    with memory._db() as conn:
        columns = {
            row["name"] for row in conn.execute(
                "PRAGMA table_info(normalized_ingest_index)"
            )
        }
        row = conn.execute(
            "SELECT normalized_id, normalized_fingerprint "
            "FROM normalized_ingest_index WHERE fact_id = ?",
            (legacy,),
        ).fetchone()

    assert "normalized_fingerprint" in columns
    assert row["normalized_id"] == _fact_id(original)
    assert row["normalized_fingerprint"] == normalized_claim_fingerprint(original)


def test_corrupt_derived_prefilter_cannot_create_false_duplicate():
    """A stale/corrupt derived row must fail the final exact-text recheck."""
    original = "I Prefer   Original Target"
    legacy = _legacy_fact_id(original)
    assert ingest(original, fact_id=legacy)["accepted"] is True

    # Build the derived mapping, then let occurrence recording advance revision.
    assert ingest("i prefer original target")["duplicate"] is True
    current = memory.get_fact(legacy)
    assert current is not None

    unrelated = "I prefer unrelated target"
    unrelated_id = normalized_ingest_id(unrelated)
    unrelated_fp = normalized_claim_fingerprint(unrelated)

    # Simulate derived-cache corruption while making the cache revision appear
    # current, so _sync_index does not repair it before the lookup. The indexed
    # prefilter will point at `legacy`, but exact normalized text must reject it.
    with memory._db() as conn:
        conn.execute(
            "UPDATE normalized_ingest_index SET normalized_id = ?, "
            "normalized_fingerprint = ?, fact_revision = ? WHERE fact_id = ?",
            (unrelated_id, unrelated_fp, current["revision"], legacy),
        )

    result = ingest(unrelated)
    assert result["accepted"] is True
    assert not result.get("duplicate")
    assert result["fact"]["fact_id"] == unrelated_id
    assert memory.get_fact(legacy) is not None
