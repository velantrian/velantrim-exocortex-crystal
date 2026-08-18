from __future__ import annotations

import pytest
from concurrent.futures import ThreadPoolExecutor

from core import embedding, evidence, query_pipeline, reconcile
from core.l3_graph import MockL3Graph
from core.memory import get_fact, store_fact, transition_esm


def _stored_verified(fid="f1", claim="alpha beta", source="file://source.txt"):
    store_fact({
        "fact_id": fid, "claim": claim, "source": source, "confidence": 0.9,
        "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
    })
    transition_esm(fid, "Validated")
    return get_fact(fid)


def test_valid_grounding_evidence_requires_digest_claim_binding_and_location():
    fact = _stored_verified()
    evidence.attach_evidence(
        fact["fact_id"], "file://source.txt", source_text="source content",
        span_start=0, span_end=6,
    )
    assert evidence.has_valid_evidence_for_grounding(fact["fact_id"])


def test_bare_source_label_or_unsealed_evidence_is_not_grant_grounding():
    fact = _stored_verified("f2")
    evidence.attach_evidence(fact["fact_id"], "file://source.txt", span_start=0, span_end=6)
    assert not evidence.has_valid_evidence_for_grounding(fact["fact_id"])


def test_lineage_defaults_unknown_and_metrics_do_not_infer_independence():
    fact = _stored_verified("f3")
    evidence.attach_evidence(
        fact["fact_id"], "file://a", source_text="a", span_start=0, span_end=1,
    )
    evidence.attach_evidence(
        fact["fact_id"], "file://b", source_text="b", span_start=0, span_end=1,
        lineage_id="family:1", independence_class="SAME_LINEAGE",
        lineage_basis="IMPORTER_DECLARED",
    )
    rows = evidence.evidence_for(fact["fact_id"])
    assert rows[0]["independence_class"] == "UNKNOWN"
    metrics = evidence.lineage_metrics([fact["fact_id"]])
    assert metrics["unknown_lineage_rate"] == pytest.approx(0.5)
    assert metrics["independence_assertion_coverage"] == 0.0


def test_reinforce_same_lineage_is_idempotent():
    _stored_verified("f4")
    first = reconcile.reinforce("f4", lineage_id="family:one")
    after_first = get_fact("f4")["metadata"]["observations"]
    second = reconcile.reinforce("f4", lineage_id="family:one")
    assert second == first
    assert get_fact("f4")["metadata"]["observations"] == after_first
    assert get_fact("f4")["metadata"]["reinforcement_lineages"] == ["family:one"]


def test_zero_length_evidence_span_is_rejected():
    fact = _stored_verified("f2-zero")
    with pytest.raises(ValueError, match="span must be non-empty"):
        evidence.attach_evidence(
            fact["fact_id"], "file://source.txt", source_text="source content",
            span_start=0, span_end=0,
        )


def _independent_evidence(fact_id, lineage_id):
    return evidence.attach_evidence(
        fact_id,
        f"file://{fact_id}-{lineage_id}.txt",
        source_text=f"source for {fact_id} {lineage_id}",
        span_start=0, span_end=6,
        lineage_id=lineage_id,
        independence_class="INDEPENDENT_ASSERTED",
        lineage_basis="IMPORTER_DECLARED",
    )


def test_grant_profile_reinforce_requires_authoritative_evidence(monkeypatch):
    _stored_verified("f5")
    monkeypatch.setenv("VELANTRIM_RELEASE_PROFILE", "grant")
    with pytest.raises(ValueError, match="requires evidence_id"):
        reconcile.reinforce("f5")
    with pytest.raises(ValueError, match="derives lineage_id"):
        reconcile.reinforce("f5", lineage_id="caller-invented")


def test_grant_reinforce_derives_lineage_and_deduplicates_across_evidence_ids(monkeypatch):
    _stored_verified("f5-dedup")
    first_evidence = _independent_evidence("f5-dedup", "family:one")
    second_evidence = _independent_evidence("f5-dedup", "family:one")
    monkeypatch.setenv("VELANTRIM_RELEASE_PROFILE", "grant")

    first = reconcile.reinforce("f5-dedup", evidence_id=first_evidence["evidence_id"])
    after_first = get_fact("f5-dedup")["metadata"]["observations"]
    second = reconcile.reinforce("f5-dedup", evidence_id=second_evidence["evidence_id"])

    assert second == first
    assert get_fact("f5-dedup")["metadata"]["observations"] == after_first
    assert get_fact("f5-dedup")["metadata"]["reinforcement_lineages"] == ["family:one"]


def test_grant_reinforce_rejects_nonindependent_or_wrong_fact_evidence(monkeypatch):
    _stored_verified("f5-primary")
    _stored_verified("f5-other")
    same_lineage = evidence.attach_evidence(
        "f5-primary", "file://same-lineage.txt", source_text="same lineage",
        span_start=0, span_end=4, lineage_id="family:one",
        independence_class="SAME_LINEAGE", lineage_basis="IMPORTER_DECLARED",
    )
    wrong_fact = _independent_evidence("f5-other", "family:other")
    monkeypatch.setenv("VELANTRIM_RELEASE_PROFILE", "grant")

    with pytest.raises(ValueError, match="INDEPENDENT_ASSERTED"):
        reconcile.reinforce("f5-primary", evidence_id=same_lineage["evidence_id"])
    with pytest.raises(ValueError, match="valid evidence for this fact"):
        reconcile.reinforce("f5-primary", evidence_id=wrong_fact["evidence_id"])


def test_grant_same_lineage_concurrent_reinforcement_increments_once(monkeypatch):
    _stored_verified("f5-race")
    first = _independent_evidence("f5-race", "family:race")
    second = _independent_evidence("f5-race", "family:race")
    monkeypatch.setenv("VELANTRIM_RELEASE_PROFILE", "grant")
    evidence_ids = [first["evidence_id"], second["evidence_id"]] * 4

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda eid: reconcile.reinforce("f5-race", evidence_id=eid), evidence_ids))

    fact = get_fact("f5-race")
    assert fact["metadata"]["observations"] == 2
    assert fact["metadata"]["reinforcement_lineages"] == ["family:race"]


def test_grant_query_refuses_verified_fact_without_valid_span(monkeypatch):
    fact = _stored_verified("f6", claim="grant alpha")
    graph = MockL3Graph()
    monkeypatch.setenv("VELANTRIM_RELEASE_PROFILE", "grant")
    monkeypatch.setenv("VELANTRIM_EMBEDDER", "hashing")
    embedding.reset_embedder()
    node = dict(fact)
    node["truth_status"] = "VERIFIED"
    graph.merge_fact(node)
    graph.set_embedder_fingerprint(embedding.get_embedder().id)
    monkeypatch.setattr(query_pipeline, "get_l3_graph", lambda: graph)
    monkeypatch.setattr("core.pipeline.get_l3_graph", lambda: graph)

    result = query_pipeline.query("grant alpha")
    assert result["answer"] is None
    assert result["reason_code"] == "insufficient_grounding_missing_verified_evidence"

    evidence.attach_evidence(
        "f6", "file://grant.txt", source_text="grant source", span_start=0, span_end=5,
    )
    result = query_pipeline.query("grant alpha")
    assert result["answer"] is not None
