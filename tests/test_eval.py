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
    assert report["cases"] == 16          # curated bundled corpus
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
    assert c["pairs"] == 12
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
    assert rep["pairs"] == 12                      # curated bundled corpus
    # in isolation the hard negatives must not be flagged → no false positives
    assert rep["false_positive_rate"] == 0.0 and rep["precision"] == 1.0
    # the negation/numeric true contradictions must be caught
    assert rep["recall"] >= 0.8


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


# ─── WP3: curated corpus, quality gate, reporting ─────────────────────────────

def test_load_retrieval_corpus_is_curated():
    corpus = ev.load_retrieval_corpus()
    assert len(corpus["cases"]) == 16
    assert len(corpus["distractors"]) >= 4
    # every case is a well-formed (query, claim) pair across multiple domains
    assert all(c.get("query") and c.get("claim") for c in corpus["cases"])
    assert len({c.get("domain") for c in corpus["cases"]}) >= 4


def test_load_contradiction_pairs_is_curated():
    pairs = ev.load_contradiction_pairs()
    assert len(pairs) == 12
    assert any(p["contradict"] for p in pairs) and any(not p["contradict"] for p in pairs)


def test_baseline_passes_the_quality_gate():
    report = ev.run_baseline()
    verdict = ev.gate(report)
    assert verdict["passed"], verdict["failures"]


def test_gate_flags_a_regression():
    report = ev.run_baseline()
    report["retrieval"]["hit@1"] = 0.1          # simulate a retrieval regression
    report["contradiction"]["recall"] = 0.0     # and a classifier regression
    verdict = ev.gate(report)
    assert not verdict["passed"]
    metrics = {f["metric"] for f in verdict["failures"]}
    assert "retrieval.hit@1" in metrics and "contradiction.recall" in metrics


def test_gate_ceiling_metric():
    report = ev.run_baseline()
    report["unsupported_provenance"] = 3        # ceiling metric: lower is better
    verdict = ev.gate(report)
    assert not verdict["passed"]
    assert any(f["metric"] == "unsupported_provenance" and f["op"] == "<="
               for f in verdict["failures"])


def test_run_baseline_detail_breakdown():
    report = ev.run_baseline(detail=True)
    detail = report["cases_detail"]
    assert len(detail) == report["cases"]
    row = detail[0]
    assert {"domain", "query", "expected", "hit@1", "hit@3", "rr"} <= set(row)


def test_format_report_md():
    md = ev.format_report_md(ev.run_baseline())
    assert "# Velantrim Crystal — Evaluation Report" in md
    assert "## Retrieval" in md and "## Contradiction classifier" in md


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_eval(capsys):
    from core.cli import main
    assert main(["eval"]) == 0
    report = json.loads(capsys.readouterr().out.strip())
    assert "retrieval" in report and report["cases"] == 16


def test_cli_eval_gate_passes(capsys):
    from core.cli import main
    assert main(["eval", "--gate"]) == 0


def test_cli_eval_md(capsys):
    from core.cli import main
    assert main(["eval", "--md"]) == 0
    assert "## Retrieval" in capsys.readouterr().out


# ─── Russian corpus (report-only, WP3) ─────────────────────────────────────────

def test_load_retrieval_corpus_ru_via_package_resources():
    """The RU fixture must load through importlib.resources (package data), not
    a repo-relative path — guards against a wheel that forgets the JSON."""
    from importlib import resources
    raw = resources.files("core").joinpath(
        "_eval_fixtures/retrieval_ru.json").read_text(encoding="utf-8")
    import json as _json
    assert _json.loads(raw)["cases"]
    corpus = ev.load_retrieval_corpus("ru")
    assert len(corpus["cases"]) >= 12
    assert len(corpus["distractors"]) >= 8
    assert any("typo" in c["domain"] or "morphology" in c["domain"]
               for c in corpus["cases"])


def test_load_retrieval_corpus_unknown_lang_raises():
    import pytest as _pytest
    with _pytest.raises(ValueError, match="lang"):
        ev.load_retrieval_corpus("de")


def test_run_baseline_ru_smoke():
    report = ev.run_baseline(lang="ru")
    assert report["cases"] == 16
    assert 0.0 <= report["retrieval"]["hit@3"] <= 1.0
    # Blocked answers (typo query, zero hits) must not crash the harness.
    assert 0.0 <= report["receipt_replay_survival"] <= 1.0


def test_trigram_beats_word_hashing_on_ru_typo_probes(monkeypatch):
    from core import embedding
    def probe_hits() -> float:
        report = ev.run_baseline(lang="ru", detail=True)
        probes = [c for c in report["cases_detail"]
                  if "typo" in c["domain"] or "morphology" in c["domain"]]
        return sum(c["hit@1"] for c in probes) / len(probes)

    word_score = probe_hits()
    monkeypatch.setenv("VELANTRIM_EMBEDDER", "hashing-trigram")
    embedding.reset_embedder()
    # Fresh canon for the second embedder: vectors are not comparable.
    from core import memory, l3_graph
    memory._L0.clear()
    l3_graph.reset_l3_graph()
    trigram_score = probe_hits()
    assert trigram_score > word_score


def test_cli_eval_lang_ru(capsys):
    from core.cli import main
    assert main(["eval", "--lang", "ru"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["cases"] == 16


def test_cli_eval_gate_refuses_ru(capsys):
    """Negative test: gate thresholds are EN-calibrated — RU is report-only."""
    from core.cli import main
    assert main(["eval", "--lang", "ru", "--gate"]) == 1
    assert "report-only" in capsys.readouterr().err


def test_missing_ru_fixture_raises(monkeypatch):
    monkeypatch.setattr(ev, "_load_fixture_json", lambda name: None)
    import pytest as _pytest
    with _pytest.raises(FileNotFoundError, match="retrieval_ru.json"):
        ev.load_retrieval_corpus("ru")
