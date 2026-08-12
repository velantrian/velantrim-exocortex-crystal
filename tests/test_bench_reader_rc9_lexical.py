from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

import scripts.bench_reader_rc9_lexical as bench


def write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def case(case_id="x", review="RELATED_CLAIM"):
    return {
        "case_id": case_id,
        "stratum": "s",
        "left": "alpha beta",
        "right": "alpha beta",
        "expected_review_class": review,
        "note": "n",
    }


def test_load_cases_validation(tmp_path: Path):
    valid = write(tmp_path / "valid.jsonl", "\n" + json.dumps(case()) + "\n")
    loaded = bench.load_cases(valid)
    assert loaded[0].case_id == "x"

    bad_json = write(tmp_path / "bad-json", "{")
    with pytest.raises(ValueError, match="malformed JSON"):
        bench.load_cases(bad_json)
    not_obj = write(tmp_path / "not-obj", "[]\n")
    with pytest.raises(ValueError, match="JSON object"):
        bench.load_cases(not_obj)
    missing = dict(case()); missing.pop("note")
    with pytest.raises(ValueError, match="missing fields"):
        bench.load_cases(write(tmp_path / "missing", json.dumps(missing)))
    blank = dict(case()); blank["left"] = " "
    with pytest.raises(ValueError, match="left"):
        bench.load_cases(write(tmp_path / "blank", json.dumps(blank)))
    duplicate = json.dumps(case()) + "\n" + json.dumps(case())
    with pytest.raises(ValueError, match="duplicate case_id"):
        bench.load_cases(write(tmp_path / "duplicate", duplicate))
    unsupported = dict(case()); unsupported["expected_review_class"] = "UNKNOWN"
    with pytest.raises(ValueError, match="unsupported"):
        bench.load_cases(write(tmp_path / "unsupported", json.dumps(unsupported)))
    with pytest.raises(ValueError, match="at least one"):
        bench.load_cases(write(tmp_path / "empty", "\n"))


def test_run_metrics_human_summary_and_empty_guard():
    cases = (
        bench.BenchmarkCase("p", "positive", "alpha beta", "alpha beta", "RELATED_CLAIM", "n"),
        bench.BenchmarkCase("miss", "miss", "unique-left", "different-right", "PARAPHRASE_CANDIDATE", "n"),
        bench.BenchmarkCase("n", "negative", "boiler common", "boiler common", "MERELY_SIMILAR", "n"),
    )
    result = bench.run_benchmark(cases, k=2)
    metrics = result["metrics"]
    assert metrics["recall_at_k"] == 0.5
    assert metrics["precision_at_k"] == 0.25
    assert metrics["mrr"] > 0
    assert metrics["paired_hard_negative_rate_at_k"] == 1.0
    assert result["cases"][0]["relevance_intent"] == "USEFUL_CANDIDATE"
    assert result["cases"][1]["paired_candidate_rank"] is None
    assert result["cases"][2]["relevance_intent"] == "HARD_NEGATIVE"
    assert "fixed K denominator" in result["metric_scope"]
    summary = bench.human_summary(result)
    assert "Recall@2" in summary and "ranking is candidate discovery only" in summary
    with pytest.raises(ValueError, match="must not be empty"):
        bench.run_benchmark(())


def test_main_human_and_json_modes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    corpus = write(tmp_path / "corpus.jsonl", json.dumps(case()))
    out = tmp_path / "nested" / "result.json"
    monkeypatch.setattr(sys, "argv", ["bench", "--corpus", str(corpus), "--k", "1", "--json-out", str(out)])
    assert bench.main() == 0
    assert out.exists()
    assert "Machine-readable JSON" in capsys.readouterr().out

    monkeypatch.setattr(sys, "argv", ["bench", "--corpus", str(corpus), "--json-only"])
    assert bench.main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["method"] == bench.RETRIEVAL_METHOD


def test_frozen_rc8_corpus_reproduces_committed_baseline_snapshot():
    cases = bench.load_cases(Path("eval/reader_rc8_retrieval_adversarial.jsonl"))
    result = bench.run_benchmark(cases, k=5)
    metrics = result["metrics"]
    assert result["case_count"] == 20
    assert metrics["recall_at_k"] == 0.9375
    assert metrics["precision_at_k"] == 0.1875
    assert metrics["mrr"] == 0.895833
    assert metrics["paired_hard_negative_rate_at_k"] == 1.0
    by_id = {item["case_id"]: item for item in result["cases"]}
    assert by_id["rc8-004"]["paired_candidate_rank"] is None
    assert by_id["rc8-015"]["paired_candidate_rank"] == 1
    committed = json.loads(Path("eval/reader_rc9_lexical_baseline.json").read_text(encoding="utf-8"))
    assert committed == json.loads(json.dumps(result, ensure_ascii=False, sort_keys=True))
