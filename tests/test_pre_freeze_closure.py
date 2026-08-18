from __future__ import annotations

import pytest

from core import concept, eval as core_eval, pipeline, query_pipeline, storage_migration, trace
from core.l3_graph import MockL3Graph
from core.storage_common import StorageOperationError


def test_trace_normalizes_missing_source_and_malformed_signals():
    rows = trace.build_trace([{
        "id": "f:trace", "source": None, "origin": "memory",
        "_score": float("inf"), "_retrieval_signals": None,
    }])
    assert rows[0]["source"] == "unknown"
    assert rows[0]["retrieval_score"] == 0.0
    assert rows[0]["retrieval_signals"] == ["memory"]
    assert isinstance(rows[0]["source"], str)


@pytest.mark.parametrize("source", ["", 123, False])
def test_trace_source_is_always_schema_string(source):
    assert trace.build_trace([{"id": "f", "source": source}])[0]["source"] == "unknown"


def test_fixture_manifest_missing_or_malformed_fails_closed(monkeypatch):
    class Missing:
        def joinpath(self, _name):
            return self

        def read_text(self, **_kwargs):
            raise FileNotFoundError("missing")

    monkeypatch.setattr(core_eval.resources, "files", lambda _pkg: Missing())
    with pytest.raises(RuntimeError, match="manifest is missing or malformed"):
        core_eval._fixture_manifest()

    class Malformed(Missing):
        def read_text(self, **_kwargs):
            return "[]"

    monkeypatch.setattr(core_eval.resources, "files", lambda _pkg: Malformed())
    with pytest.raises(RuntimeError, match="must be a JSON object"):
        core_eval._fixture_manifest()


def test_directory_inventory_has_hard_entry_ceiling(tmp_path):
    for index in range(storage_migration.MAX_MIGRATION_DIRECTORY_ENTRIES + 1):
        (tmp_path / f"entry-{index}").write_text("x", encoding="utf-8")
    with pytest.raises(StorageOperationError, match="entry resource limit"):
        storage_migration._directory_entry_inventory(tmp_path, "bundle")


def test_directory_inventory_surfaces_scandir_failure(monkeypatch, tmp_path):
    def fail_scandir(_path):
        raise OSError("cannot scan")

    monkeypatch.setattr(storage_migration.os, "scandir", fail_scandir)
    with pytest.raises(StorageOperationError, match="cannot enumerate bundle"):
        storage_migration._directory_entry_inventory(tmp_path, "bundle")


def test_directory_inventory_surfaces_entry_stat_failure(monkeypatch, tmp_path):
    class Entry:
        name = "broken-entry"

        @staticmethod
        def stat(*, follow_symlinks):
            assert follow_symlinks is False
            raise OSError("cannot stat")

    class Scanner:
        def __enter__(self):
            return iter([Entry()])

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr(storage_migration.os, "scandir", lambda _path: Scanner())
    with pytest.raises(StorageOperationError, match="cannot inspect bundle entry"):
        storage_migration._directory_entry_inventory(tmp_path, "bundle")


def test_provider_failure_uses_explicit_lexical_degradation(monkeypatch):
    graph = MockL3Graph()
    graph.merge_fact({
        "fact_id": "provider-fallback", "claim": "provider fallback topic",
        "source": "local", "confidence": 0.9, "epistemic_state": "Validated",
        "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
        "truth_status": "VERIFIED", "restricted": False,
    })
    graph.set_embedder_fingerprint("stored:embedder")
    monkeypatch.setattr(query_pipeline, "get_l3_graph", lambda: graph)
    monkeypatch.setattr(
        query_pipeline,
        "get_embedder",
        lambda: (_ for _ in ()).throw(RuntimeError("offline")),
    )
    rows = query_pipeline._retrieve_read_only("provider fallback topic", k=3)
    assert getattr(rows, "degradation_reason_code") == query_pipeline._EMBEDDER_PROVIDER_FALLBACK


def test_nonvalidated_graph_target_cannot_receive_activation():
    assert pipeline._may_propagate_activation({
        "fact_id": "observed", "epistemic_state": "Observed", "restricted": False,
    }) is False


def test_concept_eligibility_ignores_malformed_nodes():
    class Graph:
        def all_facts(self):
            return [{"claim": "missing id"}, {"fact_id": 42}]

    assert concept._concept_eligible_fact_ids(Graph()) == set()
