"""Adversarial tests for the derived exact-normalized ingest compatibility index."""

import os
import sqlite3
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from core import crypto, memory, normalized_ingest_index as normalized_index
from core.compliance import restrict_processing
from core.ingest import (
    ingest,
    _fact_id,
    _legacy_fact_id,
    _refresh_normalized_ingest_index_after_success,
)
from core.ingest_identity import normalized_ingest_id
from core.memory import (
    ClaimIdentityError,
    delete_fact_l1,
    set_restricted,
    transition_esm,
    update_fact,
)


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


def test_processing_restricted_legacy_row_is_not_a_compatibility_target():
    """A derived mapping cannot reactivate a row excluded from active processing."""
    original = "I Prefer   Restricted Legacy"
    legacy = _legacy_fact_id(original)
    normalized = _fact_id(original)
    assert legacy != normalized
    assert ingest(original, fact_id=legacy)["accepted"] is True

    # Build the mapping while the fact is eligible, then restrict it. The stale
    # derived row may remain as cache data, but final lookup must join to current
    # restriction state and refuse to route an occurrence to it.
    assert ingest("i prefer restricted legacy")["duplicate"] is True
    assert restrict_processing(legacy)["found"] is True

    res = ingest("  I PREFER RESTRICTED LEGACY  ")
    assert res["accepted"] is True
    assert not res.get("duplicate")
    assert res["fact"]["fact_id"] == normalized
    assert memory.get_fact(legacy)["restricted"] == 1


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


# ─── R-01B completeness/generation protocol ────────────────────────────────────


def _index_state():
    with memory._db() as conn:
        row = conn.execute(
            "SELECT protocol_version, generation, covered_generation, complete "
            "FROM normalized_ingest_index_state WHERE state_id = 1"
        ).fetchone()
        return dict(row)


def _is_index_complete():
    with memory._db() as conn:
        return normalized_index.is_complete(conn)


def _seed_validated_legacy(claim: str) -> str:
    fact_id = _legacy_fact_id(claim)
    result = ingest(claim, fact_id=fact_id)
    assert result["accepted"] is True
    assert result["fact"]["epistemic_state"] == "Validated"
    return fact_id


def test_v4_migration_marks_legacy_coverage_unknown_and_resolver_is_read_only():
    """A migration never trusts pre-existing/missing mappings as complete."""
    claim = "Legacy coverage remains unknown until rebuilt"
    legacy_id = _seed_validated_legacy(claim)
    state_before = _index_state()
    assert state_before["complete"] == 0
    assert state_before["generation"] != state_before["covered_generation"]

    with memory._db() as conn:
        version = conn.execute("PRAGMA user_version").fetchone()[0]
        index_table = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' "
            "AND name = 'normalized_ingest_index'"
        ).fetchone()
    assert version == 4
    assert index_table is None  # read-only preflight does not lazily create it

    assert normalized_index.resolve_validated_normalized_fact(claim) == legacy_id
    assert _index_state() == state_before
    with memory._db() as conn:
        assert conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' "
            "AND name = 'normalized_ingest_index'"
        ).fetchone() is None


def test_matching_revision_mapping_corruption_invalidates_fast_negative():
    """A wrong mapping with a current fact revision cannot hide the true row."""
    claim = "Current-revision mapping corruption target"
    legacy_id = _seed_validated_legacy(claim)
    assert normalized_index.rebuild_normalized_ingest_index() == 1
    assert _is_index_complete()
    revision = memory.get_fact(legacy_id)["revision"]
    decoy_id = normalized_ingest_id("unrelated query that must not match")

    with memory._db() as conn:
        conn.execute(
            "UPDATE normalized_ingest_index SET normalized_id = ?, "
            "fact_revision = ? WHERE fact_id = ?",
            (decoy_id, revision, legacy_id),
        )
    dirty = _index_state()
    assert dirty["complete"] == 0
    assert dirty["generation"] > dirty["covered_generation"]

    # The current-revision wrong key would be a false negative if the resolver
    # trusted the row. Its invalidation trigger forces the full exact scan.
    assert normalized_index.resolve_validated_normalized_fact(claim) == legacy_id
    assert _index_state() == dirty


