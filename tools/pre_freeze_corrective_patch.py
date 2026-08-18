from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one anchor, found {count}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def patch_evidence() -> None:
    replace_once(
        "core/evidence.py",
        """    document/chunk-level reference). A half-open [start, end) range must satisfy\n    0 <= start <= end.\n""",
        """    document/chunk-level reference). A half-open [start, end) text range must\n    satisfy 0 <= start < end; a zero-length boundary is not evidence of a claim.\n""",
    )
    replace_once(
        "core/evidence.py",
        """    if span_start > span_end:\n        raise ValueError(\n            f\"attach_evidence: invalid span [{span_start}, {span_end})\")\n""",
        """    if span_start >= span_end:\n        raise ValueError(\n            f\"attach_evidence: span must be non-empty [{span_start}, {span_end})\")\n""",
    )
    replace_once(
        "core/evidence.py",
        """        return 0 <= start <= end\n""",
        """        return 0 <= start < end\n""",
    )


def patch_reconcile() -> None:
    helper = '''def _grant_reinforcement_lineage(fact_id: str, evidence_id: Optional[str]) -> str:\n    \"\"\"Resolve grant reinforcement lineage from authoritative evidence only.\n\n    Caller-supplied lineage labels are not authority. The evidence store owns the\n    fact binding, claim binding, source digest/location and declared lineage.\n    \"\"\"\n    if not isinstance(evidence_id, str) or not evidence_id.strip():\n        raise ValueError(\"reinforce: grant profile requires evidence_id\")\n\n    from core.evidence import valid_evidence_for_grounding\n\n    row = next(\n        (item for item in valid_evidence_for_grounding(fact_id)\n         if item.get(\"evidence_id\") == evidence_id),\n        None,\n    )\n    if row is None:\n        raise ValueError(\n            \"reinforce: evidence_id must reference valid evidence for this fact\")\n    if row.get(\"independence_class\") != \"INDEPENDENT_ASSERTED\":\n        raise ValueError(\n            \"reinforce: grant confidence change requires INDEPENDENT_ASSERTED evidence\")\n    lineage = row.get(\"lineage_id\")\n    if not isinstance(lineage, str) or not lineage.strip():\n        raise ValueError(\"reinforce: grant evidence requires lineage_id\")\n    basis = row.get(\"lineage_basis\")\n    if not isinstance(basis, str) or not basis.strip() or basis == \"UNKNOWN\":\n        raise ValueError(\"reinforce: grant evidence requires lineage assertion basis\")\n    return lineage.strip()\n\n\n'''
    replace_once("core/reconcile.py", "def reinforce(\n", helper + "def reinforce(\n")
    replace_once(
        "core/reconcile.py",
        """    *,\n    lineage_id: Optional[str] = None,\n) -> Optional[float]:\n""",
        """    *,\n    lineage_id: Optional[str] = None,\n    evidence_id: Optional[str] = None,\n) -> Optional[float]:\n""",
    )
    replace_once(
        "core/reconcile.py",
        """    ``lineage_id`` identifies the evidence family that caused this explicit\n    reinforcement. In the grant profile it is mandatory. Reusing an already\n    counted lineage is idempotent: it cannot increase observations or confidence.\n    Outside the grant profile a missing lineage remains backward-compatible but\n    is recorded as UNKNOWN rather than being represented as independent evidence.\n""",
        """    In the grant profile, ``evidence_id`` is mandatory and is resolved through\n    the evidence store. Its fact binding, replayability, independence assertion,\n    lineage and assertion basis are validated before confidence may change.\n    ``lineage_id`` remains only for backward-compatible non-grant callers.\n""",
    )
    replace_once(
        "core/reconcile.py",
        """    normalized_lineage = lineage_id.strip() if isinstance(lineage_id, str) and lineage_id.strip() else None\n    grant_profile = os.environ.get(\"VELANTRIM_RELEASE_PROFILE\", \"\").strip().casefold() == \"grant\"\n    if grant_profile and normalized_lineage is None:\n        raise ValueError(\"reinforce: grant profile requires lineage_id\")\n""",
        """    normalized_lineage = lineage_id.strip() if isinstance(lineage_id, str) and lineage_id.strip() else None\n    grant_profile = os.environ.get(\"VELANTRIM_RELEASE_PROFILE\", \"\").strip().casefold() == \"grant\"\n    if grant_profile:\n        if normalized_lineage is not None:\n            raise ValueError(\n                \"reinforce: grant profile derives lineage_id from evidence_id\")\n        normalized_lineage = _grant_reinforcement_lineage(fact_id, evidence_id)\n""",
    )


