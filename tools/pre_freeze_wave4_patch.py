from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly one anchor, found {count}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def patch_concept_gating() -> None:
    replace_once(
        "core/concept.py",
        "from core.l3_graph import get_l3_graph\n",
        "from core.l3_graph import get_l3_graph\nfrom core.trust_snapshot import TrustSnapshot\n",
    )
    replace_once(
        "core/concept.py",
        '''def hebbian_weights() -> Dict[Tuple[str, str], int]:\n''',
        '''def _concept_eligible_fact_ids(graph) -> set[str]:\n    """Deny-dominant eligible facts for concept clustering.\n\n    Concept emergence may write entity/membership projections, so a non-admitted,\n    restricted, terminal, or store-conflicted fact must not shape a cluster.\n    This mirrors the read boundary without importing the retrieval pipeline.\n    """\n    eligible: set[str] = set()\n    for node in graph.all_facts():\n        fact_id = node.get("fact_id")\n        if not isinstance(fact_id, str) or not fact_id:\n            continue\n        snapshot = TrustSnapshot.from_records(\n            fact_id=fact_id, l3=node, l1=get_fact(fact_id), retrieval_score=0.0\n        )\n        if snapshot.epistemic_state == "Validated" and snapshot.restricted is False:\n            eligible.add(fact_id)\n    return eligible\n\n\ndef hebbian_weights() -> Dict[Tuple[str, str], int]:\n''',
    )
    replace_once(
        "core/concept.py",
        '''    directed: Dict[Tuple[str, str], int] = {}\n    for fact in graph.all_facts():\n        a = fact["fact_id"]\n        for edge in graph.get_edges(a, _EPISODE_REL):\n            b = edge["target"]\n            if a == b:\n                continue\n            directed[(a, b)] = directed.get((a, b), 0) + 1\n''',
        '''    directed: Dict[Tuple[str, str], int] = {}\n    eligible = _concept_eligible_fact_ids(graph)\n    for a in sorted(eligible):\n        for edge in graph.get_edges(a, _EPISODE_REL):\n            b = edge["target"]\n            if a == b or b not in eligible:\n                continue\n            directed[(a, b)] = directed.get((a, b), 0) + 1\n''',
    )


