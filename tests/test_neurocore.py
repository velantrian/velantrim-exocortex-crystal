"""Tests for the NeuroCore Phase 0 passive tracker (core/neurocore.py, RFC0068)."""
import math

import pytest

from core import neurocore


# ─── Feature flag & config ────────────────────────────────────────────────────

def test_disabled_by_default_is_a_noop():
    res = neurocore.observe(0.9, delta_norm=1.0)
    assert res == {"enabled": False, "logged": False, "reason": "disabled"}
    # Nothing was written.
    assert neurocore.log_entries() == []


def test_enabled_flag(monkeypatch):
    assert neurocore.enabled() is False
    monkeypatch.setenv("VELANTRIM_NEUROCORE", "1")
    assert neurocore.enabled() is True


def test_theta_and_alpha_defaults_and_overrides(monkeypatch):
    assert neurocore.surprise_theta() == 0.6
    assert neurocore.alpha() == 0.01
    monkeypatch.setenv("VELANTRIM_NEUROCORE_THETA", "0.8")
    monkeypatch.setenv("VELANTRIM_NEUROCORE_ALPHA", "0.05")
    assert neurocore.surprise_theta() == 0.8
    assert neurocore.alpha() == 0.05


def test_malformed_config_falls_back(monkeypatch):
    monkeypatch.setenv("VELANTRIM_NEUROCORE_THETA", "nope")
    monkeypatch.setenv("VELANTRIM_NEUROCORE_ALPHA", "nan-ish")
    assert neurocore.surprise_theta() == 0.6
    assert neurocore.alpha() == 0.01


# ─── Phase 0 observation ──────────────────────────────────────────────────────

def test_below_threshold_logs_nothing(monkeypatch):
    monkeypatch.setenv("VELANTRIM_NEUROCORE", "1")
    res = neurocore.observe(0.5, delta_norm=1.0)  # 0.5 <= θ=0.6
    assert res["logged"] is False and res["reason"] == "surprise<=theta"
    assert neurocore.log_entries() == []


def test_above_threshold_logs_delta(monkeypatch):
    monkeypatch.setenv("VELANTRIM_NEUROCORE", "1")
    res = neurocore.observe(0.9, delta_norm=2.5, domain="astronomy",
                            session_id="sess-1")
    assert res["logged"] is True
    assert res["delta_norm"] == 2.5 and res["domain"] == "astronomy"
    entries = neurocore.log_entries()
    assert len(entries) == 1
    assert entries[0]["session_id"] == "sess-1"


def test_delta_norm_computed_from_vectors(monkeypatch):
    monkeypatch.setenv("VELANTRIM_NEUROCORE", "1")
    # ‖α·(x ⊗ k)‖ = α·‖x‖·‖k‖ ; x=[3,4]→5, k=[0,1]→1, α=0.01 → 0.05
    res = neurocore.observe(0.7, x=[3.0, 4.0], k=[0.0, 1.0])
    assert math.isclose(res["delta_norm"], 0.05, rel_tol=1e-9)


def test_observe_requires_delta_or_vectors(monkeypatch):
    monkeypatch.setenv("VELANTRIM_NEUROCORE", "1")
    with pytest.raises(ValueError):
        neurocore.observe(0.9)  # no delta_norm, no x/k


# ─── Reporting ────────────────────────────────────────────────────────────────

def test_report_aggregates_by_domain(monkeypatch):
    monkeypatch.setenv("VELANTRIM_NEUROCORE", "1")
    neurocore.observe(0.9, delta_norm=1.0, domain="a")
    neurocore.observe(0.95, delta_norm=3.0, domain="a")
    neurocore.observe(0.8, delta_norm=2.0, domain="b")
    rep = neurocore.report()
    assert rep["enabled"] is True and rep["phase"] == 0
    assert rep["surprise_events"] == 3
    assert rep["max_delta_norm"] == 3.0
    assert math.isclose(rep["avg_delta_norm"], 2.0, rel_tol=1e-9)
    assert rep["by_domain"] == {"a": 2, "b": 1}