def patch_trace() -> None:
    replace_once(
        "core/trace.py",
        """        entry: Dict[str, Any] = {\n            \"trace_version\": 2,\n            \"fact_id\": fact_id,\n            \"source\": item.get(\"source\", \"unknown\"),\n""",
        """        source = item.get(\"source\")\n        if not isinstance(source, str) or not source.strip():\n            source = \"unknown\"\n\n        entry: Dict[str, Any] = {\n            \"trace_version\": 2,\n            \"fact_id\": fact_id,\n            \"source\": source,\n""",
    )


def patch_storage() -> None:
    replace_once(
        "core/storage_migration.py",
        """DATASET_FILES = {\n    \"nodes\": \"nodes.jsonl\",\n    \"vectors\": \"vectors.jsonl\",\n    \"edges\": \"edges.jsonl\",\n    \"entities\": \"entities.jsonl\",\n    \"mentions\": \"mentions.jsonl\",\n    \"meta\": \"meta.jsonl\",\n}\n""",
        """DATASET_FILES = {\n    \"nodes\": \"nodes.jsonl\",\n    \"vectors\": \"vectors.jsonl\",\n    \"edges\": \"edges.jsonl\",\n    \"entities\": \"entities.jsonl\",\n    \"mentions\": \"mentions.jsonl\",\n    \"meta\": \"meta.jsonl\",\n}\nMAX_MIGRATION_DIRECTORY_ENTRIES = 2 + len(DATASET_FILES)\n""",
    )
    replace_once(
        "core/storage_migration.py",
        """        with os.scandir(path) as iterator:\n            for entry in iterator:\n                try:\n""",
        """        with os.scandir(path) as iterator:\n            for entry in iterator:\n                if len(entries) >= MAX_MIGRATION_DIRECTORY_ENTRIES:\n                    raise StorageOperationError(\n                        f\"{label} exceeds the {MAX_MIGRATION_DIRECTORY_ENTRIES}-entry resource limit\"\n                    )\n                try:\n""",
    )


def patch_eval() -> None:
    replace_once(
        "core/eval.py",
        """def _fixture_manifest() -> Optional[Dict[str, Any]]:\n    try:\n        text = resources.files(_FIXTURE_PKG).joinpath(_FIXTURE_MANIFEST).read_text(encoding=\"utf-8\")\n        data = json.loads(text)\n    except (FileNotFoundError, ModuleNotFoundError, OSError, ValueError):\n        return None\n    return data if isinstance(data, dict) else None\n""",
        """def _fixture_manifest() -> Dict[str, Any]:\n    \"\"\"Load the frozen fixture manifest; absence or corruption is a gate failure.\"\"\"\n    try:\n        text = resources.files(_FIXTURE_PKG).joinpath(_FIXTURE_MANIFEST).read_text(encoding=\"utf-8\")\n        data = json.loads(text)\n    except (FileNotFoundError, ModuleNotFoundError, OSError, ValueError) as exc:\n        raise RuntimeError(\"fixture manifest is missing or malformed\") from exc\n    if not isinstance(data, dict):\n        raise RuntimeError(\"fixture manifest must be a JSON object\")\n    return data\n""",
    )
    replace_once(
        "core/eval.py",
        """        manifest = _fixture_manifest()\n        if manifest is not None:\n            expected = (manifest.get(\"sha256\") or {}).get(name)\n            if not isinstance(expected, str) or not expected:\n                raise RuntimeError(f\"fixture manifest has no digest for {name}\")\n            actual = hashlib.sha256(text.encode(\"utf-8\")).hexdigest()\n            if actual != expected:\n                raise RuntimeError(\n                    f\"fixture digest mismatch for {name}: expected {expected}, got {actual}\"\n                )\n""",
        """        manifest = _fixture_manifest()\n        expected = (manifest.get(\"sha256\") or {}).get(name)\n        if not isinstance(expected, str) or not expected:\n            raise RuntimeError(f\"fixture manifest has no digest for {name}\")\n        actual = hashlib.sha256(text.encode(\"utf-8\")).hexdigest()\n        if actual != expected:\n            raise RuntimeError(\n                f\"fixture digest mismatch for {name}: expected {expected}, got {actual}\"\n            )\n""",
    )


