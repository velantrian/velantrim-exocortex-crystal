"""Tests for Neurogenesis Dynamic Growth (core/neurogenesis.py, RFC0073)."""
import json
from datetime import datetime, timedelta, timezone

import pytest

from core import neurogenesis
from core.neurogenesis import REL_SEPARATED_FROM
from core.memory import store_fact, transition_esm, get_fact, update_fact
from core.l3_graph import get_l3_graph


def _born(days_ago):
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()


def _canon(fact_id, *, confidence=0.6, scale=None):
    """A Validated L3 fact (created 'now')."""
    store_fact({"fact_id": fact_id, "claim": f"claim {fact_id}", "source": "s",
                "confidence": confidence})
    transition_esm(fact_id, "Validated")
    if scale is not None:
        update_fact(fact_id, metadata={"fractal_scale": scale})
    get_l3_graph().merge_fact(get_fact(fact_id))


# ─── Plasticity & maturation (pure) ───────────────────────────────────────────

def test_plasticity_starts_high_and_matures_to_floor():
    now = datetime.now(timezone.utc)
    young = {"created_at": now.isoformat()}
    mid = {"created_at": _born(30)}
    old = {"created_at": _born(60)}
    assert neurogenesis.plasticity(young, now=now) == 2.0     # p0
    assert neurogenesis.plasticity(mid, now=now) == 1.0       # halfway
    assert neurogenesis.plasticity(old, now=now) == 0.5       # floor
    # never below the floor, even for ancient facts
    assert neurogenesis.plasticity({"created_at": _born(5000)}, now=now) == 0.5


def test_plasticity_respects_env(monkeypatch):
    monkeypatch.setenv("VELANTRIM_NEURO_PLASTICITY", "3.0")
    now = datetime.now(timezone.utc)
    assert neurogenesis.plasticity({"created_at": now.isoformat()}, now=now) == 3.0


def test_is_young_window():
    now = datetime.now(timezone.utc)
    assert neurogenesis.is_young({"created_at": _born(5)}, now=now)
    assert not neurogenesis.is_young({"created_at": _born(20)}, now=now)


def test_age_is_zero_when_timestamp_missing_or_bad():
    now = datetime.now(timezone.utc)
    assert neurogenesis.plasticity({}, now=now) == 2.0                  # treated as newborn
    assert neurogenesis.plasticity({"created_at": "not-a-date"}, now=now) == 2.0


# ─── Pattern separation ───────────────────────────────────────────────────────

def test_separate_links_related_neighbours_not_contradictions():
    _canon("prior")
    _canon("new")
    conflicts = [
        {"fact_id": "prior", "kind": "RELATED", "similarity": 0.9, "claim": "p"},
        {"fact_id": "foe", "kind": "CONTRADICTION", "similarity": 0.95, "claim": "f"},
        {"fact_id": "faint", "kind": "RELATED", "similarity": 0.60, "claim": "x"},
    ]
    out = neurogenesis.separate("new", "claim new", conflicts=conflicts)
    assert out == ["prior"]   # contradiction excluded; faint below threshold
    edges = get_l3_graph().get_edges("new")
    sep = [e for e in edges if e["rel_type"] == REL_SEPARATED_FROM]
    assert sep and sep[0]["target"] == "prior"


def test_separate_threshold_is_configurable():
    _canon("a")
    conflicts = [{"fact_id": "a", "kind": "RELATED", "similarity": 0.7, "claim": "p"}]
    assert neurogenesis.separate("a", "c", conflicts=conflicts) == []        # 0.7 < 0.85
    assert neurogenesis.separate("a", "c", conflicts=conflicts,
                                 threshold=0.5) == ["a"]


def test_separate_computes_conflicts_when_not_given(monkeypatch):
    from core import reconcile
    _canon("nbr"); _canon("src")
    monkeypatch.setattr(reconcile, "find_conflicts", lambda *a, **k: [
        {"fact_id": "nbr", "kind": "RELATED", "similarity": 0.95, "claim": "p"}])
    assert neurogenesis.separate("src", "some claim") == ["nbr"]  # conflicts=None path


