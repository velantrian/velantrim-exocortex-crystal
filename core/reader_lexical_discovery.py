"""Deterministic PRE-ADMISSION lexical candidate discovery for Reader RC-9.

The ranker answers only "which Reader proposition candidates are worth inspection?".
A lexical match is not evidence, identity, corroboration, a Canon relation, or an
adjudicated contradiction. The module is in-memory, dependency-free, and performs
no persistence, network access, evidence admission, or truth-state mutation.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import math
import re
import unicodedata
from typing import Iterable, Optional

RETRIEVAL_METHOD = "reader_rc9_bm25_lexical_v1"
MAX_READER_LEXICAL_RECORDS = 100_000
MAX_READER_LEXICAL_TOP_K = 1_000

_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_TOKEN_RE = re.compile(
    r"\d+(?:[.,]\d+)*(?:%|°[\w]+)?|[\w]+(?:[-'][\w]+)*",
    re.UNICODE,
)


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    value = value.strip()
    if not value:
        raise ValueError(f"{field_name} must be non-empty")
    return value


def normalize_reader_lexical_text(text: str) -> str:
    """Conservatively normalize text without deleting epistemically relevant words."""
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def tokenize_reader_lexical_text(text: str) -> tuple[str, ...]:
    """Stable lexical tokens; no stop-word removal or semantic normalization."""
    normalized = normalize_reader_lexical_text(text)
    return tuple(_TOKEN_RE.findall(normalized))


@dataclass(frozen=True)
class ReaderLexicalRecord:
    """Minimal auditable PRE-ADMISSION proposition representation for retrieval."""

    session_id: str
    candidate_id: str
    document_id: str
    source_uri: str
    source_sha256: str
    proposition: str
    restricted: bool = False
    sensitivity: Optional[str] = None

    def __post_init__(self) -> None:
        for name in (
            "session_id",
            "candidate_id",
            "document_id",
            "source_uri",
            "source_sha256",
            "proposition",
        ):
            object.__setattr__(self, name, _required_text(getattr(self, name), name))
        digest = self.source_sha256
        if not _SHA256_RE.fullmatch(digest):
            raise ValueError("source_sha256 must be a 64-character hexadecimal SHA-256")
        object.__setattr__(self, "source_sha256", digest.lower())
        if not isinstance(self.restricted, bool):
            raise ValueError("restricted must be a bool")
        if self.sensitivity is not None:
            object.__setattr__(self, "sensitivity", _required_text(self.sensitivity, "sensitivity"))

    @classmethod
    def from_candidate(cls, candidate: object) -> "ReaderLexicalRecord":
        """Snapshot the public RC-4 candidate surface without importing another authority path."""
        try:
            source = candidate.primary_locator.source  # type: ignore[attr-defined]
            session_id = candidate.session_id  # type: ignore[attr-defined]
            candidate_id = candidate.candidate_id  # type: ignore[attr-defined]
            proposition = candidate.proposition  # type: ignore[attr-defined]
            restricted = candidate.restricted  # type: ignore[attr-defined]
            sensitivity = candidate.sensitivity  # type: ignore[attr-defined]
        except AttributeError as exc:
            raise ValueError("candidate must expose the RC-4 Reader proposition surface") from exc
        return cls(
            session_id=session_id,
            candidate_id=candidate_id,
            document_id=source.document_id,
            source_uri=source.source_uri,
            source_sha256=source.source_sha256,
            proposition=proposition,
            restricted=restricted,
            sensitivity=sensitivity,
        )

    @property
    def key(self) -> tuple[str, str]:
        return (self.session_id, self.candidate_id)

    @property
    def sort_key(self) -> tuple[str, str, str, str, str]:
        return (
            self.document_id,
            self.source_uri,
            self.source_sha256,
            self.session_id,
            self.candidate_id,
        )


@dataclass(frozen=True)
class ReaderLexicalMatch:
    """Ranked inspection candidate. Deliberately contains no epistemic verdict."""

    query_session_id: str
    query_candidate_id: str
    query_document_id: str
    candidate_session_id: str
    candidate_id: str
    candidate_document_id: str
    candidate_source_uri: str
    candidate_source_sha256: str
    lexical_score: float
    rank: int
    retrieval_method: str
    matched_terms: tuple[str, ...]
    restricted: bool
    sensitivity: Optional[str]


class ReaderLexicalIndex:
    """Bounded deterministic in-memory BM25 index over Reader proposition records."""

    def __init__(self, records: Iterable[ReaderLexicalRecord]) -> None:
        if isinstance(records, (str, bytes)):
            raise ValueError("records must be an iterable of ReaderLexicalRecord values")
        try:
            items = tuple(records)
        except TypeError as exc:
            raise ValueError("records must be an iterable of ReaderLexicalRecord values") from exc
        if len(items) > MAX_READER_LEXICAL_RECORDS:
            raise ValueError(f"records must contain at most {MAX_READER_LEXICAL_RECORDS} values")
        if any(not isinstance(item, ReaderLexicalRecord) for item in items):
            raise ValueError("records must contain ReaderLexicalRecord values")
        keys = [item.key for item in items]
        if len(set(keys)) != len(keys):
            raise ValueError("records must have unique session_id/candidate_id keys")

        self._records = tuple(sorted(items, key=lambda item: item.sort_key))
        self._term_counts = tuple(Counter(tokenize_reader_lexical_text(item.proposition)) for item in self._records)
        self._lengths = tuple(sum(counts.values()) for counts in self._term_counts)
        self._avg_len = sum(self._lengths) / len(self._lengths) if self._lengths else 0.0
        document_frequency: Counter[str] = Counter()
        for counts in self._term_counts:
            document_frequency.update(counts.keys())
        self._document_frequency = dict(document_frequency)

    @property
    def records(self) -> tuple[ReaderLexicalRecord, ...]:
        return self._records

    @property
    def method(self) -> str:
        return RETRIEVAL_METHOD

    def discover(
        self,
        query: ReaderLexicalRecord,
        *,
        k: int = 5,
        cross_document_only: bool = True,
    ) -> tuple[ReaderLexicalMatch, ...]:
        if not isinstance(query, ReaderLexicalRecord):
            raise ValueError("query must be a ReaderLexicalRecord")
        if isinstance(k, bool) or not isinstance(k, int) or not 1 <= k <= MAX_READER_LEXICAL_TOP_K:
            raise ValueError(f"k must be an integer in [1, {MAX_READER_LEXICAL_TOP_K}]")
        if not isinstance(cross_document_only, bool):
            raise ValueError("cross_document_only must be a bool")

        query_terms = tuple(sorted(set(tokenize_reader_lexical_text(query.proposition))))
        if not query_terms or not self._records:
            return ()

        scored: list[tuple[float, tuple[str, str, str, str, str], ReaderLexicalRecord, tuple[str, ...]]] = []
        for record, counts, length in zip(self._records, self._term_counts, self._lengths):
            if record.key == query.key:
                continue
            if cross_document_only and record.document_id == query.document_id:
                continue
            matched_terms = tuple(term for term in query_terms if counts.get(term, 0) > 0)
            if not matched_terms:
                continue
            score = self._bm25(matched_terms, counts, length)
            scored.append((score, record.sort_key, record, matched_terms))

        scored.sort(key=lambda item: (-item[0], item[1]))
        matches: list[ReaderLexicalMatch] = []
        for rank, (score, _, record, matched_terms) in enumerate(scored[:k], 1):
            matches.append(
                ReaderLexicalMatch(
                    query_session_id=query.session_id,
                    query_candidate_id=query.candidate_id,
                    query_document_id=query.document_id,
                    candidate_session_id=record.session_id,
                    candidate_id=record.candidate_id,
                    candidate_document_id=record.document_id,
                    candidate_source_uri=record.source_uri,
                    candidate_source_sha256=record.source_sha256,
                    lexical_score=round(score, 12),
                    rank=rank,
                    retrieval_method=RETRIEVAL_METHOD,
                    matched_terms=matched_terms,
                    restricted=record.restricted,
                    sensitivity=record.sensitivity,
                )
            )
        return tuple(matches)

    def _bm25(self, terms: tuple[str, ...], counts: Counter[str], length: int) -> float:
        n_docs = len(self._records)
        if n_docs == 0:
            return 0.0
        k1 = 1.2
        b = 0.75
        avg_len = self._avg_len or 1.0
        score = 0.0
        for term in terms:
            tf = counts[term]
            df = self._document_frequency[term]
            idf = math.log(1.0 + (n_docs - df + 0.5) / (df + 0.5))
            denominator = tf + k1 * (1.0 - b + b * length / avg_len)
            score += idf * (tf * (k1 + 1.0) / denominator)
        return score


__all__ = [
    "MAX_READER_LEXICAL_RECORDS",
    "MAX_READER_LEXICAL_TOP_K",
    "RETRIEVAL_METHOD",
    "ReaderLexicalIndex",
    "ReaderLexicalMatch",
    "ReaderLexicalRecord",
    "normalize_reader_lexical_text",
    "tokenize_reader_lexical_text",
]
