from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RC6 = "ed96a88369f841bdb2ffd79ca020acef174685fc"
RC5 = "51c205fe048fd69d39fcd47b43e042a50de432bc"
D2 = "b7e6574dd7aefa2f32783ab79054fac6b3b4109f"
REFRESH = ("ar", "de", "es", "fr", "hi", "it", "ja", "zh-CN")


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_rc6_localization_manifest_and_russian_parity():
    manifest = json.loads(_text("docs/status/rc6-translation-manifest.json"))
    assert manifest["english_source_checkpoint"] == RC6
    assert manifest["unchanged_d2_source_checkpoint"] == D2
    assert manifest["current_locales"] == ["ru"]
    assert manifest["refresh_needed_locales"] == list(REFRESH)
    assert manifest["refresh_needed_document_count"] == 64
    assert manifest["d5_inventory"] == {
        "total": 273,
        "current": 72,
        "english_only_by_design": 127,
        "refresh_needed": 64,
        "retired": 10,
    }
    assert manifest["reader_core_rc6_long_context_strategy_claim"] is True
    assert manifest["dedicated_reader_core_implemented_claim"] is False
    assert manifest["automatic_summarization_claim"] is False
    assert manifest["cross_document_rc7_claim"] is False
    assert manifest["evidence_admission_claim"] is False
    assert manifest["active_postgresql_runtime_claim"] is False
    assert manifest["nlnet_awarded_claim"] is False

    for path in manifest["russian_current_documents"]:
        text = _text(path)
        assert RC6 in text, path
        assert "CURRENT" in text, path
        assert "reader_core_rc6_long_context_strategy" in text or "RC-6" in text, path
        assert "active=false" in text, path

    root = _text("README.ru.md")
    for marker in (
        "working-set coverage != comprehension proof",
        "summary != evidence",
        "summary != verified fact",
        "summary != Canon admission",
        "dedicated_reader_core                  = false",
        "submitted / under review / not awarded",
    ):
        assert marker in root


def test_rc6_localization_preserves_historical_rc5_and_mixed_status():
    # The D1-D5 RC-5 validators stay executable historical evidence; RC-6 adds a layer.
    assert RC5 in _text("docs/TRANSLATION_STATUS.md")
    ledger = _text("docs/TRANSLATION_STATUS.md")
    assert f"Reader RC-6 immutable English source checkpoint:** `main@{RC6}`" in ledger
    assert "64 `REFRESH_NEEDED` localized documents" in ledger
    assert f"D2 source checkpoint:** `main@{D2}`" in ledger

    for locale in REFRESH:
        index = _text(f"docs/{locale}/README.md")
        assert "REFRESH_NEEDED" in index
        assert "d2-status: CURRENT" in index
        assert f"localization-index-source: main@{RC5}" in index
        assert RC6 not in index  # rich RC-5 translation intentionally not relabeled as current RC-6

    ru_index = _text("docs/ru/README.md")
    assert f"rc6-localization-index-source: main@{RC6}" in ru_index
    assert "rc6-status: CURRENT" in ru_index


def test_rc6_english_machine_truth_and_authority_firewall_are_documented():
    manifest = json.loads(_text("docs/status/implementation-manifest.json"))
    assert manifest["implemented_boundaries"]["reader_core_rc6_long_context_strategy"] is True
    assert manifest["implemented_boundaries"]["dedicated_reader_core"] is False
    rc6 = manifest["reader_core_rc6"]
    assert rc6["max_candidates_per_working_set"] == 128
    assert rc6["max_source_locators_per_working_set"] == 512
    assert rc6["candidate_atomicity"] is True
    assert rc6["direct_rc4_leaf_provenance"] is True
    assert rc6["caller_supplied_summary_only"] is True
    assert rc6["summary_fidelity"] == "SUMMARY"
    assert rc6["automatic_cross_document_reasoning"] is False
    assert rc6["evidence_admission"] is False
    assert rc6["truth_or_canon_authority"] is False

    for path in ("README.md", "docs/STATUS.md", "docs/IMPLEMENTATION_STATUS.md"):
        text = _text(path)
        for marker in (
            "reader_core_rc6_long_context_strategy",
            "working-set coverage != comprehension proof",
            "summary",
            "RC-7",
        ):
            assert marker in text, (path, marker)