def patch_eval_gate() -> None:
    replace_once("core/eval.py", "import json\n", "import hashlib\nimport json\n")
    replace_once(
        "core/eval.py",
        '''_FIXTURE_PKG = "core._eval_fixtures"\n''',
        '''_FIXTURE_PKG = "core._eval_fixtures"\n_FIXTURE_MANIFEST = "manifest.json"\n''',
    )
    old_loader = '''def _load_fixture_json(name: str) -> Optional[Dict[str, Any]]:\n    """Load a bundled fixture JSON by file name, or None if unavailable."""\n    try:\n        text = resources.files(_FIXTURE_PKG).joinpath(name).read_text(encoding="utf-8")\n        return json.loads(text)\n    except (FileNotFoundError, ModuleNotFoundError, OSError, ValueError):\n        return None\n'''
    new_loader = '''def _fixture_manifest() -> Optional[Dict[str, Any]]:\n    try:\n        text = resources.files(_FIXTURE_PKG).joinpath(_FIXTURE_MANIFEST).read_text(encoding="utf-8")\n        data = json.loads(text)\n    except (FileNotFoundError, ModuleNotFoundError, OSError, ValueError):\n        return None\n    return data if isinstance(data, dict) else None\n\n\ndef _load_fixture_json(name: str) -> Optional[Dict[str, Any]]:\n    """Load a bundled fixture and fail closed if its frozen digest drifts."""\n    try:\n        text = resources.files(_FIXTURE_PKG).joinpath(name).read_text(encoding="utf-8")\n        manifest = _fixture_manifest()\n        if manifest is not None:\n            expected = (manifest.get("sha256") or {}).get(name)\n            if not isinstance(expected, str) or not expected:\n                raise RuntimeError(f"fixture manifest has no digest for {name}")\n            actual = hashlib.sha256(text.encode("utf-8")).hexdigest()\n            if actual != expected:\n                raise RuntimeError(\n                    f"fixture digest mismatch for {name}: expected {expected}, got {actual}"\n                )\n        return json.loads(text)\n    except RuntimeError:\n        raise\n    except (FileNotFoundError, ModuleNotFoundError, OSError, ValueError):\n        return None\n'''
    replace_once("core/eval.py", old_loader, new_loader)
    replace_once(
        "core/eval.py",
        '''def source_span_coverage(fact_ids: Sequence[str]) -> float:\n    """Fraction of facts that carry at least one source-span evidence record (WP1)."""\n    ids = list(fact_ids)\n    if not ids:\n        return 0.0\n    covered = sum(1 for fid in ids if evidence.evidence_for(fid))\n    return round(covered / len(ids), 4)\n''',
        '''def source_span_coverage(fact_ids: Sequence[str]) -> float:\n    """Fraction of facts that carry at least one source-span evidence record (WP1)."""\n    ids = list(fact_ids)\n    if not ids:\n        return 0.0\n    covered = sum(1 for fid in ids if evidence.evidence_for(fid))\n    return round(covered / len(ids), 4)\n\n\ndef strict_source_span_coverage(fact_ids: Sequence[str]) -> float:\n    """Fraction with replayable evidence eligible for grant strict grounding."""\n    ids = list(fact_ids)\n    if not ids:\n        return 0.0\n    covered = sum(1 for fid in ids if evidence.has_valid_evidence_for_grounding(fid))\n    return round(covered / len(ids), 4)\n''',
    )
    replace_once(
        "core/eval.py",
        '''    for case in cases:\n        res = ingest(case["claim"], source_status="EXTERNAL")\n        fid = res["fact"]["fact_id"]\n        claim_to_id[case["claim"]] = fid\n        evidence.attach_evidence(fid, "eval-fixture", source_kind="fixture",\n                                 claim=case["claim"])\n''',
        '''    for case_index, case in enumerate(cases, 1):\n        res = ingest(case["claim"], source_status="EXTERNAL")\n        fid = res["fact"]["fact_id"]\n        claim_to_id[case["claim"]] = fid\n        evidence.attach_evidence(\n            fid,\n            f"fixture://retrieval/{case_index}",\n            source_kind="fixture",\n            claim=case["claim"],\n            section=f"case:{case_index}",\n            source_text=case["claim"],\n            lineage_id=f"fixture-lineage:{case_index}",\n            independence_class="INDEPENDENT_ASSERTED",\n            lineage_basis="IMPORTER_DECLARED",\n        )\n''',
    )
    replace_once(
        "core/eval.py",
        '''    report = {\n        "cases": len(cases),\n        "retrieval": aggregate(per_case),\n        "trace_completeness": round(traced / n, 4),\n        "metadata_completeness": metadata_completeness(fact_ids),\n        "source_span_coverage": source_span_coverage(fact_ids),\n        "unsupported_provenance": unsupported_provenance_count(fact_ids),\n        "receipt_replay_survival": round(receipts_ok / n, 4),\n        "contradiction": contradiction_eval(),\n    }\n''',
        '''    report = {\n        "cases": len(cases),\n        "retrieval": aggregate(per_case),\n        "trace_completeness": round(traced / n, 4),\n        "metadata_completeness": metadata_completeness(fact_ids),\n        "source_span_coverage": source_span_coverage(fact_ids),\n        "strict_source_span_coverage": strict_source_span_coverage(fact_ids),\n        "unsupported_provenance": unsupported_provenance_count(fact_ids),\n        "receipt_replay_survival": round(receipts_ok / n, 4),\n        "lineage": evidence.lineage_metrics(fact_ids),\n        "contradiction": contradiction_eval(),\n    }\n''',
    )
    replace_once(
        "core/eval.py",
        '''    "source_span_coverage": 1.0,\n    "receipt_replay_survival": 1.0,\n''',
        '''    "source_span_coverage": 1.0,\n    "strict_source_span_coverage": 1.0,\n    "receipt_replay_survival": 1.0,\n    "lineage.known_lineage_coverage": 1.0,\n    "lineage.independence_assertion_coverage": 1.0,\n''',
    )
    replace_once(
        "core/eval.py",
        '''    "unsupported_provenance": 0,          # baseline 0\n    "contradiction.false_positive_rate": 0.25,   # baseline 0.1667\n''',
        '''    "unsupported_provenance": 0,          # baseline 0\n    "lineage.same_lineage_duplicate_rate": 0.0,\n    "lineage.unknown_lineage_rate": 0.0,\n    "contradiction.false_positive_rate": 0.25,   # baseline 0.1667\n''',
    )
    replace_once(
        "core/eval.py",
        '''        f"| source_span_coverage | {r['source_span_coverage']} |",\n        f"| unsupported_provenance | {r['unsupported_provenance']} |",\n''',
        '''        f"| source_span_coverage | {r['source_span_coverage']} |",\n        f"| strict_source_span_coverage | {r['strict_source_span_coverage']} |",\n        f"| lineage.known_lineage_coverage | {r['lineage']['known_lineage_coverage']} |",\n        f"| lineage.same_lineage_duplicate_rate | {r['lineage']['same_lineage_duplicate_rate']} |",\n        f"| lineage.unknown_lineage_rate | {r['lineage']['unknown_lineage_rate']} |",\n        f"| unsupported_provenance | {r['unsupported_provenance']} |",\n''',
    )
    replace_once(
        "scripts/eval_gate.py",
        '''          f"span={report['source_span_coverage']} "\n          f"receipts={report['receipt_replay_survival']} "\n''',
        '''          f"span={report['source_span_coverage']} "\n          f"strict_span={report['strict_source_span_coverage']} "\n          f"receipts={report['receipt_replay_survival']} "\n''',
    )
    replace_once(
        "scripts/eval_gate.py",
        '''          f"unsupported={report['unsupported_provenance']}")\n''',
        '''          f"unsupported={report['unsupported_provenance']} "\n          f"lineage_known={report['lineage']['known_lineage_coverage']} "\n          f"lineage_dupes={report['lineage']['same_lineage_duplicate_rate']}")\n''',
    )


