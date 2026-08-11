"""Validate D4 project/grant/governance source truth through Reader RC-5."""
from __future__ import annotations
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCE = "51c205fe048fd69d39fcd47b43e042a50de432bc"

def main() -> int:
    errors: list[str] = []
    required = {
        "docs/PROJECT_GRANT_AND_GOVERNANCE.md": ("d4-source-contract: CURRENT", "RC-5", "contradiction candidate != confirmed contradiction", "submitted", "not awarded", "€50,000", "active=false"),
        "docs/GRANT_NLNET_SCOPE.md": ("RC-5", "Potential funded delta after RC-5", "submitted / under review / not awarded", "cannot be budgeted again"),
        "docs/GLOSSARY.md": ("Reader Core RC-5", "POSSIBLE_CONTRADICTION", "TENSION", "EXCEPTION", "QUALIFICATION", "relation rationale"),
        "ROADMAP.md": ("RC-5 — Exceptions / Contradiction Candidate Detection", "RC-6 long-context strategy", "RC-7 cross-document reading"),
        "docs/grants/baseline-funded-delta-matrix.md": ("Reader RC-5", "pre-agreement RC-0..RC-5", "contradiction candidate != confirmed contradiction"),
    }
    for relative, markers in required.items():
        text = (ROOT / relative).read_text()
        for marker in markers:
            if marker not in text: errors.append(f"{relative}: missing {marker!r}")
    state = (ROOT / "docs/ai/CURRENT_STATE.md").read_text()
    for marker in (SOURCE, "reader_core_rc5_relation_candidates    = true", "NLnet remains submitted / under review / not awarded"):
        if marker not in state: errors.append(f"CURRENT_STATE: missing {marker!r}")
    if errors:
        print("D4 source validation failed:")
        for error in errors: print(f"  - {error}")
        return 1
    print(f"D4 project/grant/governance source consistent through RC-5: source={SOURCE}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
