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

def test_run_baseline_structure_and_ranges(monkeypatch):
    # Mirror the real eval gate environment (scripts/eval_gate.py): no demo
    # seed corpus — strict receipt replay requires every VERIFIED citation to
    # carry evidence, and demo seed facts intentionally have none.
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    report = ev.run_baseline()
    assert report["cases"] == 22          # curated bundled corpus
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
    assert c["pairs"] == 15
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
    assert rep["pairs"] == 15                      # curated bundled corpus
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
    # custom corpora skip the T3 boundary corpus (it assumes a fresh canon)
    assert "boundary" not in report


# ─── WP3: curated corpus, quality gate, reporting ─────────────────────────────

def test_load_retrieval_corpus_is_curated():
    corpus = ev.load_retrieval_corpus()
    assert len(corpus["cases"]) == 22
    assert len(corpus["distractors"]) >= 4
    # every case is a well-formed (query, claim) pair across multiple domains
    assert all(c.get("query") and c.get("claim") for c in corpus["cases"])
    assert len({c.get("domain") for c in corpus["cases"]}) >= 4


def test_load_contradiction_pairs_is_curated():
    pairs = ev.load_contradiction_pairs()
    assert len(pairs) == 15
    assert any(p["contradict"] for p in pairs) and any(not p["contradict"] for p in pairs)


