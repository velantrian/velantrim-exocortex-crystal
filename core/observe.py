# core/observe.py
# Velantrim ExoCortex — Memory Observability
#
# A window into L3 canonical memory: how many facts, in which ESM states, of which
# modalities and truth statuses, how many contradictions/obsolete, which
# have dropped in confidence (forgotten by SleepCycle), and edges by type. Supports the goal
# of transparent, source-grounded memory observability — the state of truth is visible in one call.

from collections import Counter
from typing import Dict, Any, List

from core.l3_graph import get_l3_graph

# Below this confidence we consider a fact "weak" (dropped during consolidation/decay).
_WEAK_CONFIDENCE = 0.2


def memory_report(*, weak_confidence: float = _WEAK_CONFIDENCE) -> Dict[str, Any]:
    """
    Summary of the L3 canonical graph. Deterministic, read-only.
    """
    graph = get_l3_graph()
    facts = graph.all_facts()

    by_state: Counter = Counter()
    by_claim_type: Counter = Counter()
    by_truth_status: Counter = Counter()
    edges_by_type: Counter = Counter()
    conf_sum = sig_sum = 0.0
    contradicted: List[str] = []
    deprecated: List[str] = []
    weak: List[str] = []

    for f in facts:
        state = f.get("epistemic_state", "Observed")
        by_state[state] += 1
        by_claim_type[f.get("claim_type", "WORLD_FACT")] += 1
        by_truth_status[f.get("truth_status", "UNVERIFIED")] += 1
        conf_sum += float(f.get("confidence", 0.0))
        sig_sum += float(f.get("significance", 0.0))
        if state == "Contradicted":
            contradicted.append(f["fact_id"])
        elif state == "Deprecated":
            deprecated.append(f["fact_id"])
        if float(f.get("confidence", 1.0)) < weak_confidence:
            weak.append(f["fact_id"])
        for edge in graph.get_edges(f["fact_id"]):
            edges_by_type[edge["rel_type"]] += 1

    n = len(facts)
    return {
        "total_facts": n,
        "by_epistemic_state": dict(by_state),
        "by_claim_type": dict(by_claim_type),
        "by_truth_status": dict(by_truth_status),
        "edges": {"total": sum(edges_by_type.values()), "by_type": dict(edges_by_type)},
        "avg_confidence": round(conf_sum / n, 4) if n else 0.0,
        "avg_significance": round(sig_sum / n, 4) if n else 0.0,
        "contradicted": sorted(contradicted),
        "deprecated": sorted(deprecated),
        "weak_confidence": sorted(weak),
    }


def format_report(report: Dict[str, Any]) -> str:
    """Human-readable rendering of the memory_report() report."""
    lines = [
        "MEMORY REPORT (L3 canonical graph)",
        f"  facts: {report['total_facts']}  "
        f"avg_confidence={report['avg_confidence']}  "
        f"avg_significance={report['avg_significance']}",
        f"  epistemic_state: {report['by_epistemic_state']}",
        f"  claim_type:      {report['by_claim_type']}",
        f"  truth_status:    {report['by_truth_status']}",
        f"  edges:           {report['edges']['total']} {report['edges']['by_type']}",
        f"  contradicted:    {len(report['contradicted'])}",
        f"  deprecated:      {len(report['deprecated'])}",
        f"  weak confidence: {len(report['weak_confidence'])}",
    ]
    return "\n".join(lines)
