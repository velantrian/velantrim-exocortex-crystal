# core/topic_facets.py
# Velantrim ExoCortex — advisory multi-label topic projection.
#
# Topic facets answer only "what is this about?" They never answer whether a
# claim is true, well evidenced, authoritative or eligible for Canon. The module
# is pure and read-only: it imports no storage, TruthGate, ESM or review code.

from __future__ import annotations

from dataclasses import dataclass
import math
import re
from typing import Any, Iterable, Mapping, Optional

TAXONOMY_VERSION = "2026-08-v1"
ASSIGNED_BY = "keyword-facet-v1"
SUGGESTED_STATUS = "suggested"

_TOKEN_RE = re.compile(r"[^\W_]+", re.UNICODE)

# Weights are relevance hints, not probabilities or epistemic confidence.
# Terms are deliberately compact and bilingual (English/Russian) for the first
# dependency-free baseline. A later adapter may supply another classifier while
# preserving the same non-authoritative output contract.
_TAXONOMY: dict[str, dict[str, float]] = {
    "computing/artificial-intelligence": {
        "ai": 1.0,
        "artificial intelligence": 1.0,
        "machine learning": 0.9,
        "neural network": 0.8,
        "llm": 0.9,
        "искусственный интеллект": 1.0,
        "машинное обучение": 0.9,
        "нейросеть": 0.8,
    },
    "computing/software-engineering": {
        "software": 0.7,
        "code": 0.6,
        "repository": 0.7,
        "api": 0.7,
        "database": 0.7,
        "программирование": 0.8,
        "код": 0.6,
        "репозиторий": 0.7,
        "база данных": 0.7,
    },
    "computing/security-privacy": {
        "security": 0.9,
        "privacy": 0.9,
        "encryption": 0.8,
        "authentication": 0.8,
        "gdpr": 0.9,
        "безопасность": 0.9,
        "приватность": 0.9,
        "шифрование": 0.8,
    },
    "science/physics": {
        "physics": 0.9,
        "energy": 0.6,
        "quantum": 0.8,
        "gravity": 0.8,
        "физика": 0.9,
        "энергия": 0.6,
        "квантовый": 0.8,
        "гравитация": 0.8,
    },
    "science/biology": {
        "biology": 0.9,
        "organism": 0.7,
        "cell": 0.7,
        "evolution": 0.8,
        "биология": 0.9,
        "организм": 0.7,
        "клетка": 0.7,
        "эволюция": 0.8,
    },
    "health/medicine": {
        "medicine": 0.9,
        "medical": 0.8,
        "disease": 0.8,
        "treatment": 0.8,
        "vaccine": 0.8,
        "медицина": 0.9,
        "болезнь": 0.8,
        "лечение": 0.8,
        "вакцина": 0.8,
    },
    "environment/climate-water": {
        "climate": 0.8,
        "water": 0.7,
        "ecology": 0.8,
        "environment": 0.8,
        "drought": 0.8,
        "климат": 0.8,
        "вода": 0.7,
        "экология": 0.8,
        "засуха": 0.8,
    },
    "society/law-governance": {
        "law": 0.8,
        "legal": 0.8,
        "governance": 0.8,
        "regulation": 0.8,
        "policy": 0.6,
        "закон": 0.8,
        "право": 0.8,
        "управление": 0.7,
        "регулирование": 0.8,
    },
    "economy/finance-business": {
        "finance": 0.8,
        "market": 0.7,
        "investment": 0.8,
        "business": 0.8,
        "economy": 0.8,
        "финансы": 0.8,
        "рынок": 0.7,
        "инвестиции": 0.8,
        "бизнес": 0.8,
        "экономика": 0.8,
    },
}


def _normalize_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.casefold().split())


def _tokens(text: str) -> frozenset[str]:
    return frozenset(_TOKEN_RE.findall(text))


def validate_taxonomy(
    taxonomy: Optional[Mapping[str, Mapping[str, Any]]] = None,
) -> dict[str, Any]:
    """Validate the taxonomy without mutating or repairing it."""
    source = _TAXONOMY if taxonomy is None else taxonomy
    errors: list[str] = []
    if not isinstance(source, Mapping) or not source:
        return {"valid": False, "errors": ["taxonomy must be a non-empty mapping"]}

    for topic_id, terms in source.items():
        if not isinstance(topic_id, str) or not topic_id.strip() or "/" not in topic_id:
            errors.append(f"invalid topic_id: {topic_id!r}")
            continue
        if not isinstance(terms, Mapping) or not terms:
            errors.append(f"{topic_id}: terms must be a non-empty mapping")
            continue
        normalized_seen: set[str] = set()
        for term, weight in terms.items():
            normalized = _normalize_text(term)
            if not normalized:
                errors.append(f"{topic_id}: term must be a non-blank string")
                continue
            if normalized in normalized_seen:
                errors.append(f"{topic_id}: duplicate normalized term {normalized!r}")
            normalized_seen.add(normalized)
            if (
                isinstance(weight, bool)
                or not isinstance(weight, (int, float))
                or not math.isfinite(float(weight))
                or not 0.0 < float(weight) <= 1.0
            ):
                errors.append(f"{topic_id}: invalid weight for {normalized!r}")
    return {"valid": not errors, "errors": errors}