def test_missing_mapping_table_and_partial_mapping_force_exact_scan_then_repair():
    first = _seed_validated_legacy("Missing mapping first target")
    second = _seed_validated_legacy("Missing mapping second target")
    assert normalized_index.rebuild_normalized_ingest_index() == 2

    with memory._db() as conn:
        conn.execute("DELETE FROM normalized_ingest_index WHERE fact_id = ?", (first,))
    assert not _is_index_complete()
    assert normalized_index.resolve_validated_normalized_fact(
        "Missing mapping first target"
    ) == first
    assert normalized_index.rebuild_if_incomplete() == 2
    assert _is_index_complete()

    with memory._db() as conn:
        conn.execute("DROP TABLE normalized_ingest_index")
    assert not _is_index_complete()
    assert normalized_index.resolve_validated_normalized_fact(
        "Missing mapping second target"
    ) == second
    assert normalized_index.rebuild_if_incomplete() == 2
    assert _is_index_complete()


def test_v3_additive_migration_keeps_old_mapping_unknown_until_rebuild():
    claim = "Version-three additive migration claim"
    legacy_id = _seed_validated_legacy(claim)
    assert normalized_index.rebuild_normalized_ingest_index() == 1

    # Model a v3 file that has legacy mappings but no R01B state/triggers.
    with memory._db() as conn:
        for trigger in conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'trigger' "
            "AND name LIKE 'normalized_ingest_%'"
        ).fetchall():
            conn.execute(f"DROP TRIGGER {trigger['name']}")
        conn.execute("DROP TABLE normalized_ingest_index_state")
        conn.execute("PRAGMA user_version = 3")

    with memory._db() as conn:
        version = conn.execute("PRAGMA user_version").fetchone()[0]
        old_mapping = conn.execute(
            "SELECT fact_id FROM normalized_ingest_index WHERE fact_id = ?",
            (legacy_id,),
        ).fetchone()
        assert version == 4
        assert old_mapping is not None
        assert not normalized_index.is_complete(conn)

    assert normalized_index.resolve_validated_normalized_fact(claim) == legacy_id
    assert normalized_index.rebuild_if_incomplete() == 1
    assert _is_index_complete()


def test_official_writer_paths_incrementally_preserve_complete_coverage():
    claim = "Official writer keeps indexed identity current"
    legacy_id = _seed_validated_legacy(claim)
    assert normalized_index.rebuild_normalized_ingest_index() == 1

    assert update_fact(legacy_id, metadata={"writer": "update_fact"}) is True
    assert _is_index_complete()
    with memory._db() as conn:
        row = conn.execute(
            "SELECT fact_revision FROM normalized_ingest_index WHERE fact_id = ?",
            (legacy_id,),
        ).fetchone()
    assert row["fact_revision"] == memory.get_fact(legacy_id)["revision"]

    assert set_restricted(legacy_id, True) is True
    assert _is_index_complete()
    with memory._db() as conn:
        assert conn.execute(
            "SELECT 1 FROM normalized_ingest_index WHERE fact_id = ?", (legacy_id,)
        ).fetchone() is None
    assert normalized_index.resolve_validated_normalized_fact(claim) is None

    assert set_restricted(legacy_id, False) is True
    assert _is_index_complete()
    assert normalized_index.resolve_validated_normalized_fact(claim) == legacy_id

    assert transition_esm(legacy_id, "Collapsed") is True
    assert _is_index_complete()
    assert normalized_index.resolve_validated_normalized_fact(claim) is None
    assert delete_fact_l1(legacy_id) is True
    assert _is_index_complete()
    with memory._db() as conn:
        assert conn.execute(
            "SELECT 1 FROM normalized_ingest_index WHERE fact_id = ?", (legacy_id,)
        ).fetchone() is None


