#!/usr/bin/env python3
"""
Check if duplicate RFC entries are intentional (sections) or actual duplicates.
"""

import json
from pathlib import Path

def check_duplicates(jsonl_path):
    chunks = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line))

    # Duplicates from audit
    duplicates = {
        "RFC0067 v2.0": [4, 11, 27, 31],
        "RFC0016": [7, 26, 45],
        "RFC0039": [14, 16, 38],
        "RFC0062": [13, 60],
        "RFC0065": [9, 62],
        "RFC0004": [25, 41],
        "RFC0001": [24, 29],
        "RFC0052": [6, 12]
    }

    for rfc, indices in duplicates.items():
        print(f"\n{'='*80}")
        print(f"{rfc}: {len(indices)} chunks at indices {indices}")
        print('='*80)

        for idx in indices:
            chunk = chunks[idx]
            print(f"\n[idx {idx}] chunk_id: {chunk['chunk_id'][:60]}")
            print(f"Title: {chunk['title'][:80]}")
            print(f"Chars: {chunk.get('char_count', 0)}")
            print(f"Status: {chunk.get('status', 'N/A')}")
            print(f"Tags: {chunk.get('tags', [])[:5]}")  # First 5 tags

        # Check if they're similar or different
        contents = [chunks[idx].get('content', '')[:100] for idx in indices]
        print("\nContent preview comparison:")
        for i, idx in enumerate(indices):
            preview = chunks[idx].get('content', '')[0:100].replace('\n', ' ')
            print(f"  [{idx}]: {preview}...")

if __name__ == '__main__':
    jsonl_path = Path('docs/Velantrim_V8_Crystal_Sprint1.jsonl')
    check_duplicates(jsonl_path)
