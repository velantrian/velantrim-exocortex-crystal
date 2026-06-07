"""Tests for the Analogy Graph / Semantic Bridge Engine / CREATIVE mode (RFC0067)."""
import json

import pytest

from core import analogy
from core.analogy import REL_ANALOGOUS_TO, REL_METAPHOR_OF
from core.memory import store_fact, transition_esm, get_fact
from core.l3_graph import get_l3_graph


def _fact(fid):
    store_fact({"fact_id": fid, "claim": f"claim {fid}", "source": "s", "confidence": 0.6})
    transition_esm(fid, "Validated")
    get_l3_graph().merge_fact(get_fact(fid))


def _edge(s, r, d):
    get_l3_graph().add_edge(s, r, d, {})


def _corecall(ids, times=1):
    g = get_l3_graph()
    for i in range(times):
        for a, b in zip(ids, ids[1:]):
            p = {"when": f"t{i}"}
            g.add_edge(a, "CO_OCCURRED", b, p)
            g.add_edge(b, "CO_OCCURRED", a, p)


# ─── Analogy edges ────────────────────────────────────────────────────────────

def test_analogous_to_is_symmetric():
    analogy.link_analogy("heart", "pump", kind=REL_ANALOGOUS_TO, weight=0.9)
    assert analogy.analogies_for("heart")[0]["target"] == "pump"
    assert analogy.analogies_for("pump")[0]["target"] == "heart"   # symmetric
    assert analogy.analogies_for("heart")[0]["weight"] == 0.9


def test_metaphor_of_is_directional():
    analogy.link_analogy("time", "river", kind=REL_METAPHOR_OF)
    assert analogy.analogies_for("time")[0] == {
        "target": "river", "kind": REL_METAPHOR_OF, "weight": 1.0, "source": "manual"}
    assert analogy.analogies_for("river") == []                    # not symmetric


def test_link_validates_input():
    with pytest.raises(ValueError):
        analogy.link_analogy("a", "b", kind="BOGUS")
    with pytest.raises(ValueError):
        analogy.link_analogy("a", "a")
    assert analogy.link_analogy("a", "b", weight=5.0)["weight"] == 1.0   # clamped


def test_analogies_for_filters_by_kind_and_weight():
    analogy.link_analogy("x", "y", kind=REL_ANALOGOUS_TO, weight=0.8)
    analogy.link_analogy("x", "z", kind=REL_METAPHOR_OF, weight=0.2)
    assert [a["target"] for a in analogy.analogies_for("x", kind=REL_METAPHOR_OF)] == ["z"]
    assert [a["target"] for a in analogy.analogies_for("x", min_weight=0.5)] == ["y"]


# ─── Structural similarity & suggestions ──────────────────────────────────────

def test_structural_similarity_is_jaccard_of_neighbourhoods():
    _edge("a", "R", "x"); _edge("a", "R", "y")
    _edge("b", "R", "x"); _edge("b", "R", "z")
    assert analogy.structural_similarity("a", "b") == round(1 / 3, 4)
    assert analogy.structural_similarity("a", "lonely") == 0.0


def test_suggest_analogies_ranks_candidates():
    for f in ("a", "b", "c"):
        _fact(f)
    _edge("a", "R", "x"); _edge("a", "R", "y")
    _edge("b", "R", "x"); _edge("b", "R", "y")    # identical structure → sim 1.0
    _edge("c", "R", "z")                          # disjoint → sim 0
    sug = analogy.suggest_analogies("a")
    assert sug[0]["node"] == "b" and sug[0]["similarity"] == 1.0
    assert sug[0]["shared"] == ["x", "y"]
    assert all(s["node"] != "c" for s in sug)     # below min_similarity


# ─── Semantic bridges ─────────────────────────────────────────────────────────

def test_find_bridges_combines_signals():
    _fact("a"); _fact("b")
    analogy.link_analogy("a", "b", kind=REL_METAPHOR_OF)   # explicit
    _edge("a", "R", "m"); _edge("b", "R", "m")             # shared neighbour
    _corecall(["a", "b"], times=2)                         # shared emergent concept
    bridges = analogy.find_bridges("a", "b")
    types = {br["type"] for br in bridges}
    assert types == {"explicit", "shared_neighbour", "shared_concept"}
    sn = [br for br in bridges if br["type"] == "shared_neighbour"]
    assert sn[0]["via"] == "m"


def test_find_bridges_empty_when_unrelated():
    _fact("a"); _fact("b")
    assert analogy.find_bridges("a", "b") == []


# ─── CREATIVE mode ────────────────────────────────────────────────────────────

def test_creative_temperature_band():
    assert analogy.creative_temperature(0.0) == 0.6
    assert analogy.creative_temperature(1.0) == 0.85
    assert analogy.creative_temperature(0.5) == 0.725
    assert analogy.creative_temperature(5.0) == 0.85          # clamped


def test_creative_temperature_env(monkeypatch):
    monkeypatch.setenv("VELANTRIM_CREATIVE_TEMP_MIN", "0.4")
    monkeypatch.setenv("VELANTRIM_CREATIVE_TEMP_MAX", "0.9")
    assert analogy.creative_temperature(0.0) == 0.4
    monkeypatch.setenv("VELANTRIM_CREATIVE_TEMP_MIN", "garbage")
    assert analogy.creative_temperature(0.0) == 0.6          # fallback default


def test_creative_associations_shape():
    _fact("a"); _fact("b")
    _edge("a", "R", "x"); _edge("b", "R", "x")
    analogy.link_analogy("a", "concept-of-flow", kind=REL_METAPHOR_OF)
    out = analogy.creative_associations("a")
    assert 0.6 <= out["temperature"] <= 0.85
    assert out["analogies"][0]["target"] == "concept-of-flow"
    assert any(s["node"] == "b" for s in out["suggested"])


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_analogy_roundtrip(capsys):
    from core.cli import main
    _fact("a"); _fact("b")
    _edge("a", "R", "m"); _edge("b", "R", "m")

    assert main(["analogy-link", "a", "b", "--kind", "METAPHOR_OF"]) == 0
    assert json.loads(capsys.readouterr().out.strip())["kind"] == "METAPHOR_OF"

    assert main(["analogy-of", "a"]) == 0
    assert json.loads(capsys.readouterr().out.strip())[0]["target"] == "b"

    assert main(["analogy-bridges", "a", "b"]) == 0
    types = {br["type"] for br in json.loads(capsys.readouterr().out.strip())}
    assert "shared_neighbour" in types and "explicit" in types

    assert main(["analogy-suggest", "a"]) == 0
    assert isinstance(json.loads(capsys.readouterr().out.strip()), list)