def test_gate_refusal_does_not_write_mapping_or_rebuild_before_admission():
    assert ingest(
        "Existing accepted fact primes a complete index",
        source="synthetic-external",
        source_status="EXTERNAL",
    )["accepted"] is True
    assert _is_index_complete()
    before_state = _index_state()
    with memory._db() as conn:
        before_mappings = conn.execute(
            "SELECT fact_id, normalized_id, fact_revision "
            "FROM normalized_ingest_index ORDER BY fact_id"
        ).fetchall()

    refused_claim = "LLM-only statement remains before gate"
    refused = ingest(
        refused_claim,
        source="synthetic-llm",
        source_status="LLM_OUTPUT",
        claim_type="WORLD_FACT",
    )
    assert refused["accepted"] is False
    assert memory.get_fact(_fact_id(refused_claim))["epistemic_state"] == "Observed"
    assert _index_state() == before_state
    with memory._db() as conn:
        after_mappings = conn.execute(
            "SELECT fact_id, normalized_id, fact_revision "
            "FROM normalized_ingest_index ORDER BY fact_id"
        ).fetchall()
    assert after_mappings == before_mappings


def test_review_decision_direct_writer_keeps_index_complete():
    from core.review_decision_store import stage_review_decision

    assert ingest(
        "Review writer index baseline",
        source="synthetic-external",
        source_status="EXTERNAL",
    )["accepted"] is True
    legacy_id = _legacy_fact_id("Review candidate is admitted")
    memory.store_fact({
        "fact_id": legacy_id,
        "claim": "Review candidate is admitted",
        "source": "synthetic-external",
        "confidence": 0.9,
        "epistemic_state": "Observed",
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
    })
    candidate = memory.get_fact(legacy_id)
    result = stage_review_decision(
        decision_id="review:index-completeness",
        fact_id=legacy_id,
        expected_revision=candidate["revision"],
        expected_state="Observed",
        candidate_path=("Validated",),
        event="review_approve",
        audit_detail={"actor": "synthetic"},
    )
    assert result["ok"] is True
    assert _is_index_complete()
    assert normalized_index.resolve_validated_normalized_fact(
        "review candidate is admitted"
    ) == legacy_id


def test_l1_gate_commit_then_l3_failure_keeps_index_and_outbox_consistent(monkeypatch):
    claim = "L1 admission survives synthetic L3 outage"
    graph = __import__("core.l3_graph", fromlist=["get_l3_graph"]).get_l3_graph()
    original_merge = graph.merge_fact
    monkeypatch.setattr(
        graph,
        "merge_fact",
        lambda _payload: (_ for _ in ()).throw(RuntimeError("synthetic outage")),
    )
    result = ingest(claim, source="synthetic-external", source_status="EXTERNAL")
    assert result["accepted"] is False
    fact_id = result["fact"]["fact_id"]
    assert memory.get_fact(fact_id)["epistemic_state"] == "Validated"
    assert fact_id in memory.pending_l3_writes()
    assert normalized_index.resolve_validated_normalized_fact(claim) == fact_id
    assert _is_index_complete()
    monkeypatch.setattr(graph, "merge_fact", original_merge)


def test_encrypted_fact_rebuild_and_exact_lookup(monkeypatch):
    monkeypatch.setenv("VELANTRIM_ENCRYPTION_KEY", "synthetic R01B test key")
    monkeypatch.setattr(crypto, "_fernet", lambda: None)
    claim = "Encrypted normalized compatibility claim"
    legacy_id = _seed_validated_legacy(claim)
    with memory._db() as conn:
        raw = conn.execute(
            "SELECT claim FROM facts WHERE fact_id = ?", (legacy_id,)
        ).fetchone()["claim"]
    assert raw.startswith("enc:h1:")
    assert normalized_index.rebuild_normalized_ingest_index() == 1
    assert normalized_index.resolve_validated_normalized_fact(
        "  ENCRYPTED   NORMALIZED COMPATIBILITY CLAIM  "
    ) == legacy_id
    assert _is_index_complete()


