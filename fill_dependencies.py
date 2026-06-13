#!/usr/bin/env python3
"""
Fill depends_on by analyzing content for RFC cross-references.
"""

import argparse
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

from utils.rfc_parser import extract_rfc_mentions


def fill_dependencies(input_path: Path, output_path: Path) -> dict:
    """Analyze content to infer dependencies. Reads input, writes output."""
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    fixes = {"depends_on_populated": 0, "total_chunks": 0}
    chunks = []

    with open(input_path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                chunk = json.loads(line)
            except json.JSONDecodeError as exc:
                print(
                    f"[ERROR] Line {lineno}: JSON parse error — {exc}",
                    file=sys.stderr,
                )
                raise

            fixes["total_chunks"] += 1

            depends_on = chunk.get("depends_on", [])
            if isinstance(depends_on, list) and len(depends_on) == 0:
                rfc_val = chunk.get("rfc") or ""
                own_rfc = rfc_val.replace(" v2.0", "").replace(" v1.0", "")

                content = chunk.get("content", "")
                mentioned = extract_rfc_mentions(content)

                deps = [
                    rfc
                    for rfc in mentioned
                    if rfc not in (own_rfc, own_rfc + " v2.0", own_rfc + " v1.0")
                ]
                deps = deps[:5]

                if deps:
                    chunk["depends_on"] = deps
                    fixes["depends_on_populated"] += 1

            chunks.append(chunk)

    output_path = Path(output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    return fixes


def _default_output_path(input_path: Path) -> Path:
    """Output file sits beside the input file."""
    return input_path.with_name(input_path.stem + "_deps.jsonl")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fill depends_on from RFC content references"
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        default="docs/Velantrim_V8_Crystal_Sprint1.jsonl",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Count changes without writing any files",
    )
    args = parser.parse_args()

    input_path = Path(args.input_file)

    if not input_path.exists():
        print(f"[ERROR] Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path = _default_output_path(input_path)

    print("Filling depends_on from content analysis...")

    if args.dry_run:
        # Dry-run: compute changes using a temp file, discard result.
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".jsonl", dir=input_path.parent
        ) as tmp:
            tmp_path = Path(tmp.name)
        try:
            fixes = fill_dependencies(input_path, tmp_path)
        finally:
            tmp_path.unlink(missing_ok=True)
        print(
            f"\n  [DRY RUN] depends_on would be populated: {fixes['depends_on_populated']}"
        )
        print(f"  Total chunks: {fixes['total_chunks']}")
        print("  No files written.")
    else:
        # Atomic write strategy:
        #   1. Create .bak copy of original.
        #   2. Write output to a temp file in the same directory.
        #   3. Only if generation succeeds, replace the original.
        #   On any failure the original is preserved intact.
        bak_path = input_path.with_suffix(input_path.suffix + ".bak")
        shutil.copy(input_path, bak_path)
        print(f"  Backup: {bak_path}")

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jsonl",
            dir=input_path.parent,
        ) as tmp:
            tmp_path = Path(tmp.name)

        try:
            fixes = fill_dependencies(input_path, tmp_path)
        except Exception:
            tmp_path.unlink(missing_ok=True)
            print(
                "[ERROR] Processing failed; original file is unchanged.",
                file=sys.stderr,
            )
            raise

        # Generation succeeded — move temp file into place as the output.
        shutil.copy(tmp_path, output_path)
        tmp_path.unlink(missing_ok=True)

        print(f"\n  depends_on populated from content: {fixes['depends_on_populated']}")
        print(f"  Total chunks: {fixes['total_chunks']}")
        print(f"\nOutput: {output_path}")

        # Replace original with the new version.
        shutil.copy(output_path, input_path)
        print(f"✓ Applied to {input_path}")
