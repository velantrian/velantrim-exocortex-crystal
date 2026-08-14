from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_readme_is_human_first_and_routes_ai_agents_explicitly() -> None:
    readme = _text("README.md")

    for marker in (
        "## 💠 Memory and evidence infrastructure that keeps retrieval separate from truth",
        "Special for AI",
        "./docs/ai/README.md",
        "Deep System Overview",
        "./docs/OVERVIEW.md",
        "## 🗺️ Architecture in one view",
        "## 🌳 Project tree",
        "## 📊 What exists today",
        "## 🧠 How Crystal differs from common memory/retrieval patterns",
        "## 🚫 What Crystal does **not** claim",
        "## 📚 Where to read next",
    ):
        assert marker in readme, marker

    for marker in (
        "Reader Retrieval Typed Inspection Contract v1",
        "RRTIC-v1 — architecture contract, not runtime",
        "reader_core_rc7_cross_document_links   = true",
        "reader_rc9_lexical_candidate_discovery = true",
        "dedicated_reader_core                  = false",
        "semantic_hybrid_reader_runtime         = false",
        "rrtic_runtime_authorization            = false",
        "retrieval match          != evidence",
        "similarity               != identity",
        "repetition               != corroboration",
        "cross-document candidate != Canon relation",
        "no automatic semantic matching",
        "NLI_NEUTRAL_FILTER_GATE_FAILED",
        "submitted / under review / not awarded",
        "active=false",
    ):
        assert marker in readme, marker

    # ASCII diagrams and tables consume source lines, but the landing page still remains
    # bounded; detailed evidence belongs in STATUS / TEST_REPORT / eval documents.
    assert len(readme.splitlines()) < 360


def test_deep_overview_is_human_explanation_not_machine_authority() -> None:
    overview = _text("docs/OVERVIEW.md")

    for marker in (
        "# 💠 Velantrim Exo-Cortex Crystal — Deep System Overview",
        "## 🧠 Mental model",
        "## 🧠 Mindmap",
        "## 🌳 Reader capability tree",
        "## 🧬 RRTIC-v1 in human terms",
        "## 🛡️ The authority firewall",
        "## 🧱 Human / AI / Machine / Evidence documentation architecture",
        "## 🆚 Crystal, Letta/MemGPT and Graphiti",
        "architectural emphasis, not overall product quality",
        "do not establish benchmark superiority",
        "[Special for AI](./ai/README.md)",
    ):
        assert marker in overview, marker

    assert "submitted / under review / not awarded" in overview


def test_ai_entrypoint_keeps_volatile_provenance_live_resolved() -> None:
    ai = _text("docs/ai/README.md")

    for marker in (
        "# 🤖 Crystal — Special for AI / Agent Entry Point",
        "machine/agent router, not a human landing page",
        "## 1. Required read order",
        "implementation-manifest.json",
        "## 2. Source-of-truth hierarchy",
        "## 3. Durable truth + live provenance resolution",
        "repository_head: RESOLVE_LIVE_GITHUB",
        "repository_ci: RESOLVE_LIVE_GITHUB",
        "documentation_lifecycle: RESOLVE_LIVE_GITHUB",
        "active_milestone: RESOLVE_LIVE_GITHUB",
        "next_milestone: RESOLVE_LIVE_GITHUB",
        "current_architecture_checkpoint: 76a9493b8ba64b832472ef9bfc1f1c23ebe6654e",
        "## 5. Permanent authority invariants",
        "## 6. Forbidden inferences",
        "historical_sha_is_live_head: true",
        "static_ai_snapshot_is_live_repository_provenance: true",
        "grant_submission_is_grant_award: true",
        "closed_milestone_is_active_work: true",
        "residual_issue_is_auto_selected: true",
        "## 8. Documentation interface architecture",
        "## 11. Current stop boundary",
    ):
        assert marker in ai, marker

    assert "No model, discriminator, reranker, Reader backend" in ai

    for volatile_marker in (
        "repository_main_at_last_audit:",
        "repository_main_at_milestone_start:",
        "latest_completed_docs_issue:",
        "latest_completed_docs_pr:",
        "current_docs_tracking_issue:",
        "active_milestone: none",
        "next_milestone_selected: false",
    ):
        assert volatile_marker not in ai, volatile_marker


def test_ai_current_state_resolves_volatile_lifecycle_live() -> None:
    state = _text("docs/ai/CURRENT_STATE.md")

    for marker in (
        "**Repository HEAD:** `RESOLVE_LIVE_GITHUB`",
        "**Repository lifecycle provenance:** `RESOLVE_LIVE_GITHUB`",
        "**Current architecture checkpoint:** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e`",
        "**Active milestone:** `RESOLVE_LIVE_GITHUB`",
        "**Next milestone selected:** `RESOLVE_LIVE_GITHUB`",
        "repository HEAD + exact CI       → RESOLVE_LIVE_GITHUB",
        "latest completed PR/issue        → RESOLVE_LIVE_GITHUB",
        "active milestone / next selected → RESOLVE_LIVE_GITHUB",
        "This file does not authorize or select the next workstream",
    ):
        assert marker in state, marker

    for volatile_marker in (
        "Repository main at last completed docs audit",
        "4628e6fe231103a57c86df8b157b87b8b6b183f2",
        "Latest completed docs milestone:",
        "Latest completed documentation closure:",
        "#395 = CLOSED / completed",
        "#396 = MERGED",
        "active_milestone = NONE",
        "next_milestone_selected = false",
    ):
        assert volatile_marker not in state, volatile_marker


def test_documentation_map_exposes_four_interfaces() -> None:
    docmap = _text("docs/DOCUMENTATION_MAP.md")

    for marker in (
        "## 🧬 One project truth, four interfaces",
        "## 👤 Human path",
        "OVERVIEW.md",
        "## 🤖 AI / agent path",
        "Special for AI",
        "## ⚙ Machine-readable truth",
        "implementation-manifest.json",
        "## 🧾 Current state and evidence",
        "overview != current state != machine truth != evidence != history",
    ):
        assert marker in docmap, marker


def test_external_comparison_does_not_claim_superiority() -> None:
    combined = "\n".join((_text("README.md"), _text("docs/OVERVIEW.md"))).lower()

    for forbidden in (
        "crystal is superior to letta",
        "crystal is superior to memgpt",
        "crystal is superior to graphiti",
        "crystal is better than letta",
        "crystal is better than graphiti",
    ):
        assert forbidden not in combined
