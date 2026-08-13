#!/usr/bin/env python3
"""Reproduce Reader RC-9 on the fully judged Retrieval Evaluation Surface v2."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

from core.reader_lexical_discovery import ReaderLexicalIndex, ReaderLexicalRecord, RETRIEVAL_METHOD

DEFAULT_QUERIES = Path("eval/reader_retrieval_eval_v2_queries.jsonl")
DEFAULT_CANDIDATES = Path("eval/reader_retrieval_eval_v2_candidates.jsonl")
DEFAULT_QRELS = Path("eval/reader_retrieval_eval_v2_qrels.jsonl")
DEFAULT_MANIFEST = Path("eval/reader_retrieval_eval_v2_manifest.json")
DEFAULT_K = 5

QUERY_FIELDS = frozenset({"query_id", "pool_id", "primary_stratum", "secondary_strata", "proposition"})
CANDIDATE_FIELDS = frozenset({"candidate_id", "pool_id", "proposition"})
QREL_FIELDS = frozenset({"query_id", "candidate_id", "judgment", "review_class"})
USEFUL_CLASSES = frozenset(
    {"SAME_PROPOSITION_CANDIDATE", "PARAPHRASE_CANDIDATE", "RELATED_CLAIM", "POSSIBLE_CONTRADICTION"}
)
HARD_NEGATIVE_CLASSES = frozenset({"SAME_TOPIC", "MERELY_SIMILAR"})
JUDGMENT_KINDS = frozenset({"USEFUL_CANDIDATE", "HARD_NEGATIVE", "NEUTRAL_DECOY"})


@dataclass(frozen=True)
class EvalQuery:
    query_id: str
    pool_id: str
    primary_stratum: str
    secondary_strata: tuple[str, ...]
    proposition: str


@dataclass(frozen=True)
class EvalCandidate:
    candidate_id: str
    pool_id: str
    proposition: str


@dataclass(frozen=True)
class EvalJudgment:
    query_id: str
    candidate_id: str
    judgment_kind: str
    expected_review_class: str


@dataclass(frozen=True)
class EvalSurface:
    queries: tuple[EvalQuery, ...]
    candidates: tuple[EvalCandidate, ...]
    qrels: tuple[EvalJudgment, ...]


def _read_jsonl(path: Path) -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}: line {line_number}: malformed JSON: {exc.msg}") from exc
            if not isinstance(payload, dict):
                raise ValueError(f"{path}: line {line_number}: JSON row must be an object")
            rows.append(payload)
    if not rows:
        raise ValueError(f"{path}: must contain at least one JSON object")
    return tuple(rows)


def _required_text(value: object, field: str, row_id: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{row_id}: {field} must be a non-empty string")
    return value.strip()


def _required_text_list(value: object, field: str, row_id: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{row_id}: {field} must be a string list")
    items = tuple(_required_text(item, field, row_id) for item in value)
    if len(set(items)) != len(items):
        raise ValueError(f"{row_id}: {field} must not contain duplicates")
    return items


def _require_fields(row: dict[str, object], required: frozenset[str], row_id: str) -> None:
    missing = required - row.keys()
    extra = row.keys() - required
    if missing:
        raise ValueError(f"{row_id}: missing fields: {', '.join(sorted(missing))}")
    if extra:
        raise ValueError(f"{row_id}: unexpected fields: {', '.join(sorted(extra))}")


def load_surface(query_path: Path, candidate_path: Path, qrel_path: Path) -> EvalSurface:
    query_rows = _read_jsonl(query_path)
    candidate_rows = _read_jsonl(candidate_path)
    qrel_rows = _read_jsonl(qrel_path)

    queries: list[EvalQuery] = []
    query_ids: set[str] = set()
    pools: set[str] = set()
    for index, row in enumerate(query_rows, 1):
        row_id = f"query row {index}"
        _require_fields(row, QUERY_FIELDS, row_id)
        query = EvalQuery(
            query_id=_required_text(row["query_id"], "query_id", row_id),
            pool_id=_required_text(row["pool_id"], "pool_id", row_id),
            primary_stratum=_required_text(row["primary_stratum"], "primary_stratum", row_id),
            secondary_strata=_required_text_list(row["secondary_strata"], "secondary_strata", row_id),
            proposition=_required_text(row["proposition"], "proposition", row_id),
        )
        if query.query_id in query_ids:
            raise ValueError(f"duplicate query_id: {query.query_id}")
        if query.pool_id in pools:
            raise ValueError(f"duplicate pool_id: {query.pool_id}")
        query_ids.add(query.query_id)
        pools.add(query.pool_id)
        queries.append(query)

    candidates: list[EvalCandidate] = []
    candidate_ids: set[str] = set()
    for index, row in enumerate(candidate_rows, 1):
        row_id = f"candidate row {index}"
        _require_fields(row, CANDIDATE_FIELDS, row_id)
        candidate = EvalCandidate(
            candidate_id=_required_text(row["candidate_id"], "candidate_id", row_id),
            pool_id=_required_text(row["pool_id"], "pool_id", row_id),
            proposition=_required_text(row["proposition"], "proposition", row_id),
        )
        if candidate.candidate_id in candidate_ids:
            raise ValueError(f"duplicate candidate_id: {candidate.candidate_id}")
        if candidate.pool_id not in pools:
            raise ValueError(f"{candidate.candidate_id}: unknown pool_id: {candidate.pool_id}")
        candidate_ids.add(candidate.candidate_id)
        candidates.append(candidate)

    query_by_id = {query.query_id: query for query in queries}
    candidate_by_id = {candidate.candidate_id: candidate for candidate in candidates}
    qrels: list[EvalJudgment] = []
    qrel_keys: set[tuple[str, str]] = set()
    for index, row in enumerate(qrel_rows, 1):
        row_id = f"qrel row {index}"
        _require_fields(row, QREL_FIELDS, row_id)
        query_id = _required_text(row["query_id"], "query_id", row_id)
        candidate_id = _required_text(row["candidate_id"], "candidate_id", row_id)
        if query_id not in query_by_id:
            raise ValueError(f"{row_id}: unknown query_id: {query_id}")
        if candidate_id not in candidate_by_id:
            raise ValueError(f"{row_id}: unknown candidate_id: {candidate_id}")
        if candidate_by_id[candidate_id].pool_id != query_by_id[query_id].pool_id:
            raise ValueError(f"{row_id}: qrel candidate is outside query pool")
        judgment_kind = _required_text(row["judgment"], "judgment", row_id)
        expected_class = _required_text(row["review_class"], "review_class", row_id)
        if judgment_kind not in JUDGMENT_KINDS:
            raise ValueError(f"{row_id}: unsupported judgment kind: {judgment_kind}")
        if judgment_kind == "USEFUL_CANDIDATE" and expected_class not in USEFUL_CLASSES:
            raise ValueError(f"{row_id}: useful judgment must use a useful review class")
        if judgment_kind == "HARD_NEGATIVE" and expected_class not in HARD_NEGATIVE_CLASSES:
            raise ValueError(f"{row_id}: hard negative must use a hard-negative review class")
        if judgment_kind == "NEUTRAL_DECOY" and expected_class != "NOT_APPLICABLE":
            raise ValueError(f"{row_id}: neutral decoy must use NOT_APPLICABLE class")
        key = (query_id, candidate_id)
        if key in qrel_keys:
            raise ValueError(f"duplicate qrel: {query_id}/{candidate_id}")
        qrel_keys.add(key)
        qrels.append(EvalJudgment(query_id, candidate_id, judgment_kind, expected_class))

    expected_keys = {
        (query.query_id, candidate.candidate_id)
        for query in queries
        for candidate in candidates
        if candidate.pool_id == query.pool_id
    }
    if qrel_keys != expected_keys:
        missing = sorted(expected_keys - qrel_keys)
        extra = sorted(qrel_keys - expected_keys)
        raise ValueError(f"qrel coverage must be complete; missing={missing!r} extra={extra!r}")
    return EvalSurface(tuple(queries), tuple(candidates), tuple(qrels))


def validate_frozen_v2_contract(surface: EvalSurface) -> None:
    if len(surface.queries) != 24 or len(surface.candidates) != 144 or len(surface.qrels) != 144:
        raise ValueError("v2 surface must contain 24 queries, 144 candidates and 144 qrels")
    strata: dict[str, int] = {}
    candidate_by_pool: dict[str, list[EvalCandidate]] = {}
    qrels_by_query: dict[str, list[EvalJudgment]] = {}
    for query in surface.queries:
        strata[query.primary_stratum] = strata.get(query.primary_stratum, 0) + 1
    for candidate in surface.candidates:
        candidate_by_pool.setdefault(candidate.pool_id, []).append(candidate)
    for judgment in surface.qrels:
        qrels_by_query.setdefault(judgment.query_id, []).append(judgment)
    if len(strata) != 12 or set(strata.values()) != {2}:
        raise ValueError("v2 surface must contain exactly 12 primary strata with two queries each")
    for query in surface.queries:
        if len(candidate_by_pool.get(query.pool_id, ())) != 6:
            raise ValueError(f"{query.query_id}: pool must contain exactly six candidates")
        judgments = qrels_by_query[query.query_id]
        kinds = [judgment.judgment_kind for judgment in judgments]
        if kinds.count("USEFUL_CANDIDATE") != 2 or kinds.count("HARD_NEGATIVE") != 2 or kinds.count("NEUTRAL_DECOY") != 2:
            raise ValueError(f"{query.query_id}: qrels must contain 2 useful, 2 hard-negative and 2 neutral judgments")


def _record(identifier: str, proposition: str) -> ReaderLexicalRecord:
    return ReaderLexicalRecord(
        session_id=f"eval-v2-session-{identifier}",
        candidate_id=identifier,
        document_id=f"eval-v2-doc-{identifier}",
        source_uri=f"synthetic://reader-eval-v2/{identifier}",
        source_sha256=hashlib.sha256(proposition.encode("utf-8")).hexdigest(),
        proposition=proposition,
    )


def run_rc9_control(surface: EvalSurface, *, k: int = DEFAULT_K) -> dict[str, object]:
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    candidates_by_pool: dict[str, list[EvalCandidate]] = {}
    judgments = {(item.query_id, item.candidate_id): item for item in surface.qrels}
    for candidate in surface.candidates:
        candidates_by_pool.setdefault(candidate.pool_id, []).append(candidate)

    retained_useful_ids: list[str] = []
    missed_useful_ids: list[str] = []
    stratum_acc: dict[str, dict[str, int]] = {}
    useful_total = useful_hits = hard_total = hard_hits = neutral_hits = returned_total = 0
    reciprocal_rank_sum = 0.0
    any_useful_queries = all_useful_queries = 0

    for query in surface.queries:
        pool = candidates_by_pool[query.pool_id]
        index = ReaderLexicalIndex(_record(item.candidate_id, item.proposition) for item in pool)
        query_record = _record(query.query_id, query.proposition)
        matches = index.discover(query_record, k=k)
        useful_in_pool = sum(
            judgment.judgment_kind == "USEFUL_CANDIDATE" for judgment in surface.qrels if judgment.query_id == query.query_id
        )
        hard_in_pool = sum(
            judgment.judgment_kind == "HARD_NEGATIVE" for judgment in surface.qrels if judgment.query_id == query.query_id
        )
        useful_ranks: list[int] = []
        query_useful_hits = query_hard_hits = query_neutral_hits = 0
        for match in matches:
            judgment = judgments[(query.query_id, match.candidate_id)]
            if judgment.judgment_kind == "USEFUL_CANDIDATE":
                query_useful_hits += 1
                useful_ranks.append(match.rank)
            elif judgment.judgment_kind == "HARD_NEGATIVE":
                query_hard_hits += 1
            else:
                query_neutral_hits += 1
        first_useful_rank = min(useful_ranks) if useful_ranks else None
        reciprocal_rank_sum += 1.0 / first_useful_rank if first_useful_rank else 0.0
        any_useful_queries += int(query_useful_hits > 0)
        all_useful_queries += int(query_useful_hits == useful_in_pool)
        useful_total += useful_in_pool
        useful_hits += query_useful_hits
        hard_total += hard_in_pool
        hard_hits += query_hard_hits
        neutral_hits += query_neutral_hits
        returned_total += len(matches)

        acc = stratum_acc.setdefault(
            query.primary_stratum,
            {"queries": 0, "useful_total": 0, "useful_hits": 0, "hard_negative_total": 0, "hard_negative_hits": 0, "returned": 0},
        )
        acc["queries"] += 1
        acc["useful_total"] += useful_in_pool
        acc["useful_hits"] += query_useful_hits
        acc["hard_negative_total"] += hard_in_pool
        acc["hard_negative_hits"] += query_hard_hits
        acc["returned"] += len(matches)

        retrieved_ids = {match.candidate_id for match in matches}
        for judgment in surface.qrels:
            if judgment.query_id != query.query_id or judgment.judgment_kind != "USEFUL_CANDIDATE":
                continue
            if judgment.candidate_id in retrieved_ids:
                retained_useful_ids.append(judgment.candidate_id)
            else:
                missed_useful_ids.append(judgment.candidate_id)

    query_count = len(surface.queries)
    stratum_metrics: dict[str, dict[str, object]] = {}
    for stratum, acc in sorted(stratum_acc.items()):
        stratum_metrics[stratum] = {
            **acc,
            "useful_recall_at_k": round(acc["useful_hits"] / acc["useful_total"], 6),
            "hard_negative_hit_rate_at_k": round(acc["hard_negative_hits"] / acc["hard_negative_total"], 6),
            "judged_precision_at_k": round(acc["useful_hits"] / acc["returned"], 6) if acc["returned"] else 0.0,
        }

    return {
        "benchmark": "reader_retrieval_eval_v2_rc9_control",
        "surface_version": 2,
        "method": RETRIEVAL_METHOD,
        "k": k,
        "query_count": query_count,
        "candidate_count": len(surface.candidates),
        "qrel_count": len(surface.qrels),
        "judgment_coverage": 1.0,
        "metrics": {
            "useful_total": useful_total,
            "useful_hits": useful_hits,
            "useful_recall_at_k": round(useful_hits / useful_total, 6),
            "returned_candidates": returned_total,
            "judged_precision_at_k": round(useful_hits / returned_total, 6),
            "mrr": round(reciprocal_rank_sum / query_count, 6),
            "hard_negative_total": hard_total,
            "hard_negative_hits": hard_hits,
            "hard_negative_hit_rate_at_k": round(hard_hits / hard_total, 6),
            "neutral_decoy_hits": neutral_hits,
            "any_useful_query_rate_at_k": round(any_useful_queries / query_count, 6),
            "all_useful_query_rate_at_k": round(all_useful_queries / query_count, 6),
        },
        "strata": stratum_metrics,
        "work_bound": {"query_pools": query_count, "index_records_total": len(surface.candidates), "max_record_comparisons": len(surface.candidates), "storage": "in_memory", "network_calls": 0, "mandatory_third_party_dependencies": 0},
        "metric_scope": (
            "Every candidate in every six-candidate query pool is explicitly judged. Recall@K counts useful qrels; "
            "judged Precision@K uses actually returned, explicitly judged candidates as its denominator; MRR uses "
            "the first useful candidate; hard-negative rate counts explicitly labeled SAME_TOPIC/MERELY_SIMILAR "
            "traps. These are retrieval measurements only, not identity, evidence, truth or Canon adjudication."
        ),
        "retained_useful_candidate_ids": sorted(retained_useful_ids),
        "missed_useful_candidate_ids": sorted(missed_useful_ids),
    }


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest(manifest_path: Path, query_path: Path, candidate_path: Path, qrel_path: Path) -> dict[str, object]:
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("manifest must be a JSON object")
    files = payload.get("surface_files")
    if not isinstance(files, dict):
        raise ValueError("manifest surface_files must be an object")
    for label, path in (("queries", query_path), ("candidates", candidate_path), ("qrels", qrel_path)):
        entry = files.get(label)
        if not isinstance(entry, dict) or entry.get("sha256") != sha256_file(path):
            raise ValueError(f"manifest hash mismatch for {label}")
    return payload


def human_summary(result: dict[str, object]) -> str:
    metrics = result["metrics"]
    assert isinstance(metrics, dict)
    return "\n".join(
        (
            "Reader Retrieval Evaluation Surface v2 — RC-9 lexical control",
            f"method: {result['method']}",
            f"queries/candidates/qrels: {result['query_count']}/{result['candidate_count']}/{result['qrel_count']}",
            f"Useful Recall@{result['k']}: {metrics['useful_recall_at_k']:.6f}",
            f"Judged Precision@{result['k']}: {metrics['judged_precision_at_k']:.6f}",
            f"MRR: {metrics['mrr']:.6f}",
            f"Hard-negative hit rate@{result['k']}: {metrics['hard_negative_hit_rate_at_k']:.6f}",
            "Boundary: fully judged retrieval evidence only; comparison pass is not runtime authorization.",
        )
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--qrels", type=Path, default=DEFAULT_QRELS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--k", type=int, default=DEFAULT_K)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--json-only", action="store_true")
    return parser


def main() -> int:
    args = _parser().parse_args()
    verify_manifest(args.manifest, args.queries, args.candidates, args.qrels)
    surface = load_surface(args.queries, args.candidates, args.qrels)
    validate_frozen_v2_contract(surface)
    result = run_rc9_control(surface, k=args.k)
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
