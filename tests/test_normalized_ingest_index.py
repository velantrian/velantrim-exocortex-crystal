"""Adversarial tests for the derived exact-normalized ingest compatibility index."""

import pytest

from core import memory
from core.ingest import ingest, _fact_id, _legacy_fact_id
from core.ingest_identity import normalized_ingest_id
from core.memory import ClaimIdentityError


def test_derived_index_schema_is_minimal_and_idempotent():
    """The compatibility cache stores only routing material and rebuilds lazily."""
    original = "I Prefer   Minimal Indexes"
    legacy = _legacy_fact_id(original)
    assert ingest(original, fact_id=legacy)["accepted"] is True

    first = ingest("i prefer minimal indexes")
    assert first["duplicate"] is True
    assert first["fact"]["fact_id"] == legacy

    # A second lookup is idempotent: no duplicate derived rows or extra
    # plaintext-derived fingerprint column is required for exact equality.
    second = ingest("  I PREFER MINIMAL INDEXES  ")
    assert second["duplicate"] is True
    assert second["fact"]["fact_id"] == legacy

    with memory._db() as conn:
        columns = [
            row["name"] for row in conn.execute(
                "PRAGMA table_info(normalized_ingest_index)"
            )
        ]
        rows = conn.execute(
            "SELECT fact_id, normalized_id, fact_revision "
            "FROM normalized_ingest_index WHERE fact_id = ?",
            (legacy,),
        ).fetchall()

    assert columns == ["fact_id", "normalized_id", "fact_revision"]
    assert len(rows) == 1
    assert rows[0]["normalized_id"] == _fact_id(original)


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

    # Simulate derived-cache corruption while making the cache revision appear
    # current, so _sync_index does not repair it before the lookup. The indexed
    # prefilter will point at `legacy`, but exact normalized text must reject it.
    with memory._db() as conn:
        conn.execute(
            "UPDATE normalized_ingest_index SET normalized_id = ?, "
            "fact_revision = ? WHERE fact_id = ?",
            (unrelated_id, current["revision"], legacy),
        )

    result = ingest(unrelated)
    assert result["accepted"] is True
    assert not result.get("duplicate")
    assert result["fact"]["fact_id"] == unrelated_id
    assert memory.get_fact(legacy) is not None


def test_noncanonical_ing_prefix_is_not_enrolled_as_legacy_auto_id():
    """Prefix sharing alone is not enough to enter the auto-id compatibility set."""
    original = "I Prefer   Prefix Isolation"
    custom = ingest(original, fact_id="ing:custom")
    assert custom["accepted"] is True

    auto = ingest("i prefer prefix isolation")
    assert auto["accepted"] is True
    assert not auto.get("duplicate")
    assert auto["fact"]["fact_id"] == _fact_id(original)
    assert memory.get_fact("ing:custom") is not None


def test_current_normalized_short_id_collision_fails_closed():
    """An occupied 12-hex current id is not itself proof of claim equality."""
    target = "I prefer collision target"
    target_id = _fact_id(target)

    # Simulate a corrupt/manual row occupying the generated id with another
    # claim. Auto ingest must not count it as a duplicate or rewrite it.
    decoy = ingest("I prefer a different claim", fact_id=target_id)
    assert decoy["accepted"] is True

    with pytest.raises(ClaimIdentityError, match="normalized auto-id collision"):
        ingest(target)


def test_legacy_raw_short_id_collision_fails_closed():
    """The byte-identical fallback also verifies content before reuse."""
    target = "I Prefer Raw Collision"
    legacy_id = _legacy_fact_id(target)

    decoy = ingest("I prefer another legacy claim", fact_id=legacy_id)
    assert decoy["accepted"] is True

    with pytest.raises(ClaimIdentityError, match="legacy raw auto-id collision"):
        ingest(target)
