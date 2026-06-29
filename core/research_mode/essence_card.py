from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal, Optional, Tuple


class EssenceCardStatus(str, Enum):
    RAW_OBSERVATION = "RAW_OBSERVATION"
    HYPOTHESIS = "HYPOTHESIS"
    PATTERN_CANDIDATE = "PATTERN_CANDIDATE"
    CONFIRMED_PATTERN = "CONFIRMED_PATTERN"
    PRINCIPLE_CANDIDATE = "PRINCIPLE_CANDIDATE"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVED = "ARCHIVED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    REJECTED = "REJECTED"


TERMINAL_STATUSES = {EssenceCardStatus.ARCHIVED, EssenceCardStatus.REJECTED}


@dataclass(frozen=True)
class FieldChange:
    field_name: str
    old_value: str
    new_value: str


@dataclass(frozen=True)
class ConfidenceBreakdown:
    overall: float
    source_quality: float
    evidence_count_score: float
    consistency_score: float
    recency_score: float
    contradiction_penalty: float
    calibration_version: str


@dataclass(frozen=True)
class ContradictionRef:
    target_card_id: str
    type: str
    severity: float
    evidence_ref: str


@dataclass(frozen=True)
class EssenceCard:
    card_id: str
    source_event_ids: Tuple[str, ...]
    core_essence: str
    topic: str
    status: EssenceCardStatus
    confidence: ConfidenceBreakdown
    stability: float
    novelty: float
    evidence_refs: Tuple[str, ...]
    contradictions: Tuple[ContradictionRef, ...]
    supersedes: Tuple[str, ...]
    superseded_by: Optional[str]
    failure_flags: Tuple[str, ...]
    created_at: datetime
    last_updated: datetime


@dataclass(frozen=True)
class EssenceCardRevision:
    revision_id: str
    card_id: str
    previous_revision_id: Optional[str]
    changed_fields: Tuple[FieldChange, ...]
    reason: str
    actor: str
    evidence_refs: Tuple[str, ...]
    created_at: datetime


@dataclass(frozen=True)
class AdmissionReceipt:
    admission_receipt_id: str
    card_id: str
    eligible: bool
    reason: str
    required_checks: Tuple[str, ...]
    passed_checks: Tuple[str, ...]
    failed_checks: Tuple[str, ...]
    human_review_performed: bool
    truthgate_receipt_id: Optional[str]
    decided_at: datetime
    decision_source: str = "ResearchAdmissionPolicy"


@dataclass(frozen=True)
class ResearchFailureEvent:
    event_id: str
    card_id: str
    failure_flag: str
    severity: float
    description: str
    detected_by: str
    evidence_refs: Tuple[str, ...]
    created_at: datetime


@dataclass(frozen=True)
class CausalCandidateEdge:
    edge_id: str
    source_card_id: str
    target_card_id: str
    phrasing: Literal["often_preceded", "may_contribute", "candidate_causal"]
    strength: float
    evidence_type: str
    evidence_refs: Tuple[str, ...]
    created_at: datetime


def _validate_score(value: float, name: str) -> None:
    if not (0.0 <= value <= 1.0):
        raise ValueError(f"{name} must be between 0.0 and 1.0, got {value}")


def validate_essence_card(card: EssenceCard) -> None:
    _validate_score(card.confidence.overall, "confidence.overall")
    _validate_score(card.confidence.source_quality, "confidence.source_quality")
    _validate_score(card.confidence.evidence_count_score, "confidence.evidence_count_score")
    _validate_score(card.confidence.consistency_score, "confidence.consistency_score")
    _validate_score(card.confidence.recency_score, "confidence.recency_score")
    _validate_score(card.confidence.contradiction_penalty, "confidence.contradiction_penalty")

    _validate_score(card.stability, "stability")
    _validate_score(card.novelty, "novelty")

    for contradiction in card.contradictions:
        _validate_score(
            contradiction.severity,
            f"contradiction.severity ({contradiction.target_card_id})",
        )


def validate_research_failure_event(event: ResearchFailureEvent) -> None:
    _validate_score(event.severity, "failure_event.severity")


def validate_causal_candidate_edge(edge: CausalCandidateEdge) -> None:
    _validate_score(edge.strength, "causal_candidate.strength")


def transition_allowed(
    from_status: EssenceCardStatus,
    to_status: EssenceCardStatus,
    actor: str = "system",
    evidence_refs: Tuple[str, ...] = (),
) -> bool:
    if from_status in TERMINAL_STATUSES:
        return False

    if from_status == to_status:
        return False

    if to_status == EssenceCardStatus.NEEDS_REVIEW:
        return True

    if to_status == EssenceCardStatus.REJECTED:
        return actor in {"human", "policy"} and len(evidence_refs) > 0

    if to_status == EssenceCardStatus.SUPERSEDED:
        return len(evidence_refs) > 0

    if (
        from_status == EssenceCardStatus.RAW_OBSERVATION
        and to_status == EssenceCardStatus.HYPOTHESIS
    ):
        return True

    if (
        from_status == EssenceCardStatus.HYPOTHESIS
        and to_status == EssenceCardStatus.PATTERN_CANDIDATE
    ):
        return True

    if (
        from_status == EssenceCardStatus.PATTERN_CANDIDATE
        and to_status == EssenceCardStatus.CONFIRMED_PATTERN
    ):
        return len(evidence_refs) > 0

    if (
        from_status == EssenceCardStatus.CONFIRMED_PATTERN
        and to_status == EssenceCardStatus.PRINCIPLE_CANDIDATE
    ):
        return len(evidence_refs) > 0

    if (
        from_status == EssenceCardStatus.NEEDS_REVIEW
        and to_status == EssenceCardStatus.ARCHIVED
    ):
        return actor in {"human", "policy"} and len(evidence_refs) > 0

    if (
        from_status == EssenceCardStatus.SUPERSEDED
        and to_status == EssenceCardStatus.ARCHIVED
    ):
        return len(evidence_refs) > 0

    return False