def write_fixture_manifest() -> None:
    fixture_dir = ROOT / "core" / "_eval_fixtures"
    names = sorted(\n        path.name for path in fixture_dir.glob("*.json")\n        if path.name != "manifest.json"\n    )
    manifest = {\n        "version": 1,\n        "algorithm": "sha256",\n        "sha256": {\n            name: hashlib.sha256((fixture_dir / name).read_bytes()).hexdigest()\n            for name in names\n        },\n    }\n    (fixture_dir / "manifest.json").write_text(\n        json.dumps(manifest, indent=2, sort_keys=True) + "\\n", encoding="utf-8"\n    )


def write_wave4_tests() -> None:
    (ROOT / "tests/test_pre_freeze_wave4.py").write_text('''from __future__ import annotations\n\nfrom core import concept, eval as core_eval\nfrom core.l3_graph import get_l3_graph\nfrom core.memory import get_fact, store_fact, transition_esm\n\n\ndef _store(fid, *, validated=True, restricted=False):\n    store_fact({\n        "fact_id": fid, "claim": fid, "source": "s", "confidence": 0.9,\n        "source_status": "EXTERNAL", "restricted": restricted,\n    })\n    if validated:\n        transition_esm(fid, "Validated")\n    fact = get_fact(fid)\n    get_l3_graph().merge_fact(fact)\n    return fact\n\n\ndef test_concept_clustering_excludes_observed_and_restricted_facts():\n    graph = get_l3_graph()\n    _store("ok-a")\n    _store("ok-b")\n    _store("observed", validated=False)\n    _store("restricted", restricted=True)\n\n    for _ in range(2):\n        graph.add_edge("ok-a", "CO_OCCURRED", "ok-b")\n        graph.add_edge("ok-b", "CO_OCCURRED", "ok-a")\n        graph.add_edge("ok-a", "CO_OCCURRED", "observed")\n        graph.add_edge("observed", "CO_OCCURRED", "ok-a")\n        graph.add_edge("ok-a", "CO_OCCURRED", "restricted")\n        graph.add_edge("restricted", "CO_OCCURRED", "ok-a")\n\n    weights = concept.hebbian_weights()\n    assert ("ok-a", "ok-b") in weights\n    assert all("observed" not in pair for pair in weights)\n    assert all("restricted" not in pair for pair in weights)\n\n\ndef test_frozen_fixture_manifest_accepts_current_retrieval_fixture():\n    corpus = core_eval.load_retrieval_corpus("en")\n    assert corpus["cases"]\n\n\ndef test_shipping_gate_requires_strict_provenance_and_lineage():\n    report = {\n        "retrieval": {"hit@1": 1.0, "hit@3": 1.0, "mrr": 1.0},\n        "trace_completeness": 1.0,\n        "metadata_completeness": 1.0,\n        "source_span_coverage": 1.0,\n        "strict_source_span_coverage": 0.0,\n        "receipt_replay_survival": 1.0,\n        "unsupported_provenance": 0,\n        "lineage": {\n            "known_lineage_coverage": 0.0,\n            "independence_assertion_coverage": 0.0,\n            "same_lineage_duplicate_rate": 0.0,\n            "unknown_lineage_rate": 1.0,\n        },\n        "contradiction": {"precision": 1.0, "recall": 1.0, "false_positive_rate": 0.0},\n        "boundary": {"refusal_correctness": 1.0, "violations": 0},\n    }\n    verdict = core_eval.gate(report)\n    metrics = {failure["metric"] for failure in verdict["failures"]}\n    assert "strict_source_span_coverage" in metrics\n    assert "lineage.known_lineage_coverage" in metrics\n    assert "lineage.unknown_lineage_rate" in metrics\n''', encoding="utf-8")


