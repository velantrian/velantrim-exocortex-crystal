#!/usr/bin/env python3
"""
Check if duplicate RFC entries are intentional (sections) or actual duplicates.
"""

import json
import sys
from pathlib import Path


def load_chunks(jsonl_path: Path) -> list[dict]:
    """Load JSONL chunks with per-line error reporting. Returns list of dicts."""
    path = Path(jsonl_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                chunks.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(
                    f"[ERROR] Line {lineno}: JSON parse error — {exc}",
                    file=sys.stderr,
                )
    return chunks


def check_duplicates(jsonl_path: Path) -> None:
    chunks = load_chunks(jsonl_path)
    total = len(chunks)

    # Duplicate RFC index map from the original corpus audit.
    duplicates = {
        "RFC0067 v2.0": [4, 11, 27, 31],
        "RFC0016": [7, 26, 45],
        "RFC0039": [14, 16, 38],
        "RFC0062": [13, 60],
        "RFC0065": [9, 62],
        "RFC0004": [25, 41],
        "RFC0001": [24, 29],
        "RFC0052": [6, 12],
    }

    for rfc, indices in duplicates.items():
        print(f"\n{'='*80}")
        print(f"{rfc}: {len(indices)} chunks at indices {indices}")
        print("=" * 80)

        for idx in indices:
            if idx >= total:
                print(
                    f"[WARN] {rfc} index {idx} is out of range for "
                    f"{total} loaded chunks; skipping.",
                    file=sys.stderr,
                )
                continue
            chunk = chunks[idx]
            chunk_id = chunk.get("chunk_id", "<missing>")
            title = chunk.get("title", "<missing>")
            print(f"\n[idx {idx}] chunk_id: {chunk_id[:60]}")
            print(f"Title: {title[:80]}")
            print(f"Chars: {chunk.get('char_count', 0)}")
            print(f"Status: {chunk.get('status', 'N/A')}")
            print(f"Tags: {chunk.get('tags', [])[:5]}")

        print("\nContent preview comparison:")
        for idx in indices:
            if idx >= total:
                continue
            preview = chunks[idx].get("content", "")[0:100].replace("\n", " ")
            print(f"  [{idx}]: {preview}...")


if __name__ == "__main__":
    jsonl_path = Path("docs/Velantrim_V8_Crystal_Sprint1.jsonl")
    check_duplicates(jsonl_path)
