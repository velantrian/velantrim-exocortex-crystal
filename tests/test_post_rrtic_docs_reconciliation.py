from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURRENT_MAIN = "76a9493b8ba64b832472ef9bfc1f1c23ebe6654e"
RRTIC_DOC = "docs/architecture/READER_RETRIEVAL_TYPED_INSPECTION_CONTRACT_V1.md"


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_active_public_surfaces_reach_rrtic_v1_without_runtime_overclaim() -> None:
    required = {
        "README.md": (
            "Reader Retrieval Typed Inspection Contract v1",
            "RRTIC-v1 — architecture contract, not runtime",
            "reader_rc9_lexical_candidate_discovery = true",
            "runtime_authorization",
            "NLI_NEUTRAL_FILTER_GATE_FAILED",
        ),
        "docs/ARCHITECTURE_OVERVIEW.md": (
            "RRTIC-v1 typed inspection contract",
            "RC-9 deterministic lexical PRE-ADMISSION discovery",
            "RRTIC-v1 has no scalar truth/confidence score",
        ),
        "docs/ARCHITECTURE.md": (
            "RRTIC-v1 typed inspection contract",
            "RRTIC-v1 has no accept/reject policy",
            "semantic/hybrid Reader runtime",
        ),
        "docs/STATUS.md": (
            CURRENT_MAIN,
            "Reader Retrieval Typed Inspection Contract v1",
            "runtime_authorization=false",
            "NLI_NEUTRAL_FILTER_GATE_FAILED",
        ),
        "docs/IMPLEMENTATION_STATUS.md": (
            "Reader RC-9 lexical candidate discovery",
            "RRTIC runtime provider",
            "NOT AUTHORIZED / NOT IMPLEMENTED",
        ),
        "ROADMAP.md": (
            "RRTIC-v1 — completed architecture contract",
            "No next model, discriminator, reranker or Reader runtime implementation is automatically selected",
        ),
        "docs/REVIEWER_OVERVIEW.md": (
            "RRTIC-v1 typed inspection contract",
            "RRTIC-v1 is **not a new runtime stage**",
        ),
        "TEST_REPORT.md": (
            CURRENT_MAIN,
            "runtime_authorization",
            "2231 passed",
        ),
    }

    for relative, markers in required.items():
        text = _read(relative)
        for marker in markers:
            assert marker in text, f"{relative} missing post-RRTIC marker: {marker}"

    assert (ROOT / RRTIC_DOC).is_file()


def test_machine_manifest_distinguishes_current_architecture_from_historical_runtime() -> None:
    manifest = json.loads(_read("docs/status/implementation-manifest.json"))

    current = manifest["current_architecture_checkpoint"]
    assert current["commit"] == CURRENT_MAIN
    assert current["pull_request"] == 392
    assert current["post_merge_ci_run"] == 31771677028
    assert current["runtime_authorization"] is False

    historical_runtime = manifest["verified_runtime_checkpoint"]
    assert historical_runtime["commit"] == "bbd816c09dd39a02e6de6c1014438490572f40f6"
    assert manifest["tests"]["scope"] == "retained_verified_runtime_checkpoint"

    boundaries = manifest["implemented_boundaries"]
    assert boundaries["reader_core_rc7_cross_document_links"] is True
    # RC-9 is a separately documented implemented component. The frozen RC-10
    # machine contract intentionally does not extend the legacy boundary-flag set.
    assert "reader_rc9_lexical_candidate_discovery" not in boundaries
    rc9 = manifest["reader_rc9_lexical_candidate_discovery"]
    assert rc9["status"] == "IMPLEMENTED"
    assert rc9["pre_admission_only"] is True
    assert rc9["identity_authority"] is False
    assert rc9["evidence_admission"] is False
    assert rc9["canon_authority"] is False
    assert boundaries["semantic_hybrid_reader_runtime"] is False
    assert boundaries["nli_reader_runtime_filter"] is False
    assert boundaries["rrtic_runtime_provider"] is False
    assert boundaries["dedicated_reader_core"] is False

    rrtic = manifest["reader_retrieval_typed_inspection_contract_v1"]
    assert rrtic["status"] == "FROZEN_ARCHITECTURE_CONTRACT"
    assert rrtic["relation_family_count"] == 6
    assert rrtic["qualifier_dimension_count"] == 10
    assert rrtic["hard_filter"] is False
    assert rrtic["reranking"] is False
    assert rrtic["model_execution"] is False
    assert rrtic["identity_claimed"] is False
    assert rrtic["evidence_admitted"] is False
    assert rrtic["adjudication_performed"] is False
    assert rrtic["runtime_authorization"] is False
    assert rrtic["replaces_rc5"] is False


def test_grant_and_localization_boundaries_remain_unchanged() -> None:
    manifest = json.loads(_read("docs/status/implementation-manifest.json"))

    grant = manifest["grant"]
    assert grant["submitted"] is True
    assert grant["under_review"] is True
    assert grant["awarded"] is False
    assert grant["budget_changed"] is False

    docs = manifest["documentation"]
    assert docs["localized_readme_source_checkpoint"] == (
        "51c205fe048fd69d39fcd47b43e042a50de432bc"
    )
    assert docs["full_parity_current_locales"] == ["de", "ru"]
    assert docs["full_parity_refresh_needed_locales"] == [
        "ar",
        "es",
        "fr",
        "hi",
        "it",
        "ja",
        "zh-CN",
    ]
