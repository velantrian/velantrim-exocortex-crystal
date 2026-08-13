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


def _small_rows() -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    queries = [{"query_id": "q", "pool_id": "p", "primary_stratum": "s", "secondary_strata": [], "proposition": "alpha"}]
    candidates = [
        {"candidate_id": "c1", "pool_id": "p", "proposition": "alpha"},
        {"candidate_id": "c2", "pool_id": "p", "proposition": "beta"},
        {"candidate_id": "c3", "pool_id": "p", "proposition": "gamma"},
    ]
    qrels = [
        {"query_id": "q", "candidate_id": "c1", "judgment": "USEFUL_CANDIDATE", "review_class": "RELATED_CLAIM"},
        {"query_id": "q", "candidate_id": "c2", "judgment": "HARD_NEGATIVE", "review_class": "SAME_TOPIC"},
        {"query_id": "q", "candidate_id": "c3", "judgment": "NEUTRAL_DECOY", "review_class": "NOT_APPLICABLE"},
    ]
    return queries, candidates, qrels


def _load_rows(tmp_path: Path, q, c, r):
    return bench.load_surface(_dump(tmp_path / "q.jsonl", q), _dump(tmp_path / "c.jsonl", c), _dump(tmp_path / "r.jsonl", r))


def test_frozen_surface_and_control_are_exact():
    surface = bench.load_surface(QUERIES, CANDIDATES, QRELS)
    bench.validate_frozen_v2_contract(surface)
    result = bench.run_rc9_control(surface, k=5)
    committed = json.loads(CONTROL.read_text(encoding="utf-8"))
    assert result == committed
    assert result["method"] == bench.RETRIEVAL_METHOD
    assert result["metrics"] == {
        "all_useful_query_rate_at_k": 0.791667,
        "any_useful_query_rate_at_k": 1.0,
        "hard_negative_hit_rate_at_k": 0.791667,
        "hard_negative_hits": 38,
        "hard_negative_total": 48,
        "judged_precision_at_k": 0.364407,
        "mrr": 0.829861,
        "neutral_decoy_hits": 37,
        "returned_candidates": 118,
        "useful_hits": 43,
        "useful_recall_at_k": 0.895833,
        "useful_total": 48,
    }
    assert result["judgment_coverage"] == 1.0
    assert result["work_bound"]["max_record_comparisons"] == 144
    assert "fully judged retrieval evidence only" in bench.human_summary(result).lower()


