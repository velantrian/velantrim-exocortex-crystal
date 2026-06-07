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
    # fixture facts get an evidence span attached → full source-span coverage
    assert report["source_span_coverage"] == 1.0
    # receipts built now must replay against the unchanged canon
    assert report["receipt_replay_survival"] == 1.0
    assert 0.0 <= report["trace_completeness"] <= 1.0
    # contradiction block present and well-formed
    c = report["contradiction"]
    assert c["pairs"] == 4
    assert 0.0 <= c["precision"] <= 1.0 and 0.0 <= c["recall"] <= 1.0


# ─── WP3: source-span coverage ────────────────────────────────────────────────

def test_source_span_coverage():
    from core.ingest import ingest
    from core import evidence
    a = ingest("Mercury is the closest planet to the Sun")["fact"]["fact_id"]
    b = ingest("Venus is the second planet")["fact"]["fact_id"]
    evidence.attach_evidence(a, "astro.md")          # only a has evidence
    assert ev.source_span_coverage([a, b]) == 0.5
    assert ev.source_span_coverage([]) == 0.0


# ─── WP3: contradiction recall/precision ──────────────────────────────────────

def test_contradiction_eval_default_fixture():
    rep = ev.contradiction_eval()
    assert rep["pairs"] == 4
    # different-subject pairs must not be flagged → no false positives
    assert rep["false_positive_rate"] == 0.0 and rep["precision"] == 1.0
    # at least one true contradiction (the numeric one) must be caught
    assert rep["recall"] >= 0.5


def test_contradiction_eval_custom_pairs():
    pairs = [{"base": "The door is open", "probe": "The door is not open",
              "contradict": True}]
    rep = ev.contradiction_eval(pairs)
    assert rep["pairs"] == 1
    assert 0.0 <= rep["recall"] <= 1.0


def test_contradiction_eval_counts_fp_and_fn():
    pairs = [
        # negation IS detected, but mislabelled non-contradiction → false positive
        {"base": "The sky is blue", "probe": "The sky is not blue",
         "contradict": False},
        # weekday difference the deterministic classifier won't catch → false negative
        {"base": "The meeting is on Monday", "probe": "The meeting is on Tuesday",
         "contradict": True},
    ]
    rep = ev.contradiction_eval(pairs)
    assert rep["fp"] == 1 and rep["fn"] == 1


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