def test_env_fallbacks_on_malformed_values(monkeypatch):
    monkeypatch.setenv("VELANTRIM_NEURO_PLASTICITY", "not-a-float")
    monkeypatch.setenv("VELANTRIM_NEURO_MAX_NODES", "not-an-int")
    now = datetime.now(timezone.utc)
    assert neurogenesis.plasticity({"created_at": now.isoformat()}, now=now) == 2.0
    _canon("e1")
    assert neurogenesis.growth_report()["max_nodes"] == 100000


def test_ingest_pattern_separation_opt_in(monkeypatch):
    from core import ingest as ingest_mod
    ingest_mod.ingest("The river flows north through the valley")
    prior_id = "ing:" + __import__("hashlib").md5(
        "The river flows north through the valley".encode()).hexdigest()[:12]
    # Force a RELATED neighbour so the test does not depend on embedder geometry.
    monkeypatch.setattr(ingest_mod, "find_conflicts", lambda *a, **k: [
        {"fact_id": prior_id, "kind": "RELATED", "similarity": 0.9,
         "claim": "x", "signal": None}])

    monkeypatch.delenv("VELANTRIM_NEURO_SEPARATION", raising=False)
    off = ingest_mod.ingest("The stream runs south past the hill")
    assert "separated_from" not in off                      # disabled by default

    monkeypatch.setenv("VELANTRIM_NEURO_SEPARATION", "1")
    on = ingest_mod.ingest("A creek meanders east of town")
    assert on["separated_from"] == [prior_id]


# ─── Growth report & pruning ──────────────────────────────────────────────────

def test_growth_report_counts_young_and_capacity():
    _canon("g1"); _canon("g2")
    rep = neurogenesis.growth_report()
    assert rep["total"] == 2 and rep["young"] == 2 and rep["mature"] == 0
    assert rep["avg_plasticity"] == 2.0
    assert rep["pattern_separation"] == 1.0
    assert rep["max_nodes"] == 100000 and rep["headroom"] == 99998
    assert rep["at_capacity"] is False


def test_growth_report_matures_with_time():
    _canon("m1")
    future = datetime.now(timezone.utc) + timedelta(days=40)
    rep = neurogenesis.growth_report(now=future)
    assert rep["young"] == 0 and rep["mature"] == 1
    assert rep["avg_plasticity"] < 2.0


def test_at_capacity_flag(monkeypatch):
    monkeypatch.setenv("VELANTRIM_NEURO_MAX_NODES", "1")
    _canon("c1"); _canon("c2")
    rep = neurogenesis.growth_report()
    assert rep["at_capacity"] is True and rep["headroom"] == 0


def test_prune_candidates_filters():
    _canon("weak", confidence=0.1)
    _canon("strong", confidence=0.9)
    _canon("anchored_weak", confidence=0.1, scale="CORE")
    future = datetime.now(timezone.utc) + timedelta(days=40)
    cands = neurogenesis.prune_candidates(now=future)
    ids = [c["fact_id"] for c in cands]
    assert ids == ["weak"]                       # strong (conf) & CORE (anchor) excluded


def test_prune_candidates_respects_age():
    _canon("freshly_weak", confidence=0.1)
    # default min age = maturation window (30d); nothing is old enough "now"
    assert neurogenesis.prune_candidates() == []


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_neuro_roundtrip(capsys):
    from core.cli import main
    _canon("n1", confidence=0.1)

    assert main(["neuro-report"]) == 0
    rep = json.loads(capsys.readouterr().out.strip())
    assert rep["total"] == 1

    assert main(["neuro-prune-candidates", "--max-confidence", "0.5"]) == 0
    # freshly created → too young to be a candidate yet
    assert json.loads(capsys.readouterr().out.strip()) == []