def test_jsonl_and_scalar_validation(tmp_path: Path):
    valid = tmp_path / "valid"
    valid.write_text("\n{}\n", encoding="utf-8")
    assert bench._read_jsonl(valid) == ({},)
    malformed = tmp_path / "malformed"
    malformed.write_text("{", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed JSON"):
        bench._read_jsonl(malformed)
    non_object = tmp_path / "non-object"
    non_object.write_text("[]\n", encoding="utf-8")
    with pytest.raises(ValueError, match="must be an object"):
        bench._read_jsonl(non_object)
    empty = tmp_path / "empty"
    empty.write_text("\n", encoding="utf-8")
    with pytest.raises(ValueError, match="at least one"):
        bench._read_jsonl(empty)
    assert bench._required_text(" x ", "f", "r") == "x"
    with pytest.raises(ValueError, match="non-empty"):
        bench._required_text(" ", "f", "r")
    assert bench._required_text_list([], "f", "r") == ()
    assert bench._required_text_list([" a ", "b"], "f", "r") == ("a", "b")
    with pytest.raises(ValueError, match="string list"):
        bench._required_text_list("no", "f", "r")
    with pytest.raises(ValueError, match="non-empty"):
        bench._required_text_list([""], "f", "r")
    with pytest.raises(ValueError, match="duplicates"):
        bench._required_text_list(["a", "a"], "f", "r")
    bench._require_fields({"a": 1}, frozenset({"a"}), "r")
    with pytest.raises(ValueError, match="missing fields"):
        bench._require_fields({}, frozenset({"a"}), "r")
    with pytest.raises(ValueError, match="unexpected fields"):
        bench._require_fields({"a": 1, "b": 2}, frozenset({"a"}), "r")


def test_load_surface_duplicate_and_pool_validation(tmp_path: Path):
    q, c, r = _small_rows()
    q2 = [dict(q[0]), dict(q[0])]
    with pytest.raises(ValueError, match="duplicate query_id"):
        _load_rows(tmp_path, q2, c, r)
    q2[1]["query_id"] = "q2"
    with pytest.raises(ValueError, match="duplicate pool_id"):
        _load_rows(tmp_path, q2, c, r)
    c2 = [dict(c[0]), dict(c[0]), dict(c[2])]
    with pytest.raises(ValueError, match="duplicate candidate_id"):
        _load_rows(tmp_path, q, c2, r)
    c2 = [dict(item) for item in c]
    c2[0]["pool_id"] = "unknown"
    with pytest.raises(ValueError, match="unknown pool_id"):
        _load_rows(tmp_path, q, c2, r)


def test_load_surface_qrel_reference_and_relevance_validation(tmp_path: Path):
    q, c, r = _small_rows()
    bad = [dict(item) for item in r]
    bad[0]["query_id"] = "missing"
    with pytest.raises(ValueError, match="unknown query_id"):
        _load_rows(tmp_path, q, c, bad)
    bad = [dict(item) for item in r]
    bad[0]["candidate_id"] = "missing"
    with pytest.raises(ValueError, match="unknown candidate_id"):
        _load_rows(tmp_path, q, c, bad)
    q2 = [dict(q[0]), {**q[0], "query_id": "q2", "pool_id": "p2"}]
    c2 = [dict(item) for item in c] + [{"candidate_id": "c4", "pool_id": "p2", "proposition": "delta"}]
    r2 = [dict(item) for item in r] + [{"query_id": "q2", "candidate_id": "c4", "judgment": "USEFUL_CANDIDATE", "review_class": "RELATED_CLAIM"}]
    r2[-1]["candidate_id"] = "c1"
    with pytest.raises(ValueError, match="outside query pool"):
        _load_rows(tmp_path, q2, c2, r2)


def test_load_surface_judgment_semantics_duplicates_and_coverage(tmp_path: Path):
    q, c, r = _small_rows()
    bad = [dict(item) for item in r]
    bad[0]["judgment"] = "UNKNOWN"
    with pytest.raises(ValueError, match="unsupported judgment kind"):
        _load_rows(tmp_path, q, c, bad)
    bad = [dict(item) for item in r]
    bad[0]["review_class"] = "SAME_TOPIC"
    with pytest.raises(ValueError, match="useful judgment"):
        _load_rows(tmp_path, q, c, bad)
    bad = [dict(item) for item in r]
    bad[1]["review_class"] = "RELATED_CLAIM"
    with pytest.raises(ValueError, match="hard negative"):
        _load_rows(tmp_path, q, c, bad)
    bad = [dict(item) for item in r]
    bad[2]["review_class"] = "SAME_TOPIC"
    with pytest.raises(ValueError, match="neutral decoy"):
        _load_rows(tmp_path, q, c, bad)
    bad = [dict(item) for item in r] + [dict(r[0])]
    with pytest.raises(ValueError, match="duplicate qrel"):
        _load_rows(tmp_path, q, c, bad)
    bad = [dict(item) for item in r[:-1]]
    with pytest.raises(ValueError, match="coverage must be complete"):
        _load_rows(tmp_path, q, c, bad)


def test_validate_frozen_v2_contract_failure_modes():
    surface = bench.load_surface(QUERIES, CANDIDATES, QRELS)
    with pytest.raises(ValueError, match="24 queries"):
        bench.validate_frozen_v2_contract(replace(surface, queries=surface.queries[:-1]))
    queries = list(surface.queries)
    queries[2] = replace(queries[2], primary_stratum=queries[0].primary_stratum)
    with pytest.raises(ValueError, match="12 primary strata"):
        bench.validate_frozen_v2_contract(replace(surface, queries=tuple(queries)))
    candidates = list(surface.candidates)
    candidates[0] = replace(candidates[0], pool_id=surface.queries[1].pool_id)
    with pytest.raises(ValueError, match="exactly six"):
        bench.validate_frozen_v2_contract(replace(surface, candidates=tuple(candidates)))
    qrels = list(surface.qrels)
    first = qrels[0]
    qrels[0] = replace(first, judgment_kind="NEUTRAL_DECOY", expected_review_class="NOT_APPLICABLE")
    with pytest.raises(ValueError, match="2 useful"):
        bench.validate_frozen_v2_contract(replace(surface, qrels=tuple(qrels)))


def test_run_guard_and_zero_match_path():
    with pytest.raises(ValueError, match="positive integer"):
        bench.run_rc9_control(bench.EvalSurface((), (), ()), k=True)
    surface = bench.EvalSurface(
        queries=(bench.EvalQuery("q0", "p0", "zero", (), "unmatched"), bench.EvalQuery("q1", "p1", "neutral", (), "gamma")),
        candidates=(bench.EvalCandidate("c01", "p0", "beta"), bench.EvalCandidate("c02", "p0", "theta"), bench.EvalCandidate("c03", "p0", "delta"), bench.EvalCandidate("c11", "p1", "beta"), bench.EvalCandidate("c12", "p1", "theta"), bench.EvalCandidate("c13", "p1", "gamma")),
        qrels=(bench.EvalJudgment("q0", "c01", "USEFUL_CANDIDATE", "RELATED_CLAIM"), bench.EvalJudgment("q0", "c02", "HARD_NEGATIVE", "SAME_TOPIC"), bench.EvalJudgment("q0", "c03", "NEUTRAL_DECOY", "NOT_APPLICABLE"), bench.EvalJudgment("q1", "c11", "USEFUL_CANDIDATE", "RELATED_CLAIM"), bench.EvalJudgment("q1", "c12", "HARD_NEGATIVE", "SAME_TOPIC"), bench.EvalJudgment("q1", "c13", "NEUTRAL_DECOY", "NOT_APPLICABLE")),
    )
    result = bench.run_rc9_control(surface, k=2)
    assert result["metrics"]["useful_hits"] == 0
    assert result["metrics"]["judged_precision_at_k"] == 0.0
    assert result["metrics"]["mrr"] == 0.0
    assert result["strata"]["zero"]["judged_precision_at_k"] == 0.0
    assert result["missed_useful_candidate_ids"] == ["c01", "c11"]


def test_manifest_verification(tmp_path: Path):
    payload = bench.verify_manifest(MANIFEST, QUERIES, CANDIDATES, QRELS)
    assert payload["surface_version"] == 2
    assert bench.sha256_file(QUERIES) == payload["surface_files"]["queries"]["sha256"]
    not_object = tmp_path / "not-object.json"
    not_object.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="manifest must be"):
        bench.verify_manifest(not_object, QUERIES, CANDIDATES, QRELS)
    no_files = tmp_path / "no-files.json"
    no_files.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="surface_files"):
        bench.verify_manifest(no_files, QUERIES, CANDIDATES, QRELS)
    bad = json.loads(MANIFEST.read_text(encoding="utf-8"))
    bad["surface_files"]["queries"]["sha256"] = "0" * 64
    bad_path = tmp_path / "bad.json"
    bad_path.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(ValueError, match="hash mismatch for queries"):
        bench.verify_manifest(bad_path, QUERIES, CANDIDATES, QRELS)


def test_main_human_json_and_output_modes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    args = ["bench", "--queries", str(QUERIES), "--candidates", str(CANDIDATES), "--qrels", str(QRELS), "--manifest", str(MANIFEST)]
    monkeypatch.setattr(sys, "argv", args)
    assert bench.main() == 0
    human = capsys.readouterr().out
    assert "Machine-readable JSON" in human and "Useful Recall@5" in human
    out = tmp_path / "nested" / "control.json"
    monkeypatch.setattr(sys, "argv", args + ["--k", "5", "--json-out", str(out), "--json-only"])
    assert bench.main() == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["metrics"]["useful_hits"] == 43
    assert json.loads(out.read_text(encoding="utf-8")) == printed
