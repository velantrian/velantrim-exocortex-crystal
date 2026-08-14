from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RFC = ROOT / "docs" / "rfcs" / "RFC_EPIS_001_EPISTEMIC_ROUTER.md"
STATUS = ROOT / "docs" / "rfcs" / "EPIS_001_STATUS.json"
AI_CONTEXT = ROOT / "docs" / "ai" / "EPIS_001_EPISTEMIC_ROUTER.md"


def test_epis_001_is_architecture_only_and_not_runtime() -> None:
    rfc = RFC.read_text(encoding="utf-8")
    ai = AI_CONTEXT.read_text(encoding="utf-8")

    assert "Status:                FROZEN_ARCHITECTURE_CONTRACT" in rfc
    assert "Runtime implementation: NOT IMPLEMENTED" in rfc
    assert "Runtime authorization:  false" in rfc
    assert "KNOWN | PARTIAL | UNKNOWN" in rfc
    assert "evidence_state" in rfc
    assert "!= truth_status" in rfc
    assert "!= epistemic_state" in rfc
    assert "!= CanonicalReadMode" in rfc
    assert "future implementation test plan" in rfc.lower()

    assert "runtime_implemented: false" in ai
    assert "runtime_authorization: false" in ai
    assert "KNOWN == VERIFIED truth" in ai
    assert not (ROOT / "core" / "epistemic_router.py").exists()


def test_epis_001_machine_status_fails_closed_on_authority() -> None:
    status = json.loads(STATUS.read_text(encoding="utf-8"))

    assert status["contract"] == "EPIS-001-v1"
    assert status["status"] == "FROZEN_ARCHITECTURE_CONTRACT"
    assert status["architecture_only"] is True
    assert status["runtime_implemented"] is False
    assert status["runtime_authorization"] is False
    assert status["pipeline_wired"] is False
    assert status["evidence_states"] == ["KNOWN", "PARTIAL", "UNKNOWN"]
    assert status["known_requires_explicit_complete_coverage"] is True
    assert status["canonical_view_recheck_required_for_support"] is True
    assert status["malformed_input_fails_closed"] is True

    denied_authorities = (
        "l3_write_authority",
        "truth_status_mutation_authority",
        "esm_transition_authority",
        "confidence_promotion_authority",
        "evidence_admission_authority",
        "canon_authority",
        "contradiction_adjudication_authority",
        "guardian_bypass",
        "truth_gate_bypass",
        "canonical_view_bypass",
    )
    assert all(status[key] is False for key in denied_authorities)
    assert all(value is False for value in status["state_separation"].values())


def test_epis_001_preserves_existing_authority_boundaries() -> None:
    pipeline = (ROOT / "core" / "pipeline.py").read_text(encoding="utf-8")
    truth_gate = (ROOT / "core" / "truth_gate.py").read_text(encoding="utf-8")
    canonical_view = (ROOT / "core" / "canonical_view.py").read_text(encoding="utf-8")
    trace = (ROOT / "core" / "trace.py").read_text(encoding="utf-8")
    rfc = RFC.read_text(encoding="utf-8")

    assert "Structural integrity gate on FactsPack + Trace before TruthGate" in pipeline
    assert "from core.truth_gate import truth_gate" in pipeline
    assert "The only automatic entry into the L3 graph" in truth_gate
    assert "This module is READ-ONLY and PURE" in canonical_view
    assert "Trace → Validation → Answer" in trace

    assert "Guardian remains the structural integrity gate" in rfc
    assert "TruthGate remains the L3 admission boundary" in rfc
    assert "CanonicalView is the existing strict read-time authority" in rfc
    assert "TRACE is provenance metadata" in rfc


def test_epis_001_known_cannot_be_inferred_from_retrieval_or_confidence() -> None:
    rfc = RFC.read_text(encoding="utf-8")

    required_guards = (
        "A non-empty FactsPack, high confidence, retrieval rank, physical L3 membership, or `Validated` ESM state alone is **never sufficient** for `KNOWN`.",
        "`PARTIAL` is not permission to fill missing content from model priors.",
        "A malformed condition must never be normalized into `KNOWN` merely because some facts exist.",
        "Direct callers cannot fabricate strict support through a boolean flag.",
    )
    for guard in required_guards:
        assert guard in rfc
