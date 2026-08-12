#!/usr/bin/env python3
"""Reproducible benchmark for the Reader RC-9 lexical discovery baseline."""
from __future__ import annotations

import argparse
import hashlib
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Iterable

from core.reader_lexical_discovery import ReaderLexicalIndex, ReaderLexicalRecord, RETRIEVAL_METHOD

POSITIVE_REVIEW_CLASSES = frozenset(
    {
        "SAME_PROPOSITION_CANDIDATE",
        "PARAPHRASE_CANDIDATE",
        "RELATED_CLAIM",
        "POSSIBLE_CONTRADICTION",
    }
)
HARD_NEGATIVE_REVIEW_CLASSES = frozenset({"SAME_TOPIC", "MERELY_SIMILAR"})
REQUIRED_FIELDS = frozenset({"case_id", "stratum", "left", "right", "expected_review_class", "note"})


@dataclass(frozen=True)
class BenchmarkCase:
    case_id: str
    stratum: str
    left: str
    right: str
    expected_review_class: str
    note: str


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    stratum: str
    expected_review_class: str
    relevance_intent: str
    paired_candidate_rank: int | None
    paired_candidate_score: float | None
    paired_candidate_retrieved_at_k: bool
    candidates_returned: int
    matched_terms: tuple[str, ...]


def _required_string(value: object, field_name: str, line_number: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"line {line_number}: {field_name} must be a non-empty string")
    return value.strip()


def load_cases(path: Path) -> tuple[BenchmarkCase, ...]:
    cases: list[BenchmarkCase] = []
    seen: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"line {line_number}: malformed JSON: {exc.msg}") from exc
            if not isinstance(payload, dict):
                raise ValueError(f"line {line_number}: case must be a JSON object")
            missing = REQUIRED_FIELDS - payload.keys()
            if missing:
                raise ValueError(f"line {line_number}: missing fields: {', '.join(sorted(missing))}")
            case = BenchmarkCase(
                case_id=_required_string(payload["case_id"], "case_id", line_number),
                stratum=_required_string(payload["stratum"], "stratum", line_number),
                left=_required_string(payload["left"], "left", line_number),
                right=_required_string(payload["right"], "right", line_number),
                expected_review_class=_required_string(
                    payload["expected_review_class"], "expected_review_class", line_number
                ),
                note=_required_string(payload["note"], "note", line_number),
            )
            if case.case_id in seen:
                raise ValueError(f"line {line_number}: duplicate case_id: {case.case_id}")
            if case.expected_review_class not in POSITIVE_REVIEW_CLASSES | HARD_NEGATIVE_REVIEW_CLASSES:
                raise ValueError(
                    f"line {line_number}: unsupported expected_review_class: {case.expected_review_class}"
                )
            seen.add(case.case_id)
            cases.append(case)
    if not cases:
        raise ValueError("benchmark corpus must contain at least one case")
    return tuple(cases)


def _record(case: BenchmarkCase, side: str, proposition: str) -> ReaderLexicalRecord:
    return ReaderLexicalRecord(
        session_id=f"bench-{side}-{case.case_id}",
        candidate_id=f"{case.case_id}-{side}",
        document_id=f"bench-{side}-doc-{case.case_id}",
        source_uri=f"synthetic://reader-rc8/{case.case_id}/{side}",
        source_sha256=hashlib.sha256(proposition.encode("utf-8")).hexdigest(),
        proposition=proposition,
    )


