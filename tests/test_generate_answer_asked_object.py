"""Object-applicability filter in generate_answer (asked_object)."""
from core.pipeline import generate_answer
from core.applicability import _facts_applicable_to_asked_object, _declared_primary_object


def _verified(fact_id, claim, **extra):
    fact = {
        "fact_id": fact_id,
        "claim": claim,
        "source": f"independent-source:{fact_id}",
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
        "truth_status": "VERIFIED",
        "epistemic_state": "Validated",
        "confidence": 1.0,
        "restricted": False,
    }
    fact.update(extra)
    return fact


def _pack(*facts, asked_object=None, query="q"):
    pack = {"facts": list(facts), "query": query, "total": len(facts)}
    if asked_object is not None:
        pack["asked_object"] = asked_object
    return pack


def test_no_asked_object_keeps_mismatched_primary_documents():
    r14 = _verified("e2", "R-14 closed", object="R-41", primary_object="R-14")
    r41 = _verified("e3", "R-41 pending", object="R-41", primary_object="R-41")
    out = generate_answer(_pack(r14, r41), trace=[])
    assert out["answer"] is not None
    assert "R-14 closed" in out["answer"]
    assert "R-41 pending" in out["answer"]
    assert {f["fact_id"] for f in out["facts"]} == {"e2", "e3"}


def test_asked_object_excludes_other_primary_document():
    r14 = _verified("e2", "status closed via R-14", object="R-41", primary_object="R-14")
    r41 = _verified("e3", "status pending review", object="R-41", primary_object="R-41")
    out = generate_answer(_pack(r14, r41, asked_object="R-41"), trace=[])
    assert out["answer"] == "status pending review"
    assert [f["fact_id"] for f in out["facts"]] == ["e3"]
    assert "closed" not in out["answer"]


def test_wrapper_attribution_does_not_override_primary_object():
    trap = _verified(
        "ac07-e2",
        "ready",
        object="L",
        primary_object="L2",
    )
    assert _declared_primary_object(trap) == "L2"
    kept = _facts_applicable_to_asked_object([trap], "L")
    assert kept == []


def test_missing_object_belonging_is_a_gap():
    legacy = _verified("old", "legacy claim stands")
    out = generate_answer(_pack(legacy, asked_object="L"), trace=[])
    assert out["answer"] is None
    assert "object belonging not established" in out["error"]


def test_l2_excluded_but_old_l_card_remains():
    old_l = _verified("e1", "L in progress", object="L", primary_object="L")
    l2 = _verified("e2", "ready", object="L", primary_object="L2")
    summary = _verified("e3", "repeats readiness", object="L", primary_object="L2")
    out = generate_answer(_pack(old_l, l2, summary, asked_object="L"), trace=[])
    assert out["answer"] == "L in progress"
    assert [f["fact_id"] for f in out["facts"]] == ["e1"]


def test_all_mismatched_facts_block_answer():
    l2 = _verified("e2", "ready", object="L", primary_object="L2")
    out = generate_answer(_pack(l2, asked_object="L"), trace=[])
    assert out["answer"] is None
    assert "grounding" in out["error"]
    assert out["total_facts"] == 0


def test_absent_primary_object_matching_object_is_kept():
    fact = _verified("only-object", "same object claim", object="R-41")
    assert "primary_object" not in fact
    out = generate_answer(_pack(fact, asked_object="R-41"), trace=[])
    assert out["answer"] == "same object claim"


def test_absent_primary_object_mismatching_object_is_excluded():
    fact = _verified("other-object", "other object claim", object="R-14")
    assert "primary_object" not in fact
    out = generate_answer(_pack(fact, asked_object="R-41"), trace=[])
    assert out["answer"] is None
    assert "grounding" in out["error"]


def test_linked_objects_does_not_keep_foreign_status():
    link = _verified(
        "link-r41-r14",
        "Register R-41 attaches primary document R-14",
        object="R-41",
        primary_object="R-14",
        linked_objects=["R-41", "R-14"],
    )
    trap = _verified(
        "trap-status",
        "status closed via R-14",
        object="R-41",
        primary_object="R-14",
    )
    on_object = _verified(
        "on-r41",
        "status pending review",
        object="R-41",
        primary_object="R-41",
    )
    out = generate_answer(_pack(link, trap, on_object, asked_object="R-41"), trace=[])
    assert out["answer"] == "status pending review"
    ids = [f["fact_id"] for f in out["facts"]]
    assert ids == ["on-r41"]
    assert "Register R-41 attaches primary document R-14" not in out["answer"]
    assert "status closed via R-14" not in out["answer"]


