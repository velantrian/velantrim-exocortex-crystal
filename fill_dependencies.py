#!/usr/bin/env python3
"""
Fill depends_on by analyzing content for RFC cross-references.
"""

import argparse
import json
import shutil
from pathlib import Path

from utils.rfc_parser import extract_rfc_mentions


def fill_dependencies(input_path: str, output_path: str) -> dict:
    """Analyze content to infer dependencies. Reads input, writes output."""

    fixes = {'depends_on_populated': 0, 'total_chunks': 0}
    chunks = []

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue

            chunk = json.loads(line)
            fixes['total_chunks'] += 1

            depends_on = chunk.get('depends_on', [])
            if isinstance(depends_on, list) and len(depends_on) == 0:
                rfc_val = chunk.get('rfc') or ''
                own_rfc = rfc_val.replace(' v2.0', '').replace(' v1.0', '')

                content = chunk.get('content', '')
                mentioned = extract_rfc_mentions(content)

                deps = [rfc for rfc in mentioned
                        if rfc not in (own_rfc, own_rfc + ' v2.0', own_rfc + ' v1.0')]
                deps = deps[:5]

                if deps:
                    chunk['depends_on'] = deps
                    fixes['depends_on_populated'] += 1

            chunks.append(chunk)

    with open(output_path, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')

    return fixes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Fill depends_on from RFC content references")
    parser.add_argument('input_file', nargs='?', default='docs/Velantrim_V8_Crystal_Sprint1.jsonl')
    parser.add_argument('--dry-run', action='store_true',
                        help="Count changes without writing any files")
    args = parser.parse_args()

    input_file = args.input_file
    output_file = Path(input_file).stem + '_deps.jsonl'

    print("Filling depends_on from content analysis...")

    if args.dry_run:
        # Dry-run: compute changes, write to a temp path that we discard
        import tempfile, os
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jsonl') as tmp:
            tmp_path = tmp.name
        try:
            fixes = fill_dependencies(input_file, tmp_path)
        finally:
            os.unlink(tmp_path)
        print(f"\n  [DRY RUN] depends_on would be populated: {fixes['depends_on_populated']}")
        print(f"  Total chunks: {fixes['total_chunks']}")
        print("  No files written.")
    else:
        # D3: create .bak before overwriting original
        bak_path = input_file + '.bak'
        shutil.copy(input_file, bak_path)
        print(f"  Backup: {bak_path}")

        fixes = fill_dependencies(input_file, output_file)

        print(f"\n  depends_on populated from content: {fixes['depends_on_populated']}")
        print(f"  Total chunks: {fixes['total_chunks']}")
        print(f"\nOutput: {output_file}")

        # Replace original
        shutil.copy(output_file, input_file)
        print(f"✓ Applied to {input_file}")
