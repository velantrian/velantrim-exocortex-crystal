from __future__ import annotations

from dataclasses import fields
from types import SimpleNamespace

import pytest

from core.reader_lexical_discovery import (
    MAX_READER_LEXICAL_RECORDS,
    MAX_READER_LEXICAL_TOP_K,
    RETRIEVAL_METHOD,
    ReaderLexicalIndex,
    ReaderLexicalMatch,
    ReaderLexicalRecord,
    normalize_reader_lexical_text,
    tokenize_reader_lexical_text,
)


def record(candidate_id: str, text: str, *, document_id: str | None = None, session_id: str | None = None, restricted: bool = False, sensitivity: str | None = None) -> ReaderLexicalRecord:
    return ReaderLexicalRecord(
        session_id=session_id or f"session-{candidate_id}",
        candidate_id=candidate_id,
        document_id=document_id or f"doc-{candidate_id}",
        source_uri=f"file:///{candidate_id}.txt",
        source_sha256=(candidate_id.encode().hex() + "0" * 64)[:64],
        proposition=text,
        restricted=restricted,
        sensitivity=sensitivity,
    )


def test_normalization_and_tokenization_preserve_material_lexical_distinctions():
    assert normalize_reader_lexical_text("  MUST\tNot  K  ") == "must not k"
    tokens = tokenize_reader_lexical_text("must may all most 2024 2025 Python 3.11 10 mg 100 mg 80 °C")
    for expected in ("must", "may", "all", "most", "2024", "2025", "3.11", "10", "100", "80", "c"):
        assert expected in tokens
    with pytest.raises(ValueError, match="string"):
        normalize_reader_lexical_text(3)  # type: ignore[arg-type]


def test_record_contract_and_rc4_snapshot_surface():
    item = record("c", " statement ", restricted=True, sensitivity=" private ")
    assert item.proposition == "statement"
    assert item.sensitivity == "private"
    assert item.key == ("session-c", "c")
    assert item.sort_key[-2:] == ("session-c", "c")

    source = SimpleNamespace(document_id="doc-x", source_uri="file:///x", source_sha256="a" * 64)
    candidate = SimpleNamespace(
        primary_locator=SimpleNamespace(source=source),
        session_id="s",
        candidate_id="id",
        proposition="Text",
        restricted=False,
        sensitivity=None,
    )
    snap = ReaderLexicalRecord.from_candidate(candidate)
    assert snap.document_id == "doc-x"
    with pytest.raises(ValueError, match="RC-4"):
        ReaderLexicalRecord.from_candidate(object())

    required = ("session_id", "candidate_id", "document_id", "source_uri", "source_sha256", "proposition")
    kwargs = dict(session_id="s", candidate_id="c", document_id="d", source_uri="u", source_sha256="a" * 64, proposition="p")
    for name in required:
        bad = dict(kwargs)
        bad[name] = " "
        with pytest.raises(ValueError, match=name):
            ReaderLexicalRecord(**bad)
    non_string = dict(kwargs)
    non_string["session_id"] = 7
    with pytest.raises(ValueError, match="session_id must be a string"):
        ReaderLexicalRecord(**non_string)  # type: ignore[arg-type]
    bad_sha = dict(kwargs); bad_sha["source_sha256"] = "not-a-digest"
    with pytest.raises(ValueError, match="64-character"):
        ReaderLexicalRecord(**bad_sha)
    with pytest.raises(ValueError, match="restricted"):
        ReaderLexicalRecord(**kwargs, restricted=1)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="sensitivity"):
        ReaderLexicalRecord(**kwargs, sensitivity=" ")


def test_index_validation_empty_behavior_and_method():
    with pytest.raises(ValueError, match="iterable"):
        ReaderLexicalIndex("bad")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="iterable"):
        ReaderLexicalIndex(3)  # type: ignore[arg-type]
    base = record("a", "alpha")
    with pytest.raises(ValueError, match="at most"):
        ReaderLexicalIndex((base,) * (MAX_READER_LEXICAL_RECORDS + 1))
    with pytest.raises(ValueError, match="ReaderLexicalRecord"):
        ReaderLexicalIndex((object(),))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="unique"):
        ReaderLexicalIndex((base, base))

    empty = ReaderLexicalIndex(())
    assert empty.records == ()
    assert empty.method == RETRIEVAL_METHOD
    assert empty.discover(base) == ()
    assert empty._bm25(("alpha",), {}, 0) == 0.0  # type: ignore[arg-type]


def test_discovery_is_deterministic_bounded_cross_document_and_authority_safe():
    query = record("q", "alpha beta beta 2024 must not", document_id="doc-q")
    same = record("same", "alpha beta", document_id="doc-q")
    self_copy = record("q", "alpha beta", document_id="other", session_id=query.session_id)
    a = record("a", "alpha beta 2024 must not", document_id="doc-a", restricted=True, sensitivity="r")
    b = record("b", "alpha beta 2024 may", document_id="doc-b")
    c = record("c", "unrelated text", document_id="doc-c")
    index = ReaderLexicalIndex((b, c, same, a, self_copy))

    first = index.discover(query, k=2)
    second = index.discover(query, k=2)
    assert first == second
    assert [m.candidate_id for m in first] == ["a", "b"]
    assert [m.rank for m in first] == [1, 2]
    assert first[0].retrieval_method == RETRIEVAL_METHOD
    assert first[0].restricted is True and first[0].sensitivity == "r"
    assert "not" in first[0].matched_terms and "2024" in first[0].matched_terms
    assert first[0].lexical_score > first[1].lexical_score > 0
    forbidden = {"truth_score", "confidence_of_truth", "corroboration_score", "same_claim"}
    assert forbidden.isdisjoint({f.name for f in fields(ReaderLexicalMatch)})

    with_same_doc = index.discover(query, k=5, cross_document_only=False)
    assert "same" in {m.candidate_id for m in with_same_doc}
    assert "q" not in {m.candidate_id for m in with_same_doc}
    assert index.discover(record("empty", "..."), k=5) == ()

    duplicate_query = record("dup", "alpha alpha alpha", document_id="doc-dup")
    single_query = record("single", "alpha", document_id="doc-single")
    assert [m.candidate_id for m in index.discover(duplicate_query)] == [m.candidate_id for m in index.discover(single_query)]


def test_discovery_validation_and_stable_tie_breaking():
    a = record("a", "same token", document_id="doc-a")
    b = record("b", "same token", document_id="doc-b")
    query = record("q", "same token", document_id="doc-q")
    index = ReaderLexicalIndex((b, a))
    assert [m.candidate_id for m in index.discover(query)] == ["a", "b"]
    with pytest.raises(ValueError, match="query"):
        index.discover(object())  # type: ignore[arg-type]
    for bad in (True, 0, MAX_READER_LEXICAL_TOP_K + 1, 1.5):
        with pytest.raises(ValueError, match="k must"):
            index.discover(query, k=bad)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="cross_document_only"):
        index.discover(query, cross_document_only=1)  # type: ignore[arg-type]