def patch_existing_tests() -> None:
    replace_once(
        "tests/test_bounded_legacy_retrieval.py",
        """        \"reindex_recommended\": True,\n    }\n""",
        """        \"reindex_recommended\": True,\n        \"reason_code\": LEGACY_REINDEX_REASON_CODE,\n    }\n""",
    )
    path = ROOT / "tests/test_pre_freeze_wave3.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace("import pytest\n", "import pytest\nfrom concurrent.futures import ThreadPoolExecutor\n", 1)
    text = text.replace(
        """def test_grant_profile_reinforce_requires_lineage(monkeypatch):\n    _stored_verified(\"f5\")\n    monkeypatch.setenv(\"VELANTRIM_RELEASE_PROFILE\", \"grant\")\n    with pytest.raises(ValueError, match=\"requires lineage_id\"):\n        reconcile.reinforce(\"f5\")\n\n\n""",
        '''def test_zero_length_evidence_span_is_rejected():\n    fact = _stored_verified("f2-zero")\n    with pytest.raises(ValueError, match="span must be non-empty"):\n        evidence.attach_evidence(\n            fact["fact_id"], "file://source.txt", source_text="source content",\n            span_start=0, span_end=0,\n        )\n\n\ndef _independent_evidence(fact_id, lineage_id):\n    return evidence.attach_evidence(\n        fact_id,\n        f"file://{fact_id}-{lineage_id}.txt",\n        source_text=f"source for {fact_id} {lineage_id}",\n        span_start=0, span_end=6,\n        lineage_id=lineage_id,\n        independence_class="INDEPENDENT_ASSERTED",\n        lineage_basis="IMPORTER_DECLARED",\n    )\n\n\ndef test_grant_profile_reinforce_requires_authoritative_evidence(monkeypatch):\n    _stored_verified("f5")\n    monkeypatch.setenv("VELANTRIM_RELEASE_PROFILE", "grant")\n    with pytest.raises(ValueError, match="requires evidence_id"):\n        reconcile.reinforce("f5")\n    with pytest.raises(ValueError, match="derives lineage_id"):\n        reconcile.reinforce("f5", lineage_id="caller-invented")\n\n\ndef test_grant_reinforce_derives_lineage_and_deduplicates_across_evidence_ids(monkeypatch):\n    _stored_verified("f5-dedup")\n    first_evidence = _independent_evidence("f5-dedup", "family:one")\n    second_evidence = _independent_evidence("f5-dedup", "family:one")\n    monkeypatch.setenv("VELANTRIM_RELEASE_PROFILE", "grant")\n\n    first = reconcile.reinforce("f5-dedup", evidence_id=first_evidence["evidence_id"])\n    after_first = get_fact("f5-dedup")["metadata"]["observations"]\n    second = reconcile.reinforce("f5-dedup", evidence_id=second_evidence["evidence_id"])\n\n    assert second == first\n    assert get_fact("f5-dedup")["metadata"]["observations"] == after_first\n    assert get_fact("f5-dedup")["metadata"]["reinforcement_lineages"] == ["family:one"]\n\n\ndef test_grant_reinforce_rejects_nonindependent_or_wrong_fact_evidence(monkeypatch):\n    _stored_verified("f5-primary")\n    _stored_verified("f5-other")\n    same_lineage = evidence.attach_evidence(\n        "f5-primary", "file://same-lineage.txt", source_text="same lineage",\n        span_start=0, span_end=4, lineage_id="family:one",\n        independence_class="SAME_LINEAGE", lineage_basis="IMPORTER_DECLARED",\n    )\n    wrong_fact = _independent_evidence("f5-other", "family:other")\n    monkeypatch.setenv("VELANTRIM_RELEASE_PROFILE", "grant")\n\n    with pytest.raises(ValueError, match="INDEPENDENT_ASSERTED"):\n        reconcile.reinforce("f5-primary", evidence_id=same_lineage["evidence_id"])\n    with pytest.raises(ValueError, match="valid evidence for this fact"):\n        reconcile.reinforce("f5-primary", evidence_id=wrong_fact["evidence_id"])\n\n\ndef test_grant_same_lineage_concurrent_reinforcement_increments_once(monkeypatch):\n    _stored_verified("f5-race")\n    first = _independent_evidence("f5-race", "family:race")\n    second = _independent_evidence("f5-race", "family:race")\n    monkeypatch.setenv("VELANTRIM_RELEASE_PROFILE", "grant")\n    evidence_ids = [first["evidence_id"], second["evidence_id"]] * 4\n\n    with ThreadPoolExecutor(max_workers=8) as pool:\n        list(pool.map(lambda eid: reconcile.reinforce("f5-race", evidence_id=eid), evidence_ids))\n\n    fact = get_fact("f5-race")\n    assert fact["metadata"]["observations"] == 2\n    assert fact["metadata"]["reinforcement_lineages"] == ["family:race"]\n\n\n''',
        1,
    )
    path.write_text(text, encoding="utf-8")


