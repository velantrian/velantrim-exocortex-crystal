"""Tests for the baseline evaluation harness (core/eval.py)."""
import json

from core import eval as ev


# ─── Pure metric functions (exact) ────────────────────────────────────────────

def test_hit_at_k():
    assert ev.hit_at_k(["a", "b", "c"], ["c"], 3) == 1.0
    assert ev.hit_at_k(["a", "b", "c"], ["c"], 2) == 0.0     # c is rank 3
    assert ev.hit_at_k(["a", "b"], ["z"], 5) == 0.0          # not present
    assert ev.hit_at_k(["a"], ["a"], 1) == 1.0


def test_reciprocal_rank():
    assert ev.reciprocal_rank(["a", "b", "c"], ["a"]) == 1.0
    assert ev.reciprocal_rank(["a", "b", "c"], ["b"]) == 0.5
    assert ev.reciprocal_rank(["a", "b", "c"], ["c"]) == 1 / 3
    assert ev.reciprocal_rank(["a", "b"], ["z"]) == 0.0


def test_aggregate():
    cases = [
        {"ranked": ["x", "a"], "relevant": ["a"]},   # hit@1 miss, hit@3 hit, rr=0.5
        {"ranked": ["b", "y"], "relevant": ["b"]},   # hit@1 hit, rr=1.0
    ]
    agg = ev.aggregate(cases, ks=(1, 3))
    assert agg["hit@1"] == 0.5
    assert agg["hit@3"] == 1.0
    assert agg["mrr"] == 0.75


def test_aggregate_empty_is_safe():
    agg = ev.aggregate([], ks=(1,))
    assert agg["hit@1"] == 0.0 and agg["mrr"] == 0.0


def test_metadata_completeness_empty():
    assert ev.metadata_completeness([]) == 0.0


def test_metadata_completeness_after_ingest():
    from core.ingest import ingest
    fid = ingest("Helium is a chemical element")["fact"]["fact_id"]
    assert ev.metadata_completeness([fid]) == 1.0
    assert ev.metadata_completeness(["does-not-exist"]) == 0.0


# ─── Baseline run over the real pipeline ──────────────────────────────────────

def test_run_baseline_structure_and_ranges():
    report = ev.run_baseline()
    assert report["cases"] == 4
    # well-formed retrieval block
    for key in ("hit@1", "hit@3", "hit@5", "mrr"):
        assert 0.0 <= report["retrieval"][key] <= 1.0
    # every ingested fact is fully typed
    assert report["metadata_completeness"] == 1.0
    # receipts built now must replay against the unchanged canon
    assert report["receipt_replay_survival"] == 1.0
    assert 0.0 <= report["trace_completeness"] <= 1.0


def test_run_baseline_custom_fixture():
    fixture = [{"query": "what is the capital of France",
                "claim": "Paris is the capital of France"}]
    report = ev.run_baseline(fixture)
    assert report["cases"] == 1
    # the expected fact should be retrievable for its own query
    assert report["retrieval"]["hit@5"] == 1.0


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_eval(capsys):
    from core.cli import main
    assert main(["eval"]) == 0
    report = json.loads(capsys.readouterr().out.strip())
    assert "retrieval" in report and report["cases"] == 4