@dataclass(frozen=True, slots=True)
class TopicFacet:
    """One advisory topic label; score is relevance, never truth/confidence."""

    topic_id: str
    score: float
    matched_terms: tuple[str, ...]
    assigned_by: str = ASSIGNED_BY
    taxonomy_version: str = TAXONOMY_VERSION
    status: str = SUGGESTED_STATUS

    def __post_init__(self) -> None:
        if not isinstance(self.topic_id, str) or not self.topic_id.strip():
            raise ValueError("TopicFacet.topic_id must be a non-blank string")
        if (
            isinstance(self.score, bool)
            or not isinstance(self.score, (int, float))
            or not math.isfinite(float(self.score))
            or not 0.0 <= float(self.score) <= 1.0
        ):
            raise ValueError("TopicFacet.score must be finite and within [0, 1]")
        if not isinstance(self.matched_terms, tuple):
            raise TypeError("TopicFacet.matched_terms must be an immutable tuple")
        if any(not isinstance(term, str) or not term for term in self.matched_terms):
            raise ValueError("TopicFacet.matched_terms must contain non-blank strings")
        for field_name in ("assigned_by", "taxonomy_version", "status"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"TopicFacet.{field_name} must be a non-blank string")

    def to_dict(self) -> dict[str, Any]:
        return {
            "topic_id": self.topic_id,
            "score": self.score,
            "matched_terms": list(self.matched_terms),
            "assigned_by": self.assigned_by,
            "taxonomy_version": self.taxonomy_version,
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class TopicProjection:
    """Immutable, ephemeral multi-label projection for one text value."""

    facets: tuple[TopicFacet, ...]
    taxonomy_version: str = TAXONOMY_VERSION
    authoritative: bool = False
    writes_memory: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.facets, tuple):
            raise TypeError("TopicProjection.facets must be an immutable tuple")
        if self.authoritative is not False or self.writes_memory is not False:
            raise ValueError("topic projections must remain advisory and read-only")

    def to_dict(self) -> dict[str, Any]:
        return {
            "facets": [facet.to_dict() for facet in self.facets],
            "taxonomy_version": self.taxonomy_version,
            "authoritative": False,
            "writes_memory": False,
            "score_meaning": "topic_relevance_not_truth",
        }


def classify_topics(
    text: Any,
    *,
    max_facets: int = 3,
    min_score: float = 0.15,
    taxonomy: Optional[Mapping[str, Mapping[str, Any]]] = None,
) -> TopicProjection:
    """Return deterministic advisory topic facets for text.

    Scores are bounded lexical relevance hints. They are not calibrated
    probabilities, truth confidence, evidence quality or source authority.
    """
    if isinstance(max_facets, bool) or not isinstance(max_facets, int) or max_facets < 0:
        raise ValueError("max_facets must be a non-negative integer")
    if (
        isinstance(min_score, bool)
        or not isinstance(min_score, (int, float))
        or not math.isfinite(float(min_score))
        or not 0.0 <= float(min_score) <= 1.0
    ):
        raise ValueError("min_score must be finite and within [0, 1]")

    source = _TAXONOMY if taxonomy is None else taxonomy
    validation = validate_taxonomy(source)
    if not validation["valid"]:
        raise ValueError("invalid topic taxonomy: " + "; ".join(validation["errors"]))

    normalized = _normalize_text(text)
    if not normalized or max_facets == 0:
        return TopicProjection(facets=())
    token_set = _tokens(normalized)

    candidates: list[TopicFacet] = []
    for topic_id, terms in source.items():
        matched: list[tuple[str, float]] = []
        total_weight = sum(float(weight) for weight in terms.values())
        for raw_term, raw_weight in terms.items():
            term = _normalize_text(raw_term)
            is_phrase = " " in term
            present = (
                f" {term} " in f" {normalized} "
                if is_phrase
                else term in token_set
            )
            if present:
                matched.append((term, float(raw_weight)))
        if not matched:
            continue
        # Coverage plus a small multi-term bonus. The value is deterministic and
        # bounded but deliberately not described as a probability.
        coverage = sum(weight for _, weight in matched) / total_weight
        bonus = min(0.2, 0.05 * (len(matched) - 1))
        score = round(min(1.0, coverage + bonus), 6)
        if score >= float(min_score):
            candidates.append(
                TopicFacet(
                    topic_id=topic_id,
                    score=score,
                    matched_terms=tuple(sorted(term for term, _ in matched)),
                )
            )

    candidates.sort(key=lambda facet: (-facet.score, facet.topic_id))
    return TopicProjection(facets=tuple(candidates[:max_facets]))


def project_fact_topics(
    facts: Iterable[Mapping[str, Any]],
    *,
    text_field: str = "claim",
    max_facets: int = 3,
    min_score: float = 0.15,
) -> list[dict[str, Any]]:
    """Return fresh fact mappings with ephemeral `topic_projection` metadata."""
    if not isinstance(text_field, str) or not text_field.strip():
        raise ValueError("text_field must be a non-blank string")
    projected: list[dict[str, Any]] = []
    for fact in facts:
        if not isinstance(fact, Mapping):
            raise TypeError("every fact must be a mapping")
        copy = dict(fact)
        copy["topic_projection"] = classify_topics(
            fact.get(text_field), max_facets=max_facets, min_score=min_score
        ).to_dict()
        projected.append(copy)
    return projected


__all__ = [
    "ASSIGNED_BY",
    "SUGGESTED_STATUS",
    "TAXONOMY_VERSION",
    "TopicFacet",
    "TopicProjection",
    "classify_topics",
    "project_fact_topics",
    "validate_taxonomy",
]
