# core/eval.py
# Velantrim ExoCortex — Evaluation Harness (baseline)
# v8.24.0-sprint5
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


def unsupported_provenance_count(fact_ids: Sequence[str]) -> int:
    """Number of VERIFIED facts that present high-confidence provenance with no
    source-span evidence (#61). A healthy corpus keeps this at zero."""
    return len(evidence.provenance_gaps(list(fact_ids)))


# ─── Curated fixture loading (WP3) ────────────────────────────────────────────
# Fixtures live in JSON files bundled with the package; the inline constants below
# are a robust fallback if the data files are ever missing.

def _load_fixture_json(name: str) -> Optional[Dict[str, Any]]:
    """Load a bundled fixture JSON by file name, or None if unavailable."""
    try:
        text = resources.files(_FIXTURE_PKG).joinpath(name).read_text(encoding="utf-8")
        return json.loads(text)
    except (FileNotFoundError, ModuleNotFoundError, OSError, ValueError):
        return None


def load_retrieval_corpus(lang: str = "en") -> Dict[str, Any]:
    """The curated retrieval corpus: {"cases": [...], "distractors": [...]}.

    lang="en" is the canonical CI-gated corpus; lang="ru" is the report-only
    Russian corpus (typo/morphology probes for embedder comparison). The English
    corpus falls back to the inline `_FIXTURE` (no distractors) if the bundled
    data file is missing, so the harness always runs; the Russian corpus has no
    inline fallback and raises if its fixture is absent.
    """
    if lang not in ("en", "ru"):
        raise ValueError(f"load_retrieval_corpus: unknown lang '{lang}' "
                         f"(available: en, ru)")
    name = "retrieval.json" if lang == "en" else "retrieval_ru.json"
    data = _load_fixture_json(name)
    if not data or not data.get("cases"):
        if lang == "ru":
            raise FileNotFoundError(f"bundled fixture {name} is missing")
        return {"cases": list(_FIXTURE), "distractors": []}
    return {"cases": data["cases"], "distractors": data.get("distractors", [])}


def load_contradiction_pairs() -> List[Dict[str, Any]]:
    """The curated labelled contradiction pairs (falls back to the inline set)."""
    data = _load_fixture_json("contradictions.json")
    if not data or not data.get("pairs"):
        return list(_CONTRADICTION_FIXTURE)
    return data["pairs"]


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
    else:
        corpus = load_retrieval_corpus(lang)
        cases = corpus["cases"]
        distractors = corpus["distractors"]

    # 0. Ingest distractor facts so retrieval ranking is non-trivial (the target
    #    fact must out-rank unrelated facts that share the same canon).
    for text in distractors:
        ingest(text)

    # 1. Ingest the corpus; remember the fact id for each expected claim. Attach a
    #    source-span evidence record so source-span coverage is measured on real data.
    claim_to_id: Dict[str, str] = {}
    for case in cases:
        res = ingest(case["claim"])
        fid = res["fact"]["fact_id"]
        claim_to_id[case["claim"]] = fid
        evidence.attach_evidence(fid, "eval-fixture", source_kind="fixture",
                                 claim=case["claim"])
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
        # A receipt built now must re-verify against the unchanged canon. A
        # blocked answer (e.g. a typo query with zero retrieval hits under the
        # word-level embedder) has no receipt — it scores 0, it must not crash
        # the harness.
        if result.get("answer") is not None:
            receipt = build_receipt(result)
            if verify_receipt(receipt).get("verified"):
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
        "unsupported_provenance": unsupported_provenance_count(fact_ids),
        "receipt_replay_survival": round(receipts_ok / n, 4),
        "contradiction": contradiction_eval(),
    }
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
    "receipt_replay_survival": 1.0,
    "contradiction.precision": 0.75,   # baseline 0.8333
    "contradiction.recall": 0.75,      # baseline 0.8333
}
# Metrics where LOWER is better (ceilings, not floors).
_GATE_MAX: Dict[str, float] = {
    "unsupported_provenance": 0,          # baseline 0
    "contradiction.false_positive_rate": 0.25,   # baseline 0.1667
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
        value = _dig(report, metric)
        if value < floor:
            failures.append({"metric": metric, "value": value,
                             "op": ">=", "threshold": floor})
    for metric, ceil in _GATE_MAX.items():
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
    return "\n".join(lines)
