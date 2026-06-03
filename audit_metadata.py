#!/usr/bin/env python3
"""
Audit script for Velantrim V8 Crystal Sprint1 JSONL metadata.
Maps all RFC mismatches, duplicates, missing fields, and structural issues.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

def audit_jsonl(filepath):
    """Parse JSONL and identify all metadata issues."""

    issues = {
        "rfc_mismatches": [],  # RFC field vs title mismatch
        "duplicate_rfcs": defaultdict(list),  # RFC numbers appearing multiple times
        "cyrillic_chunk_ids": [],  # chunk_id with non-ASCII
        "null_layers": [],  # layer=null chunks
        "empty_depends_on": [],  # depends_on=[]
        "mega_blobs": [],  # char_count > 50k
        "empty_stubs": [],  # char_count < 150
        "duplicate_chunk_ids": defaultdict(list),  # identical chunk_ids
        "rfc0067_versions": [],  # RFC0067 v1.0 vs v2.0 inconsistencies
    }

    chunks = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                chunk = json.loads(line)
                chunks.append(chunk)
                idx = chunk.get('idx', line_num - 1)

                # Check RFC field vs title
                rfc = chunk.get('rfc', '')
                title = chunk.get('title', '')
                if rfc and title:
                    # Extract RFC number from title
                    title_rfc = None
                    if 'RFC' in title:
                        for word in title.split():
                            if word.startswith('RFC'):
                                title_rfc = word.rstrip(':—-')
                                break

                    if title_rfc and rfc != title_rfc:
                        issues['rfc_mismatches'].append({
                            'idx': idx,
                            'chunk_id': chunk.get('chunk_id'),
                            'rfc_field': rfc,
                            'title_rfc': title_rfc,
                            'title': title[:80]
                        })

                # Track RFC duplicates
                if rfc:
                    issues['duplicate_rfcs'][rfc].append(idx)

                # Check for Cyrillic in chunk_id
                chunk_id = chunk.get('chunk_id', '')
                if chunk_id and not all(ord(c) < 128 for c in chunk_id):
                    issues['cyrillic_chunk_ids'].append({
                        'idx': idx,
                        'chunk_id': chunk_id
                    })

                # Track duplicate chunk_ids
                if chunk_id:
                    issues['duplicate_chunk_ids'][chunk_id].append(idx)

                # Check for null layer
                if chunk.get('layer') is None:
                    issues['null_layers'].append(idx)

                # Check for empty depends_on
                depends_on = chunk.get('depends_on')
                if depends_on is not None and len(depends_on) == 0:
                    issues['empty_depends_on'].append(idx)

                # E1: use actual content length, not stale char_count field
                content_len = len(chunk.get('content', ''))
                if content_len > 50000:
                    issues['mega_blobs'].append({
                        'idx': idx,
                        'chunk_id': chunk_id,
                        'char_count': content_len,
                        'title': title[:60]
                    })
                if content_len < 150:
                    issues['empty_stubs'].append({
                        'idx': idx,
                        'chunk_id': chunk_id,
                        'char_count': content_len,
                        'title': title[:60]
                    })

                # Check RFC0067 version consistency
                if rfc and ('RFC0067' in rfc or 'RFC0067' in title):
                    tags = chunk.get('tags', [])
                    has_v1 = any('v1.0' in str(tag) for tag in tags)
                    has_v2 = any('v2.0' in str(tag) for tag in tags)
                    has_mixed = has_v1 and has_v2

                    if 'v1.0' in rfc and 'v2.0' in title:
                        issues['rfc0067_versions'].append({
                            'idx': idx,
                            'chunk_id': chunk_id,
                            'rfc': rfc,
                            'title': title[:80],
                            'issue': 'rfc_field_v1_title_v2'
                        })
                    elif 'v2.0' in rfc and 'v1.0' in title:
                        issues['rfc0067_versions'].append({
                            'idx': idx,
                            'chunk_id': chunk_id,
                            'rfc': rfc,
                            'title': title[:80],
                            'issue': 'rfc_field_v2_title_v1'
                        })
                    elif has_mixed:
                        issues['rfc0067_versions'].append({
                            'idx': idx,
                            'chunk_id': chunk_id,
                            'rfc': rfc,
                            'tags': tags,
                            'issue': 'mixed_versions_in_tags'
                        })

            except json.JSONDecodeError as e:
                print(f"Error on line {line_num}: {e}", file=sys.stderr)

    # Clean up duplicate tracking (only report actual duplicates)
    issues['duplicate_rfcs'] = {k: v for k, v in issues['duplicate_rfcs'].items() if len(v) > 1}
    issues['duplicate_chunk_ids'] = {k: v for k, v in issues['duplicate_chunk_ids'].items() if len(v) > 1}

    return chunks, issues

def print_report(chunks, issues):
    """Print comprehensive audit report."""

    print("=" * 80)
    print("VELANTRIM V8 CRYSTAL SPRINT1 METADATA AUDIT REPORT")
    print("=" * 80)
    print(f"\nTotal chunks: {len(chunks)}\n")

    # Summary
    print("SUMMARY OF ISSUES:")
    print(f"  RFC mismatches: {len(issues['rfc_mismatches'])}")
    print(f"  Duplicate RFC numbers: {len(issues['duplicate_rfcs'])}")
    print(f"  Cyrillic chunk_ids: {len(issues['cyrillic_chunk_ids'])}")
    print(f"  Chunks with layer=null: {len(issues['null_layers'])}")
    print(f"  Chunks with empty depends_on: {len(issues['empty_depends_on'])}")
    print(f"  Mega-blobs (>50k chars): {len(issues['mega_blobs'])}")
    print(f"  Empty stubs (<150 chars): {len(issues['empty_stubs'])}")
    print(f"  Duplicate chunk_ids: {len(issues['duplicate_chunk_ids'])}")
    print(f"  RFC0067 version inconsistencies: {len(issues['rfc0067_versions'])}\n")

    # RFC mismatches
    if issues['rfc_mismatches']:
        print("RFC MISMATCHES (CRITICAL):")
        for issue in issues['rfc_mismatches']:
            print(f"  [idx {issue['idx']}] {issue['chunk_id'][:50]}")
            print(f"    RFC field: {issue['rfc_field']} | Title RFC: {issue['title_rfc']}")
            print(f"    Title: {issue['title']}\n")

    # Duplicate RFCs
    if issues['duplicate_rfcs']:
        print("DUPLICATE RFC NUMBERS:")
        for rfc, indices in sorted(issues['duplicate_rfcs'].items()):
            print(f"  {rfc}: indices {indices}\n")

    # RFC0067 version issues
    if issues['rfc0067_versions']:
        print("RFC0067 VERSION INCONSISTENCIES:")
        for issue in issues['rfc0067_versions']:
            print(f"  [idx {issue['idx']}] {issue['chunk_id'][:50]}")
            print(f"    RFC: {issue['rfc']} | Title: {issue['title'][:60]}")
            print(f"    Problem: {issue['issue']}\n")

    # Cyrillic chunk_ids
    if issues['cyrillic_chunk_ids']:
        print("CYRILLIC CHUNK_IDS (NOT URL-SAFE):")
        for issue in issues['cyrillic_chunk_ids'][:10]:
            print(f"  [idx {issue['idx']}] {issue['chunk_id']}\n")
        if len(issues['cyrillic_chunk_ids']) > 10:
            print(f"  ... and {len(issues['cyrillic_chunk_ids']) - 10} more\n")

    # Mega-blobs
    if issues['mega_blobs']:
        print("MEGA-BLOBS (>50k chars):")
        for issue in issues['mega_blobs']:
            print(f"  [idx {issue['idx']}] {issue['title']} ({issue['char_count']} chars)\n")

    # Empty stubs
    if issues['empty_stubs']:
        print("EMPTY STUBS (<150 chars):")
        for issue in issues['empty_stubs']:
            print(f"  [idx {issue['idx']}] {issue['title']} ({issue['char_count']} chars)\n")

    # Duplicate chunk_ids
    if issues['duplicate_chunk_ids']:
        print("DUPLICATE CHUNK_IDS:")
        for chunk_id, indices in sorted(issues['duplicate_chunk_ids'].items()):
            print(f"  {chunk_id}: indices {indices}\n")

    print("=" * 80)

if __name__ == '__main__':
    jsonl_path = Path(__file__).parent / 'docs' / 'Velantrim_V8_Crystal_Sprint1.jsonl'

    if not jsonl_path.exists():
        print(f"Error: {jsonl_path} not found", file=sys.stderr)
        sys.exit(1)

    chunks, issues = audit_jsonl(jsonl_path)
    print_report(chunks, issues)

    # Save detailed issues to JSON for programmatic processing
    with open('audit_issues.json', 'w', encoding='utf-8') as f:
        json.dump(issues, f, ensure_ascii=False, indent=2)
    print(f"\nDetailed audit saved to audit_issues.json")