def test_report_empty_is_safe():
    rep = neurocore.report()
    assert rep["surprise_events"] == 0
    assert rep["avg_delta_norm"] == 0.0 and rep["max_delta_norm"] == 0.0
    assert rep["by_domain"] == {}


# ─── I68: NeuroCore never writes to the L3 graph ──────────────────────────────

def test_I68_neurocore_never_touches_the_graph(monkeypatch):
    """I68 (NeuroCoreIsolation): the module must not import or write to L3."""
    import ast
    monkeypatch.setenv("VELANTRIM_NEUROCORE", "1")
    src = open(neurocore.__file__, encoding="utf-8").read()
    tree = ast.parse(src)
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)
        elif isinstance(node, ast.Import):
            imported.extend(a.name for a in node.names)
    assert not any("l3_graph" in m for m in imported)  # never imports the canon
    # Observing does not create any graph node/edge.
    from core.l3_graph import get_l3_graph
    graph = get_l3_graph()
    before = len(graph.all_nodes()) if hasattr(graph, "all_nodes") else None
    neurocore.observe(0.9, delta_norm=1.0)
    if before is not None:
        assert len(graph.all_nodes()) == before


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_neurocore_report(monkeypatch, capsys):
    import json
    from core.cli import main
    monkeypatch.setenv("VELANTRIM_NEUROCORE", "1")
    neurocore.observe(0.9, delta_norm=1.0, domain="x")
    assert main(["neurocore-report"]) == 0
    rep = json.loads(capsys.readouterr().out.strip())
    assert rep["surprise_events"] == 1 and rep["by_domain"] == {"x": 1}


# ─── pipeline wiring (neurocore is actually connected) ─────────────────────────

def test_pipeline_invokes_neurocore_when_enabled(monkeypatch):
    monkeypatch.setenv("VELANTRIM_NEUROCORE", "1")
    calls = []
    real = neurocore.observe

    def spy(surprise_score, **kw):
        calls.append((surprise_score, kw))
        return real(surprise_score, **kw)

    monkeypatch.setattr(neurocore, "observe", spy)
    from core.pipeline import run
    run("water")  # demo-seed corpus has a water fact → retrieval returns results
    assert calls, "pipeline.run should call neurocore.observe when enabled"
    surprise, kw = calls[0]
    assert 0.0 <= surprise <= 1.0
    assert kw.get("domain") == "pipeline"


def test_pipeline_records_zero_hit_query_as_max_surprise(monkeypatch):
    # A query with no retrieval hits is the most surprising case (surprise=1.0)
    # and must be recorded BEFORE the zero-hit early return (cold-start telemetry).
    monkeypatch.setenv("VELANTRIM_NEUROCORE", "1")
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")  # empty corpus → guaranteed 0 hits
    calls = []
    real = neurocore.observe

    def spy(surprise_score, **kw):
        calls.append((surprise_score, kw))
        return real(surprise_score, **kw)

    monkeypatch.setattr(neurocore, "observe", spy)
    from core.pipeline import run
    res = run("anything at all")
    assert res.get("answer") is None        # blocked: nothing to ground on
    assert calls and calls[0][0] == 1.0     # but the surprise was still recorded
    assert calls[0][1].get("domain") == "pipeline"
    assert neurocore.log_entries(), "zero-hit surprise (1.0 > θ) should be logged"


def test_pipeline_skips_neurocore_when_disabled(monkeypatch):
    monkeypatch.setenv("VELANTRIM_NEUROCORE", "0")
    calls = []
    monkeypatch.setattr(neurocore, "observe", lambda *a, **k: calls.append(a))
    from core.pipeline import run
    run("water")
    assert calls == [], "neurocore.observe must not be called when disabled"
