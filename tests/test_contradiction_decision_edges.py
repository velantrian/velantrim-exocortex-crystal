"""Focused edge coverage for the explicit contradiction decision boundary."""

from core import conflict_decision, review
from core.contradiction import CONTRADICTION
from core.contradiction_report import ContradictionReport
from core.l3_graph import get_l3_graph
from core.memory import get_fact, store_fact, transition_esm
from core.reconcile import REL_CONTRADICTS


def _store(fact_id: str, claim: str, *, state: str = "Observed") -> dict:
    store_fact(
        {
            "fact_id": fact_id,
            "claim": claim,
            "source": "edge-test",
            "confidence": 0.9,
            "epistemic_state": "Observed",
            "claim_type": "WORLD_FACT",
            "source_status": "EXTERNAL",
            "significance": 0.5,
        }
    )
    if state == "Validated":
        assert transition_esm(fact_id, "Validated") is True
        fact = get_fact(fact_id)
        fact["truth_status"] = "VERIFIED"
        get_l3_graph().merge_fact(fact)
    return get_fact(fact_id)


def _report(candidate_id: str, target_id: str) -> ContradictionReport:
    return ContradictionReport.from_candidates(
        candidate_fact_id=candidate_id,
        candidates=[
            {
                "fact_id": target_id,
                "kind": CONTRADICTION,
                "signal": "negation",
                "similarity": 0.9,
            }
        ],
    )


def test_metadata_persistence_fails_closed_when_candidate_disappears(monkeypatch):
    monkeypatch.setattr(conflict_decision, "get_fact", lambda _fact_id: None)
    assert conflict_decision._persist_candidate_metadata("missing", {"x": 1}) is False


def test_non_world_fact_never_builds_contradiction_report(monkeypatch):
    monkeypatch.setattr(
        review,
        "find_conflicts",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("domain-ineligible claim must not query conflicts")
        ),
    )
    assert review._build_contradiction_report(
        {
            "fact_id": "opinion:1",
            "claim": "I prefer local systems",
            "claim_type": "OPINION",
        }
    ) is None


def test_resolve_conflict_returns_blocked_diagnosis_without_mutation(monkeypatch):
    candidate = _store("blocked:new", "A pending world fact")
    monkeypatch.setattr(
        review,
        "_diagnose",
        lambda _fact: {"verdict": "blocked", "reason": "blocked by test gate"},
    )

    result = review.resolve_conflict(
        candidate["fact_id"],
        disposition="COEXIST",
        actor="curator",
        reason="must not apply",
    )

    assert result["approved"] is False
    assert result["reason"] == "blocked by test gate"
    assert result["diagnosis"]["verdict"] == "blocked"
    assert get_fact(candidate["fact_id"])["epistemic_state"] == "Observed"
    assert get_l3_graph().get_fact(candidate["fact_id"]) is None


def test_supersede_target_transition_exception_becomes_explicit_partial_coexistence(
    monkeypatch,
):
    target = _store(
        "exception:old",
        "The vaccine is effective against the virus",
        state="Validated",
    )
    candidate = _store(
        "exception:new",
        "The vaccine is not effective against the virus",
    )
    report = _report(candidate["fact_id"], target["fact_id"])
    real_transition = transition_esm

    def raising_transition(fact_id: str, state: str) -> bool:
        if fact_id == target["fact_id"] and state == "Contradicted":
            raise ValueError("simulated concurrent target transition")
        return real_transition(fact_id, state)

    monkeypatch.setattr(conflict_decision, "transition_esm", raising_transition)
    result = conflict_decision.apply_conflict_decision(
        fact=candidate,
        report=report,
        disposition="SUPERSEDE",
        actor="curator",
        reason="newer evidence",
        target_fact_ids=[target["fact_id"]],
    )

    assert result["approved"] is True
    assert result["applied"] is False
    assert result["partial"] is True
    assert result["partial_target_ids"] == [target["fact_id"]]
    assert get_fact(candidate["fact_id"])["epistemic_state"] == "Validated"
    assert get_fact(target["fact_id"])["epistemic_state"] == "Validated"
    edges = get_l3_graph().get_edges(candidate["fact_id"], REL_CONTRADICTS)
    assert [edge["target"] for edge in edges] == [target["fact_id"]]
    assert edges[0]["props"]["partial_supersede"] is True
