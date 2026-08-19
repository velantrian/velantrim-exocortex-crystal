# core/eval.py
# Velantrim ExoCortex — Evaluation Harness (baseline)
#
# Beyond unit-test coverage, this module MEASURES whether memory answers stay
# grounded, replayable and well-typed. It is deterministic and dependency-free:
# it ingests a small fixture corpus, runs the real retrieval/answer/receipt path,
# and reports quality metrics. See docs/EVAL.md for the metric definitions.
#
# The pure metric functions (hit@k, MRR, aggregate) are exact and side-effect free.
# run_baseline() exercises the actual pipeline so the numbers reflect real behaviour
# rather than a narrative. Advanced fixtures (source-span coverage, dry-run review)
# remain future work (grant scope WP2/WP3).

import hashlib
import json
from importlib import resources
from typing import Any, Dict, List, Optional, Sequence

from core.ingest import ingest, _fact_id
from core.pipeline import retrieve, run
from core.memory import get_fact
from core.provenance import build_receipt, verify_receipt
from core.reconcile import find_conflicts
from core import contradiction, evidence

# Metadata every stored fact must carry (typing / provenance completeness).
_REQUIRED_FIELDS = ("source", "source_status", "claim_type", "epistemic_state")

# Curated fixture corpora are bundled inside the package (WP3) so `velantrim eval`
# works from an installed wheel as well as the repo.
_FIXTURE_PKG = "core._eval_fixtures"
_FIXTURE_MANIFEST = "manifest.json"


# ─── Pure metric functions ────────────────────────────────────────────────────

def hit_at_k(ranked: Sequence[str], relevant: Sequence[str], k: int) -> float:
    """1.0 if any relevant id appears in the top-k of `ranked`, else 0.0."""
    rel = set(relevant)
    return 1.0 if any(r in rel for r in list(ranked)[:k]) else 0.0


def reciprocal_rank(ranked: Sequence[str], relevant: Sequence[str]) -> float:
    """1/rank of the first relevant id (0.0 if none present)."""
    rel = set(relevant)
    for i, r in enumerate(ranked, start=1):
        if r in rel:
            return 1.0 / i
    return 0.0


def aggregate(per_case: List[Dict[str, Any]], ks: Sequence[int] = (1, 3, 5)) -> Dict[str, float]:
    """Aggregate hit@k and MRR over cases of {"ranked": [...], "relevant": [...]}."""
    n = len(per_case) or 1
    out: Dict[str, float] = {}
    for k in ks:
        out[f"hit@{k}"] = round(
            sum(hit_at_k(c["ranked"], c["relevant"], k) for c in per_case) / n, 4)
    out["mrr"] = round(
        sum(reciprocal_rank(c["ranked"], c["relevant"]) for c in per_case) / n, 4)
    return out


def metadata_completeness(fact_ids: Sequence[str]) -> float:
    """Fraction of facts that carry all required typing/provenance fields."""
    ids = list(fact_ids)
    if not ids:
        return 0.0
    ok = 0
    for fid in ids:
        fact = get_fact(fid)
        if fact and all(fact.get(f) for f in _REQUIRED_FIELDS):
            ok += 1
    return round(ok / len(ids), 4)


def source_span_coverage(fact_ids: Sequence[str]) -> float:
    """Fraction of facts that carry at least one source-span evidence record (WP1)."""
    ids = list(fact_ids)
    if not ids:
        return 0.0
    covered = sum(1 for fid in ids if evidence.evidence_for(fid))
    return round(covered / len(ids), 4)


def strict_source_span_coverage(fact_ids: Sequence[str]) -> float:
    """Fraction with replayable evidence eligible for grant strict grounding."""
    ids = list(fact_ids)
    if not ids:
        return 0.0
    covered = sum(1 for fid in ids if evidence.has_valid_evidence_for_grounding(fid))
    return round(covered / len(ids), 4)


def unsupported_provenance_count(fact_ids: Sequence[str]) -> int:
    """Number of VERIFIED facts that present high-confidence provenance with no
    source-span evidence (#61). A healthy corpus keeps this at zero."""
    return len(evidence.provenance_gaps(list(fact_ids)))


