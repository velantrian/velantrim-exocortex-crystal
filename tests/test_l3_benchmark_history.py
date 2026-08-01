"""Tests for versioned L3 benchmark history artifacts."""

import json
import runpy
import sys

import pytest

from scripts import l3_benchmark_history as history


def _size(facts=1000, **overrides):
    row = {
        "facts": facts,
        "measured_searches_total": 100,
        "query_templates": 20,
        "top_k": 10,
        "warmup_queries": 10,
        "p50_ms": 10.0,
        "p95_ms": 20.0,
        "max_ms": 30.0,
        "load_seconds": 1.5,
        "db_size_bytes": 4096,
    }
    row.update(overrides)
    return row


def _raw(*rows, backend="sqlite", embedder="hashing"):
    return {
        "benchmark": "l3_retrieval_scale",
        "commit": "abc1234",
        "backend": backend,
        "embedder": embedder,
        "python_version": "3.12.1",
        "platform": "Linux-test",
        "sizes": list(rows or (_size(),)),
    }


def _history(*rows, **kwargs):
    return history.pack_history(
        _raw(*rows, **kwargs),
        collected_at="2026-08-01T08:00:00+00:00",
        run_metadata={"run_id": 10, "repository": "owner/repo", "ref": "refs/heads/main"},
    )


def test_validate_raw_result_sorts_sizes_and_returns_fresh_copy():
    raw = _raw(_size(10000, p50_ms=50.0, p95_ms=70.0, max_ms=90.0), _size(100))
    result = history.validate_raw_result(raw)

    assert [row["facts"] for row in result["sizes"]] == [100, 10000]
    assert result is not raw
    result["sizes"][0]["p50_ms"] = 999
    assert raw["sizes"][1]["p50_ms"] == 10.0


@pytest.mark.parametrize(
    "raw,match",
    [
        ([], "mapping"),
        ({**_raw(), "benchmark": "other"}, "benchmark"),
        ({**_raw(), "commit": " "}, "commit"),
        ({**_raw(), "sizes": []}, "non-empty list"),
        ({**_raw(), "sizes": ["bad"]}, "must be a mapping"),
        ({**_raw(), "sizes": [{"facts": 1}]}, "missing fields"),
        ({**_raw(), "sizes": [_size(facts=True)]}, "facts must be an integer"),
        ({**_raw(), "sizes": [_size(facts=0)]}, "facts must be > 0"),
        ({**_raw(), "sizes": [_size(10), _size(10)]}, "duplicate fact size"),
        ({**_raw(), "sizes": [_size(top_k=-1)]}, "non-negative integer"),
        ({**_raw(), "sizes": [_size(p50_ms="slow")]}, "must be numeric"),
        ({**_raw(), "sizes": [_size(p50_ms=float("nan"))]}, "must be finite"),
        ({**_raw(), "sizes": [_size(p95_ms=float("inf"), max_ms=float("inf"))]}, "must be finite"),
        ({**_raw(), "sizes": [_size(load_seconds=-1.0)]}, "must be >= 0.0"),
        ({**_raw(), "sizes": [_size(p50_ms=21.0)]}, "not ordered"),
    ],
)
def test_validate_raw_result_rejects_malformed_payloads(raw, match):
    with pytest.raises(ValueError, match=match):
        history.validate_raw_result(raw)


def test_pack_validate_and_summarize_history():
    doc = history.pack_history(
        _raw(_size(100), _size(1000, p50_ms=15, p95_ms=25, max_ms=40)),
        collected_at=" 2026-08-01T08:00:00+00:00 ",
        run_metadata={
            "repository": "owner/repo",
            "run_id": 22,
            "runner_os": "Linux",
            "runner_arch": "X64",
            "event": "schedule",
            "ref": "",
            "sha": None,
            "ignored": "not copied",
        },
    )

    assert doc["history_schema_version"] == 1
    assert doc["collected_at"] == "2026-08-01T08:00:00+00:00"
    assert doc["run"] == {
        "repository": "owner/repo",
        "event": "schedule",
        "run_id": "22",
        "runner_os": "Linux",
        "runner_arch": "X64",
    }
    validated = history.validate_history(doc)
    assert validated == doc
    assert validated is not doc

    markdown = history.summarize_markdown(doc)
    assert "L3 retrieval benchmark history" in markdown
    assert "| 100 | 1.5 | 10.0 | 20.0 | 30.0 | 4096 |" in markdown
    assert "not a production SLO" in markdown


def test_pack_uses_current_time_and_rejects_bad_envelopes(monkeypatch):
    class FixedDateTime:
        @classmethod
        def now(cls, _tz):
            class Value:
                @staticmethod
                def isoformat():
                    return "2026-08-01T09:00:00+00:00"

            return Value()

    monkeypatch.setattr(history, "datetime", FixedDateTime)
    packed = history.pack_history(_raw(_size()))
    assert packed["collected_at"] == "2026-08-01T09:00:00+00:00"
    assert packed["run"] == {}

    with pytest.raises(ValueError, match="run_metadata"):
        history.pack_history(_raw(_size()), run_metadata=[])
    with pytest.raises(ValueError, match="history document"):
        history.validate_history([])
    with pytest.raises(ValueError, match="history_schema_version"):
        history.validate_history({**packed, "history_schema_version": 2})
    with pytest.raises(ValueError, match="run metadata"):
        history.validate_history({**packed, "run": []})
    with pytest.raises(ValueError, match="collected_at"):
        history.validate_history({**packed, "collected_at": " "})


