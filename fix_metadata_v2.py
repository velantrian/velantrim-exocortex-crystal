#!/usr/bin/env python3
"""
Enhanced metadata fixes with content-based layer detection and comprehensive dependencies.
"""

import json
from pathlib import Path
from unidecode import unidecode

# More complete layer assignment logic
LAYER_KEYWORDS = {
    'L0': ['Ring Zero', 'Core Values', 'pinned', 'critical', 'VALUES_CORE', 'L0', 'working memory'],
    'L1': ['L1', 'STM', 'short-term', 'session', 'episode', 'recency', 'SQLite FTS5'],
    'L1.5': ['Velum', 'L1.5', 'neighboring', 'neighbors', 'synaptic', 'Wigner'],
    'L2': ['L2', 'consolidation', 'staging_candidates', 'temporary', 'buffering'],
    'L2.5': ['L2.5', 'Staging', 'staging', 'candidate', 'resource-aware'],
    'L3': ['L3', 'Neo4j', 'Graph', 'cold', 'persistent', '[:SUPPORTED_BY]', 'long-term'],
    'L4': ['L4', 'reasoning', 'reasoning_bank', 'strategy', 'Thompson Sampling', 'creative', 'Creative Intelligence'],
    'L6': ['audit', 'L6', 'Audit', 'Observer'],
}

# RFC to layer mapping (authoritative)
RFC_TO_LAYER = {
    'RFC0001': 'L0',      # Formal invariants
    'RFC0004': 'L0',      # Truth Gate
    'RFC0014': 'L2.5',    # Staging Layer
    'RFC0016': 'L1.5',    # Velum
    'RFC0039': 'L2.5',    # Integration
    'RFC0062': 'L3',      # TZ-Fix / Token contract
    'RFC0063': 'L3',      # Knowledge Ingestion
    'RFC0065': 'L3',      # Memory-as-Volition
    'RFC0066': 'L3',      # Concept Emergence
    'RFC0067 v2.0': 'L4', # Creative Intelligence
}

# RFC dependencies - comprehensive
FULL_DEPENDS_ON = {
    'RFC0067 v2.0': ['RFC0016', 'RFC0066', 'RFC0039'],  # Creative needs Velum, Concepts, Integration
    'RFC0066': ['RFC0016', 'RFC0052'],  # Concepts need Velum & components
    'RFC0065': ['RFC0016', 'RFC0004'],  # Memory needs Velum & Truth Gate
    'RFC0064': ['RFC0065'],  # Versioning depends on Memory
    'RFC0063': ['RFC0016', 'RFC0004', 'RFC0062'],  # Ingestion needs Velum, Truth, TZ-Fix
    'RFC0062': ['RFC0016', 'RFC0004', 'RFC0052'],  # TZ-Fix needs Velum, Truth, Components
    'RFC0039': ['RFC0016', 'RFC0004', 'RFC0062'],  # Integration needs Velum, Truth, TZ-Fix
    'RFC0016': ['RFC0004', 'RFC0001'],  # Velum needs Truth Gate & Invariants
    'RFC0014': ['RFC0016', 'RFC0004'],  # Staging needs Velum & Truth
    'RFC0004': ['RFC0001'],  # Truth depends on Invariants
}

def get_layer_from_rfc(rfc):
    """Get layer from RFC-to-layer mapping."""
    # Normalize RFC (remove version info if present)
    rfc_base = rfc.replace(' v2.0', '').replace(' v1.0', '') if rfc else ''
    return RFC_TO_LAYER.get(rfc) or RFC_TO_LAYER.get(rfc_base)

def detect_layer_from_content(chunk):
    """Detect layer from content keywords."""
    content = chunk.get('content', '').lower()
    title = chunk.get('title', '').lower()
    combined = content[:5000] + title  # Check first 5k chars + title

    scores = {}
    for layer, keywords in LAYER_KEYWORDS.items():
        score = sum(combined.count(kw.lower()) for kw in keywords if kw.lower())
        if score > 0:
            scores[layer] = score

    if scores:
        return max(scores, key=scores.get)
    return None

