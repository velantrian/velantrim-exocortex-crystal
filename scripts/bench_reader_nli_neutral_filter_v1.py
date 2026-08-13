#!/usr/bin/env python3
"""Offline bidirectional NLI neutral-filter evaluation over frozen Reader comparator rankings."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import resource
import sys
import time
from typing import Any

SEM_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
SEM_REV = "e8f8c211226b894fcb81acc59f3b34ba3efd5f42"
SEM_SHA = "eaa086f0ffee582aeb45b36e34cdd1fe2d6de2bef61f8a559a1bbc9bd955917b"
NLI_MODEL = "MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli"
NLI_REV = "0a71e92a985b6e1ad1828cf67ce9c459639c1dca"
NLI_SHA = "91b323ccf247ec1e3b5925d566230bae7c52de8147e6062b42e250089a3fc80b"
DEPS_SHA = "9a2902d1b7d5b7ca5b5105be46d1a1151fddf683e0ed67b078a09c948b3f4bd9"
LABELS = {0: "entailment", 1: "neutral", 2: "contradiction"}
POSITIVE = {
    "SAME_PROPOSITION_CANDIDATE",
    "PARAPHRASE_CANDIDATE",
    "RELATED_CLAIM",
    "POSSIBLE_CONTRADICTION",
}
RECOVERED = {
    "v2-c-0a8ace12cae2f46b",
    "v2-c-276b3efe332a9a8e",
    "v2-c-2dbbcb4d5fd9024b",
    "v2-c-33a2bceca3914a17",
    "v2-c-bd24e316a3f799aa",
    "v2-c-ea4d49c11eccb857",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: object required")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{n}: object required")
        rows.append(value)
    if not rows:
        raise ValueError(f"{path}: rows required")
    return rows


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_file(path: Path, expected: str, name: str) -> None:
    if not path.is_file():
        raise RuntimeError(f"missing {name}: {path}")
    actual = sha256(path)
    if actual != expected:
        raise RuntimeError(f"{name} sha256 mismatch: expected {expected}, got {actual}")


def load_models(sem_path: Path, nli_path: Path) -> tuple[Any, Any, Any]:
    if os.environ.get("HF_HUB_OFFLINE") != "1" or os.environ.get("TRANSFORMERS_OFFLINE") != "1":
        raise RuntimeError("HF_HUB_OFFLINE=1 and TRANSFORMERS_OFFLINE=1 required")
    check_file(sem_path / "model.safetensors", SEM_SHA, "semantic weights")
    check_file(nli_path / "model.safetensors", NLI_SHA, "NLI weights")
    if importlib.metadata.version("sentence-transformers") != "5.7.0":
        raise RuntimeError("sentence-transformers version mismatch")
    if importlib.metadata.version("transformers") != "5.14.1":
        raise RuntimeError("transformers version mismatch")
    if importlib.metadata.version("torch") != "2.13.0":
        raise RuntimeError("torch version mismatch")

    from sentence_transformers import SentenceTransformer
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    semantic = SentenceTransformer(str(sem_path), device="cpu", local_files_only=True)
    tok = AutoTokenizer.from_pretrained(str(nli_path), local_files_only=True)
    nli = AutoModelForSequenceClassification.from_pretrained(
        str(nli_path), local_files_only=True, use_safetensors=True
    )
    nli.to("cpu")
    nli.eval()
    actual_labels = {int(k): str(v).lower() for k, v in nli.config.id2label.items()}
    if actual_labels != LABELS:
        raise RuntimeError(f"NLI label mapping mismatch: {actual_labels}")
    return semantic, tok, nli


def semantic_rank(model: Any, query: str, candidates: list[tuple[str, str]], k: int) -> list[dict[str, Any]]:
    vectors = model.encode(
        [query, *(text for _, text in candidates)],
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    qv = vectors[0]
    scored = []
    for (cid, text), vec in zip(candidates, vectors[1:]):
        score = float(qv @ vec)
        if not math.isfinite(score):
            raise RuntimeError(f"non-finite semantic score for {cid}")
        scored.append((cid, text, score))
    scored.sort(key=lambda x: (-x[2], x[0]))
    return [
        {"candidate_id": cid, "text": text, "semantic_rank": i, "semantic_score": round(score, 9)}
        for i, (cid, text, score) in enumerate(scored[:k], 1)
    ]


def infer(tok: Any, model: Any, premise: str, hypothesis: str) -> dict[str, Any]:
    import torch

    batch = tok(
        premise,
        hypothesis,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=False,
    )
    with torch.no_grad():
        logits = model(**batch).logits[0]
        probs = torch.softmax(logits, dim=-1).cpu().tolist()
    idx = int(logits.argmax().item())
    return {
        "label": LABELS[idx],
        "probabilities": {LABELS[i]: round(float(probs[i]), 9) for i in range(3)},
    }


def apply_filter(tok: Any, nli: Any, query: str, ranked: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    retained_rank = 0
    for row in ranked:
        forward = infer(tok, nli, query, str(row["text"]))
        reverse = infer(tok, nli, str(row["text"]), query)
        filtered = forward["label"] == "neutral" and reverse["label"] == "neutral"
        if not filtered:
            retained_rank += 1
        rows.append(
            {
                "candidate_id": row["candidate_id"],
                "semantic_rank": row["semantic_rank"],
                "semantic_score": row["semantic_score"],
                "forward": forward,
                "reverse": reverse,
                "filtered": filtered,
                "retained_rank": None if filtered else retained_rank,
            }
        )
    return rows


def run_historical(semantic: Any, tok: Any, nli: Any, path: Path, k: int) -> dict[str, Any]:
    cases = load_jsonl(path)
    pool = [(f"{c['case_id']}-right", str(c["right"])) for c in cases]
    positive_total = hard_total = positive_hits = hard_hits = 0
    rr = []
    hit_ids = []
    details = []
    for case in cases:
        ranked = semantic_rank(semantic, str(case["left"]), pool, k)
        filtered = apply_filter(tok, nli, str(case["left"]), ranked)
        paired = f"{case['case_id']}-right"
        kept = next((r for r in filtered if r["candidate_id"] == paired and not r["filtered"]), None)
        useful = str(case["expected_review_class"]) in POSITIVE
        if useful:
            positive_total += 1
            if kept:
                positive_hits += 1
                hit_ids.append(str(case["case_id"]))
                rr.append(1.0 / int(kept["retained_rank"]))
            else:
                rr.append(0.0)
        else:
            hard_total += 1
            if kept:
                hard_hits += 1
        paired_row = next((r for r in filtered if r["candidate_id"] == paired), None)
        details.append(
            {
                "case_id": case["case_id"],
                "stratum": case["stratum"],
                "expected_review_class": case["expected_review_class"],
                "paired": paired_row,
            }
        )
    return {
        "positive_hit_case_ids": sorted(hit_ids),
        "metrics": {
            "positive_hits": positive_hits,
            "positive_total": positive_total,
            "recall_at_5": round(positive_hits / positive_total, 6),
            "mrr": round(sum(rr) / positive_total, 6),
            "hard_negative_hits": hard_hits,
            "hard_negative_total": hard_total,
            "hard_negative_rate_at_5": round(hard_hits / hard_total, 6),
        },
        "cases": details,
    }


def run_v2(
    semantic: Any,
    tok: Any,
    nli: Any,
    queries_path: Path,
    candidates_path: Path,
    qrels_path: Path,
    k: int,
) -> dict[str, Any]:
    queries = load_jsonl(queries_path)
    candidates = load_jsonl(candidates_path)
    qrels = load_jsonl(qrels_path)
    pools: dict[str, list[tuple[str, str]]] = {}
    for c in candidates:
        pools.setdefault(str(c["pool_id"]), []).append((str(c["candidate_id"]), str(c["proposition"])))
    judgments = {(str(r["query_id"]), str(r["candidate_id"])): str(r["judgment"]) for r in qrels}
    qrels_q: dict[str, list[dict[str, Any]]] = {}
    for r in qrels:
        qrels_q.setdefault(str(r["query_id"]), []).append(r)

    all_useful_ids = {str(r["candidate_id"]) for r in qrels if r["judgment"] == "USEFUL_CANDIDATE"}
    all_hard_ids = {str(r["candidate_id"]) for r in qrels if r["judgment"] == "HARD_NEGATIVE"}
    useful_hits: set[str] = set()
    hard_hits: set[str] = set()
    neutral_hits: set[str] = set()
    rr = []
    details = []
    strata: dict[str, dict[str, int]] = {}
    label_counts: dict[str, dict[str, int]] = {}

    for q in queries:
        qid, pool_id, stratum = str(q["query_id"]), str(q["pool_id"]), str(q["primary_stratum"])
        ranked = semantic_rank(semantic, str(q["proposition"]), pools[pool_id], k)
        filtered = apply_filter(tok, nli, str(q["proposition"]), ranked)
        kept = [r for r in filtered if not r["filtered"]]
        query_useful, query_hard, query_neutral = [], [], []
        first_useful_rank = None
        for row in filtered:
            cid = str(row["candidate_id"])
            judgment = judgments[(qid, cid)]
            row["judgment"] = judgment
            pair = f"{row['forward']['label']}|{row['reverse']['label']}"
            bucket = label_counts.setdefault(judgment, {})
            bucket[pair] = bucket.get(pair, 0) + 1
            if row["filtered"]:
                continue
            if judgment == "USEFUL_CANDIDATE":
                useful_hits.add(cid)
                query_useful.append(cid)
                if first_useful_rank is None:
                    first_useful_rank = int(row["retained_rank"])
            elif judgment == "HARD_NEGATIVE":
                hard_hits.add(cid)
                query_hard.append(cid)
            else:
                neutral_hits.add(cid)
                query_neutral.append(cid)
        rr.append(1.0 / first_useful_rank if first_useful_rank else 0.0)

        rows = qrels_q[qid]
        useful_total = sum(r["judgment"] == "USEFUL_CANDIDATE" for r in rows)
        hard_total = sum(r["judgment"] == "HARD_NEGATIVE" for r in rows)
        s = strata.setdefault(
            stratum,
            {"queries": 0, "useful_hits": 0, "useful_total": 0, "hard_negative_hits": 0, "hard_negative_total": 0},
        )
        s["queries"] += 1
        s["useful_hits"] += len(query_useful)
        s["useful_total"] += useful_total
        s["hard_negative_hits"] += len(query_hard)
        s["hard_negative_total"] += hard_total
        details.append(
            {
                "query_id": qid,
                "primary_stratum": stratum,
                "semantic_candidate_ids": [r["candidate_id"] for r in filtered],
                "retained_candidate_ids": [r["candidate_id"] for r in kept],
                "useful_hits": query_useful,
                "hard_negative_hits": query_hard,
                "neutral_decoy_hits": query_neutral,
                "candidates": filtered,
            }
        )

    strata_out = {}
    for name, s in sorted(strata.items()):
        strata_out[name] = {
            **s,
            "useful_recall_at_5": round(s["useful_hits"] / s["useful_total"], 6),
            "hard_negative_rate_at_5": round(s["hard_negative_hits"] / s["hard_negative_total"], 6),
        }
    returned = sum(len(r["retained_candidate_ids"]) for r in details)
    return {
        "useful_hit_candidate_ids": sorted(useful_hits),
        "hard_negative_hit_candidate_ids": sorted(hard_hits),
        "metrics": {
            "useful_hits": len(useful_hits),
            "useful_total": len(all_useful_ids),
            "useful_recall_at_5": round(len(useful_hits) / len(all_useful_ids), 6),
            "precision_at_5": round(len(useful_hits) / (len(queries) * k), 6),
            "judged_precision_over_returned": round(len(useful_hits) / returned, 6) if returned else 0.0,
            "mrr": round(sum(rr) / len(queries), 6),
            "hard_negative_hits": len(hard_hits),
            "hard_negative_total": len(all_hard_ids),
            "hard_negative_rate_at_5": round(len(hard_hits) / len(all_hard_ids), 6),
            "neutral_decoy_hits": len(neutral_hits),
            "returned_candidates": returned,
            "any_useful_query_rate_at_5": round(sum(bool(r["useful_hits"]) for r in details) / len(queries), 6),
            "all_useful_query_rate_at_5": round(
                sum(
                    len(r["useful_hits"])
                    == sum(x["judgment"] == "USEFUL_CANDIDATE" for x in qrels_q[r["query_id"]])
                    for r in details
                )
                / len(queries),
                6,
            ),
            "judgment_coverage": 1.0,
        },
        "per_stratum": strata_out,
        "nli_directional_label_pairs_by_judgment": label_counts,
        "queries": details,
    }


def fingerprint(historical: dict[str, Any], v2: dict[str, Any]) -> str:
    payload = {
        "historical": [
            (
                r["case_id"],
                r["paired"]["filtered"] if r["paired"] else None,
                r["paired"]["forward"]["label"] if r["paired"] else None,
                r["paired"]["reverse"]["label"] if r["paired"] else None,
            )
            for r in historical["cases"]
        ],
        "v2": [
            (
                r["query_id"],
                r["retained_candidate_ids"],
                [(x["candidate_id"], x["forward"]["label"], x["reverse"]["label"]) for x in r["candidates"]],
            )
            for r in v2["queries"]
        ],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def gates(historical: dict[str, Any], v2: dict[str, Any], rc10_path: Path, v2_gate_path: Path) -> dict[str, Any]:
    hgate = load_json(rc10_path)["future_comparison_gate"]
    gate = load_json(v2_gate_path)["future_comparator_gate"]
    hm = historical["metrics"]
    vm = v2["metrics"]
    historical_checks = {
        "positive_hits": hm["positive_hits"] >= hgate["required_positive_hits"],
        "recall": hm["recall_at_5"] >= hgate["required_recall_at_k"],
        "required_cases": set(hgate["required_recover_case_ids"]).issubset(historical["positive_hit_case_ids"]),
        "mrr": hm["mrr"] >= hgate["mrr_floor"],
        "hard_negative_hits": hm["hard_negative_hits"] <= hgate["max_hard_negative_hits"],
        "hard_negative_rate": hm["hard_negative_rate_at_5"] <= hgate["max_paired_hard_negative_rate_at_k"],
    }
    recovered = set(v2["useful_hit_candidate_ids"]) & set(gate["rc9_v2_miss_candidate_ids"])
    retained = set(gate["required_retain_rc9_useful_candidate_ids"]).issubset(v2["useful_hit_candidate_ids"])
    v2_checks = {
        "retain_rc9_useful": retained,
        "recover_required_misses": len(recovered) >= gate["required_recover_at_least_n_rc9_v2_misses"],
        "useful_hits": vm["useful_hits"] >= gate["required_useful_hits_min"],
        "useful_recall": vm["useful_recall_at_5"] >= gate["required_useful_recall_at_k_min"],
        "mrr": vm["mrr"] >= gate["mrr_floor"],
        "hard_negative_hits": vm["hard_negative_hits"] <= gate["max_hard_negative_hits"],
        "hard_negative_rate": vm["hard_negative_rate_at_5"] <= gate["max_hard_negative_hit_rate_at_k"],
        "any_useful_query_rate": vm["any_useful_query_rate_at_5"] >= gate["min_any_useful_query_rate_at_k"],
        "all_useful_query_rate": vm["all_useful_query_rate_at_5"] >= gate["min_all_useful_query_rate_at_k"],
        "per_stratum_useful": all(
            s["useful_recall_at_5"] >= gate["min_per_stratum_useful_recall_at_k"] for s in v2["per_stratum"].values()
        ),
        "per_stratum_hard_negative": all(
            s["hard_negative_rate_at_5"] <= gate["max_per_stratum_hard_negative_hit_rate_at_k"]
            for s in v2["per_stratum"].values()
        ),
    }
    no_loss = {
        "useful_hits_48": vm["useful_hits"] == 48,
        "recall_1": vm["useful_recall_at_5"] == 1.0,
        "all_useful_queries_1": vm["all_useful_query_rate_at_5"] == 1.0,
        "mrr_1": vm["mrr"] == 1.0,
        "all_six_recovered": RECOVERED.issubset(v2["useful_hit_candidate_ids"]),
    }
    return {
        "historical": {"checks": historical_checks, "pass": all(historical_checks.values())},
        "v2": {"checks": v2_checks, "pass": all(v2_checks.values()), "recovered_rc9_misses": sorted(recovered)},
        "no_recall_loss": {"checks": no_loss, "pass": all(no_loss.values())},
    }


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--semantic-model-path", type=Path, required=True)
    p.add_argument("--nli-model-path", type=Path, required=True)
    p.add_argument("--dependencies", type=Path, required=True)
    p.add_argument("--json-out", type=Path, required=True)
    p.add_argument("--k", type=int, default=5)
    p.add_argument("--rc8-corpus", type=Path, default=Path("eval/reader_rc8_retrieval_adversarial.jsonl"))
    p.add_argument("--rc10-gate", type=Path, default=Path("eval/reader_rc10_retrieval_comparison_preregistration.json"))
    p.add_argument("--v2-queries", type=Path, default=Path("eval/reader_retrieval_eval_v2_queries.jsonl"))
    p.add_argument("--v2-candidates", type=Path, default=Path("eval/reader_retrieval_eval_v2_candidates.jsonl"))
    p.add_argument("--v2-qrels", type=Path, default=Path("eval/reader_retrieval_eval_v2_qrels.jsonl"))
    p.add_argument("--v2-gate", type=Path, default=Path("eval/reader_retrieval_eval_v2_future_comparator_gate.json"))
    return p


def main() -> int:
    args = parser().parse_args()
    if args.k != 5:
        raise RuntimeError("K is frozen at 5")
    check_file(args.dependencies, DEPS_SHA, "dependency freeze")
    started = time.perf_counter()
    rss_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    semantic, tok, nli = load_models(args.semantic_model_path, args.nli_model_path)
    h1 = run_historical(semantic, tok, nli, args.rc8_corpus, args.k)
    v1 = run_v2(semantic, tok, nli, args.v2_queries, args.v2_candidates, args.v2_qrels, args.k)
    f1 = fingerprint(h1, v1)
    h2 = run_historical(semantic, tok, nli, args.rc8_corpus, args.k)
    v2 = run_v2(semantic, tok, nli, args.v2_queries, args.v2_candidates, args.v2_qrels, args.k)
    f2 = fingerprint(h2, v2)
    repeatable = f1 == f2
    result_gates = gates(h1, v1, args.rc10_gate, args.v2_gate)
    authority_violations = 0
    overall = (
        result_gates["historical"]["pass"]
        and result_gates["v2"]["pass"]
        and result_gates["no_recall_loss"]["pass"]
        and repeatable
        and authority_violations == 0
    )
    result = {
        "schema_version": 1,
        "milestone": "reader_nli_neutral_filter_v1",
        "status": "QUALIFYING_RESULT_PASS" if overall else "QUALIFYING_RESULT_FAIL",
        "classification": "NLI_NEUTRAL_FILTER_GATE_PASSED_ARCHITECTURE_REVIEW_ONLY" if overall else "NLI_NEUTRAL_FILTER_GATE_FAILED",
        "identity": {
            "semantic_model": SEM_MODEL,
            "semantic_revision": SEM_REV,
            "semantic_safetensors_sha256": SEM_SHA,
            "nli_model": NLI_MODEL,
            "nli_revision": NLI_REV,
            "nli_safetensors_sha256": NLI_SHA,
            "nli_id2label": {str(k): v for k, v in LABELS.items()},
            "rule": "filter iff both directional argmax labels are neutral",
            "k": 5,
            "device": "cpu",
            "index": "NO_INDEX_EXACT_POOL_SCORING",
        },
        "execution": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "dependency_freeze_sha256": sha256(args.dependencies),
            "network_isolation_required_by_workflow": True,
            "hf_hub_offline": os.environ.get("HF_HUB_OFFLINE") == "1",
            "transformers_offline": os.environ.get("TRANSFORMERS_OFFLINE") == "1",
            "external_reader_source_text_transmission": False,
            "repeatability_fingerprint_first": f1,
            "repeatability_fingerprint_second": f2,
            "repeatable": repeatable,
            "wall_seconds_two_passes_including_load": round(time.perf_counter() - started, 6),
            "max_rss_before_kib": rss_before,
            "max_rss_after_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "production_slo": False,
        },
        "historical_rc10": h1,
        "evaluation_surface_v2": v1,
        "gates": result_gates,
        "authority": {
            "authority_violations": authority_violations,
            "nli_label_is_identity": False,
            "nli_label_is_adjudication": False,
            "filtering_is_epistemic_authority": False,
            "pass_is_runtime_authorization": False,
        },
        "overall_gate_pass": overall,
        "runtime_authorization": False,
    }
    args.json_out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(
        {
            "status": result["status"],
            "classification": result["classification"],
            "historical_metrics": h1["metrics"],
            "v2_metrics": v1["metrics"],
            "gates": result_gates,
            "repeatable": repeatable,
        },
        ensure_ascii=False,
        sort_keys=True,
    ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
