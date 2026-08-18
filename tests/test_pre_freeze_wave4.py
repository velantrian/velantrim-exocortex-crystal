from __future__ import annotations

from core import concept, eval as core_eval
from core.l3_graph import get_l3_graph
from core.memory import get_fact, store_fact, transition_esm


def _store(fid, *, validated=True, restricted=False):
    store_fact({
        "fact_id": fid, "claim": fid, "source": "s", "confidence": 0.9,
        "source_status": "EXTERNAL", "restricted": restricted,
    })
    if validated:
        transition_esm(fid, "Validated")
    fact = get_fact(fid)
    node = dict(fact)
    node["restricted"] = restricted
    get_l3_graph().merge_fact(node)
    return fact


def test_concept_clustering_excludes_observed_and_restricted_facts():
    graph = get_l3_graph()
    _store("ok-a")
    _store("ok-b")
    _store("observed", validated=False)
    _store("restricted", restricted=True)

    for _ in range(2):
        graph.add_edge("ok-a", "CO_OCCURRED", "ok-b")
        graph.add_edge("ok-b", "CO_OCCURRED", "ok-a")
        graph.add_edge("ok-a", "CO_OCCURRED", "observed")
        graph.add_edge("observed", "CO_OCCURRED", "ok-a")
        graph.add_edge("ok-a", "CO_OCCURRED", "restricted")
        graph.add_edge("restricted", "CO_OCCURRED", "ok-a")

    weights = concept.hebbian_weights()
    assert ("ok-a", "ok-b") in weights
    assert all("observed" not in pair for pair in weights)
    assert all("restricted" not in pair for pair in weights)


def test_frozen_fixture_manifest_accepts_current_retrieval_fixture():
    corpus = core_eval.load_retrieval_corpus("en")
    assert corpus["cases"]


def test_shipping_gate_requires_strict_provenance_and_lineage():
    report = {
        "retrieval": {"hit@1": 1.0, "hit@3": 1.0, "mrr": 1.0},
        "trace_completeness": 1.0,
        "metadata_completeness": 1.0,
        "source_span_coverage": 1.0,
        "strict_source_span_coverage": 0.0,
        "receipt_replay_survival": 1.0,
        "unsupported_provenance": 0,
        "lineage": {
            "known_lineage_coverage": 0.0,
            "independence_assertion_coverage": 0.0,
            "same_lineage_duplicate_rate": 0.0,
            "unknown_lineage_rate": 1.0,
        },
        "contradiction": {"precision": 1.0, "recall": 1.0, "false_positive_rate": 0.0},
        "boundary": {"refusal_correctness": 1.0, "violations": 0},
    }
    verdict = core_eval.gate(report)
    metrics = {failure["metric"] for failure in verdict["failures"]}
    assert "strict_source_span_coverage" in metrics
    assert "lineage.known_lineage_coverage" in metrics
    assert "lineage.unknown_lineage_rate" in metrics
