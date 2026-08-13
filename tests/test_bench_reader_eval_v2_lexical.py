from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import sys

import pytest

import scripts.bench_reader_eval_v2_lexical as bench


ROOT = Path(__file__).resolve().parents[1]
QUERIES = ROOT / "eval/reader_retrieval_eval_v2_queries.jsonl"
CANDIDATES = ROOT / "eval/reader_retrieval_eval_v2_candidates.jsonl"
QRELS = ROOT / "eval/reader_retrieval_eval_v2_qrels.jsonl"
MANIFEST = ROOT / "eval/reader_retrieval_eval_v2_manifest.json"
CONTROL = ROOT / "eval/reader_retrieval_eval_v2_rc9_control.json"


def _dump(path: Path, rows: list[object]) -> Path:
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    return path


def _candidate(pool_id: str, proposition: str) -> dict[str, object]:
    return {
        "candidate_id": bench.opaque_candidate_id(pool_id, proposition),
        "pool_id": pool_id,
        "proposition": proposition,
    }


def _small_rows() -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    queries = [{"query_id": "q", "pool_id": "p", "primary_stratum": "s", "secondary_strata": [], "proposition": "alpha"}]
    candidates = sorted(
        [_candidate("p", "alpha"), _candidate("p", "beta"), _candidate("p", "gamma")],
        key=lambda item: item["candidate_id"],
    )
    by_prop = {item["proposition"]: item["candidate_id"] for item in candidates}
    qrels = [
        {"query_id": "q", "candidate_id": by_prop["alpha"], "judgment": "USEFUL_CANDIDATE", "review_class": "RELATED_CLAIM"},
        {"query_id": "q", "candidate_id": by_prop["beta"], "judgment": "HARD_NEGATIVE", "review_class": "SAME_TOPIC"},
        {"query_id": "q", "candidate_id": by_prop["gamma"], "judgment": "NEUTRAL_DECOY", "review_class": "NOT_APPLICABLE"},
    ]
    return queries, candidates, qrels


def _load_rows(tmp_path: Path, q, c, r):
    return bench.load_surface(
        _dump(tmp_path / "q.jsonl", q),
        _dump(tmp_path / "c.jsonl", c),
        _dump(tmp_path / "r.jsonl", r),
    )


def test_frozen_surface_and_control_are_exact():
    surface = bench.load_surface(QUERIES, CANDIDATES, QRELS)
    bench.validate_frozen_v2_contract(surface)
    result = bench.run_rc9_control(surface, k=5)
    committed = json.loads(CONTROL.read_text(encoding="utf-8"))
    assert result == committed
    assert result["method"] == bench.RETRIEVAL_METHOD
    assert result["metrics"] == {
        "all_useful_query_rate_at_k": 0.75,
        "any_useful_query_rate_at_k": 1.0,
        "hard_negative_hit_rate_at_k": 0.791667,
        "hard_negative_hits": 38,
        "hard_negative_total": 48,
        "judged_precision_over_returned": 0.355932,
        "mrr": 0.857639,
        "neutral_decoy_hits": 38,
        "precision_at_k": 0.35,
        "returned_candidates": 118,
        "useful_hits": 42,
        "useful_recall_at_k": 0.875,
        "useful_total": 48,
    }
    assert result["judgment_coverage"] == 1.0
    assert result["work_bound"]["max_record_comparisons"] == 144
    summary = bench.human_summary(result).lower()
    assert "precision@5 (fixed slots)" in summary
    assert "judged precision over returned" in summary
    assert "fully judged retrieval evidence only" in summary


def test_frozen_candidate_ids_are_label_independent_and_content_derived():
    surface = bench.load_surface(QUERIES, CANDIDATES, QRELS)
    for candidate in surface.candidates:
        assert candidate.candidate_id == bench.opaque_candidate_id(candidate.pool_id, candidate.proposition)
    assert [(item.pool_id, item.candidate_id) for item in surface.candidates] == sorted(
        (item.pool_id, item.candidate_id) for item in surface.candidates
    )
    assert not any(item.candidate_id.endswith(("-c01", "-c02", "-c03", "-c04", "-c05", "-c06")) for item in surface.candidates)