# ─── Curated fixture loading (WP3) ────────────────────────────────────────────
# Fixtures live in JSON files bundled with the package; the inline constants below
# are a robust fallback if the data files are ever missing.

def _fixture_manifest() -> Dict[str, Any]:
    """Load the frozen fixture manifest; absence or corruption is a gate failure."""
    try:
        text = resources.files(_FIXTURE_PKG).joinpath(_FIXTURE_MANIFEST).read_text(encoding="utf-8")
        data = json.loads(text)
    except (FileNotFoundError, ModuleNotFoundError, OSError, ValueError) as exc:
        raise RuntimeError("fixture manifest is missing or malformed") from exc
    if not isinstance(data, dict):
        raise RuntimeError("fixture manifest must be a JSON object")
    return data


def _load_fixture_json(name: str) -> Optional[Dict[str, Any]]:
    """Load a bundled fixture and fail closed if its frozen digest drifts."""
    try:
        text = resources.files(_FIXTURE_PKG).joinpath(name).read_text(encoding="utf-8")
        manifest = _fixture_manifest()
        expected = (manifest.get("sha256") or {}).get(name)
        if not isinstance(expected, str) or not expected:
            raise RuntimeError(f"fixture manifest has no digest for {name}")
        actual = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if actual != expected:
            raise RuntimeError(
                f"fixture digest mismatch for {name}: expected {expected}, got {actual}"
            )
        return json.loads(text)
    except RuntimeError:
        raise
    except (FileNotFoundError, ModuleNotFoundError, OSError, ValueError):
        return None


def load_retrieval_corpus(lang: str = "en") -> Dict[str, Any]:
    """The curated retrieval corpus: {"cases": [...], "distractors": [...]}.

    lang="en" is the canonical CI-gated corpus; lang="ru"/"de"/"fr" are the
    report-only corpora (typo/morphology probes and multilingual coverage for
    embedder comparison). The English corpus falls back to the inline `_FIXTURE`
    (no distractors) if the bundled data file is missing, so the harness always
    runs; the non-English corpora have no inline fallback and raise if absent.
    """
    _REPORT_ONLY_LANGS = {"ru": "retrieval_ru.json",
                          "de": "retrieval_de.json",
                          "fr": "retrieval_fr.json"}
    if lang not in ("en", "ru", "de", "fr"):
        raise ValueError(f"load_retrieval_corpus: unknown lang '{lang}' "
                         f"(available: en, ru, de, fr)")
    if lang == "en":
        name = "retrieval.json"
    else:
        name = _REPORT_ONLY_LANGS[lang]
    data = _load_fixture_json(name)
    if not data or not data.get("cases"):
        if lang != "en":
            raise FileNotFoundError(f"bundled fixture {name} is missing")
        return {"cases": list(_FIXTURE), "distractors": []}
    return {"cases": data["cases"], "distractors": data.get("distractors", [])}


def load_contradiction_pairs() -> List[Dict[str, Any]]:
    """The curated labelled contradiction pairs (falls back to the inline set)."""
    data = _load_fixture_json("contradictions.json")
    if not data or not data.get("pairs"):
        return list(_CONTRADICTION_FIXTURE)
    return data["pairs"]


def load_boundary_cases() -> List[Dict[str, Any]]:
    """The curated T3 trust-boundary behaviour corpus (boundaries.json).

    Returns an empty list if the bundled fixture is missing, so the harness
    degrades to "no boundary cases" instead of crashing.
    """
    data = _load_fixture_json("boundaries.json")
    if not data or not data.get("cases"):
        return []
    return list(data["cases"])