def test_compare_histories_reports_warning_only_for_comparable_workloads():
    baseline = _history(_size(1000, p50_ms=10, p95_ms=20))
    current = _history(_size(1000, p50_ms=14, p95_ms=24))
    comparison = history.compare_histories(baseline, current, warn_ratio=1.25)

    assert comparison == {
        "informational_only": True,
        "comparable_environment": True,
        "warn_ratio": 1.25,
        "shared_sizes": [1000],
        "warning_sizes": [1000],
        "rows": [
            {
                "facts": 1000,
                "workload_match": True,
                "p50_ratio": 1.4,
                "p95_ratio": 1.2,
                "warning": True,
            }
        ],
    }
    markdown = history.comparison_markdown(comparison)
    assert "⚠️" in markdown
    assert "Informational only" in markdown

    different_workload = _history(
        _size(1000, p50_ms=20, p95_ms=40, max_ms=50, top_k=5)
    )
    mismatch = history.compare_histories(baseline, different_workload)
    assert mismatch["rows"][0]["workload_match"] is False
    assert mismatch["warning_sizes"] == []

    different_backend = history.pack_history(
        _raw(_size(1000, p50_ms=20, p95_ms=40, max_ms=50), backend="other"),
        collected_at="2026-08-01T08:00:00+00:00",
    )
    environment = history.compare_histories(baseline, different_backend)
    assert environment["comparable_environment"] is False
    assert environment["warning_sizes"] == []


def test_compare_handles_zero_baseline_no_shared_sizes_and_bad_ratio():
    zero = _history(_size(100, p50_ms=0.0, p95_ms=0.0, max_ms=0.0))
    current = _history(_size(100, p50_ms=1.0, p95_ms=2.0, max_ms=3.0))
    comparison = history.compare_histories(zero, current)
    assert comparison["rows"][0]["p50_ratio"] is None
    assert comparison["rows"][0]["p95_ratio"] is None

    no_shared = history.compare_histories(_history(_size(10)), _history(_size(20)))
    assert no_shared["rows"] == []
    assert "no shared sizes" in history.comparison_markdown(no_shared)

    with pytest.raises(ValueError, match="warn_ratio"):
        history.compare_histories(zero, current, warn_ratio=0)
    with pytest.raises(ValueError, match="finite"):
        history.compare_histories(zero, current, warn_ratio=float("inf"))


def test_pack_and_compare_cli_write_files(tmp_path, capsys):
    raw_path = tmp_path / "raw.json"
    history_path = tmp_path / "nested" / "history.json"
    summary_path = tmp_path / "summary.md"
    raw_path.write_text(json.dumps(_raw(_size(100))), encoding="utf-8")

    assert history.main(
        [
            "pack",
            "--input",
            str(raw_path),
            "--output",
            str(history_path),
            "--summary-out",
            str(summary_path),
            "--collected-at",
            "2026-08-01T08:00:00+00:00",
            "--run-id",
            "123",
            "--repository",
            "owner/repo",
        ]
    ) == 0
    assert history_path.is_file()
    assert summary_path.is_file()
    assert "L3 retrieval benchmark history" in capsys.readouterr().out

    comparison_path = tmp_path / "comparison.md"
    assert history.main(
        [
            "compare",
            "--baseline",
            str(history_path),
            "--current",
            str(history_path),
            "--output",
            str(comparison_path),
            "--warn-ratio",
            "1.5",
        ]
    ) == 0
    assert comparison_path.is_file()
    assert "L3 retrieval benchmark comparison" in capsys.readouterr().out


def test_cli_returns_two_for_io_json_and_validation_errors(tmp_path, capsys):
    missing = tmp_path / "missing.json"
    assert history.main(
        ["pack", "--input", str(missing), "--output", str(tmp_path / "out.json")]
    ) == 2
    assert "benchmark history error" in capsys.readouterr().err

    bad_json = tmp_path / "bad.json"
    bad_json.write_text("{", encoding="utf-8")
    assert history.main(
        ["pack", "--input", str(bad_json), "--output", str(tmp_path / "out.json")]
    ) == 2
    assert "benchmark history error" in capsys.readouterr().err

    invalid = tmp_path / "invalid.json"
    invalid.write_text(json.dumps({"benchmark": "wrong"}), encoding="utf-8")
    assert history.main(
        ["pack", "--input", str(invalid), "--output", str(tmp_path / "out.json")]
    ) == 2
    assert "benchmark history error" in capsys.readouterr().err


def test_script_main_guard(monkeypatch, tmp_path):
    raw_path = tmp_path / "raw.json"
    out_path = tmp_path / "history.json"
    raw_path.write_text(json.dumps(_raw(_size(100))), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "l3_benchmark_history.py",
            "pack",
            "--input",
            str(raw_path),
            "--output",
            str(out_path),
            "--collected-at",
            "2026-08-01T08:00:00+00:00",
        ],
    )
    with pytest.raises(SystemExit, match="0"):
        runpy.run_path(history.__file__, run_name="__main__")
    assert out_path.is_file()