def test_linked_objects_does_not_admit_l2_status_for_l():
    l2 = _verified(
        "e2",
        "ready",
        object="L",
        primary_object="L2",
        linked_objects=["L"],
    )
    kept = _facts_applicable_to_asked_object([l2], "L")
    assert kept == []
    out = generate_answer(_pack(l2, asked_object="L"), trace=[])
    assert out["answer"] is None
    assert "grounding" in out["error"]


def test_status_applies_to_keeps_explicit_status_transfer():
    transfer = _verified(
        "xfer",
        "L inherited ready status from L2",
        object="L2",
        primary_object="L2",
        status_applies_to=["L"],
    )
    on_object = _verified(
        "on-l",
        "L in progress",
        object="L",
        primary_object="L",
    )
    out = generate_answer(_pack(transfer, on_object, asked_object="L"), trace=[])
    assert out["answer"] is not None
    ids = [f["fact_id"] for f in out["facts"]]
    assert "xfer" in ids
    assert "on-l" in ids
    assert "L inherited ready status from L2" in out["answer"]
    assert "L in progress" in out["answer"]


def _retrieved_r41_pair():
    return [
        {
            "id": "e2",
            "text": "status closed via R-14",
            "source": "register",
            "confidence": 0.9,
            "_score": 0.8,
            "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL",
            "epistemic_state": "Observed",
            "origin": "retrieval",
            "object": "R-41",
            "primary_object": "R-14",
        },
        {
            "id": "e3",
            "text": "status pending review",
            "source": "independent-report",
            "confidence": 0.95,
            "_score": 0.7,
            "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL",
            "epistemic_state": "Observed",
            "origin": "retrieval",
            "object": "R-41",
            "primary_object": "R-41",
        },
    ]


def test_run_without_asked_object_keeps_mismatched_document(monkeypatch):
    from core import pipeline

    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: _retrieved_r41_pair())
    out = pipeline.run("Какой статус сообщить для R-41?")
    assert out["answer"] is not None
    assert "status closed via R-14" in out["answer"]
    assert "status pending review" in out["answer"]


def test_run_forwards_explicit_asked_object_to_generate_answer(monkeypatch):
    from core import pipeline

    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: _retrieved_r41_pair())
    out = pipeline.run(
        "Какой статус сообщить для R-41?",
        asked_object="R-41",
    )
    assert out.get("error") is None or out.get("answer") is not None
    assert out["answer"] == "status pending review"
    assert [f["fact_id"] for f in out["facts"]] == ["e3"]
    assert "closed" not in out["answer"]


def test_run_does_not_treat_linked_objects_as_status_transfer(monkeypatch):
    from core import pipeline

    items = _retrieved_r41_pair()
    items.append(
        {
            "id": "link-1",
            "text": "Register R-41 attaches primary document R-14",
            "source": "register-index",
            "confidence": 0.9,
            "_score": 0.6,
            "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL",
            "epistemic_state": "Observed",
            "origin": "retrieval",
            "object": "R-41",
            "primary_object": "R-14",
            "linked_objects": ["R-41", "R-14"],
        }
    )
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: items)
    out = pipeline.run("Какой статус сообщить для R-41?", asked_object="R-41")
    assert out["answer"] == "status pending review"
    ids = [f["fact_id"] for f in out["facts"]]
    assert ids == ["e3"]
    assert "Register R-41 attaches primary document R-14" not in out["answer"]
    assert "status closed via R-14" not in out["answer"]


def test_run_forwards_status_applies_to_through_query_path(monkeypatch):
    from core import pipeline

    items = _retrieved_r41_pair()
    items.append(
        {
            "id": "xfer-1",
            "text": "R-41 inherited pending status from R-14",
            "source": "register-index",
            "confidence": 0.9,
            "_score": 0.6,
            "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL",
            "epistemic_state": "Observed",
            "origin": "retrieval",
            "object": "R-14",
            "primary_object": "R-14",
            "status_applies_to": ["R-41"],
        }
    )
    monkeypatch.setattr(pipeline, "retrieve", lambda q, k=3: items)
    out = pipeline.run("Какой статус сообщить для R-41?", asked_object="R-41")
    assert out["answer"] is not None
    ids = [f["fact_id"] for f in out["facts"]]
    assert "e3" in ids
    assert "xfer-1" in ids
    assert "e2" not in ids
    assert "R-41 inherited pending status from R-14" in out["answer"]
    assert "status pending review" in out["answer"]
    assert "status closed via R-14" not in out["answer"]
