'''Tests for response_policy v0 (Crystal-native contract).

Covers the new ResponsePolicyInput / ResponsePolicyDecision API and
all key decision rules aligned with CLAIM_TYPES, SOURCE_STATUSES, ESM_STATES.
'''

import pytest
from core.response_policy import (
    decide_response_policy,
    ResponsePolicyInput,
    ResponsePolicyDecision,
)


def make_input(
    claim_type="WORLD_FACT",
    source_status="UNKNOWN",
    epistemic_state="Hypothesized",
    truth_status=None,
    risk_domain="GENERAL",
    mode_hint=None,
) -> ResponsePolicyInput:
    return ResponsePolicyInput(
        claim_type=claim_type,
        source_status=source_status,
        epistemic_state=epistemic_state,
        truth_status=truth_status,
        risk_domain=risk_domain,
        mode_hint=mode_hint,
    )


def test_subjective_claims_acknowledge():
    for ct in ["EMOTION", "USER_EXPERIENCE", "OPINION", "PREFERENCE", "GOAL"]:
        inp = make_input(claim_type=ct)
        decision = decide_response_policy(inp)
        assert decision.action == "ACKNOWLEDGE"
        assert not decision.requires_citation


def test_world_fact_llm_output_refuse():
    inp = make_input(claim_type="WORLD_FACT", source_status="LLM_OUTPUT")
    decision = decide_response_policy(inp)
    assert decision.action == "REFUSE"
    assert "LLM_OUTPUT" in decision.reason


def test_bad_epistemic_states_refuse():
    for es in ["Contradicted", "Deprecated", "Collapsed"]:
        inp = make_input(epistemic_state=es)
        decision = decide_response_policy(inp)
        assert decision.action == "REFUSE"


def test_high_risk_requires_citation_or_limit():
    inp = make_input(
        claim_type="WORLD_FACT",
        source_status="EXTERNAL",
        epistemic_state="Supported",
        risk_domain="HEALTH",
    )
    decision = decide_response_policy(inp)
    assert decision.action == "CITE_OR_LIMIT"
    assert decision.requires_citation


def test_strong_validated_assert():
    inp = make_input(
        claim_type="WORLD_FACT",
        source_status="EXTERNAL",
        epistemic_state="Validated",
    )
    decision = decide_response_policy(inp)
    assert decision.action == "ASSERT"
    assert decision.requires_citation  # even strong ASSERT remains citation-aware in Crystal


def test_supported_hedge():
    inp = make_input(epistemic_state="Supported")
    decision = decide_response_policy(inp)
    assert decision.action == "HEDGE"


def test_user_reported_world_fact_speculative():
    inp = make_input(
        claim_type="WORLD_FACT",
        source_status="USER_REPORTED",
        epistemic_state="Hypothesized",
    )
    decision = decide_response_policy(inp)
    assert decision.action == "SPECULATIVE"
    assert decision.requires_citation


def test_pure_no_side_effects():
    inp = make_input()
    original = inp.claim_type
    decide_response_policy(inp)
    assert inp.claim_type == original  # frozen dataclass, input not mutated


def test_decision_is_frozen():
    decision = decide_response_policy(make_input())
    with pytest.raises(Exception):  # frozen dataclass
        decision.action = "HEDGE"  # type: ignore


def test_read_path_only_no_forbidden_calls():
    """Guard: response_policy must never call write-path or TruthGate functions."""
    import ast
    import inspect

    source = inspect.getsource(decide_response_policy)
    forbidden = ["truth_gate(", "transition_esm(", "merge_fact(", "get_l3_graph("]
    for call in forbidden:
        assert call not in source, f"Forbidden call found: {call}"


def test_mode_hint_cannot_upgrade_weak_claim_to_assert():
    """Invariant: mode_hint must never promote weak evidence to ASSERT."""
    # Weak user-reported + mode_hint
    inp1 = make_input(
        claim_type="WORLD_FACT",
        source_status="USER_REPORTED",
        epistemic_state="Hypothesized",
        mode_hint="science",
    )
    decision1 = decide_response_policy(inp1)
    assert decision1.action != "ASSERT"

    # Another weak case with strict mode
    inp2 = make_input(
        claim_type="WORLD_FACT",
        source_status="UNKNOWN",
        epistemic_state="Observed",
        mode_hint="strict",
    )
    decision2 = decide_response_policy(inp2)
    assert decision2.action != "ASSERT"
