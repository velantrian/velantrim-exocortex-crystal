"""Regression tests for the privileged HTTP-ingest metadata boundary."""

import pytest

from core.api_ingest_policy import resolve_api_ingest


def _resolve(monkeypatch, refs):
    monkeypatch.setenv("VELANTRIM_API_PRIVILEGED_INGEST", "1")
    return resolve_api_ingest(
        source_status="EXTERNAL",
        import_mode=True,
        evidence_refs=refs,
    )


def test_privileged_ingest_deduplicates_and_marks_unresolved(monkeypatch):
    result = _resolve(
        monkeypatch,
        ["https://example.org/source", " https://example.org/source "],
    )
    metadata = result["metadata"]
    assert metadata["evidence_refs"] == ["https://example.org/source"]
    assert metadata["evidence_resolution"] == "DECLARED_NOT_RESOLVED"


@pytest.mark.parametrize(
    "refs, message",
    [
        ([123], "must be strings"),
        (["https://example.org/source\nforged-log-line"], "control characters"),
        (["javascript:alert(1)"], "unsupported evidence URI scheme"),
        (["https:///missing-host"], "requires a host"),
        (["file://"], "requires a path"),
        (["x" * 2049], "exceeds 2048"),
    ],
)
def test_privileged_ingest_rejects_malformed_references(monkeypatch, refs, message):
    with pytest.raises(ValueError, match=message):
        _resolve(monkeypatch, refs)


def test_privileged_ingest_limits_reference_count(monkeypatch):
    refs = [f"urn:velantrim:evidence:{i}" for i in range(33)]
    with pytest.raises(ValueError, match="at most 32"):
        _resolve(monkeypatch, refs)