def write_reviewer_package() -> None:
    path = ROOT / "docs" / "grant" / "CRYSTAL_PRE_FREEZE_EVIDENCE.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('''# Crystal Pre-Freeze Evidence Package\n\nStatus: **freeze candidate; not production authorization**.\n\nThis package accompanies the Crystal pre-freeze remediation branch. The exact\nimplementation baseline SHA and CI run IDs are pinned only after the final code\ncommit has passed the supported Python 3.11/3.12 matrix. A documentation-only\nclosure commit may reference that already-tested implementation SHA.\n\n## Architecture boundary\n\n- General admitted-memory retrieval: bounded vector recall + default-deny graph recall + RRF.\n- Reader RC-9: deterministic lexical **pre-admission** candidate discovery.\n- Reader semantic/hybrid runtime: **not authorized**.\n- Retrieval rank / graph activation: navigation signals only; never truth or evidence authority.\n- Public query path: read-only and deny-dominant.\n\n## Freeze blockers remediated\n\n1. Logical-export verification uses directory identity plus deterministic entry inventory.\n2. Graph recall uses a positive edge allow-list and independent work ceilings.\n3. Grant strict grounding requires replayable evidence spans for VERIFIED facts.\n4. Grant retrieval profile requires a pinned embedder; mismatch/provider degradation is explicit.\n5. TRACE v2 calls relevance `retrieval_score` and carries bounded retrieval explanation.\n6. Evidence lineage is unknown by default; same-lineage reinforcement cannot increase support twice.\n7. Concept clustering excludes non-Validated, restricted, and store-conflicted facts.\n8. The shipping evaluation corpus is hash-frozen and gates strict provenance + lineage metrics.\n\n## Explicit non-claims\n\nCrystal does not claim that retrieval equals truth, ranking equals confidence, a graph\npath is proof, a source label is exact evidence, source count implies independent\ncorroboration, an embedding fallback preserves semantic equivalence, bounded hop\ndepth alone bounds graph work, or green CI constitutes production authorization.\n\n## Freeze exit gate\n\n- [ ] Python 3.11 full CI green on the exact implementation candidate.\n- [ ] Python 3.12 full CI green on the exact implementation candidate.\n- [ ] `scripts/eval_gate.py` green with the frozen fixture manifest.\n- [ ] No temporary pre-freeze patch/workflow files remain.\n- [ ] Final reviewer package pins the tested implementation SHA and CI/eval evidence.\n- [ ] No advanced RAG framework, semantic Reader runtime, or new authority path introduced.\n''', encoding="utf-8")


def main() -> None:
    patch_concept_gating()
    patch_eval_gate()
    write_fixture_manifest()
    write_wave4_tests()
    write_reviewer_package()


if __name__ == "__main__":
    main()