def test_baseline_passes_the_quality_gate(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")  # mirror scripts/eval_gate.py
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
    assert "retrieval" in report and report["cases"] == 22


def test_cli_eval_gate_passes(capsys, monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")  # mirror scripts/eval_gate.py
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
        ev.load_retrieval_corpus("zz")


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


# ─── German corpus (report-only, WP3) ──────────────────────────────────────────

def test_load_retrieval_corpus_de():
    """DE fixture loads through importlib.resources, has 8+ cases across 4+ domains."""
    from importlib import resources
    import json as _json
    raw = resources.files("core").joinpath(
        "_eval_fixtures/retrieval_de.json").read_text(encoding="utf-8")
    assert _json.loads(raw)["cases"]
    corpus = ev.load_retrieval_corpus("de")
    assert len(corpus["cases"]) >= 8
    assert len(corpus["distractors"]) >= 3
    assert all(c.get("query") and c.get("claim") for c in corpus["cases"])
    assert len({c.get("domain") for c in corpus["cases"]}) >= 4


def test_run_baseline_de():
    report = ev.run_baseline(lang="de")
    assert report["cases"] >= 8
    for key in ("hit@1", "hit@3", "hit@5", "mrr"):
        assert 0.0 <= report["retrieval"][key] <= 1.0
    assert 0.0 <= report["receipt_replay_survival"] <= 1.0
    assert "contradiction" in report


def test_cli_eval_lang_de(capsys):
    from core.cli import main
    assert main(["eval", "--lang", "de"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["cases"] >= 8
    assert "retrieval" in out


def test_cli_eval_gate_refuses_de(capsys):
    """gate thresholds are EN-calibrated — DE is report-only."""
    from core.cli import main
    assert main(["eval", "--lang", "de", "--gate"]) == 1
    assert "report-only" in capsys.readouterr().err


def test_missing_de_fixture_raises(monkeypatch):
    monkeypatch.setattr(ev, "_load_fixture_json", lambda name: None)
    import pytest as _pytest
    with _pytest.raises(FileNotFoundError, match="retrieval_de.json"):
        ev.load_retrieval_corpus("de")


# ─── French corpus (report-only, WP3) ──────────────────────────────────────────

def test_load_retrieval_corpus_fr():
    """FR fixture loads through importlib.resources, has 8+ cases across 4+ domains."""
    from importlib import resources
    import json as _json
    raw = resources.files("core").joinpath(
        "_eval_fixtures/retrieval_fr.json").read_text(encoding="utf-8")
    assert _json.loads(raw)["cases"]
    corpus = ev.load_retrieval_corpus("fr")
    assert len(corpus["cases"]) >= 8
    assert len(corpus["distractors"]) >= 3
    assert all(c.get("query") and c.get("claim") for c in corpus["cases"])
    assert len({c.get("domain") for c in corpus["cases"]}) >= 4


def test_run_baseline_fr():
    report = ev.run_baseline(lang="fr")
    assert report["cases"] >= 8
    for key in ("hit@1", "hit@3", "hit@5", "mrr"):
        assert 0.0 <= report["retrieval"][key] <= 1.0
    assert 0.0 <= report["receipt_replay_survival"] <= 1.0
    assert "contradiction" in report


def test_cli_eval_lang_fr(capsys):
    from core.cli import main
    assert main(["eval", "--lang", "fr"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["cases"] >= 8
    assert "retrieval" in out


def test_cli_eval_gate_refuses_fr(capsys):
    """gate thresholds are EN-calibrated — FR is report-only."""
    from core.cli import main
    assert main(["eval", "--lang", "fr", "--gate"]) == 1
    assert "report-only" in capsys.readouterr().err


def test_missing_fr_fixture_raises(monkeypatch):
    monkeypatch.setattr(ev, "_load_fixture_json", lambda name: None)
    import pytest as _pytest
    with _pytest.raises(FileNotFoundError, match="retrieval_fr.json"):
        ev.load_retrieval_corpus("fr")


# ─── T3: trust-boundary behaviour corpus ──────────────────────────────────────

def test_load_boundary_cases_is_curated():
    cases = ev.load_boundary_cases()
    assert len(cases) >= 15
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids))                      # unique case ids
    known = {"abstention", "llm_output_boundary",
             "subjective_boundary", "no_trace_refusal"}
    assert {c["category"] for c in cases} <= known
    # every case is well-formed: expectations present, setup is a list
    assert all(isinstance(c.get("setup"), list) and c.get("expected")
               for c in cases)


def test_load_boundary_cases_missing_fixture_is_empty(monkeypatch):
    monkeypatch.setattr(ev, "_load_fixture_json", lambda name: None)
    assert ev.load_boundary_cases() == []


def test_boundary_eval_default_corpus_is_clean(monkeypatch):
    """T3 pin: the live pipeline honours every trust boundary in the corpus —
    abstention on unsupported queries, LLM_OUTPUT never VERIFIED, subjective
    claims typed SUBJECTIVE/HYPOTHESIS, refusal without a trace."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")  # fresh canon, as in the gate
    result = ev.boundary_eval()
    assert result["cases"] == 15
    assert result["refusal_correctness"] == 1.0
    assert result["violations"] == 0
    assert result["violations_detail"] == []
    assert len(result["cases_detail"]) == 15
    assert all(row["passed"] for row in result["cases_detail"])


def test_boundary_eval_detects_violations():
    """Synthetic cases exercise every violation branch: a wrong gate verdict,
    a wrong/banned truth_status, and a missing abstention."""
    cases = [
        {
            # An EXTERNAL world fact is accepted as VERIFIED — every
            # expectation below is deliberately wrong about that.
            "id": "syn-1", "category": "abstention",
            "setup": [{"utterance": "The copper kettle holds two liters",
                       "source_status": "EXTERNAL", "confidence": 0.9}],
            "query": "how much does the copper kettle hold",
            "expected": {"setup_accepted": [False],
                         "setup_truth_status": ["SUBJECTIVE"],
                         "setup_truth_status_not": ["VERIFIED"],
                         "answer": "abstain"},
        },
        {
            # Null expectations are explicitly skipped; a query without an
            # "answer" expectation is measured for nothing.
            "id": "syn-2", "category": "abstention",
            "setup": [{"utterance": "The copper kettle whistles loudly",
                       "source_status": "EXTERNAL", "confidence": 0.9}],
            "query": "does the copper kettle whistle",
            "expected": {"setup_accepted": [True],
                         "setup_truth_status": [None],
                         "setup_truth_status_not": [None]},
        },
    ]
    result = ev.boundary_eval(cases)
    assert result["cases"] == 2
    assert result["violations"] == 1
    [violation] = result["violations_detail"]
    assert violation["id"] == "syn-1"
    assert len(violation["problems"]) == 4   # verdict + status + banned + answer
    assert result["refusal_correctness"] == 0.0
    passed = {row["id"]: row["passed"] for row in result["cases_detail"]}
    assert passed == {"syn-1": False, "syn-2": True}


def test_boundary_eval_no_refusal_cases_scores_one():
    """refusal_correctness defaults to 1.0 when no case expects abstention."""
    result = ev.boundary_eval([])
    assert result == {"cases": 0, "refusal_correctness": 1.0, "violations": 0,
                      "violations_detail": [], "cases_detail": []}


def test_run_baseline_includes_boundary_block(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    report = ev.run_baseline()
    bnd = report["boundary"]
    assert bnd["cases"] == 15
    assert bnd["violations"] == 0
    assert bnd["refusal_correctness"] == 1.0


def test_gate_skips_boundary_metrics_without_boundary_block():
    """A custom-fixture report has no 'boundary' block — the gate must skip
    the boundary thresholds instead of crashing."""
    fixture = [{"query": "what is the capital of France",
                "claim": "Paris is the capital of France"}]
    report = ev.run_baseline(fixture)
    assert "boundary" not in report
    verdict = ev.gate(report)                # must not raise KeyError
    metrics = {f["metric"] for f in verdict["failures"]}
    assert not any(m.startswith("boundary.") for m in metrics)


def test_gate_flags_boundary_regression(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    report = ev.run_baseline()
    report["boundary"]["refusal_correctness"] = 0.5   # simulated regression
    report["boundary"]["violations"] = 2
    verdict = ev.gate(report)
    assert not verdict["passed"]
    metrics = {f["metric"] for f in verdict["failures"]}
    assert "boundary.refusal_correctness" in metrics
    assert "boundary.violations" in metrics


def test_format_report_md_boundary_section(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    md = ev.format_report_md(ev.run_baseline())
    assert "## Trust-boundary behaviour (T3)" in md
    # a custom-fixture report has no boundary block → no boundary section
    md_custom = ev.format_report_md(ev.run_baseline(
        [{"query": "what is the capital of France",
          "claim": "Paris is the capital of France"}]))
    assert "Trust-boundary" not in md_custom


# ─── T3: T2 vocabulary guard (schemas ↔ runtime enums) ───────────────────────

def test_schema_enums_match_runtime_vocabulary():
    """T2 guard: the canonical enums in schemas/ must stay bit-identical to
    core/memory.py, and FACT must never appear as a machine truth_status."""
    from pathlib import Path
    from core.memory import CLAIM_TYPES, SOURCE_STATUSES, ESM_STATES

    root = Path(__file__).resolve().parent.parent
    fact = json.loads((root / "schemas" / "fact.schema.json").read_text())
    meta = json.loads((root / "schemas" / "metadata.schema.json").read_text())
    truth_enum = {"VERIFIED", "USER_CLAIMED", "UNVERIFIED",
                  "HYPOTHESIS", "SUBJECTIVE"}

    for schema in (fact, meta):
        props = schema["properties"]
        assert set(props["claim_type"]["enum"]) == CLAIM_TYPES
        assert set(props["source_status"]["enum"]) == SOURCE_STATUSES
        assert set(props["truth_status"]["enum"]) == truth_enum
        assert "FACT" not in props["truth_status"]["enum"]
    assert set(fact["properties"]["epistemic_state"]["enum"]) == set(ESM_STATES)


def test_boundary_fixture_uses_canonical_vocabulary():
    """T2 guard: every value in boundaries.json must come from the canonical
    machine vocabulary — fixtures must not drift either."""
    from core.memory import CLAIM_TYPES, SOURCE_STATUSES
    truth_enum = {"VERIFIED", "USER_CLAIMED", "UNVERIFIED",
                  "HYPOTHESIS", "SUBJECTIVE"}
    for case in ev.load_boundary_cases():
        for spec in case["setup"]:
            assert spec.get("claim_type") in CLAIM_TYPES | {None}
            assert spec.get("source_status") in SOURCE_STATUSES | {None}
        exp = case["expected"]
        for status in exp.get("setup_truth_status", []):
            assert status in truth_enum | {None}
        for status in exp.get("setup_truth_status_not", []):
            assert status in truth_enum | {None}


# ─── T3: research-status confusion guard (narrow, negation-aware) ────────────

def test_status_docs_do_not_claim_future_components_implemented():
    """Narrow docs scan: reviewer/status documents must never present future
    research components as implemented runtime. Negated/future-labelled lines
    are allowed; only affirmative implemented-claims fail."""
    import re
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    scanned = ["README.md", "docs/REVIEWER_OVERVIEW.md",
               "docs/IMPLEMENTATION_STATUS.md", "docs/ADR.md",
               "docs/FAILURE_MODES.md", "docs/EVALUATION_METRICS.md"]
    components = ["ProfSearch", "Causal Spine", "Meta-Cognitive Monitor",
                  "Training Substrate", "Temporal Layer"]
    negation_markers = ("future", "rfc", "not implemented", "research",
                        "roadmap", "planned", "docs boundary", "vision")

    offences = []
    for rel in scanned:
        path = root / rel
        assert path.exists(), f"scanned doc missing: {rel}"
        lines = path.read_text(encoding="utf-8").splitlines()
        for n, line in enumerate(lines, 1):
            low = line.lower()
            for comp in components:
                if comp.lower() not in low:
                    continue
                affirmative = (
                    re.search(rf"{re.escape(comp.lower())}\s+is\s+implemented", low)
                    or re.search(rf"\|\s*{re.escape(comp.lower())}[^|]*\|\s*[^|]*\bimplemented\b", low)
                )
                if affirmative and not any(m in low for m in negation_markers):
                    offences.append(f"{rel}:{n}: {line.strip()}")
            if re.search(r"crystal is (a |an )?brain-?like", low):
                # Markdown wraps sentences: the negation ("not claims that
                # Crystal is brain-like…") may sit on the preceding line, so
                # the check is paragraph-aware.
                context = " ".join(lines[max(0, n - 3):n]).lower()
                if " not " not in f" {context} " and "never" not in context:
                    offences.append(f"{rel}:{n}: {line.strip()}")
    assert not offences, "affirmative research-status claims found:\n" + "\n".join(offences)
