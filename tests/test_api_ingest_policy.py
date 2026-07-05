"""Tests for core/api_ingest_policy.py — HTTP ingest epistemic hardening."""
import pytest

from core.api_ingest_policy import resolve_api_ingest, privileged_ingest_enabled


def test_public_ingest_defaults_to_user_reported():
    out = resolve_api_ingest(source_status=None)
    assert out["source_status"] == "USER_REPORTED"


def test_public_ingest_rejects_privileged_source_status():
    with pytest.raises(ValueError, match="privileged source_status"):
        resolve_api_ingest(source_status="EXTERNAL")


def test_privileged_ingest_requires_env_import_mode_and_refs(monkeypatch):
    monkeypatch.setenv("VELANTRIM_API_PRIVILEGED_INGEST", "1")
    with pytest.raises(ValueError, match="import_mode"):
        resolve_api_ingest(source_status="EXTERNAL", import_mode=False,
                           evidence_refs=["doc.txt"])
    out = resolve_api_ingest(
        source_status="DERIVED", import_mode=True,
        evidence_refs=[" corpus.jsonl "],
    )
    assert out["source_status"] == "DERIVED"
    assert out["metadata"]["evidence_refs"] == ["corpus.jsonl"]
    assert out["metadata"]["admission_path"] == "api_privileged_import"


def test_privileged_ingest_disabled_even_with_import_mode(monkeypatch):
    monkeypatch.delenv("VELANTRIM_API_PRIVILEGED_INGEST", raising=False)
    with pytest.raises(ValueError, match="VELANTRIM_API_PRIVILEGED_INGEST"):
        resolve_api_ingest(source_status="OBSERVED", import_mode=True,
                           evidence_refs=["x.txt"])


def test_public_ingest_allows_llm_output_status():
    out = resolve_api_ingest(source_status="LLM_OUTPUT")
    assert out["source_status"] == "LLM_OUTPUT"


def test_privileged_ingest_enabled_flag(monkeypatch):
    monkeypatch.setenv("VELANTRIM_API_PRIVILEGED_INGEST", "1")
    assert privileged_ingest_enabled() is True
