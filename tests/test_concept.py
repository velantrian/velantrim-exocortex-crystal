"""Tests for Concept Emergence (core/concept.py, RFC0066)."""
import json

import pytest

from core import concept
from core.memory import store_fact, transition_esm, get_fact
from core.l3_graph import get_l3_graph


def _canon(fact_id, claim="c"):
    store_fact({"fact_id": fact_id, "claim": claim, "source": "s", "confidence": 0.6})
    transition_esm(fact_id, "Validated")
    get_l3_graph().merge_fact(get_fact(fact_id))


def _corecall(ids, times=1):
    """Mirror pipeline._link_episode: co-recall a chain of facts `times` over,
    writing CO_OCCURRED edges both directions for each adjacent pair. Each recall
    carries a distinct `when` (as the real pipeline does), so edges accumulate
    instead of de-duplicating."""
    g = get_l3_graph()
    for i in range(times):
        for a, b in zip(ids, ids[1:]):
            props = {"query": "q", "when": f"t{i}"}
            g.add_edge(a, "CO_OCCURRED", b, props)
            g.add_edge(b, "CO_OCCURRED", a, props)


# ─── Hebbian weights ──────────────────────────────────────────────────────────

def test_hebbian_weight_counts_co_recalls():
    _canon("fa"); _canon("fb")
    _corecall(["fa", "fb"], times=3)
    w = concept.hebbian_weights()
    assert w[("fa", "fb")] == 3


def test_no_weights_without_co_activation():
    _canon("solo")
    assert concept.hebbian_weights() == {}


def test_self_loop_edges_are_ignored():
    _canon("fa")
    get_l3_graph().add_edge("fa", "CO_OCCURRED", "fa", {"when": "t0"})
    assert concept.hebbian_weights() == {}


def test_min_weight_env_falls_back_on_garbage(monkeypatch):
    monkeypatch.setenv("VELANTRIM_CONCEPT_MIN_WEIGHT", "not-an-int")
    _canon("fa"); _canon("fb")
    _corecall(["fa", "fb"], times=2)
    assert concept.detect_concepts()          # default min_weight (2) still applies


def test_union_find_path_compression():
    uf = concept._UnionFind()
    uf.union("c", "b")    # parent[c] = b
    uf.union("b", "a")    # parent[b] = a  → c is now two levels deep
    assert uf.find("c") == "a"   # exercises path compression


# ─── Concept detection ────────────────────────────────────────────────────────

def test_detect_forms_concept_from_repeated_co_activation():
    _canon("fa"); _canon("fb"); _canon("fc")
    _corecall(["fa", "fb", "fc"], times=2)        # chain, weight 2 each ≥ min_weight
    concepts = concept.detect_concepts()
    assert len(concepts) == 1
    c = concepts[0]
    assert c["members"] == ["fa", "fb", "fc"]
    assert c["size"] == 3
    assert c["anchor"] == "fb"                    # central node, highest degree
    assert c["concept_id"] == "concept:fb"
    assert c["coactivations"] == 4                # w(fa,fb)+w(fb,fc) = 2+2


def test_weak_co_activation_does_not_wire():
    _canon("fa"); _canon("fb")
    _corecall(["fa", "fb"], times=1)              # weight 1 < default min_weight 2
    assert concept.detect_concepts() == []


def test_min_size_filters_small_clusters():
    _canon("fa"); _canon("fb")
    _corecall(["fa", "fb"], times=2)
    assert concept.detect_concepts(min_size=2)    # pair qualifies
    assert concept.detect_concepts(min_size=3) == []


def test_min_weight_override(monkeypatch):
    _canon("fa"); _canon("fb")
    _corecall(["fa", "fb"], times=1)
    assert concept.detect_concepts(min_weight=1)  # now a single co-recall wires
    monkeypatch.setenv("VELANTRIM_CONCEPT_MIN_WEIGHT", "1")
    assert concept.detect_concepts()              # env honoured


def test_two_separate_concepts():
    for fid in ("a1", "a2", "b1", "b2"):
        _canon(fid)
    _corecall(["a1", "a2"], times=2)
    _corecall(["b1", "b2"], times=2)
    concepts = concept.detect_concepts()
    assert len(concepts) == 2
    member_sets = sorted(tuple(c["members"]) for c in concepts)
    assert member_sets == [("a1", "a2"), ("b1", "b2")]


# ─── Materialisation ──────────────────────────────────────────────────────────

def test_emerge_materialises_concept_nodes_and_links():
    _canon("fa"); _canon("fb"); _canon("fc")
    _corecall(["fa", "fb", "fc"], times=2)
    res = concept.emerge_concepts()
    assert res["emerged"] == 1
    # The concept is materialised as an entity node with its members linked
    # (MEMBER_OF), queryable via facts_for_entity.
    g = get_l3_graph()
    members = {f["fact_id"] for f in g.facts_for_entity("concept:fb")}
    assert members == {"fa", "fb", "fc"}


def test_emerge_is_idempotent():
    _canon("fa"); _canon("fb")
    _corecall(["fa", "fb"], times=2)
    first = concept.emerge_concepts()
    second = concept.emerge_concepts()
    assert first["emerged"] == second["emerged"] == 1
    members = {f["fact_id"] for f in get_l3_graph().facts_for_entity("concept:fa")}
    assert members == {"fa", "fb"}                # no phantom duplicates


# ─── Lookup & report ──────────────────────────────────────────────────────────

def test_concepts_for_fact():
    _canon("fa"); _canon("fb"); _canon("loner")
    _corecall(["fa", "fb"], times=2)
    assert concept.concepts_for_fact("fa")[0]["concept_id"] == "concept:fa"
    assert concept.concepts_for_fact("loner") == []


def test_concept_report():
    _canon("fa"); _canon("fb"); _canon("fc")
    _corecall(["fa", "fb", "fc"], times=2)
    rep = concept.concept_report()
    assert rep["total_concepts"] == 1
    assert rep["clustered_facts"] == 3
    assert rep["min_weight"] == 2 and rep["min_size"] == 2


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_concepts_roundtrip(capsys):
    from core.cli import main
    _canon("fa"); _canon("fb")
    _corecall(["fa", "fb"], times=2)

    assert main(["concepts"]) == 0
    assert json.loads(capsys.readouterr().out.strip())["total_concepts"] == 1

    assert main(["concepts-emerge"]) == 0
    assert json.loads(capsys.readouterr().out.strip())["emerged"] == 1

    assert main(["concepts-for", "fa"]) == 0
    out = json.loads(capsys.readouterr().out.strip())
    assert out and out[0]["concept_id"] == "concept:fa"