def test_rebuild_failure_rolls_back_and_exact_scan_survives_restart(monkeypatch):
    first = _seed_validated_legacy("Rebuild rollback first row")
    second = _seed_validated_legacy("Rebuild rollback second row")
    real_normalized_id = normalized_index.normalized_ingest_id
    calls = {"count": 0}

    def fail_during_population(value):
        calls["count"] += 1
        if calls["count"] == 2:
            raise RuntimeError("simulated rebuild interruption")
        return real_normalized_id(value)

    monkeypatch.setattr(normalized_index, "normalized_ingest_id", fail_during_population)
    with pytest.raises(RuntimeError, match="rebuild interruption"):
        normalized_index.rebuild_normalized_ingest_index()
    assert not _is_index_complete()
    assert normalized_index.resolve_validated_normalized_fact(
        "Rebuild rollback first row"
    ) == first
    monkeypatch.setattr(normalized_index, "normalized_ingest_id", real_normalized_id)
    assert normalized_index.rebuild_if_incomplete() == 2
    memory._L0.clear()  # force a new L1 read, analogous to process restart
    assert normalized_index.resolve_validated_normalized_fact(
        "Rebuild rollback second row"
    ) == second
    assert _is_index_complete()


def test_process_crash_during_uncommitted_index_rebuild_rolls_back_and_recovers():
    claim = "Crash recovery exact-scan target"
    legacy_id = _seed_validated_legacy(claim)
    assert normalized_index.rebuild_normalized_ingest_index() == 1
    with memory._db() as conn:
        conn.execute(
            "UPDATE facts SET confidence = confidence WHERE fact_id = ?", (legacy_id,)
        )
    assert not _is_index_complete()  # committed direct SQL invalidation

    child_code = r"""
import os, sqlite3, sys
conn = sqlite3.connect(sys.argv[1], timeout=10)
conn.execute('BEGIN IMMEDIATE')
conn.execute('DELETE FROM normalized_ingest_index')
os._exit(23)
"""
    env = dict(os.environ)
    env.pop("VELANTRIM_ENCRYPTION_KEY", None)
    child = subprocess.run(
        [sys.executable, "-c", child_code, memory.SQLITE_PATH],
        cwd=str(Path(__file__).resolve().parents[1]),
        env=env,
        check=False,
        timeout=20,
    )
    assert child.returncode == 23

    # Opening a fresh connection runs SQLite WAL recovery. Uncommitted DELETE
    # rolls back, but the already-committed state remains dirty, so lookup scans.
    assert not _is_index_complete()
    assert normalized_index.resolve_validated_normalized_fact(claim) == legacy_id
    assert normalized_index.rebuild_if_incomplete() == 1
    assert _is_index_complete()


def test_concurrent_thread_writers_preserve_generation_and_mapping_revisions():
    legacy_ids = [
        _seed_validated_legacy(f"Concurrent writer fact {index}")
        for index in range(4)
    ]
    assert normalized_index.rebuild_normalized_ingest_index() == 4

    def write(index_and_id):
        index, fact_id = index_and_id
        assert update_fact(fact_id, metadata={"concurrent_writer": index}) is True

    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(write, enumerate(legacy_ids)))

    assert _is_index_complete()
    with memory._db() as conn:
        mappings = {
            row["fact_id"]: row["fact_revision"]
            for row in conn.execute(
                "SELECT fact_id, fact_revision FROM normalized_ingest_index"
            )
        }
    assert mappings == {
        fact_id: memory.get_fact(fact_id)["revision"] for fact_id in legacy_ids
    }


