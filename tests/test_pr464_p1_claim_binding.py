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


def test_matching_l1_l3_claim_and_evidence_remains_answerable():
    """CASE A: matching L1/L3 C1 with evidence SHA(C1) retains public authority."""
    claim = "P1 R464 matching claim remains answerable"
    fact_id = "p1-r464-matching"
    ingest(
        claim,
        fact_id=fact_id,
        source="file://p1-r464-matching.txt",
        confidence=0.91,
        source_status="EXTERNAL",
    )
    evidence.attach_evidence(
        fact_id,
        "file://p1-r464-matching.txt",
        source_text="matching source text",
        span_start=0,
        span_end=6,
    )

    result = query_pipeline.query(claim)

    assert evidence.has_valid_evidence_for_grounding(
        fact_id, expected_claim=claim
    ) is True
    assert result["answer"] is not None
    assert result.get("reason_code") is None
    assert [fact["fact_id"] for fact in result["facts"]] == [fact_id]


def test_one_matching_support_remains_answerable_after_other_span_removed():
    """CASE D: one valid exact-claim span remains sufficient after one disappears."""
    claim = "P1 R464 one remaining exact claim support"
    fact_id = "p1-r464-one-support-remains"
    ingest(
        claim,
        fact_id=fact_id,
        source="file://p1-r464-one-remains.txt",
        confidence=0.91,
        source_status="EXTERNAL",
    )
    removed = evidence.attach_evidence(
        fact_id,
        "file://p1-r464-one-remains-a.txt",
        source_text="first support text",
        span_start=0,
        span_end=6,
    )
    retained = evidence.attach_evidence(
        fact_id,
        "file://p1-r464-one-remains-b.txt",
        source_text="second support text",
        span_start=0,
        span_end=6,
    )
    with memory._db() as conn:
        conn.execute(
            "DELETE FROM evidence_spans WHERE evidence_id = ?",
            (removed["evidence_id"],),
        )

    eligible = evidence.valid_evidence_for_grounding(
        fact_id, expected_claim=claim
    )
    result = query_pipeline.query(claim)

    assert [span["evidence_id"] for span in eligible] == [retained["evidence_id"]]
    assert result["answer"] is not None
    assert [fact["fact_id"] for fact in result["facts"]] == [fact_id]


def test_mixed_retrieval_keeps_exactly_bound_fact_and_filters_split_claim_fact():
    """CASE E: a C1-bound F2 cannot leak alongside valid exact-bound F1."""
    common = "P1 R464 mixed retrieval shared anchor"
    valid_claim = f"{common} valid-f1"
    stale_l1_claim = f"{common} original-f2"
    resolved_l3_claim = f"{common} replacement-f2"
    valid_id = "p1-r464-mixed-valid"
    split_id = "p1-r464-mixed-split"

    ingest(
        valid_claim,
        fact_id=valid_id,
        source="file://p1-r464-mixed-valid.txt",
        confidence=0.91,
        source_status="EXTERNAL",
    )
    evidence.attach_evidence(
        valid_id,
        "file://p1-r464-mixed-valid.txt",
        source_text="valid f1 source",
        span_start=0,
        span_end=6,
    )

    ingest(
        stale_l1_claim,
        fact_id=split_id,
        source="file://p1-r464-mixed-split.txt",
        confidence=0.91,
        source_status="EXTERNAL",
    )
    evidence.attach_evidence(
        split_id,
        "file://p1-r464-mixed-split.txt",
        source_text="C1-only f2 source",
        span_start=0,
        span_end=6,
    )
    graph = get_l3_graph()
    split_l3 = graph.get_fact(split_id)
    assert split_l3 is not None
    graph.merge_fact({**split_l3, "claim": resolved_l3_claim})

    result = query_pipeline.query(common)
    returned_ids = [fact["fact_id"] for fact in result["facts"]]

    assert evidence.has_valid_evidence_for_grounding(
        split_id, expected_claim=resolved_l3_claim
    ) is False
    assert result["answer"] is not None
    assert valid_id in returned_ids
    assert split_id not in returned_ids
    assert all(fact["claim"] != resolved_l3_claim for fact in result["facts"])


def test_explicit_expected_claim_never_falls_back_to_stale_l1_claim():
    """The optional compatibility argument is fail-closed when exact claim is absent/mismatched."""
    l1, _l3, snapshot, _span = _create_split_claim_state()

    assert l1["claim"] == C1
    assert snapshot.claim == C2
    assert evidence.has_valid_evidence_for_grounding(FACT_ID) is True
    assert evidence.has_valid_evidence_for_grounding(
        FACT_ID, expected_claim=C2
    ) is False
    assert evidence.has_valid_evidence_for_grounding(
        FACT_ID, expected_claim=None
    ) is False