def run_benchmark(cases: Iterable[BenchmarkCase], *, k: int = 5) -> dict[str, object]:
    items = tuple(cases)
    if not items:
        raise ValueError("cases must not be empty")
    rights = tuple(_record(case, "right", case.right) for case in items)
    index = ReaderLexicalIndex(rights)

    case_results: list[CaseResult] = []
    reciprocal_ranks: list[float] = []
    positive_hits = 0
    positive_count = 0
    hard_negative_hits = 0
    hard_negative_count = 0
    returned_slots_for_positive_queries = 0

    for case in items:
        query = _record(case, "left", case.left)
        matches = index.discover(query, k=k)
        paired_id = f"{case.case_id}-right"
        paired = next((match for match in matches if match.candidate_id == paired_id), None)
        relevant = case.expected_review_class in POSITIVE_REVIEW_CLASSES
        if relevant:
            positive_count += 1
            returned_slots_for_positive_queries += len(matches)
            if paired is not None:
                positive_hits += 1
                reciprocal_ranks.append(1.0 / paired.rank)
            else:
                reciprocal_ranks.append(0.0)
            intent = "USEFUL_CANDIDATE"
        else:
            hard_negative_count += 1
            if paired is not None:
                hard_negative_hits += 1
            intent = "HARD_NEGATIVE"
        case_results.append(
            CaseResult(
                case_id=case.case_id,
                stratum=case.stratum,
                expected_review_class=case.expected_review_class,
                relevance_intent=intent,
                paired_candidate_rank=paired.rank if paired else None,
                paired_candidate_score=paired.lexical_score if paired else None,
                paired_candidate_retrieved_at_k=paired is not None,
                candidates_returned=len(matches),
                matched_terms=paired.matched_terms if paired else (),
            )
        )

    recall_at_k = positive_hits / positive_count if positive_count else 0.0
    precision_at_k = (
        positive_hits / returned_slots_for_positive_queries
        if returned_slots_for_positive_queries
        else 0.0
    )
    mrr = sum(reciprocal_ranks) / positive_count if positive_count else 0.0
    hard_negative_rate = hard_negative_hits / hard_negative_count if hard_negative_count else 0.0
    return {
        "benchmark": "reader_rc9_lexical_baseline",
        "method": RETRIEVAL_METHOD,
        "k": k,
        "case_count": len(items),
        "work_bound": {
            "index_records": len(rights),
            "queries": len(items),
            "max_record_comparisons": len(rights) * len(items),
            "storage": "in_memory",
            "network_calls": 0,
            "mandatory_third_party_dependencies": 0,
        },
        "positive_case_count": positive_count,
        "hard_negative_case_count": hard_negative_count,
        "metrics": {
            "recall_at_k": round(recall_at_k, 6),
            "precision_at_k": round(precision_at_k, 6),
            "mrr": round(mrr, 6),
            "paired_hard_negative_rate_at_k": round(hard_negative_rate, 6),
            "positive_hits": positive_hits,
            "hard_negative_hits": hard_negative_hits,
            "returned_slots_for_positive_queries": returned_slots_for_positive_queries,
        },
        "metric_scope": (
            "The RC-8 JSONL judges only each case's left/right pair. Recall/MRR track the paired "
            "useful candidate; precision treats other returned corpus entries as benchmark decoys. "
            "Hard-negative rate tracks only the paired SAME_TOPIC/MERELY_SIMILAR traps. Metrics are "
            "retrieval evidence, never epistemic adjudication."
        ),
        "cases": [asdict(result) for result in case_results],
    }


def human_summary(result: dict[str, object]) -> str:
    metrics = result["metrics"]
    assert isinstance(metrics, dict)
    return "\n".join(
        (
            "Reader RC-9 deterministic lexical baseline",
            f"method: {result['method']}",
            f"cases: {result['case_count']} (useful={result['positive_case_count']}, hard-negative={result['hard_negative_case_count']})",
            f"Recall@{result['k']}: {metrics['recall_at_k']:.6f}",
            f"Precision@{result['k']}: {metrics['precision_at_k']:.6f}",
            f"MRR: {metrics['mrr']:.6f}",
            f"Paired hard-negative rate@{result['k']}: {metrics['paired_hard_negative_rate_at_k']:.6f}",
            "Boundary: ranking is candidate discovery only; no identity/evidence/Canon verdict is produced.",
        )
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--corpus",
        type=Path,
        default=Path("eval/reader_rc8_retrieval_adversarial.jsonl"),
    )
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--json-only", action="store_true")
    return parser


def main() -> int:
    args = _parser().parse_args()
    cases = load_cases(args.corpus)
    result = run_benchmark(cases, k=args.k)
    encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(encoded + "\n", encoding="utf-8")
    if args.json_only:
        print(encoded)
    else:
        print(human_summary(result))
        print("\nMachine-readable JSON:\n" + encoded)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