def test_cross_process_direct_sql_writers_invalidate_without_lost_generation():
    legacy_ids = [
        _seed_validated_legacy(f"Cross-process raw writer fact {index}")
        for index in range(2)
    ]
    assert normalized_index.rebuild_normalized_ingest_index() == 2
    base = _index_state()
    child_code = r"""
import sqlite3, sys
conn = sqlite3.connect(sys.argv[1], timeout=20)
conn.execute('BEGIN IMMEDIATE')
conn.execute('UPDATE facts SET confidence = confidence + 0.001 WHERE fact_id = ?', (sys.argv[2],))
conn.commit()
"""
    env = dict(os.environ)
    env.pop("VELANTRIM_ENCRYPTION_KEY", None)
    root = str(Path(__file__).resolve().parents[1])
    children = [
        subprocess.Popen(
            [sys.executable, "-c", child_code, memory.SQLITE_PATH, fact_id],
            cwd=root,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for fact_id in legacy_ids
    ]
    for child in children:
        stdout, stderr = child.communicate(timeout=30)
        assert child.returncode == 0, (stdout, stderr)

    dirty = _index_state()
    assert dirty["complete"] == 0
    assert dirty["generation"] >= base["generation"] + 2
    assert normalized_index.resolve_validated_normalized_fact(
        "Cross-process raw writer fact 1"
    ) == legacy_ids[1]
    assert normalized_index.rebuild_if_incomplete() == 2
    assert _is_index_complete()


def test_complete_lookup_decrypts_only_indexed_candidate_while_dirty_scans_all(monkeypatch):
    _seed_validated_legacy("Earlier eligible fact before target")
    target = _seed_validated_legacy("Last eligible fact is the exact target")
    assert normalized_index.rebuild_normalized_ingest_index() == 2

    real_decrypt = crypto.decrypt
    calls = {"count": 0}

    def counted_decrypt(value):
        calls["count"] += 1
        return real_decrypt(value)

    monkeypatch.setattr(crypto, "decrypt", counted_decrypt)
    assert normalized_index.resolve_validated_normalized_fact(
        "Last eligible fact is the exact target"
    ) == target
    assert calls["count"] == 1
    calls["count"] = 0
    assert normalized_index.resolve_validated_normalized_fact(
        "No synthetic fact has this normalized claim"
    ) is None
    assert calls["count"] == 0

    with memory._db() as conn:
        conn.execute(
            "UPDATE facts SET confidence = confidence + 0.001 "
            "WHERE fact_id = (SELECT fact_id FROM facts ORDER BY created_at, fact_id LIMIT 1)"
        )
    calls["count"] = 0
    assert normalized_index.resolve_validated_normalized_fact(
        "Last eligible fact is the exact target"
    ) == target
    assert calls["count"] == 2
    calls["count"] = 0
    assert normalized_index.resolve_validated_normalized_fact(
        "No synthetic fact has this normalized claim"
    ) is None
    assert calls["count"] == 2


def test_successful_auto_ingest_after_complete_snapshot_keeps_mapping_current():
    first = ingest(
        "Accepted starter makes the index complete",
        source="synthetic-external",
        source_status="EXTERNAL",
    )
    assert first["accepted"] is True
    assert _is_index_complete()

    second_claim = "New accepted fact added to a complete index"
    second = ingest(
        second_claim,
        source="synthetic-external",
        source_status="EXTERNAL",
    )
    assert second["accepted"] is True
    assert _is_index_complete()
    with memory._db() as conn:
        mapping = conn.execute(
            "SELECT normalized_id, fact_revision FROM normalized_ingest_index "
            "WHERE fact_id = ?",
            (second["fact"]["fact_id"],),
        ).fetchone()
    assert mapping["normalized_id"] == _fact_id(second_claim)
    assert mapping["fact_revision"] == second["fact"]["revision"]

    duplicate = ingest(second_claim.lower(), source="synthetic-repeat")
    assert duplicate["duplicate"] is True
    assert _is_index_complete()


# ─── Defensive schema and error-path coverage for the fail-closed protocol ────


def _bare_protocol_connection():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE facts (fact_id TEXT PRIMARY KEY, claim TEXT, revision INTEGER, "
        "epistemic_state TEXT, restricted INTEGER, created_at TEXT)"
    )
    return conn


def _insert_protocol_fact(conn, claim="isolated protocol target"):
    fact_id = "ing:0123456789ab"
    conn.execute(
        "INSERT INTO facts (fact_id, claim, revision, epistemic_state, "
        "restricted, created_at) VALUES (?, ?, 1, 'Validated', 0, '2020')",
        (fact_id, claim),
    )
    return fact_id


def _complete_protocol_connection():
    conn = _bare_protocol_connection()
    fact_id = _insert_protocol_fact(conn)
    assert normalized_index._rebuild_conn(conn) == 1
    assert normalized_index.is_complete(conn)
    return conn, fact_id


@pytest.mark.parametrize("object_kind", ["view", "index", "trigger"])
def test_state_storage_replaces_wrong_sqlite_object_kinds(object_kind):
    conn = _bare_protocol_connection()
    conn.execute("CREATE TABLE holder (value TEXT)")
    if object_kind == "view":
        conn.execute(
            "CREATE VIEW normalized_ingest_index_state AS SELECT value FROM holder"
        )
    elif object_kind == "index":
        conn.execute(
            "CREATE INDEX normalized_ingest_index_state ON holder(value)"
        )
    else:
        conn.execute(
            "CREATE TRIGGER normalized_ingest_index_state AFTER INSERT ON holder "
            "BEGIN SELECT 1; END"
        )

    normalized_index.install_state_migration(conn)
    assert normalized_index._object_type(
        conn, "normalized_ingest_index_state"
    ) == "table"
    conn.close()


def test_state_storage_replaces_malformed_table_and_wrong_trigger_sql():
    conn = _bare_protocol_connection()
    conn.execute("CREATE TABLE normalized_ingest_index_state (wrong TEXT)")
    normalized_index.install_state_migration(conn)
    assert [
        row["name"]
        for row in conn.execute("PRAGMA table_info(normalized_ingest_index_state)")
    ] == ["state_id", "protocol_version", "generation", "covered_generation", "complete"]

    conn.execute("DROP TRIGGER normalized_ingest_facts_ai")
    conn.execute(
        "CREATE TRIGGER normalized_ingest_facts_ai AFTER INSERT ON facts "
        "BEGIN SELECT 1; END"
    )
    normalized_index.install_state_migration(conn)
    found = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='trigger' "
        "AND name='normalized_ingest_facts_ai'"
    ).fetchone()["sql"]
    assert normalized_index._sql_key(found) == normalized_index._sql_key(
        normalized_index._FACT_TRIGGERS["normalized_ingest_facts_ai"]
    )
    conn.close()


