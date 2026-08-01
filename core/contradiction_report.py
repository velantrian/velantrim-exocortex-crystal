# core/contradiction_report.py
# Velantrim ExoCortex — immutable contradiction review contract.
#
# A ContradictionReport is an advisory, content-free snapshot of the conflicts
# detected for one pending fact. It never promotes, rejects, supersedes or edits
# memory by itself. Resolution requires a separate, explicit curator decision.

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
import math
from typing import Any, Iterable, Mapping, Optional


class ConflictDisposition(str, Enum):
    """Explicit curator outcomes supported by the first decision baseline."""

    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    COEXIST = "COEXIST"
    CONTEXTUALIZE = "CONTEXTUALIZE"
    SUPERSEDE = "SUPERSEDE"


@dataclass(frozen=True, slots=True)
class ConflictReference:
    """Content-free reference to one conflicting physical-L3 fact."""

    fact_id: str
    kind: str
    signal: Optional[str]
    similarity: float

    def __post_init__(self) -> None:
        if not isinstance(self.fact_id, str) or not self.fact_id.strip():
            raise ValueError("ConflictReference.fact_id must be a non-blank string")
        if not isinstance(self.kind, str) or not self.kind.strip():
            raise ValueError("ConflictReference.kind must be a non-blank string")
        if self.signal is not None and not isinstance(self.signal, str):
            raise TypeError("ConflictReference.signal must be a string or None")
        if isinstance(self.similarity, bool) or not isinstance(
            self.similarity, (int, float)
        ):
            raise TypeError("ConflictReference.similarity must be numeric")
        if not math.isfinite(float(self.similarity)):
            raise ValueError("ConflictReference.similarity must be finite")

    @classmethod
    def from_candidate(cls, candidate: Mapping[str, Any]) -> "ConflictReference":
        """Build from reconcile.find_conflicts() output without retaining claim text."""
        if not isinstance(candidate, Mapping):
            raise TypeError("conflict candidate must be a mapping")
        similarity = candidate.get("similarity", 0.0)
        if isinstance(similarity, bool) or not isinstance(similarity, (int, float)):
            similarity = 0.0
        similarity = float(similarity)
        if not math.isfinite(similarity):
            similarity = 0.0
        signal = candidate.get("signal")
        return cls(
            fact_id=candidate.get("fact_id"),
            kind=candidate.get("kind"),
            signal=signal if isinstance(signal, str) else None,
            similarity=similarity,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "fact_id": self.fact_id,
            "kind": self.kind,
            "signal": self.signal,
            "similarity": self.similarity,
        }


@dataclass(frozen=True, slots=True)
class ContradictionReport:
    """Immutable review snapshot for a pending claim and its contradictions.

    The report intentionally retains no claim/source text. It is safe to place in
    audit detail or return from a diagnosis without duplicating memory content.
    A report is advisory: no similarity/confidence value selects a winner.
    """

    report_id: str
    candidate_fact_id: str
    conflicts: tuple[ConflictReference, ...]
    disposition: ConflictDisposition = ConflictDisposition.REVIEW_REQUIRED

    def __post_init__(self) -> None:
        if not isinstance(self.report_id, str) or not self.report_id.strip():
            raise ValueError("ContradictionReport.report_id must be non-blank")
        if not isinstance(self.candidate_fact_id, str) or not self.candidate_fact_id.strip():
            raise ValueError("ContradictionReport.candidate_fact_id must be non-blank")
        if not isinstance(self.conflicts, tuple):
            raise TypeError("ContradictionReport.conflicts must be an immutable tuple")
        if not self.conflicts:
            raise ValueError("ContradictionReport requires at least one conflict")
        if any(ref.fact_id == self.candidate_fact_id for ref in self.conflicts):
            raise ValueError("a contradiction report cannot conflict with itself")

    @property
    def conflict_ids(self) -> tuple[str, ...]:
        return tuple(ref.fact_id for ref in self.conflicts)

    @classmethod
    def from_candidates(
        cls,
        *,
        candidate_fact_id: str,
        candidates: Iterable[Mapping[str, Any]],
    ) -> "ContradictionReport":
        refs_by_id: dict[str, ConflictReference] = {}
        for candidate in candidates:
            ref = ConflictReference.from_candidate(candidate)
            if ref.fact_id == candidate_fact_id:
                continue
            # Stable first-seen semantics: duplicate retrieval hits cannot inflate
            # the report or create repeated audit identifiers.
            refs_by_id.setdefault(ref.fact_id, ref)
        refs = tuple(sorted(refs_by_id.values(), key=lambda ref: ref.fact_id))
        if not refs:
            raise ValueError("ContradictionReport requires at least one conflict")

        sealed = {
            "candidate_fact_id": candidate_fact_id,
            "conflicts": [ref.to_dict() for ref in refs],
            "version": 1,
        }
        canonical = json.dumps(
            sealed, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        )
        report_id = "ctr:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return cls(
            report_id=report_id,
            candidate_fact_id=candidate_fact_id,
            conflicts=refs,
        )

    def with_disposition(self, disposition: ConflictDisposition | str) -> "ContradictionReport":
        return ContradictionReport(
            report_id=self.report_id,
            candidate_fact_id=self.candidate_fact_id,
            conflicts=self.conflicts,
            disposition=ConflictDisposition(disposition),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "candidate_fact_id": self.candidate_fact_id,
            "conflicts": [ref.to_dict() for ref in self.conflicts],
            "conflict_ids": list(self.conflict_ids),
            "disposition": self.disposition.value,
            "automatic_winner": None,
        }


__all__ = [
    "ConflictDisposition",
    "ConflictReference",
    "ContradictionReport",
]
