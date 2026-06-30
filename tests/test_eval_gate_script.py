"""Tests for scripts/eval_gate.py — CI quality gate entry point."""
import importlib.util
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


def _load_eval_gate():
    path = _REPO / "scripts" / "eval_gate.py"
    spec = importlib.util.spec_from_file_location("eval_gate_script", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_eval_gate_script_main_passes(tmp_path, monkeypatch):
    mod = _load_eval_gate()
    monkeypatch.setattr(sys, "argv", ["eval_gate.py", "--out-dir", str(tmp_path)])
    assert mod.main() == 0
    assert (tmp_path / "metrics.jsonl").is_file()
    assert (tmp_path / "eval_report.md").is_file()


def test_eval_gate_script_main_failure_path(tmp_path, monkeypatch):
    mod = _load_eval_gate()
    monkeypatch.setattr(sys, "argv", ["eval_gate.py", "--out-dir", str(tmp_path)])
    monkeypatch.setattr(
        "core.eval.gate",
        lambda _report: {"passed": False, "failures": [
            {"metric": "hit@1", "value": 0.0, "op": ">=", "threshold": 0.5},
        ]},
    )
    assert mod.main() == 1