@pytest.mark.parametrize("object_kind", ["view", "index", "trigger"])
def test_index_storage_replaces_wrong_sqlite_object_kinds(object_kind):
    conn = _bare_protocol_connection()
    normalized_index.install_state_migration(conn)
    conn.execute("CREATE TABLE holder (value TEXT)")
    if object_kind == "view":
        conn.execute(
            "CREATE VIEW normalized_ingest_index AS SELECT value FROM holder"
        )
    elif object_kind == "index":
        conn.execute("CREATE INDEX normalized_ingest_index ON holder(value)")
    else:
        conn.execute(
            "CREATE TRIGGER normalized_ingest_index AFTER INSERT ON holder "
            "BEGIN SELECT 1; END"
        )

    normalized_index._ensure_index_storage(conn)
    assert normalized_index._object_type(conn, "normalized_ingest_index") == "table"
    assert normalized_index._structure_is_valid(conn)
    conn.close()


def test_index_storage_repairs_malformed_table_and_misplaced_lookup_index():
    conn = _bare_protocol_connection()
    normalized_index.install_state_migration(conn)
    conn.execute("CREATE TABLE normalized_ingest_index (wrong TEXT)")
    normalized_index._ensure_index_storage(conn)
    assert normalized_index._index_columns(conn) == [
        "fact_id", "normalized_id", "fact_revision"
    ]
    assert normalized_index._structure_is_valid(conn)

    conn.execute("DROP INDEX idx_normalized_ingest_id")
    conn.execute(
        "CREATE INDEX idx_normalized_ingest_id ON normalized_ingest_index(fact_id)"
    )
    normalized_index._ensure_index_storage(conn)
    assert [
        row["name"] for row in conn.execute(
            "PRAGMA index_info(idx_normalized_ingest_id)"
        )
    ] == ["normalized_id"]
    assert normalized_index._structure_is_valid(conn)
    conn.close()


