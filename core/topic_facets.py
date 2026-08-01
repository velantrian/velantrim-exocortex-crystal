"""Advisory, non-authoritative topic facets.

Facets help navigation and filtering. They never change epistemic state,
truth status, evidence, contradiction decisions, or Canon membership.
The module is intentionally storage-agnostic: callers may persist the returned
metadata through their existing write path after applying normal authorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence
import re

FACET_METADATA_KEY = "topic_facets"
_LABEL_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
_ALLOWED_ORIGINS = frozenset({"curator", "rule", "model", "import"})


@dataclass(frozen=True, order=True)
class TopicFacet:
    """One advisory label with provenance and bounded confidence."""

    label: str
    score: float = 1.0
    origin: str = "curator"

    def __post_init__(self) -> None:
        label = normalize_label(self.label)
        if not _LABEL_RE.fullmatch(label):
            raise ValueError("facet label must match [a-z0-9][a-z0-9._-]{0,63}")
        if not isinstance(self.score, (int, float)) or isinstance(self.score, bool):
            raise TypeError("facet score must be numeric")
        score = float(self.score)
        if not 0.0 <= score <= 1.0:
            raise ValueError("facet score must be between 0 and 1")
        if self.origin not in _ALLOWED_ORIGINS:
            raise ValueError(f"facet origin must be one of {sorted(_ALLOWED_ORIGINS)}")
        object.__setattr__(self, "label", label)
        object.__setattr__(self, "score", score)

    def to_dict(self) -> dict[str, Any]:
        return {"label": self.label, "score": self.score, "origin": self.origin}



def normalize_label(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("facet label must be a string")
    return value.strip().lower().replace(" ", "-")



def canonicalize_facets(facets: Iterable[TopicFacet]) -> tuple[TopicFacet, ...]:
    """Deduplicate by label, keeping the highest-scored assignment.

    Equal scores prefer curator over rule, rule over import, and import over
    model. This is only deterministic navigation metadata, not a trust ranking.
    """
    origin_rank = {"curator": 3, "rule": 2, "import": 1, "model": 0}
    chosen: dict[str, TopicFacet] = {}
    for facet in facets:
        if not isinstance(facet, TopicFacet):
            raise TypeError("facets must contain TopicFacet values")
        current = chosen.get(facet.label)
        if current is None or (facet.score, origin_rank[facet.origin]) > (
            current.score,
            origin_rank[current.origin],
        ):
            chosen[facet.label] = facet
    return tuple(chosen[label] for label in sorted(chosen))



def attach_facets(
    record: Mapping[str, Any], facets: Iterable[TopicFacet]
) -> dict[str, Any]:
    """Return a copy of a fact-like record with canonical facet metadata.

    No authority-bearing field is modified. Existing metadata is copied.
    """
    updated = dict(record)
    metadata = dict(record.get("metadata") or {})
    metadata[FACET_METADATA_KEY] = [item.to_dict() for item in canonicalize_facets(facets)]
    updated["metadata"] = metadata
    return updated



def read_facets(record: Mapping[str, Any]) -> tuple[TopicFacet, ...]:
    raw = (record.get("metadata") or {}).get(FACET_METADATA_KEY, ())
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        return ()
    parsed: list[TopicFacet] = []
    for item in raw:
        if not isinstance(item, Mapping):
            continue
        try:
            parsed.append(
                TopicFacet(
                    label=item.get("label", ""),
                    score=item.get("score", 0.0),
                    origin=item.get("origin", "model"),
                )
            )
        except (TypeError, ValueError):
            continue
    return canonicalize_facets(parsed)



def matches_facets(
    record: Mapping[str, Any],
    *,
    any_of: Iterable[str] = (),
    all_of: Iterable[str] = (),
    min_score: float = 0.0,
) -> bool:
    """Evaluate an advisory facet filter without affecting retrieval authority."""
    if not 0.0 <= min_score <= 1.0:
        raise ValueError("min_score must be between 0 and 1")
    scores = {item.label: item.score for item in read_facets(record)}
    wanted_any = {normalize_label(value) for value in any_of}
    wanted_all = {normalize_label(value) for value in all_of}
    if wanted_any and not any(scores.get(label, -1.0) >= min_score for label in wanted_any):
        return False
    return all(scores.get(label, -1.0) >= min_score for label in wanted_all)



def filter_records(
    records: Iterable[Mapping[str, Any]],
    *,
    any_of: Iterable[str] = (),
    all_of: Iterable[str] = (),
    min_score: float = 0.0,
) -> list[Mapping[str, Any]]:
    return [
        record
        for record in records
        if matches_facets(record, any_of=any_of, all_of=all_of, min_score=min_score)
    ]


__all__ = [
    "FACET_METADATA_KEY",
    "TopicFacet",
    "attach_facets",
    "canonicalize_facets",
    "filter_records",
    "matches_facets",
    "normalize_label",
    "read_facets",
]
