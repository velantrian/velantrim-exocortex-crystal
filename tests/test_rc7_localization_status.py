from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "ab3ad31c437647535030e371d58f456faf14017b"
RC6_SOURCE = "ed96a88369f841bdb2ffd79ca020acef174685fc"
D2_SOURCE = "b7e6574dd7aefa2f32783ab79054fac6b3b4109f"

RUSSIAN_DOCS = (
    "README.ru.md",
    "docs/ru/README.md",
    "docs/ru/STATUS.md",
    "docs/ru/IMPLEMENTATION_STATUS.md",
    "docs/ru/ARCHITECTURE_OVERVIEW.md",
    "docs/ru/STORAGE_AND_AUTHORITY_BOUNDARIES.md",
    "docs/ru/GRANT_OVERVIEW.md",
    "docs/ru/GLOSSARY.md",
    "docs/ru/EXTENDED_REFERENCE_GUIDE.md",
)
MACHINE_DOCS = (
    "README.ru.md",
    "docs/ru/README.md",
    "docs/ru/STATUS.md",
    "docs/ru/IMPLEMENTATION_STATUS.md",
)


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_rc7_localization_manifest_is_bounded_and_honest():
    manifest = json.loads(_text("docs/status/rc7-translation-manifest.json"))
    assert manifest["phase"] == "RC7_LOCALIZATION"
    assert manifest["tracking_issue"] == 371
    assert manifest["pull_request"] == 372
    assert manifest["english_source_checkpoint"] == SOURCE
    assert manifest["english_checkpoint_ci"] == 31570690153
    assert manifest["previous_rc6_source_checkpoint"] == RC6_SOURCE
    assert manifest["unchanged_d2_source_checkpoint"] == D2_SOURCE
    assert manifest["current_locales"] == ["ru"]
    assert manifest["refresh_needed_locales"] == ["ar", "de", "es", "fr", "hi", "it", "ja", "zh-CN"]
    assert set(manifest["russian_current_documents"]) == set(RUSSIAN_DOCS)
    assert manifest["refresh_needed_document_count"] == 64
    # Immutable RC-7 manifest records the inventory at that historical checkpoint.
    assert manifest["d5_inventory"] == {"total": 273, "current": 72, "english_only_by_design": 127, "refresh_needed": 64, "retired": 10}
    assert manifest["reader_core_rc6_long_context_strategy_claim"] is True
    assert manifest["reader_core_rc7_cross_document_links_claim"] is True
    for key in (
        "dedicated_reader_core_implemented_claim",
        "automatic_semantic_matching_claim",
        "claim_identity_claim",
        "automatic_corroboration_claim",
        "embeddings_or_ann_claim",
        "evidence_admission_claim",
        "contradiction_resolution_claim",
        "active_postgresql_runtime_claim",
        "nlnet_awarded_claim",
        "approved_budget_claim",
        "budget_change_claim",
    ):
        assert manifest[key] is False


def test_russian_rc7_machine_surfaces_pin_exact_source():
    for path in MACHINE_DOCS:
        text = _text(path)
        assert SOURCE in text, path
        assert "reader_core_rc7_cross_document_links" in text, path
        assert "dedicated_reader_core" in text, path


def test_all_russian_reader_surfaces_preserve_rc7_authority_firewall():
    required = (
        SOURCE,
        "cross-document link",
        "same-topic",
        "possible-same-claim",
        "similarity signal",
        "repetition across sources",
        "active=false",
        "submitted / under review / not awarded",
    )
    for path in RUSSIAN_DOCS:
        text = _text(path)
        for marker in required:
            assert marker in text, (path, marker)


def test_rc7_russian_refresh_preserves_legacy_markers_and_rich_root():
    root = _text("README.ru.md")
    assert "localization-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc" in root
    assert f"rc6-localization-source: main@{RC6_SOURCE}" in root
    assert f"rc7-localization-source: main@{SOURCE}" in root
    assert "localization-status: CURRENT" in root
    assert len(root) >= 6000
    assert root.count("```text") >= 7
    assert root.count("|") >= 20
    for marker in ("L0", "L1", "L2", "L3", "Guardian", "TruthGate", "TrustSnapshot", "CanonicalView", "HTTP /ask", "CLI ask", "MCP search"):
        assert marker in root

    index = _text("docs/ru/README.md")
    for marker in (
        "d1-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc",
        f"d2-source: main@{D2_SOURCE}",
        "d3-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc",
        "d4-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc",
        "d5-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc",
        f"rc7-localization-index-source: main@{SOURCE}",
    ):
        assert marker in index


def test_translation_ledger_records_rc7_without_erasing_history():
    ledger = _text("docs/TRANSLATION_STATUS.md")
    normalized = " ".join(ledger.split())
    assert f"Reader RC-7 immutable English source checkpoint:** `main@{SOURCE}`" in ledger
    assert f"Reader RC-6 immutable English source checkpoint:** `main@{RC6_SOURCE}`" in ledger
    assert "Reader RC-5 immutable English source checkpoint" in ledger
    assert "64 `REFRESH_NEEDED` localized documents" in ledger
    # Current ledger may grow as new English-only reference material is added. It must report
    # the executable current inventory without rewriting the immutable RC-7 manifest above.
    assert "279 total = 72 CURRENT + 133 ENGLISH_ONLY_BY_DESIGN + 64 REFRESH_NEEDED + 10 RETIRED" in ledger
    assert "D2 reviewer/safety translations remain current across all nine supported locales" in normalized
    assert "does not claim later RC-8/RC-9 meaning" in normalized