def test_structure_validator_rejects_missing_columns_constraints_and_index():
    conn = _bare_protocol_connection()
    assert normalized_index._index_columns(conn) == []
    assert not normalized_index._structure_is_valid(conn)  # missing state table

    normalized_index.install_state_migration(conn)
    assert not normalized_index._structure_is_valid(conn)  # missing mapping table

    conn.execute(
        "CREATE TABLE normalized_ingest_index (fact_id TEXT, normalized_id TEXT, "
        "fact_revision INTEGER)"
    )
    assert not normalized_index._structure_is_valid(conn)  # no PK/NOT NULL/index
    conn.close()

    conn, _ = _complete_protocol_connection()
    for trigger in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='trigger' "
        "AND name LIKE 'normalized_ingest_%'"
    ).fetchall():
        conn.execute(f"DROP TRIGGER {trigger['name']}")
    conn.execute("DROP TABLE normalized_ingest_index_state")
    conn.execute("CREATE TABLE normalized_ingest_index_state (wrong TEXT)")
    assert not normalized_index._structure_is_valid(conn)  # wrong state columns
    conn.close()

    conn, _ = _complete_protocol_connection()
    conn.execute("DROP INDEX idx_normalized_ingest_id")
    assert not normalized_index._structure_is_valid(conn)  # missing lookup B-tree
    conn.close()


def test_structure_and_state_errors_fail_closed(monkeypatch):
    conn = _bare_protocol_connection()
    original_object_type = normalized_index._object_type

    def sqlite_error(_conn, _name):
        raise sqlite3.DatabaseError("damaged sqlite_master")

    monkeypatch.setattr(normalized_index, "_object_type", sqlite_error)
    assert not normalized_index._structure_is_valid(conn)
    normalized_index._mark_incomplete(conn)  # missing table is a harmless no-op

    class BrokenConnection:
        def execute(self, *_args, **_kwargs):
            raise sqlite3.DatabaseError("simulated state read failure")

    monkeypatch.setattr(normalized_index, "_structure_is_valid", lambda _conn: True)
    assert not normalized_index.is_complete(BrokenConnection())
    normalized_index._mark_incomplete(BrokenConnection())  # swallowed fail-closed

    monkeypatch.setattr(normalized_index, "_object_type", original_object_type)
    conn.close()


def test_refresh_facts_after_write_marks_damage_dirty_and_swallows_cache_errors(
    monkeypatch,
):
    conn = _bare_protocol_connection()
    with monkeypatch.context() as patcher:
        patcher.setattr(
            normalized_index, "_structure_is_valid", lambda _conn: False
        )
        normalized_index.refresh_facts_after_write(
            conn, ["unused"], was_complete=True
        )
    conn.close()

    conn, fact_id = _complete_protocol_connection()
    conn.execute(
        "UPDATE facts SET claim = 'changed' WHERE fact_id = ?", (fact_id,)
    )
    with monkeypatch.context() as patcher:
        patcher.setattr(normalized_index, "is_complete", lambda _conn: False)
        normalized_index.refresh_facts_after_write(
            conn, [fact_id], was_complete=True
        )
    assert conn.execute(
        "SELECT complete FROM normalized_ingest_index_state WHERE state_id = 1"
    ).fetchone()[0] == 0
    conn.close()

    conn, fact_id = _complete_protocol_connection()
    conn.execute(
        "UPDATE facts SET claim = 'changed again' WHERE fact_id = ?", (fact_id,)
    )

    def fail_upsert(*_args, **_kwargs):
        raise RuntimeError("synthetic derived cache failure")

    with monkeypatch.context() as patcher:
        patcher.setattr(normalized_index, "_upsert_fact_mapping", fail_upsert)
        normalized_index.refresh_facts_after_write(
            conn, [fact_id], was_complete=True
        )
    assert conn.execute(
        "SELECT complete FROM normalized_ingest_index_state WHERE state_id = 1"
    ).fetchone()[0] == 0
    conn.close()


