"""Tests for L1.5 Velum, the synaptic pre-graph (core/velum.py, RFC0016)."""
import json

import pytest

from core import velum
from core.velum import get_velum, reset_velum, Velum


# ─── Observation & weight growth ──────────────────────────────────────────────

def test_co_occurrence_strengthens_edge():
    v = Velum()
    v.observe_episode("e1", ["a", "b"])
    assert v.get_neighbors("a", min_weight=0.0) == [("b", 0.2)]
    v.observe_episode("e2", ["a", "b"])
    assert v.get_neighbors("a", min_weight=0.0) == [("b", 0.4)]


def test_signal_emitted_once_at_threshold():
    v = Velum()
    assert v.observe_episode("e1", ["a", "b"]) == []        # weight 0.2
    assert v.observe_episode("e2", ["a", "b"]) == []        # weight 0.4
    sig = v.observe_episode("e3", ["a", "b"])               # weight 0.6 → promote
    assert len(sig) == 1
    assert sig[0]["kind"] == "THRESHOLD" and sig[0]["pair"] == ("a", "b")
    assert v.observe_episode("e4", ["a", "b"]) == []        # already signalled


def test_multi_entity_episode_links_all_pairs():
    v = Velum()
    v.observe_episode("e1", ["x", "y", "z"])
    assert v.degree("x") == 2 and v.degree("y") == 2 and v.degree("z") == 2
    assert v.report()["edges"] == 3


# ─── Neighbours & degree cache ────────────────────────────────────────────────

def test_get_neighbors_filters_and_sorts():
    v = Velum()
    for _ in range(3):
        v.observe_episode("s", ["a", "b"])     # weight 0.6
    v.observe_episode("s2", ["a", "c"])        # weight 0.2
    assert v.get_neighbors("a", min_weight=0.3) == [("b", 0.6)]   # c filtered out
    assert v.get_neighbors("a", min_weight=0.0) == [("b", 0.6), ("c", 0.2)]


def test_degree_cache_tracks_connections():
    v = Velum()
    v.observe_episode("e1", ["a", "b"])
    v.observe_episode("e2", ["a", "c"])
    assert v.degree("a") == 2
    assert v.degree("b") == 1
    assert v.degree("absent") == 0


# ─── Session boundary ─────────────────────────────────────────────────────────

def test_session_end_signals_strong_and_decays_weak():
    v = Velum()
    for _ in range(3):
        v.observe_episode("s", ["a", "b"])     # strong: weight 0.6
    v.observe_episode("s", ["c", "d"])         # weak: weight 0.2
    signals = v.on_session_end()
    kinds = {s["pair"]: s["kind"] for s in signals}
    assert kinds == {("a", "b"): "SESSION_END"}           # only strong edge signals
    assert v.get_neighbors("c", min_weight=0.0) == [("d", 0.14)]  # 0.2 × (1−0.3)


def test_session_end_prunes_faded_edges(monkeypatch):
    monkeypatch.setenv("VELANTRIM_VELUM_DECAY", "1.0")     # weak edge → 0 → pruned
    v = Velum()
    v.observe_episode("s", ["c", "d"])         # weight 0.2, weak
    v.on_session_end()
    assert v.report()["edges"] == 0
    assert v.degree("c") == 0


# ─── Garbage collection ───────────────────────────────────────────────────────

def test_gc_drops_weakest_when_over_capacity(monkeypatch):
    monkeypatch.setenv("VELANTRIM_VELUM_MAX_EDGES", "3")
    v = Velum()
    for pair in (["a", "b"], ["c", "d"], ["e", "f"], ["g", "h"]):
        v.observe_episode("s", pair)           # 4 distinct edges > cap 3
    assert v.report()["edges"] == 3            # weakest 25% (1 edge) dropped


def test_gc_decrements_shared_degree_and_neighbors_second_position(monkeypatch):
    monkeypatch.setenv("VELANTRIM_VELUM_MAX_EDGES", "2")
    v = Velum()
    # A hub "h" sits in the second slot of every key (a<b<c<h):
    v.observe_episode("s1", ["a", "h"])
    v.observe_episode("s2", ["b", "h"])
    v.observe_episode("s3", ["c", "h"])        # 3 > cap → GC removes ("a","h")
    assert v.report()["edges"] == 2
    assert v.degree("h") == 2                   # decremented from 3 but still > 0
    assert sorted(n for n, _ in v.get_neighbors("h", min_weight=0.0)) == ["b", "c"]


# ─── Config overrides ─────────────────────────────────────────────────────────

def test_threshold_is_configurable(monkeypatch):
    monkeypatch.setenv("VELANTRIM_VELUM_COOCCUR", "2")
    monkeypatch.setenv("VELANTRIM_VELUM_PROMOTE_WEIGHT", "0.5")
    v = Velum()
    v.observe_episode("e1", ["a", "b"])        # weight 0.25
    sig = v.observe_episode("e2", ["a", "b"])  # weight 0.5 → promote at count 2
    assert len(sig) == 1


def test_env_fallback_on_garbage(monkeypatch):
    monkeypatch.setenv("VELANTRIM_VELUM_COOCCUR", "not-an-int")
    monkeypatch.setenv("VELANTRIM_VELUM_PROMOTE_WEIGHT", "not-a-float")
    v = Velum()
    for _ in range(3):
        v.observe_episode("s", ["a", "b"])     # defaults: cooccur 3, promote 0.6
    assert v.get_neighbors("a", min_weight=0.0) == [("b", 0.6)]


def test_report_shape():
    v = Velum()
    for _ in range(3):
        v.observe_episode("s", ["a", "b"])
    rep = v.report()
    assert rep["edges"] == 1 and rep["strong_edges"] == 1
    assert rep["signals_emitted"] == 1 and rep["entities"] == 2
    assert rep["top_edges"][0]["pair"] == ["a", "b"]


# ─── Singleton ────────────────────────────────────────────────────────────────

def test_singleton_get_and_reset():
    a = get_velum()
    a.observe_episode("s", ["a", "b"])
    assert get_velum() is a
    reset_velum()
    assert get_velum() is not a
    assert get_velum().report()["edges"] == 0


# ─── Pipeline integration (fire-and-forget hint) ──────────────────────────────

def test_link_episode_feeds_velum():
    from core import pipeline
    from core.l3_graph import get_l3_graph
    facts = [{"fact_id": "f1"}, {"fact_id": "f2"}]
    pipeline._link_episode(get_l3_graph(), facts, "why", None)
    # one co-recall → a 0.2 synaptic edge between the two facts
    assert get_velum().get_neighbors("f1", min_weight=0.1) == [("f2", 0.2)]


def test_link_episode_single_fact_is_noop():
    from core import pipeline
    from core.l3_graph import get_l3_graph
    pipeline._link_episode(get_l3_graph(), [{"fact_id": "solo"}], "q", None)
    assert get_velum().report()["edges"] == 0


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_velum_roundtrip(capsys):
    from core.cli import main
    for _ in range(3):
        get_velum().observe_episode("s", ["alpha", "beta"])

    assert main(["velum-report"]) == 0
    assert json.loads(capsys.readouterr().out.strip())["edges"] == 1

    assert main(["velum-neighbors", "alpha", "--min-weight", "0.3"]) == 0
    out = json.loads(capsys.readouterr().out.strip())
    assert out == [["beta", 0.6]]
