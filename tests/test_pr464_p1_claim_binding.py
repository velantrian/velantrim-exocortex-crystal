"""P1-R464-01 exact public-path regression: evidence must bind resolved L3 claim."""

import json

from core import evidence, memory, query_pipeline
from core.evidence import sha256
from core.ingest import ingest
from core.l3_graph import get_l3_graph
from core.trust_snapshot import TrustSnapshot


C1 = "P1 R464 original L1 claim about cobalt kestrels"
C2 = "P1 R464 canonical L3 claim about quartz badgers"
FACT_ID = "p1-r464-claim-binding"


def _create_split_claim_state():
    admitted = ingest(
        C1,
        fact_id=FACT_ID,
        source="file://p1-r464-c1.txt",
        confidence=0.91,
        source_status="EXTERNAL",
    )["fact"]
    assert admitted["claim"] == C1
    assert admitted["epistemic_state"] == "Validated"
    assert admitted["truth_status"] == "VERIFIED"

    evidence.attach_evidence(
        FACT_ID,
        "file://p1-r464-c1.txt",
        source_text="P1 R464 evidence text for C1 only",
        span_start=0,
        span_end=6,
    )

    graph = get_l3_graph()
    l3_before = graph.get_fact(FACT_ID)
    assert l3_before is not None
    graph.merge_fact({**l3_before, "claim": C2})

    l1 = memory.get_fact(FACT_ID)
    l3 = graph.get_fact(FACT_ID)
    assert l1 is not None and l3 is not None
    snapshot = TrustSnapshot.from_records(fact_id=FACT_ID, l1=l1, l3=l3)
    span = evidence.evidence_for(FACT_ID)[0]
    return l1, l3, snapshot, span


def test_public_query_requires_evidence_bound_to_exact_resolved_claim(capsys):
    """C2 must not receive public answer authority from evidence sealed to C1."""
    l1, l3, snapshot, span = _create_split_claim_state()
    result = query_pipeline.query(C2)

    observations = {
        "l1_claim": l1["claim"],
        "l3_claim": l3["claim"],
        "resolved_claim": snapshot.claim,
        "evidence_claim_sha256": span["claim_sha256"],
        "sha256_c1": sha256(C1),
        "sha256_c2": sha256(C2),
        "predicate_using_l1_claim": evidence.has_valid_evidence_for_grounding(FACT_ID),
        "public_query_answer": result["answer"],
        "public_query_reason_code": result.get("reason_code"),
        "public_query_facts": result["facts"],
        "public_query_trace": result["trace"],
    }
    print(json.dumps(observations, sort_keys=True, default=str))

    assert l1["claim"] == C1
    assert l3["claim"] == C2
    assert snapshot.claim == C2
    assert span["claim_sha256"] == sha256(C1)
    assert span["claim_sha256"] != sha256(C2)
    assert evidence.has_valid_evidence_for_grounding(FACT_ID) is True

    assert result["answer"] is None
    assert result["reason_code"] == "insufficient_grounding_missing_verified_evidence"