def determine_layer(chunk):
    """Determine layer with priority: RFC > content keywords > null."""
    # Priority 1: RFC field
    rfc = chunk.get('rfc', '')
    if rfc:
        layer = get_layer_from_rfc(rfc)
        if layer:
            return layer

    # Priority 2: Content-based detection
    layer = detect_layer_from_content(chunk)
    if layer:
        return layer

    # Priority 3: Cross-cutting RFCs stay null
    if any(word in chunk.get('title', '').lower() for word in
           ['protocol', 'invariant', 'meta', 'config', 'audit', 'changelog', 'roadmap']):
        return None

    return None

def get_dependencies(rfc):
    """Get RFC dependencies."""
    if not rfc:
        return []

    rfc_base = rfc.replace(' v2.0', '').replace(' v1.0', '')
    return FULL_DEPENDS_ON.get(rfc_base, [])

def transliterate_chunk_id(chunk_id):
    """Convert to ASCII-safe version."""
    if not chunk_id or all(ord(c) < 128 for c in chunk_id):
        return chunk_id

    ascii_id = unidecode(chunk_id)
    ascii_id = ascii_id.lower().replace(' ', '_')
    ascii_id = ''.join(c for c in ascii_id if c.isalnum() or c == '_')
    while '__' in ascii_id:
        ascii_id = ascii_id.replace('__', '_')
    return ascii_id.rstrip('_')

def fix_rfc_mismatch(chunk):
    """Try to fix RFC field/title mismatches."""
    rfc = chunk.get('rfc', '')
    title = chunk.get('title', '')

    if not rfc or not title:
        return None

    # RFC0067 v2.0 in title but field as "RFC0067 v2.0" - OK
    if 'RFC0067 v2.0' in title and rfc == 'RFC0067 v2.0':
        return None

    # RFC field has hyphen, title has en-dash (dash normalization)
    # These are minor formatting differences, not critical

    return None

def fix_jsonl(input_path, output_path):
    """Apply all metadata fixes."""

    fixes = {
        'chunk_ids_transliterated': 0,
        'layers_populated': 0,
        'depends_on_populated': 0,
        'total_chunks': 0,
    }

    chunks = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue

            chunk = json.loads(line)
            fixes['total_chunks'] += 1

            # Fix chunk_id
            if chunk.get('chunk_id'):
                original = chunk['chunk_id']
                fixed = transliterate_chunk_id(original)
                if fixed != original:
                    chunk['chunk_id'] = fixed
                    fixes['chunk_ids_transliterated'] += 1

            # Fix layer
            if chunk.get('layer') is None:
                new_layer = determine_layer(chunk)
                if new_layer is not None:
                    chunk['layer'] = new_layer
                    fixes['layers_populated'] += 1

            # Fix depends_on
            depends_on = chunk.get('depends_on')
            if depends_on is not None and len(depends_on) == 0:
                rfc = chunk.get('rfc', '')
                new_deps = get_dependencies(rfc)
                if new_deps:
                    chunk['depends_on'] = new_deps
                    fixes['depends_on_populated'] += 1

            chunks.append(chunk)

    # Write fixed JSONL
    with open(output_path, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')

    return fixes

if __name__ == '__main__':
    input_file = 'Velantrim_V8_Crystal_Sprint1.jsonl'
    output_file = 'Velantrim_V8_Crystal_Sprint1_fixed_v2.jsonl'

    print("Applying enhanced metadata fixes...")
    fixes = fix_jsonl(input_file, output_file)

    print("\nFixes applied:")
    for key, count in fixes.items():
        if key != 'total_chunks':
            print(f"  {key}: {count}")

    print(f"  Total chunks processed: {fixes['total_chunks']}")
    print(f"\nOutput: {output_file}")