def write_closure_tests() -> None:
    (ROOT / "tests/test_pre_freeze_closure.py").write_text('''from __future__ import annotations\n\nimport json\n\nimport pytest\n\nfrom core import concept, eval as core_eval, pipeline, query_pipeline, trace\nfrom core.l3_graph import MockL3Graph\nfrom core.storage_common import StorageOperationError\nfrom core import storage_migration\n\n\ndef test_trace_normalizes_missing_source_and_malformed_signals():\n    rows = trace.build_trace([{\n        "id": "f:trace", "source": None, "origin": "memory",\n        "_score": float("inf"), "_retrieval_signals": None,\n    }])\n    assert rows[0]["source"] == "unknown"\n    assert rows[0]["retrieval_score"] == 0.0\n    assert rows[0]["retrieval_signals"] == ["memory"]\n    assert isinstance(rows[0]["source"], str)\n\n\n@pytest.mark.parametrize("source", ["", 123, False])\ndef test_trace_source_is_always_schema_string(source):\n    assert trace.build_trace([{"id": "f", "source": source}])[0]["source"] == "unknown"\n\n\ndef test_fixture_manifest_missing_or_malformed_fails_closed(monkeypatch):\n    class Missing:\n        def joinpath(self, _name):\n            return self\n        def read_text(self, **_kwargs):\n            raise FileNotFoundError("missing")\n    monkeypatch.setattr(core_eval.resources, "files", lambda _pkg: Missing())\n    with pytest.raises(RuntimeError, match="manifest is missing or malformed"):\n        core_eval._fixture_manifest()\n\n    class Malformed(Missing):\n        def read_text(self, **_kwargs):\n            return "[]"\n    monkeypatch.setattr(core_eval.resources, "files", lambda _pkg: Malformed())\n    with pytest.raises(RuntimeError, match="must be a JSON object"):\n        core_eval._fixture_manifest()\n\n\ndef test_directory_inventory_has_hard_entry_ceiling(tmp_path):\n    for index in range(storage_migration.MAX_MIGRATION_DIRECTORY_ENTRIES + 1):\n        (tmp_path / f"entry-{index}").write_text("x", encoding="utf-8")\n    with pytest.raises(StorageOperationError, match="entry resource limit"):\n        storage_migration._directory_entry_inventory(tmp_path, "bundle")\n\n\ndef test_provider_failure_uses_explicit_lexical_degradation(monkeypatch):\n    graph = MockL3Graph()\n    graph.merge_fact({\n        "fact_id": "provider-fallback", "claim": "provider fallback topic",\n        "source": "local", "confidence": 0.9, "epistemic_state": "Validated",\n        "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",\n        "truth_status": "VERIFIED", "restricted": False,\n    })\n    graph.set_embedder_fingerprint("stored:embedder")\n    monkeypatch.setattr(query_pipeline, "get_l3_graph", lambda: graph)\n    monkeypatch.setattr(query_pipeline, "get_embedder", lambda: (_ for _ in ()).throw(RuntimeError("offline")))\n    rows = query_pipeline._retrieve_read_only("provider fallback topic", k=3)\n    assert getattr(rows, "degradation_reason_code") == query_pipeline._EMBEDDER_PROVIDER_FALLBACK\n\n\ndef test_nonvalidated_graph_target_cannot_receive_activation():\n    assert pipeline._may_propagate_activation({\n        "fact_id": "observed", "epistemic_state": "Observed", "restricted": False,\n    }) is False\n\n\ndef test_concept_eligibility_ignores_malformed_nodes():\n    class Graph:\n        def all_facts(self):\n            return [{"claim": "missing id"}, {"fact_id": 42}]\n    assert concept._concept_eligible_fact_ids(Graph()) == set()\n''', encoding="utf-8")