def boundary_eval(cases: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    """
    Behaviour-level trust-boundary checks (T3): replay each boundary case
    against the LIVE pipeline and verify the *existing* pinned behaviour —
    abstention on unsupported queries, the LLM_OUTPUT→VERIFIED promotion ban,
    subjective-claim typing, and no-trace refusal. This is an eval-layer
    measurement only: it never modifies TruthGate/pipeline/ingest behaviour,
    and a failing case is a metric (`violations`), never a runtime change.

    Cases assume a fresh canon (no demo seed): the bundled abstention cases
    rely on retrieval finding nothing for their queries, so run this BEFORE
    ingesting any corpus (run_baseline() does exactly that). Case order inside
    the fixture is significant — see boundaries.json `description`.

    Reports:
      - cases:               number of boundary cases evaluated;
      - refusal_correctness: correct abstentions / cases expecting abstention
                             (1.0 when no case expects abstention);
      - violations:          number of cases whose expectations failed;
      - violations_detail:   [{id, category, problems}, ...];
      - cases_detail:        [{id, category, passed}, ...].
    """
    if cases is None:
        cases = load_boundary_cases()
    refusal_total = 0
    refusal_ok = 0
    violations: List[Dict[str, Any]] = []
    detail: List[Dict[str, Any]] = []
    for case in cases:
        problems: List[str] = []
        exp = case.get("expected", {})

        # 1. Setup claims go through the real ingest path (gates included).
        setup_results: List[Dict[str, Any]] = []
        for spec in case.get("setup", []):
            kwargs = {k: spec[k] for k in ("claim_type", "source_status", "confidence")
                      if k in spec}
            setup_results.append(ingest(spec["utterance"], **kwargs))

        # 2. Pin the gate verdict and the assigned truth_status per setup claim.
        #    Defensive .get(): on a non-fresh canon a re-ingested utterance can
        #    take the reinforcement path and return a fact without truth_status
        #    — that surfaces as an honest violation, never a crash.
        for i, want in enumerate(exp.get("setup_accepted", [])):
            got = bool(setup_results[i].get("accepted"))
            if got is not bool(want):
                problems.append(f"setup[{i}]: accepted={got}, expected {want}")
        for i, want in enumerate(exp.get("setup_truth_status", [])):
            got = (setup_results[i].get("fact") or {}).get("truth_status")
            if want is not None and got != want:
                problems.append(f"setup[{i}]: truth_status={got}, expected {want}")
        for i, banned in enumerate(exp.get("setup_truth_status_not", [])):
            got = (setup_results[i].get("fact") or {}).get("truth_status")
            if banned is not None and got == banned:
                problems.append(f"setup[{i}]: truth_status must not be {banned}")

        # 3. Pin the answer-path behaviour (abstain = answer is None).
        query = case.get("query")
        if query:
            result = run(query)
            if exp.get("answer") == "abstain":
                refusal_total += 1
                if result.get("answer") is None:
                    refusal_ok += 1
                else:
                    problems.append("expected abstain, got a confident answer")

        if problems:
            violations.append({"id": case.get("id", "?"),
                               "category": case.get("category", "?"),
                               "problems": problems})
        detail.append({"id": case.get("id", "?"),
                       "category": case.get("category", "?"),
                       "passed": not problems})
    return {
        "cases": len(cases),
        "refusal_correctness": (round(refusal_ok / refusal_total, 4)
                                if refusal_total else 1.0),
        "violations": len(violations),
        "violations_detail": violations,
        "cases_detail": detail,
    }



# ─── Contradiction handling (WP3) ─────────────────────────────────────────────

_CONTRADICTION_FIXTURE: List[Dict[str, Any]] = [
    {"base": "The sky is blue", "probe": "The sky is not blue", "contradict": True},
    {"base": "Water boils at 100 degrees Celsius",
     "probe": "Water boils at 50 degrees Celsius", "contradict": True},
    {"base": "Paris is the capital of France",
     "probe": "Berlin is the capital of Germany", "contradict": False},
    {"base": "Gold is a chemical element",
     "probe": "Silver is a chemical element", "contradict": False},
]


def contradiction_eval(pairs: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    """
    Measure the deterministic contradiction classifier on labelled pairs: ingest
    each `base`, then check whether `probe` is flagged as a CONTRADICTION against
    the canon. Reports precision, recall and the false-positive rate.
    """
    pairs = pairs if pairs is not None else load_contradiction_pairs()
    tp = fp = fn = tn = 0
    for p in pairs:
        ingest(p["base"])
        conflicts = find_conflicts(p["probe"], fact_id=_fact_id(p["probe"]))
        predicted = any(c["kind"] == contradiction.CONTRADICTION for c in conflicts)
        actual = bool(p["contradict"])
        if predicted and actual:
            tp += 1
        elif predicted and not actual:
            fp += 1
        elif not predicted and actual:
            fn += 1
        else:
            tn += 1
    precision = round(tp / (tp + fp), 4) if (tp + fp) else 1.0
    recall = round(tp / (tp + fn), 4) if (tp + fn) else 1.0
    fpr = round(fp / (fp + tn), 4) if (fp + tn) else 0.0
    return {"pairs": len(pairs), "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": precision, "recall": recall, "false_positive_rate": fpr}


# ─── Default fixture (deterministic, dependency-free) ─────────────────────────

_FIXTURE: List[Dict[str, str]] = [
    {"query": "what temperature does water boil at sea level",
     "claim": "Water boils at 100 degrees Celsius at sea level"},
    {"query": "what is the capital of Austria",
     "claim": "Vienna is the capital of Austria"},
    {"query": "what does the Earth orbit",
     "claim": "The Earth orbits the Sun"},
    {"query": "what is gold",
     "claim": "Gold is a chemical element and a metal"},
]


# ─── Baseline run over the real pipeline ──────────────────────────────────────

def run_baseline(fixture: List[Dict[str, str]] | None = None, *, k: int = 5,
                 detail: bool = False, lang: str = "en") -> Dict[str, Any]:
    """
    Ingest the fixture corpus and measure the live pipeline:

    - retrieval: hit@1/3/5 + MRR of the expected fact for each query;
    - trace_completeness: share of answers that carry a non-empty trace;
    - metadata_completeness: share of facts with full typing/provenance;
    - source_span_coverage: share of facts with attached source-span evidence;
    - receipt_replay_survival: share of receipts that re-verify against the
      unchanged canon;
    - contradiction: precision/recall of the deterministic classifier.

    With no explicit `fixture`, the curated bundled corpus for `lang` is used
    ("en" — the CI-gated default; "ru" — report-only, with typo/morphology
    probes) and its `distractors` are ingested as ranking noise so the metrics
    are non-trivial. Pass an explicit list to evaluate a custom corpus (no
    distractors). Set `detail=True` to include a per-case breakdown
    (`cases_detail`).

    Deterministic with the dependency-free hashing embedder + extractive answerer.
    Returns a machine-readable report (also see docs/EVAL.md).
    """
    if fixture is not None:
        cases: List[Dict[str, str]] = fixture
        distractors: List[str] = []
        boundary: Optional[Dict[str, Any]] = None
    else:
        # T3 trust-boundary corpus runs FIRST, on the still-empty canon: its
        # abstention cases require retrieval to find nothing for their queries.
        # Accepted boundary setup facts then remain as extra ranking noise for
        # the retrieval corpus below. Custom fixtures skip the boundary corpus
        # (their report carries no "boundary" block; gate() skips accordingly).
        boundary = boundary_eval()
        corpus = load_retrieval_corpus(lang)
        cases = corpus["cases"]
        distractors = corpus["distractors"]

    # 0. Ingest distractor facts so retrieval ranking is non-trivial (the target
    #    fact must out-rank unrelated facts that share the same canon).
    # Deliberately left as plain ingest() (source_status default →
    # truth_status=USER_CLAIMED, never VERIFIED): distractors are ranking
    # noise only, never intended to ground an answer or carry evidence. If
    # they were EXTERNAL/VERIFIED, an unrelated distractor pulled into the
    # same facts_pack as a target case (close vector similarity / graph-walk)
    # would be cited as VERIFIED grounding with no evidence attached and fail
    # strict-provenance receipt verification for a reason unrelated to this
    # corpus's actual retrieval/grounding quality.
    for text in distractors:
        ingest(text)

    # 1. Ingest the corpus; remember the fact id for each expected claim. Attach a
    #    source-span evidence record so source-span coverage is measured on real data.
    # source_status="EXTERNAL": this fixture represents a curated reference
    # corpus (docs/EVAL.md), the same convention core/demo_seed.py documents
    # for "curated reference knowledge, not user reports". Without this,
    # ingest()'s classifier defaults every utterance to source_status=
    # USER_REPORTED, which core.pipeline._truth_status_for() maps to
    # truth_status=USER_CLAIMED — never VERIFIED — so after CanonicalView
    # strict grounding (this PR), run()/generate_answer() would abstain on
    # every case and collapse receipt_replay_survival to 0, not because
    # retrieval/grounding quality regressed, but because the fixture was
    # accidentally exercising the "unverified user claim" path instead of the
    # "verified external corpus" path it is documented to simulate.
    claim_to_id: Dict[str, str] = {}
    for case_index, case in enumerate(cases, 1):
        res = ingest(case["claim"], source_status="EXTERNAL")
        fid = res["fact"]["fact_id"]
        claim_to_id[case["claim"]] = fid
        evidence.attach_evidence(
            fid,
            f"fixture://retrieval/{case_index}",
            source_kind="fixture",
            claim=case["claim"],
            section=f"case:{case_index}",
            source_text=case["claim"],
            lineage_id=f"fixture-lineage:{case_index}",
            independence_class="INDEPENDENT_ASSERTED",
            lineage_basis="IMPORTER_DECLARED",
        )
    fact_ids = list(claim_to_id.values())

    # 2. Per-query retrieval ranking + trace + receipt.
    per_case: List[Dict[str, Any]] = []
    cases_detail: List[Dict[str, Any]] = []
    traced = 0
    receipts_ok = 0
    for case in cases:
        relevant = [claim_to_id[case["claim"]]]
        ranked = [item["id"] for item in retrieve(case["query"], k=k)]
        per_case.append({"ranked": ranked, "relevant": relevant})

        result = run(case["query"])
        if result.get("trace"):
            traced += 1
# A receipt built now must re-verify against the unchanged canon —
        # strictly: a VERIFIED citation with no source-span evidence fails the
        # replay (and thus the CI gate), not just the unsupported_provenance
        # count. A blocked answer (e.g. a typo query with zero retrieval hits
        # under the word-level embedder) has no receipt — it scores 0, it must
        # not crash the harness.
        if result.get("answer") is not None:
            receipt = build_receipt(result)
            if verify_receipt(receipt, strict_provenance=True).get("verified"):
                receipts_ok += 1

        if detail:
            cases_detail.append({
                "domain": case.get("domain", "default"),
                "query": case["query"],
                "expected": relevant[0],
                "hit@1": hit_at_k(ranked, relevant, 1),
                "hit@3": hit_at_k(ranked, relevant, 3),
                "rr": round(reciprocal_rank(ranked, relevant), 4),
            })

    n = len(cases) or 1
    report = {
        "cases": len(cases),
        "retrieval": aggregate(per_case),
        "trace_completeness": round(traced / n, 4),
        "metadata_completeness": metadata_completeness(fact_ids),
        "source_span_coverage": source_span_coverage(fact_ids),
        "strict_source_span_coverage": strict_source_span_coverage(fact_ids),
        "unsupported_provenance": unsupported_provenance_count(fact_ids),
        "receipt_replay_survival": round(receipts_ok / n, 4),
        "lineage": evidence.lineage_metrics(fact_ids),
        "contradiction": contradiction_eval(),
    }
    if boundary is not None:
        report["boundary"] = boundary
    if detail:
        report["cases_detail"] = cases_detail
    return report


# ─── Quality gate (WP3) ───────────────────────────────────────────────────────
# Regression thresholds: the baseline currently scores at or above each of these.
# CI fails if a change drops a metric below its floor, so quality cannot silently
# degrade between releases. Tune upward as the corpus and embedder improve.

DEFAULT_GATE: Dict[str, float] = {
    "retrieval.hit@1": 0.80,           # baseline 0.875
    "retrieval.hit@3": 0.85,           # baseline 0.9375
    "retrieval.mrr": 0.85,             # baseline 0.9115
    "trace_completeness": 1.0,
    "metadata_completeness": 1.0,
    "source_span_coverage": 1.0,
    "strict_source_span_coverage": 1.0,
    "receipt_replay_survival": 1.0,
    "lineage.known_lineage_coverage": 1.0,
    "lineage.independence_assertion_coverage": 1.0,
    "contradiction.precision": 0.75,   # baseline 0.8333
    "contradiction.recall": 0.75,      # baseline 0.8333
    "boundary.refusal_correctness": 1.0,   # T3: every expected abstention happens
}
# Metrics where LOWER is better (ceilings, not floors).
_GATE_MAX: Dict[str, float] = {
    "unsupported_provenance": 0,          # baseline 0
    "lineage.same_lineage_duplicate_rate": 0.0,
    "lineage.unknown_lineage_rate": 0.0,
    "contradiction.false_positive_rate": 0.25,   # baseline 0.1667
    "boundary.violations": 0,             # T3: no trust-boundary expectation may fail
}


def _dig(report: Dict[str, Any], dotted: str) -> Any:
    cur: Any = report
    for part in dotted.split("."):
        cur = cur[part]
    return cur


def gate(report: Dict[str, Any],
         thresholds: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Compare a report against floor/ceiling thresholds.

    Returns {"passed": bool, "failures": [{metric, value, op, threshold}, ...]}.
    """
    floors = thresholds if thresholds is not None else DEFAULT_GATE
    failures: List[Dict[str, Any]] = []
    for metric, floor in floors.items():
        # Boundary metrics exist only for the bundled-corpus run; a custom
        # fixture report carries no "boundary" block, so those thresholds are
        # skipped rather than crashing the gate.
        if metric.startswith("boundary.") and "boundary" not in report:
            continue
        value = _dig(report, metric)
        if value < floor:
            failures.append({"metric": metric, "value": value,
                             "op": ">=", "threshold": floor})
    for metric, ceil in _GATE_MAX.items():
        if metric.startswith("boundary.") and "boundary" not in report:
            continue
        value = _dig(report, metric)
        if value > ceil:
            failures.append({"metric": metric, "value": value,
                             "op": "<=", "threshold": ceil})
    return {"passed": not failures, "failures": failures}


def format_report_md(report: Dict[str, Any]) -> str:
    """Render a report as a human-readable Markdown summary (CI artifact)."""
    r = report
    ret = r["retrieval"]
    con = r["contradiction"]
    lines = [
        "# Velantrim Crystal — Evaluation Report",
        "",
        f"- **cases:** {r['cases']}",
        "",
        "## Retrieval",
        "",
        "| hit@1 | hit@3 | hit@5 | MRR |",
        "|---|---|---|---|",
        f"| {ret['hit@1']} | {ret['hit@3']} | {ret['hit@5']} | {ret['mrr']} |",
        "",
        "## Grounding & provenance",
        "",
        "| metric | value |",
        "|---|---|",
        f"| trace_completeness | {r['trace_completeness']} |",
        f"| metadata_completeness | {r['metadata_completeness']} |",
        f"| source_span_coverage | {r['source_span_coverage']} |",
        f"| strict_source_span_coverage | {r['strict_source_span_coverage']} |",
        f"| lineage.known_lineage_coverage | {r['lineage']['known_lineage_coverage']} |",
        f"| lineage.same_lineage_duplicate_rate | {r['lineage']['same_lineage_duplicate_rate']} |",
        f"| lineage.unknown_lineage_rate | {r['lineage']['unknown_lineage_rate']} |",
        f"| unsupported_provenance | {r['unsupported_provenance']} |",
        f"| receipt_replay_survival | {r['receipt_replay_survival']} |",
        "",
        "## Contradiction classifier",
        "",
        "| pairs | precision | recall | FPR |",
        "|---|---|---|---|",
        f"| {con['pairs']} | {con['precision']} | {con['recall']} "
        f"| {con['false_positive_rate']} |",
        "",
    ]
    bnd = r.get("boundary")
    if bnd is not None:
        lines += [
            "## Trust-boundary behaviour (T3)",
            "",
            "| cases | refusal_correctness | violations |",
            "|---|---|---|",
            f"| {bnd['cases']} | {bnd['refusal_correctness']} "
            f"| {bnd['violations']} |",
            "",
        ]
    return "\n".join(lines)
