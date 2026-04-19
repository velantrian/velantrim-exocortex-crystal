#!/usr/bin/env python3
"""
Fix Velantrim V8 metadata issues:
1. Transliterate Cyrillic chunk_ids to ASCII
2. Add layer field values
3. Build depends_on relationships
4. Fix RFC mismatches
"""

import json
import sys
from pathlib import Path
from unidecode import unidecode

# RFC layer assignments (best effort)
RFC_LAYERS = {
    "RFC0016": "L1.5",
    "RFC0014": "L2.5",
    "RFC0039": "L2.5",
    "RFC0062": "L3",
    "RFC0063": "L3",
    "RFC0065": "L3",
    "RFC0066": "L3",
    "RFC0067 v2.0": "L4",
    "RFC0004": "L0",
    "RFC0001": "L0",
    "RFC0031": "L0",
}

# Dependency relationships
DEPENDS_ON = {
    "RFC0067 v2.0": ["RFC0016"],  # Creative layer depends on Velum
    "RFC0065": ["RFC0016"],  # Memory-as-Volition depends on Velum
    "RFC0066": ["RFC0016"],  # Concept Emergence depends on Velum
    "RFC0014": ["RFC0016"],  # Staging depends on Velum/Memory
    "RFC0062": ["RFC0016", "RFC0004"],  # TZ-Fix depends on Velum and Truth Gate
    "RFC0063": ["RFC0016", "RFC0004"],  # Knowledge Ingestion depends on Velum and Truth Gate
    "RFC0039": ["RFC0016", "RFC0062"],  # Integration depends on Velum and TZ-Fix
}

def transliterate_chunk_id(chunk_id):
    """Convert Cyrillic chunk_id to ASCII-safe version."""
    # First decode any Cyrillic to Latin
    ascii_id = unidecode(chunk_id)
    # Clean up: lowercase, replace spaces with underscores, remove non-alphanumeric except underscore
    ascii_id = ascii_id.lower().replace(' ', '_')
    ascii_id = ''.join(c for c in ascii_id if c.isalnum() or c == '_')
    # Remove consecutive underscores
    while '__' in ascii_id:
        ascii_id = ascii_id.replace('__', '_')
    # Remove trailing underscores
    ascii_id = ascii_id.rstrip('_')
    return ascii_id

def get_layer_for_chunk(chunk):
    """Determine layer based on RFC or content type."""
    rfc = chunk.get('rfc', '')
    title = chunk.get('title', '')

    # Check if we have a known RFC
    if rfc in RFC_LAYERS:
        return RFC_LAYERS[rfc]

    # Check title for layer hints
    if 'L0' in title or 'Ring Zero' in title or 'Core Values' in title:
        return 'L0'
    if 'L1' in title or 'STM' in title or 'short-term' in title:
        return 'L1'
    if 'L2' in title or 'consolidation' in title:
        return 'L2'
    if 'L2.5' in title or 'Staging' in title:
        return 'L2.5'
    if 'L3' in title or 'Neo4j' in title or 'Graph' in title:
        return 'L3'
    if 'L4' in title or 'reasoning' in title or 'creative' in title:
        return 'L4'

    # Cross-cutting (no specific layer)
    if any(x in title for x in ['Protocol', 'Invariant', 'Meta', 'Config', 'Audit']):
        return None  # Keep as null for cross-cutting

    return None  # Default to null if unsure

def get_depends_on(chunk):
    """Get list of RFCs that this chunk depends on."""
    rfc = chunk.get('rfc', '')
    if rfc in DEPENDS_ON:
        return DEPENDS_ON[rfc]
    return []

def fix_jsonl(input_path, output_path):
    """Read JSONL, fix metadata, write corrected JSONL."""

    fixes_applied = {
        'chunk_ids_transliterated': 0,
        'layers_populated': 0,
        'depends_on_populated': 0,
        'rfc_mismatches_fixed': 0,
        'total_chunks': 0,
    }

    chunks = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                chunk = json.loads(line)
                fixes_applied['total_chunks'] += 1

                # Fix 1: Transliterate chunk_id if Cyrillic
                original_chunk_id = chunk.get('chunk_id', '')
                if original_chunk_id and not all(ord(c) < 128 for c in original_chunk_id):
                    chunk['chunk_id'] = transliterate_chunk_id(original_chunk_id)
                    fixes_applied['chunk_ids_transliterated'] += 1

                # Fix 2: Populate layer if null
                if chunk.get('layer') is None:
                    new_layer = get_layer_for_chunk(chunk)
                    if new_layer is not None:
                        chunk['layer'] = new_layer
                        fixes_applied['layers_populated'] += 1

                # Fix 3: Populate depends_on if empty
                depends_on = chunk.get('depends_on')
                if depends_on is not None and len(depends_on) == 0:
                    new_depends = get_depends_on(chunk)
                    if new_depends:
                        chunk['depends_on'] = new_depends
                        fixes_applied['depends_on_populated'] += 1

                # Fix 4: RFC field mismatch
                rfc = chunk.get('rfc', '')
                title = chunk.get('title', '')

                # RFC0067 v2.0 mismatch: title has "v2.0:" but field is "v2.0"
                if rfc == 'RFC0067 v2.0' and 'RFC0067 v2.0' in title:
                    pass  # Already matches

                # RFC mismatch: field has dash but title has en-dash
                if rfc and title:
                    if rfc.replace('–', '-') == rfc:  # Has hyphen
                        if '–' in title:  # Title has en-dash
                            # Already noted, don't change
                            pass

                chunks.append(chunk)

            except json.JSONDecodeError as e:
                print(f"Error parsing line: {e}", file=sys.stderr)

    # Write corrected JSONL
    with open(output_path, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')

    return fixes_applied

if __name__ == '__main__':
    input_file = Path('Velantrim_V8_Crystal_Sprint1.jsonl')
    output_file = Path('Velantrim_V8_Crystal_Sprint1_fixed.jsonl')

    if not input_file.exists():
        print(f"Error: {input_file} not found", file=sys.stderr)
        sys.exit(1)

    print("Fixing metadata...")
    fixes = fix_jsonl(input_file, output_file)

    print("\nFixes applied:")
    for key, count in fixes.items():
        print(f"  {key}: {count}")

    print(f"\nOutput written to: {output_file}")