def patch_evidence_doc() -> None:
    path = ROOT / "docs/grant/CRYSTAL_PRE_FREEZE_EVIDENCE.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "Cleaned implementation baseline SHA: `5b419ed8e268c72caf3d707666006507ab2eefe7`\n\nThis package accompanies the Crystal pre-freeze remediation branch. The baseline above contains the production remediation code with all temporary pre-freeze patch scripts and one-shot workflows removed. The current documentation-only child commit is used to trigger the repository's normal supported CI matrix against the same implementation tree.\n",
        "Corrective closure status: **pending final exact-SHA CI evidence**.\n\nThe exact freeze-candidate SHA is intentionally not pinned until the corrective delta and the full Python 3.11/3.12 matrix are green on one head. Intermediate SHAs are not freeze evidence.\n",
    )
    text = text.replace(
        "6. Evidence lineage is unknown by default; same-lineage reinforcement cannot increase support twice.\n",
        "6. In the grant profile, reinforcement accepts an authoritative `evidence_id`; lineage is derived from the evidence store, `UNKNOWN`/`SAME_LINEAGE` cannot raise support, and one lineage can contribute at most once.\n",
    )
    text = text.replace(
        "8. The shipping evaluation corpus is hash-frozen and gates strict provenance + lineage metrics.\n",
        "8. The shipping evaluation corpus is hash-frozen; a missing/malformed manifest fails closed and the gate checks strict provenance + lineage metrics.\n",
    )
    text = text.replace(
        "Crystal does not claim that retrieval equals truth, ranking equals confidence, a graph path is proof, a source label is exact evidence, source count implies independent corroboration, an embedding fallback preserves semantic equivalence, bounded hop depth alone bounds graph work, or green CI constitutes production authorization.\n",
        "Crystal does not claim that retrieval equals truth, ranking equals confidence, a graph path is proof, a source label is exact evidence, source count implies independent corroboration, an embedding fallback preserves semantic equivalence, bounded hop depth alone bounds graph work, or green CI constitutes production authorization. Durable SQLite/Cypher graph backends push edge limits into the backend query; `MockL3Graph` is a non-durable test backend and is not part of the production resource-bound claim. The HTTP API exposes evidence read-only; it does not expose `attach_evidence()` or `reinforce()` as remote write authority.\n",
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    patch_evidence()
    patch_reconcile()
    patch_trace()
    patch_storage()
    patch_eval()
    patch_existing_tests()
    write_closure_tests()
    patch_evidence_doc()


if __name__ == "__main__":
    main()