def test_jsonl_and_scalar_validation(tmp_path: Path):
    valid = tmp_path / "valid"; valid.write_text("\n{}\n", encoding="utf-8")
    assert bench._read_jsonl(valid) == ({},)
    malformed = tmp_path / "malformed"; malformed.write_text("{", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed JSON"): bench._read_jsonl(malformed)
    non_object = tmp_path / "non-object"; non_object.write_text("[]\n", encoding="utf-8")
    with pytest.raises(ValueError, match="must be an object"): bench._read_jsonl(non_object)
    empty = tmp_path / "empty"; empty.write_text("\n", encoding="utf-8")
    with pytest.raises(ValueError, match="at least one"): bench._read_jsonl(empty)
    assert bench._required_text(" x ", "f", "r") == "x"
    with pytest.raises(ValueError, match="non-empty"): bench._required_text(" ", "f", "r")
    assert bench._required_text_list([], "f", "r") == ()
    assert bench._required_text_list([" a ", "b"], "f", "r") == ("a", "b")
    with pytest.raises(ValueError, match="string list"): bench._required_text_list("no", "f", "r")
    with pytest.raises(ValueError, match="non-empty"): bench._required_text_list([""], "f", "r")
    with pytest.raises(ValueError, match="duplicates"): bench._required_text_list(["a", "a"], "f", "r")
    bench._require_fields({"a": 1}, frozenset({"a"}), "r")
    with pytest.raises(ValueError, match="missing fields"): bench._require_fields({}, frozenset({"a"}), "r")
    with pytest.raises(ValueError, match="unexpected fields"): bench._require_fields({"a": 1, "b": 2}, frozenset({"a"}), "r")


def test_load_surface_duplicate_pool_identity_and_order_validation(tmp_path: Path):
    q, c, r = _small_rows()
    q2 = [dict(q[0]), dict(q[0])]
    with pytest.raises(ValueError, match="duplicate query_id"): _load_rows(tmp_path, q2, c, r)
    q2[1]["query_id"] = "q2"
    with pytest.raises(ValueError, match="duplicate pool_id"): _load_rows(tmp_path, q2, c, r)
    c2 = [dict(c[0]), dict(c[0]), dict(c[2])]
    with pytest.raises(ValueError, match="duplicate candidate_id"): _load_rows(tmp_path, q, c2, r)
    c2 = [dict(item) for item in c]; c2[0]["pool_id"] = "unknown"
    with pytest.raises(ValueError, match="unknown pool_id"): _load_rows(tmp_path, q, c2, r)
    c2 = [dict(item) for item in c]; c2[0]["candidate_id"] = "v2-c-deadbeefdeadbeef"
    with pytest.raises(ValueError, match="content-derived"): _load_rows(tmp_path, q, c2, r)
    c2 = list(reversed([dict(item) for item in c]))
    with pytest.raises(ValueError, match="strictly sorted"): _load_rows(tmp_path, q, c2, r)


def test_load_surface_qrel_reference_and_relevance_validation(tmp_path: Path):
    q, c, r = _small_rows()
    bad = [dict(item) for item in r]; bad[0]["query_id"] = "missing"
    with pytest.raises(ValueError, match="unknown query_id"): _load_rows(tmp_path, q, c, bad)
    bad = [dict(item) for item in r]; bad[0]["candidate_id"] = "missing"
    with pytest.raises(ValueError, match="unknown candidate_id"): _load_rows(tmp_path, q, c, bad)
    q2 = [dict(q[0]), {**q[0], "query_id": "q2", "pool_id": "p2"}]
    c4 = _candidate("p2", "delta")
    c2 = sorted([dict(item) for item in c] + [c4], key=lambda item: (item["pool_id"], item["candidate_id"]))
    r2 = [dict(item) for item in r] + [{"query_id": "q2", "candidate_id": c4["candidate_id"], "judgment": "USEFUL_CANDIDATE", "review_class": "RELATED_CLAIM"}]
    r2[-1]["candidate_id"] = c[0]["candidate_id"]
    with pytest.raises(ValueError, match="outside query pool"): _load_rows(tmp_path, q2, c2, r2)


def test_load_surface_judgment_semantics_duplicates_and_coverage(tmp_path: Path):
    q, c, r = _small_rows()
    bad = [dict(item) for item in r]; bad[0]["judgment"] = "UNKNOWN"
    with pytest.raises(ValueError, match="unsupported judgment kind"): _load_rows(tmp_path, q, c, bad)
    bad = [dict(item) for item in r]; bad[0]["review_class"] = "SAME_TOPIC"
    with pytest.raises(ValueError, match="useful judgment"): _load_rows(tmp_path, q, c, bad)
    bad = [dict(item) for item in r]; bad[1]["review_class"] = "RELATED_CLAIM"
    with pytest.raises(ValueError, match="hard negative"): _load_rows(tmp_path, q, c, bad)
    bad = [dict(item) for item in r]; bad[2]["review_class"] = "SAME_TOPIC"
    with pytest.raises(ValueError, match="neutral decoy"): _load_rows(tmp_path, q, c, bad)
    bad = [dict(item) for item in r] + [dict(r[0])]
    with pytest.raises(ValueError, match="duplicate qrel"): _load_rows(tmp_path, q, c, bad)
    bad = [dict(item) for item in r[:-1]]
    with pytest.raises(ValueError, match="coverage must be complete"): _load_rows(tmp_path, q, c, bad)


def test_validate_frozen_v2_contract_failure_modes():
    surface = bench.load_surface(QUERIES, CANDIDATES, QRELS)
    with pytest.raises(ValueError, match="24 queries"): bench.validate_frozen_v2_contract(replace(surface, queries=surface.queries[:-1]))
    queries = list(surface.queries); queries[2] = replace(queries[2], primary_stratum=queries[0].primary_stratum)
    with pytest.raises(ValueError, match="12 primary strata"): bench.validate_frozen_v2_contract(replace(surface, queries=tuple(queries)))
    candidates = list(surface.candidates); candidates[0] = replace(candidates[0], pool_id=surface.queries[1].pool_id)
    with pytest.raises(ValueError, match="exactly six"): bench.validate_frozen_v2_contract(replace(surface, candidates=tuple(candidates)))
    qrels = list(surface.qrels); qrels[0] = replace(qrels[0], judgment_kind="NEUTRAL_DECOY", expected_review_class="NOT_APPLICABLE")
    with pytest.raises(ValueError, match="2 useful"): bench.validate_frozen_v2_contract(replace(surface, qrels=tuple(qrels)))


def test_run_guard_zero_match_and_fixed_slot_precision():
    with pytest.raises(ValueError, match="positive integer"): bench.run_rc9_control(bench.EvalSurface((), (), ()), k=True)
    p0, p1 = "p0", "p1"
    c01 = bench.EvalCandidate(bench.opaque_candidate_id(p0, "beta"), p0, "beta")
    c02 = bench.EvalCandidate(bench.opaque_candidate_id(p0, "theta"), p0, "theta")
    c03 = bench.EvalCandidate(bench.opaque_candidate_id(p0, "delta"), p0, "delta")
    c11 = bench.EvalCandidate(bench.opaque_candidate_id(p1, "beta"), p1, "beta")
    c12 = bench.EvalCandidate(bench.opaque_candidate_id(p1, "theta"), p1, "theta")
    c13 = bench.EvalCandidate(bench.opaque_candidate_id(p1, "gamma"), p1, "gamma")
    surface = bench.EvalSurface(
        queries=(bench.EvalQuery("q0", p0, "zero", (), "unmatched"), bench.EvalQuery("q1", p1, "neutral", (), "gamma")),
        candidates=(c01, c02, c03, c11, c12, c13),
        qrels=(
            bench.EvalJudgment("q0", c01.candidate_id, "USEFUL_CANDIDATE", "RELATED_CLAIM"), bench.EvalJudgment("q0", c02.candidate_id, "HARD_NEGATIVE", "SAME_TOPIC"), bench.EvalJudgment("q0", c03.candidate_id, "NEUTRAL_DECOY", "NOT_APPLICABLE"),
            bench.EvalJudgment("q1", c11.candidate_id, "USEFUL_CANDIDATE", "RELATED_CLAIM"), bench.EvalJudgment("q1", c12.candidate_id, "HARD_NEGATIVE", "SAME_TOPIC"), bench.EvalJudgment("q1", c13.candidate_id, "NEUTRAL_DECOY", "NOT_APPLICABLE"),
        ),
    )
    result = bench.run_rc9_control(surface, k=2)
    assert result["metrics"]["useful_hits"] == 0
    assert result["metrics"]["precision_at_k"] == 0.0
    assert result["metrics"]["judged_precision_over_returned"] == 0.0
    assert result["metrics"]["mrr"] == 0.0
    assert result["strata"]["zero"]["judged_precision_over_returned"] == 0.0
    assert result["missed_useful_candidate_ids"] == sorted([c01.candidate_id, c11.candidate_id])


def test_manifest_verification_and_composite_identity(tmp_path: Path):
    payload = bench.verify_manifest(MANIFEST, QUERIES, CANDIDATES, QRELS)
    assert payload["surface_version"] == 2
    hashes = {key: bench.sha256_file(ROOT / payload["surface_files"][key]["path"]) for key in ("queries", "candidates", "qrels")}
    assert bench.surface_identity_digest(hashes) == payload["surface_identity"]["digest"]
    not_object = tmp_path / "not-object.json"; not_object.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="manifest must be"): bench.verify_manifest(not_object, QUERIES, CANDIDATES, QRELS)
    no_files = tmp_path / "no-files.json"; no_files.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="surface_files"): bench.verify_manifest(no_files, QUERIES, CANDIDATES, QRELS)
    base = json.loads(MANIFEST.read_text(encoding="utf-8"))
    bad = json.loads(json.dumps(base)); bad["surface_files"]["queries"]["sha256"] = "0" * 64
    bad_path = tmp_path / "bad-hash.json"; bad_path.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(ValueError, match="hash mismatch for queries"): bench.verify_manifest(bad_path, QUERIES, CANDIDATES, QRELS)
    for field, value, message in (("surface_identity", None, "surface_identity"), ("algorithm", "sha512", "algorithm"), ("construction", "other", "construction"), ("digest", "0" * 64, "composite")):
        bad = json.loads(json.dumps(base))
        if field == "surface_identity": bad[field] = value
        else: bad["surface_identity"][field] = value
        path = tmp_path / f"bad-{field}.json"; path.write_text(json.dumps(bad), encoding="utf-8")
        with pytest.raises(ValueError, match=message): bench.verify_manifest(path, QUERIES, CANDIDATES, QRELS)


def test_main_human_json_and_output_modes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    args = ["bench", "--queries", str(QUERIES), "--candidates", str(CANDIDATES), "--qrels", str(QRELS), "--manifest", str(MANIFEST)]
    monkeypatch.setattr(sys, "argv", args)
    assert bench.main() == 0
    human = capsys.readouterr().out
    assert "Machine-readable JSON" in human and "Precision@5 (fixed slots)" in human
    out = tmp_path / "nested" / "control.json"
    monkeypatch.setattr(sys, "argv", args + ["--k", "5", "--json-out", str(out), "--json-only"])
    assert bench.main() == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["metrics"]["useful_hits"] == 42
    assert json.loads(out.read_text(encoding="utf-8")) == printed
