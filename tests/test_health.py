"""Tests for core/health.py — the diagnostic memory-health score."""
import core.health as health_mod
from core.health import health_score


def _report(**kw):
    base = {
        "total_facts": 0,
        "avg_confidence": 0.0,
        "contradicted": [],
        "deprecated": [],
        "weak_confidence": [],
    }
    base.update(kw)
    return base


def test_health_empty_store(monkeypatch):
    monkeypatch.setattr(health_mod, "memory_report", lambda: _report())
    out = health_score()
    assert out["health_score"] == 0.0
    assert out["meaning"] == "diagnostic memory-health score, not a truth guarantee"
    comp = out["components"]
    assert comp["total_facts"] == 0
    assert comp["contradicted_ratio"] == 0.0
    assert comp["deprecated_ratio"] == 0.0
    assert comp["weak_confidence_ratio"] == 0.0


def test_health_clean_store(monkeypatch):
    monkeypatch.setattr(
        health_mod, "memory_report",
        lambda: _report(total_facts=100, avg_confidence=0.91))
    out = health_score()
    assert out["health_score"] == 0.91
    assert out["components"]["avg_confidence"] == 0.91


def test_health_applies_penalties(monkeypatch):
    monkeypatch.setattr(health_mod, "memory_report", lambda: _report(
        total_facts=100,
        avg_confidence=0.91,
        contradicted=["a", "b"],                  # ratio 0.02
        deprecated=["c"],                          # ratio 0.01
        weak_confidence=["d", "e", "f", "g"],      # ratio 0.04
    ))
    out = health_score()
    # 0.91 - 0.02*0.30 - 0.01*0.20 - 0.04*0.20 = 0.894
    assert out["health_score"] == 0.894
    comp = out["components"]
    assert comp["contradicted_ratio"] == 0.02
    assert comp["deprecated_ratio"] == 0.01
    assert comp["weak_confidence_ratio"] == 0.04


def test_health_score_clamped_to_zero(monkeypatch):
    monkeypatch.setattr(health_mod, "memory_report", lambda: _report(
        total_facts=10,
        avg_confidence=0.1,
        contradicted=["x"] * 10,                   # ratio 1.0 → penalty 0.30
    ))
    out = health_score()
    # 0.1 - 1.0*0.30 = -0.2 → clamped to 0.0
    assert out["health_score"] == 0.0
