"""Regression contract for issue #214 supply-chain verification hardening."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = (
    ROOT / ".github/workflows/ci.yml",
    ROOT / ".github/workflows/l3-benchmark-history.yml",
    ROOT / ".github/workflows/postgresql-integration.yml",
)
EXPECTED_ACTION_REFS = {
    "actions/checkout": "34e114876b0b11c390a56381ad16ebd13914f8d5",
    "actions/setup-python": "a26af69be951a213d495a4c3e4e4022e16d87065",
    "actions/upload-artifact": "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
    "gitleaks/gitleaks-action": "e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e",
}
USE_RE = re.compile(r"^\s*-?\s*uses:\s*([^@\s]+)@([0-9a-f]{40})(?:\s+#\s+.+)?$")


def test_all_committed_workflow_actions_are_immutable_reviewed_refs():
    seen: set[str] = set()
    for workflow in WORKFLOWS:
        for line in workflow.read_text(encoding="utf-8").splitlines():
            if "uses:" not in line:
                continue
            match = USE_RE.match(line)
            assert match is not None, f"mutable or malformed action ref: {workflow}: {line}"
            action, ref = match.groups()
            assert action in EXPECTED_ACTION_REFS, f"unreviewed action: {action}"
            assert ref == EXPECTED_ACTION_REFS[action], f"unexpected ref for {action}: {ref}"
            seen.add(action)
    assert seen == set(EXPECTED_ACTION_REFS)


def test_security_job_installs_exact_dedicated_tool_constraints():
    requirements = ROOT / ".github/requirements-security.txt"
    pins = {
        line.strip()
        for line in requirements.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    assert pins == {"bandit==1.9.4", "pip-audit==2.10.1"}

    ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert "pip install -r .github/requirements-security.txt" in ci
    assert "pip install bandit pip-audit" not in ci


def test_dependabot_has_bounded_weekly_action_and_security_tool_update_paths():
    config = (ROOT / ".github/dependabot.yml").read_text(encoding="utf-8")
    assert 'package-ecosystem: "github-actions"' in config
    assert 'directory: "/"' in config
    assert 'package-ecosystem: "pip"' in config
    assert 'directory: "/.github"' in config
    assert config.count('interval: "weekly"') == 2


def test_fixture_data_manifest_is_bounded_and_non_certifying():
    path = ROOT / "docs/security/FIXTURE_DATA_MANIFEST.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))

    assert manifest["tracking_issue"] == 214
    assert manifest["review_status"] == "BOUNDED_REVIEW_COMPLETE"
    assert manifest["repository_wide_pii_clean_claim"] is False
    assert manifest["confirmed_secret_or_pii_incident"] is False
    assert manifest["history_rewrite_authorized"] is False

    classes = {item["classification"] for item in manifest["classifications"]}
    assert "GENERATED_SYNTHETIC_BENCHMARK_DATA" in classes
    assert "GENERATED_BENCHMARK_RESULT_DATA" in classes
    assert "ARCHIVED_DESIGN_MATERIAL" in classes

    reviewed_paths = {
        reviewed_path
        for item in manifest["classifications"]
        for reviewed_path in item["paths"]
    }
    required = {
        "eval/reader_rc8_retrieval_adversarial.jsonl",
        "eval/reader_retrieval_eval_v2_queries.jsonl",
        "eval/reader_retrieval_eval_v2_candidates.jsonl",
        "eval/reader_retrieval_eval_v2_qrels.jsonl",
        "docs/archive/Velantrim_V8_Crystal_Sprint1.jsonl",
        "docs/archive/Velantrim_V8_Crystal_Sprint1_toc.md",
    }
    assert required <= reviewed_paths
    for reviewed_path in reviewed_paths:
        assert (ROOT / reviewed_path).is_file(), reviewed_path
