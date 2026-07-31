#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONDONTWRITEBYTECODE=1

python - "$ROOT" <<'PY'
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


@dataclass(frozen=True)
class Mutation:
    name: str
    target: str
    old: str
    new: str
    tests: tuple[str, ...]


MUTATIONS = (
    Mutation(
        name="truthgate-threshold-equality",
        target="core/truth_gate.py",
        old="if confidence < min_confidence:",
        new="if confidence <= min_confidence:",
        tests=("tests/test_truth_gate.py::test_confidence_exactly_at_threshold_passes",),
    ),
    Mutation(
        name="truthgate-llm-origin-block",
        target="core/truth_gate.py",
        old='and fact.get("source_status") == "LLM_OUTPUT"',
        new='and fact.get("source_status") == "EXTERNAL"',
        tests=("tests/test_truth_gate.py::test_llm_output_world_fact_is_blocked",),
    ),
    Mutation(
        name="canonical-requires-verified-status",
        target="core/canonical_view.py",
        old="if truth_status != VERIFIED_TRUTH_STATUS:",
        new="if truth_status == VERIFIED_TRUTH_STATUS:",
        tests=(
            "tests/test_canonical_view.py::test_verified_fact_with_valid_metadata_is_strict_canonical",
            "tests/test_canonical_view.py::test_user_claimed_world_fact_excluded_from_strict_even_at_full_confidence",
        ),
    ),
    Mutation(
        name="canonical-restriction-deny",
        target="core/canonical_view.py",
        old='if _normalize_restricted_bit(fact.get("restricted")) is not False:',
        new='if _normalize_restricted_bit(fact.get("restricted")) is False:',
        tests=(
            "tests/test_canonical_view.py::test_verified_fact_with_valid_metadata_is_strict_canonical",
            "tests/test_canonical_view.py::test_contextual_mode_still_excludes_restricted_facts",
        ),
    ),
    Mutation(
        name="canonical-esm-allowlist",
        target="core/canonical_view.py",
        old='if not _in(fact.get("epistemic_state"), STRICT_CANONICAL_ESM_STATES):',
        new='if _in(fact.get("epistemic_state"), STRICT_CANONICAL_ESM_STATES):',
        tests=(
            "tests/test_canonical_view.py::test_verified_fact_with_valid_metadata_is_strict_canonical",
            "tests/test_canonical_view.py::test_strict_projection_of_mixed_set_returns_only_the_verified_fact",
        ),
    ),
    Mutation(
        name="snapshot-malformed-confidence-conflict",
        target="core/trust_snapshot.py",
        old="if confidence is None:",
        new="if confidence is not None:",
        tests=(
            "tests/test_trust_snapshot.py::test_malformed_l3_confidence_is_unknown_and_fails_closed",
            "tests/test_trust_snapshot.py::test_equal_confidence_representations_do_not_conflict",
        ),
    ),
    Mutation(
        name="receipt-digest-comparison",
        target="core/provenance.py",
        old='_digest(receipt) == receipt["digest"]',
        new='_digest(receipt) != receipt["digest"]',
        tests=(
            "tests/test_provenance.py::test_verify_fresh_receipt_ok",
            "tests/test_provenance.py::test_tampered_answer_breaks_digest",
        ),
    ),
)


def prepare_workspace(root: Path, destination: Path) -> None:
    shutil.copytree(root / "core", destination / "core")
    shutil.copytree(root / "tests", destination / "tests")
    shutil.copy2(root / "adaptive_threshold_module.py", destination)


def apply_mutation(path: Path, mutation: Mutation) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(mutation.old)
    if count != 1:
        raise RuntimeError(
            f"{mutation.name}: expected exactly one source fragment in "
            f"{mutation.target}, found {count}"
        )
    path.write_text(text.replace(mutation.old, mutation.new, 1), encoding="utf-8")


def run_mutation(root: Path, mutation: Mutation) -> tuple[str, str]:
    with tempfile.TemporaryDirectory(prefix="velantrim-mutation-") as tmp:
        workspace = Path(tmp)
        prepare_workspace(root, workspace)
        apply_mutation(workspace / mutation.target, mutation)
        command = [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-o",
            "addopts=",
            *mutation.tests,
        ]
        completed = subprocess.run(
            command,
            cwd=workspace,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        output = completed.stdout.strip()
        if completed.returncode == 1:
            return "killed", output
        if completed.returncode == 0:
            return "survived", output
        return f"infrastructure-error({completed.returncode})", output


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    failures: list[str] = []
    print(f"Ring Zero mutation gate: {len(MUTATIONS)} deterministic mutants")
    for mutation in MUTATIONS:
        try:
            status, output = run_mutation(root, mutation)
        except Exception as exc:  # source drift is a gate failure, not a skip
            status, output = "harness-error", f"{type(exc).__name__}: {exc}"
        print(f"[{status.upper()}] {mutation.name}")
        if status != "killed":
            failures.append(mutation.name)
            print(output[-4000:])

    if failures:
        print("Mutation gate failed: " + ", ".join(failures))
        return 1
    print("Mutation gate passed: every declared Ring Zero mutant was killed.")
    return 0


raise SystemExit(main())
PY
