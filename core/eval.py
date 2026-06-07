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

from typing import Any, Dict, List, Sequence

from core.ingest import ingest
from core.pipeline import retrieve, run
from core.memory import get_fact
from core.provenance import build_receipt, verify_receipt

# Metadata every stored fact must carry (typing / provenance completeness).
_REQUIRED_FIELDS = ("source", "source_status", "claim_type", "epistemic_state")


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

def run_baseline(fixture: List[Dict[str, str]] | None = None, *, k: int = 5) -> Dict[str, Any]:
    """
    Ingest the fixture corpus and measure the live pipeline:

    - retrieval: hit@1/3/5 + MRR of the expected fact for each query;
    - trace_completeness: share of answers that carry a non-empty trace;
    - metadata_completeness: share of facts with full typing/provenance;
    - receipt_replay_survival: share of receipts that re-verify against the
      unchanged canon.

    Deterministic with the dependency-free hashing embedder + extractive answerer.
    Returns a machine-readable report (also see docs/EVAL.md).
    """
    fixture = fixture if fixture is not None else _FIXTURE

    # 1. Ingest the corpus; remember the fact id for each expected claim.
    claim_to_id: Dict[str, str] = {}
    for case in fixture:
        res = ingest(case["claim"])
        claim_to_id[case["claim"]] = res["fact"]["fact_id"]
    fact_ids = list(claim_to_id.values())

    # 2. Per-query retrieval ranking + trace + receipt.
    per_case: List[Dict[str, Any]] = []
    traced = 0
    receipts_ok = 0
    for case in fixture:
        relevant = [claim_to_id[case["claim"]]]
        ranked = [item["id"] for item in retrieve(case["query"], k=k)]
        per_case.append({"ranked": ranked, "relevant": relevant})

        result = run(case["query"])
        if result.get("trace"):
            traced += 1
        # A receipt built now must re-verify against the unchanged canon.
        receipt = build_receipt(result)
        if verify_receipt(receipt).get("verified"):
            receipts_ok += 1

    n = len(fixture) or 1
    report = {
        "cases": len(fixture),
        "retrieval": aggregate(per_case),
        "trace_completeness": round(traced / n, 4),
        "metadata_completeness": metadata_completeness(fact_ids),
        "receipt_replay_survival": round(receipts_ok / n, 4),
    }
    return report
