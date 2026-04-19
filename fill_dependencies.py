#!/usr/bin/env python3
"""
Fill depends_on by analyzing content for RFC cross-references.
"""

import json
import re
from pathlib import Path

def extract_rfc_mentions(content):
    """Find all RFC mentions in content."""
    pattern = r'RFC\d{4}(?:\s+v\d+\.\d+)?'
    matches = re.findall(pattern, content)
    return list(set(matches))  # unique

def fill_dependencies(input_path, output_path):
    """Analyze content to infer dependencies."""

    fixes = {'depends_on_populated': 0, 'total_chunks': 0}
    chunks = []

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue

            chunk = json.loads(line)
            fixes['total_chunks'] += 1

            # For chunks with empty depends_on, infer from content
            depends_on = chunk.get('depends_on', [])
            if isinstance(depends_on, list) and len(depends_on) == 0:
                # Extract own RFC
                rfc_val = chunk.get('rfc') or ''
                own_rfc = rfc_val.replace(' v2.0', '').replace(' v1.0', '')

                # Find mentioned RFCs in content
                content = chunk.get('content', '')
                mentioned = extract_rfc_mentions(content)

                # Filter: remove self-references, keep unique
                deps = [rfc for rfc in mentioned
                        if rfc not in (own_rfc, own_rfc + ' v2.0', own_rfc + ' v1.0')]
                deps = list(dict.fromkeys(deps))[:5]  # Limit to 5, preserve order

                if deps:
                    chunk['depends_on'] = deps
                    fixes['depends_on_populated'] += 1

            chunks.append(chunk)

    # Write fixed JSONL
    with open(output_path, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')

    return fixes

if __name__ == '__main__':
    input_file = 'Velantrim_V8_Crystal_Sprint1.jsonl'
    output_file = 'Velantrim_V8_Crystal_Sprint1_deps.jsonl'

    print("Filling depends_on from content analysis...")
    fixes = fill_dependencies(input_file, output_file)

    print(f"\n  depends_on populated from content: {fixes['depends_on_populated']}")
    print(f"  Total chunks: {fixes['total_chunks']}")
    print(f"\nOutput: {output_file}")

    # Replace original
    import shutil
    shutil.copy(output_file, input_file)
    print(f"✓ Applied to {input_file}")
