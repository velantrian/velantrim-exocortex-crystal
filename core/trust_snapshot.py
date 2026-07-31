# core/trust_snapshot.py
# Velantrim ExoCortex — immutable trust snapshot for read-time reconciliation.
#
# This module provides one typed, immutable representation for the trust fields
# assembled from physical L3 plus deny-dominant L1 state. It is deliberately a
# read model: no storage calls, no TruthGate decision, no ESM transition and no
# Canon mutation happen here.

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Mapping, Optional

DEFAULT_CLAIM_TYPE = "WORLD_FACT"
STORE_STATE_CONFLICT = "STORE_STATE_CONFLICT"
TERMINAL_ESM_STATES = frozenset({"Collapsed", "Contradicted", "Deprecated"})


def _string_or_none(value: Any) -> Optional[str]:
    """Return a non-blank string, otherwise None without coercion."""
    return value if isinstance(value, str) and value.strip() else None


def _finite_number(value: Any) -> Optional[float]:
    """Return a finite numeric value, rejecting bool and coercible strings."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    try:
        result = float(value)
    except OverflowError:
        return None
    return result if math.isfinite(result) else None


def _confidence_or_none(value: Any) -> Optional[float]:
    """Normalize confidence without turning malformed metadata into 0.0."""
    result = _finite_number(value)
    if result is None or not 0.0 <= result <= 1.0:
        return None
    return result


def _score_or_zero(value: Any) -> float:
    """Retrieval score is ranking metadata; malformed values become 0.0."""
    result = _finite_number(value)
    return 0.0 if result is None else result


def normalize_restricted_bit(value: Any) -> Optional[bool]:
    """Normalize a storage restriction bit, preserving UNKNOWN as None.

    Only actual bools and exact integer 0/1 values are accepted. Strings,
    floats, missing values and out-of-range integers remain unknown so a read
    boundary can fail closed instead of silently coercing them.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and value in (0, 1):
        return value == 1
    return None


def _confidence_disagrees(l1: Mapping[str, Any], l3: Mapping[str, Any]) -> bool:
    if "confidence" not in l1:
        return False
    left = _confidence_or_none(l1.get("confidence"))
    right = _confidence_or_none(l3.get("confidence"))
    if left is None or right is None:
        return True
    return not math.isclose(left, right, abs_tol=1e-9)


def _claim_type_value(record: Mapping[str, Any]) -> Optional[str]:
    raw = record.get("claim_type", DEFAULT_CLAIM_TYPE)
    return _string_or_none(raw)


def _source_status_value(record: Mapping[str, Any]) -> Optional[str]:
    return _string_or_none(record.get("source_status"))


@dataclass(frozen=True, slots=True)
class TrustSnapshot:
    """Immutable read model for one resolved physical-L3 fact.

    Content and verdict fields come from L3. L1 may only make the snapshot more
    restrictive: a terminal state, a processing restriction or a genuine trust
    metadata disagreement wins fail-closed. `conflict_fields` is content-free;
    it names categories, never the disagreeing values.
    """

    fact_id: str
    claim: Optional[str]
    source: Optional[str]
    confidence: Optional[float]
    epistemic_state: Optional[str]
    claim_type: Optional[str]
    source_status: Optional[str]
    truth_status: Optional[str]
    restricted: Optional[bool]
    significance: float
    retrieval_score: float
    conflict_fields: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.fact_id, str) or not self.fact_id.strip():
            raise ValueError("TrustSnapshot.fact_id must be a non-blank string")
        if not isinstance(self.conflict_fields, tuple):
            raise TypeError("TrustSnapshot.conflict_fields must be an immutable tuple")

    @classmethod
    def from_records(
        cls,
        *,
        fact_id: str,
        l3: Mapping[str, Any],
        l1: Optional[Mapping[str, Any]] = None,
        retrieval_score: Any = 0.0,
    ) -> "TrustSnapshot":
        """Reconcile L3 content with deny-dominant L1 trust state.

        The function is pure. Input mappings are never mutated and no nested
        mutable metadata is retained in the snapshot.
        """
        if not isinstance(l3, Mapping):
            raise TypeError("TrustSnapshot.l3 must be a mapping")
        if l1 is not None and not isinstance(l1, Mapping):
            raise TypeError("TrustSnapshot.l1 must be a mapping or None")

        state_raw = l3.get("epistemic_state")
        state = _string_or_none(state_raw)
        confidence = _confidence_or_none(l3.get("confidence"))
        l3_restricted = normalize_restricted_bit(l3.get("restricted"))
        restricted = l3_restricted
        conflicts: list[str] = []

        # Confidence is a trust field, not display metadata. Missing, malformed,
        # non-finite or out-of-range L3 confidence is itself a store-integrity
        # conflict even when no L1 row exists. Preserve the unknown as None in the
        # typed snapshot; the compatibility mapping may use a legacy safe sentinel.
        if confidence is None:
            conflicts.append("confidence")
            state = STORE_STATE_CONFLICT

        if l1 is not None:
            l1_state_raw = l1.get("epistemic_state")
            l1_state = _string_or_none(l1_state_raw)
            if l1_state in TERMINAL_ESM_STATES:
                state = l1_state
            elif l1_state_raw is not None and state_raw != l1_state_raw:
                conflicts.append("epistemic_state")
                state = STORE_STATE_CONFLICT

            l1_restricted = normalize_restricted_bit(l1.get("restricted"))
            if l1_restricted is True or l3_restricted is True:
                restricted = True
            elif l1_restricted is False:
                restricted = False

            if _confidence_disagrees(l1, l3):
                conflicts.append("confidence")
            if "claim_type" in l1 and _claim_type_value(l1) != _claim_type_value(l3):
                conflicts.append("claim_type")
            if (
                "source_status" in l1
                and _source_status_value(l1) != _source_status_value(l3)
            ):
                conflicts.append("source_status")

            if conflicts:
                state = STORE_STATE_CONFLICT

        significance = _finite_number(l3.get("significance", 0.5))
        if significance is None:
            significance = 0.5

        return cls(
            fact_id=fact_id,
            claim=_string_or_none(l3.get("claim")),
            source=_string_or_none(l3.get("source")),
            confidence=confidence,
            epistemic_state=state,
            claim_type=_claim_type_value(l3),
            source_status=_source_status_value(l3),
            truth_status=_string_or_none(l3.get("truth_status")),
            restricted=restricted,
            significance=significance,
            retrieval_score=_score_or_zero(retrieval_score),
            conflict_fields=tuple(dict.fromkeys(conflicts)),
        )

    def to_fact_dict(self) -> dict[str, Any]:
        """Return a fresh compatibility dict for existing Guardian/View code.

        Existing mapping consumers historically receive 0.0 for malformed
        confidence. Preserve that safe outward sentinel during this narrow
        migration while the typed snapshot retains None plus a confidence
        conflict, so unknown/corrupt metadata is not confused with a real zero
        inside the trust boundary.
        """
        return {
            "fact_id": self.fact_id,
            "claim": self.claim,
            "source": self.source,
            "confidence": 0.0 if self.confidence is None else self.confidence,
            "epistemic_state": self.epistemic_state,
            "claim_type": self.claim_type,
            "source_status": self.source_status,
            "significance": self.significance,
            "truth_status": self.truth_status,
            "restricted": self.restricted,
            "_score": self.retrieval_score,
            "_store_conflicts": self.conflict_fields,
        }


__all__ = [
    "DEFAULT_CLAIM_TYPE",
    "STORE_STATE_CONFLICT",
    "TERMINAL_ESM_STATES",
    "TrustSnapshot",
    "normalize_restricted_bit",
]
