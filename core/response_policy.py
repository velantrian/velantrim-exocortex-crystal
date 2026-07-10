'''response_policy v0 - Crystal-native deterministic read-path policy.

This module decides response strategy (ASSERT / HEDGE / etc.) using the
existing Crystal axes from core/memory.py:
- claim_type (WORLD_FACT, USER_EXPERIENCE, EMOTION, ...)
- source_status (USER_REPORTED, OBSERVED, DERIVED, EXTERNAL, LLM_OUTPUT, ...)
- epistemic_state (Validated, Supported, Contradicted, ...)
- risk_domain + mode_hint for context.

It is strictly read-path. Never calls TruthGate, never writes to L3/Canon,
never touches ESM state.
'''

from dataclasses import dataclass
from typing import Optional, Literal

ActionType = Literal[
    "ASSERT", "HEDGE", "SPECULATIVE", "REFUSE", "ACKNOWLEDGE", "CITE_OR_LIMIT"
]

@dataclass(frozen=True)
class ResponsePolicyInput:
    """Crystal-native input contract for response policy decisions."""
    claim_type: str
    source_status: str
    epistemic_state: str
    truth_status: Optional[str] = None
    risk_domain: str = "GENERAL"
    mode_hint: Optional[str] = None


@dataclass(frozen=True)
class ResponsePolicyDecision:
    """Deterministic output of the policy."""
    action: ActionType
    reason: str
    requires_citation: bool = False


def decide_response_policy(inp: ResponsePolicyInput) -> ResponsePolicyDecision:
    """Pure function implementing Crystal-native response policy v0.

    Rules (aligned with CLAIM_TYPES, SOURCE_STATUSES, ESM_STATES):
    - Subjective claim_types (EMOTION, USER_EXPERIENCE, OPINION, PREFERENCE, GOAL) → ACKNOWLEDGE
    - WORLD_FACT + LLM_OUTPUT → REFUSE (model output is not ground truth)
    - Contradicted / Deprecated / Collapsed → REFUSE
    - High-risk domains (HEALTH/LEGAL/FINANCIAL/SAFETY) require CITE_OR_LIMIT unless strongly validated
    - Validated + reliable source (EXTERNAL/DERIVED/OBSERVED) → ASSERT (with citation=True)
    - Supported → HEDGE
    - Weak WORLD_FACT from USER_REPORTED → SPECULATIVE
    - Default safe fallback: ACKNOWLEDGE
    """
    ct = (inp.claim_type or "").upper().strip()
    ss = (inp.source_status or "").upper().strip()
    es = (inp.epistemic_state or "").strip()
    es_upper = es.upper()
    risk = (inp.risk_domain or "GENERAL").upper().strip()
    # 1. Subjective claims → ACKNOWLEDGE (personal, not world facts)
    subjective = {"EMOTION", "USER_EXPERIENCE", "OPINION", "PREFERENCE", "GOAL"}
    if ct in subjective:
        return ResponsePolicyDecision(
            action="ACKNOWLEDGE",
            reason=f"Subjective claim_type '{ct}' – acknowledge without strong factual assertion.",
            requires_citation=False
        )

    # 2. WORLD_FACT sourced from LLM_OUTPUT → REFUSE
    if ct == "WORLD_FACT" and ss == "LLM_OUTPUT":
        return ResponsePolicyDecision(
            action="REFUSE",
            reason="WORLD_FACT cannot be asserted from LLM_OUTPUT (hallucination risk).",
            requires_citation=False
        )

    # 3. Bad epistemic states → REFUSE
    bad_states = {"CONTRADICTED", "DEPRECATED", "COLLAPSED"}
    if es_upper in bad_states:
        return ResponsePolicyDecision(
            action="REFUSE",
            reason=f"Epistemic state '{es}' indicates conflict or obsolescence.",
            requires_citation=False
        )

    # 4. High-risk domains need explicit caution unless strongly validated
    high_risk = risk in {"HEALTH", "LEGAL", "FINANCIAL", "SAFETY"}
    strong = es_upper in {"VALIDATED", "IMMUTABLECORE"}

    if high_risk and not strong:
        return ResponsePolicyDecision(
            action="CITE_OR_LIMIT",
            reason="High-risk domain requires citation or explicit scope limitation.",
            requires_citation=True
        )

    # 5. Strong validated from reliable source → ASSERT (citation-aware)
    reliable_sources = {"EXTERNAL", "DERIVED", "OBSERVED"}
    if strong and ss in reliable_sources:
        return ResponsePolicyDecision(
            action="ASSERT",
            reason="Validated fact from reliable source.",
            requires_citation=True
        )

    # 6. Supported state → HEDGE
    if es_upper == "SUPPORTED":
        return ResponsePolicyDecision(
            action="HEDGE",
            reason="Supporting evidence exists but not yet fully validated by TruthGate.",
            requires_citation=high_risk
        )

    # 7. Weak user-reported world fact → SPECULATIVE
    weak_states = {"HYPOTHESIZED", "OBSERVED"}
    if ct == "WORLD_FACT" and ss == "USER_REPORTED" and es_upper in weak_states:
        return ResponsePolicyDecision(
            action="SPECULATIVE",
            reason="User-reported world fact without strong validation.",
            requires_citation=True
        )

    # 8. Safe default
    return ResponsePolicyDecision(
        action="ACKNOWLEDGE",
        reason="Current epistemic grounding does not support a stronger claim.",
        requires_citation=high_risk
    )