def test_rebuild_row_count_and_final_completeness_checks_fail_closed(monkeypatch):
    conn = _bare_protocol_connection()
    _insert_protocol_fact(conn)
    conn.execute(
        "CREATE TABLE normalized_ingest_index (fact_id TEXT PRIMARY KEY, "
        "normalized_id TEXT NOT NULL, fact_revision INTEGER NOT NULL)"
    )
    conn.execute(
        "CREATE TRIGGER suppress_index_insert BEFORE INSERT ON normalized_ingest_index "
        "BEGIN SELECT RAISE(IGNORE); END"
    )
    with pytest.raises(RuntimeError, match="row-count mismatch"):
        normalized_index._rebuild_conn(conn)
    conn.close()

    conn = _bare_protocol_connection()
    _insert_protocol_fact(conn)
    monkeypatch.setattr(normalized_index, "is_complete", lambda _conn: False)
    with pytest.raises(RuntimeError, match="completeness check"):
        normalized_index._rebuild_conn(conn)
    conn.close()


def test_stale_revision_candidate_falls_back_to_exact_scan(monkeypatch):
    claim = "Stale revision candidate must not become a false negative"
    legacy_id = _seed_validated_legacy(claim)
    assert normalized_index.rebuild_normalized_ingest_index() == 1
    with memory._db() as conn:
        conn.execute(
            "UPDATE normalized_ingest_index SET fact_revision = -1 WHERE fact_id = ?",
            (legacy_id,),
        )
    # Simulate a marker reader racing a stale candidate; the candidate-level
    # revision check independently refuses a fast negative and exact-scans.
    monkeypatch.setattr(normalized_index, "is_complete", lambda _conn: True)
    assert normalized_index.resolve_validated_normalized_fact(claim) == legacy_id


def test_remove_mapping_handles_missing_and_existing_rows():
    assert normalized_index.remove_fact("ing:does-not-exist") is False
    legacy_id = _seed_validated_legacy("Remove mapping helper target")
    assert normalized_index.rebuild_normalized_ingest_index() == 1
    assert normalized_index.remove_fact(legacy_id) is True
    assert normalized_index.remove_fact(legacy_id) is False


def test_memory_and_ingest_best_effort_hooks_swallow_derived_failures(monkeypatch, caplog):
    conn = _bare_protocol_connection()

    def fail_capture(_conn):
        raise RuntimeError("capture failure")

    def fail_refresh(*_args, **_kwargs):
        raise RuntimeError("refresh failure")

    monkeypatch.setattr(normalized_index, "capture_complete", fail_capture)
    assert memory._normalized_index_capture_complete(conn) is False
    monkeypatch.setattr(normalized_index, "refresh_facts_after_write", fail_refresh)
    memory._normalized_index_refresh_after_write(conn, [], was_complete=True)
    conn.close()

    def fail_rebuild():
        raise RuntimeError("rebuild failure")

    monkeypatch.setattr("core.ingest.rebuild_if_incomplete", fail_rebuild)
    _refresh_normalized_ingest_index_after_success("warning-only path")
    assert "Skipping derived normalized-ingest index refresh" in caplog.text


def test_direct_sql_claim_change_invalidates_and_exact_scans():
    original_claim = "Direct SQL claim mutation original content"
    changed_claim = "Direct SQL claim mutation updated content"
    legacy_id = _seed_validated_legacy(original_claim)
    assert normalized_index.rebuild_normalized_ingest_index() == 1

    with memory._db() as conn:
        conn.execute(
            "UPDATE facts SET claim = ?, revision = revision + 1 WHERE fact_id = ?",
            (crypto.encrypt(changed_claim), legacy_id),
        )
    assert not _is_index_complete()
    assert normalized_index.resolve_validated_normalized_fact(original_claim) is None
    assert normalized_index.resolve_validated_normalized_fact(changed_claim) == legacy_id


def test_structure_validator_rejects_wrong_mapping_column_names():
    conn = _bare_protocol_connection()
    normalized_index.install_state_migration(conn)
    conn.execute(
        "CREATE TABLE normalized_ingest_index (fact_id TEXT PRIMARY KEY, "
        "wrong_column TEXT NOT NULL, fact_revision INTEGER NOT NULL)"
    )
    assert not normalized_index._structure_is_valid(conn)
    conn.close()
