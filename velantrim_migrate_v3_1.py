#!/usr/bin/env python3
"""
VELANTRIM MIGRATION CORE v3.1 – STABILIZED
P0 fixes: two-pass streaming (OOM), correct diff, regex compiled once,
has_cycle path=None, no deepcopy, safe_slug [:16] hash.
"""

import json
import shutil
import re
import hashlib
import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime
from collections import defaultdict

from utils.rfc_parser import extract_rfc

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

CYRILLIC_MAP = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ы': 'y', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '_',
    'ъ': '', 'ь': '', '—': '_', '–': '_', '\'': '', '"': '',
}

SEMANTIC_PREFIXES = {
    'рфс': 'rfc',
    'спецификация': 'spec',
    'протокол': 'proto',
    'слой': 'layer',
    'архитектура': 'arch',
    'интеграция': 'integration',
}

_CYRILLIC_RE = re.compile(r'[а-яА-Я]')

# A3: module-level counter for empty-text slugs (no repeated hash collisions)
_slug_counter = 0

# ----------------------------------------------------------------------
# Utilities
# ----------------------------------------------------------------------

def compute_checksum(chunks: List[Dict]) -> str:
    content = json.dumps(chunks, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()


def safe_slug(text: str, prefix: str = "vel") -> str:
    """
    Generate ASCII-safe ID. Uses [:16] hash to reduce collision risk.
    Empty/blank text gets a unique counter-based fallback.
    """
    global _slug_counter

    if not text or not text.strip():
        _slug_counter += 1
        return f"{prefix}_empty_{_slug_counter}"

    for ru_prefix, en_prefix in SEMANTIC_PREFIXES.items():
        if text.lower().startswith(ru_prefix):
            text = text[len(ru_prefix):].strip()
            prefix = en_prefix
            break

    base = ''.join(CYRILLIC_MAP.get(c, c) for c in text.lower())
    base = re.sub(r'[^a-z0-9_]', '', base)
    base = re.sub(r'_+', '_', base).strip('_')

    if not base:
        base = 'unnamed'

    # A6: [:16] reduces collision probability vs old [:8]
    h = hashlib.sha256(text.encode()).hexdigest()[:16]
    slug = f"{prefix}_{base}_{h}"
    if len(slug) > 200:
        slug = f"{prefix}_{base[:100]}_{h}"

    return slug


def compile_id_pattern(id_map: Dict[str, str]) -> Optional[re.Pattern]:
    """A3: Compile replacement regex once from id_map for reuse across all chunks."""
    if not id_map:
        return None
    sorted_keys = sorted(id_map.keys(), key=len, reverse=True)
    escaped = [re.escape(k) for k in sorted_keys]
    return re.compile(r'(?<!\w)(' + '|'.join(escaped) + r')(?!\w)')


def replace_ids_safe(text: str, id_map: Dict[str, str],
                     pattern: Optional[re.Pattern] = None) -> str:
    """
    Single-pass word-boundary replacement.
    Pass a pre-compiled pattern (from compile_id_pattern) to avoid
    re-compiling on every chunk.
    """
    if not id_map or not text:
        return text
    if pattern is None:
        pattern = compile_id_pattern(id_map)
    return pattern.sub(lambda m: id_map[m.group(1)], text)


# ----------------------------------------------------------------------
# Dependency validation (A4 fix: adjacency map + path=None)
# ----------------------------------------------------------------------

def validate_dependency_chain(chunks: List[Dict]) -> Dict[str, Any]:
    """
    Detect cycles, dangling refs, RFC duplicates.
    A4: builds adjacency map upfront (O(N+E)), uses path=None default.
    """
    id_set = {c.get("chunk_id") for c in chunks if "chunk_id" in c}

    # O(N) adjacency map — avoids O(N²) search inside has_cycle
    adjacency: Dict[str, List[str]] = {
        c["chunk_id"]: c.get("depends_on", [])
        for c in chunks if "chunk_id" in c
    }

    report: Dict[str, Any] = {
        'cycles': [],
        'dangling': [],
        'orphaned': [],
        'rfc_duplicates': defaultdict(list),
    }

    visited: Set[str] = set()
    rec_stack: Set[str] = set()

    def has_cycle(node_id: str, path: Optional[List[str]] = None) -> bool:
        # A4: path=None prevents shared mutable default across calls
        if path is None:
            path = []
        if node_id in rec_stack:
            report['cycles'].append(path + [node_id])
            return True
        if node_id in visited:
            return False

        visited.add(node_id)
        rec_stack.add(node_id)

        for dep in adjacency.get(node_id, []):
            if has_cycle(dep, path + [node_id]):
                return True

        rec_stack.remove(node_id)
        return False

    for cid in id_set:
        if cid and cid not in visited:
            has_cycle(cid)

    for c in chunks:
        for dep in c.get('depends_on', []):
            if dep not in id_set:
                report['dangling'].append({'chunk': c.get('chunk_id'), 'missing': dep})

    for c in chunks:
        if c.get('rfc'):
            report['rfc_duplicates'][c.get('rfc')].append(c.get('chunk_id'))
    report['rfc_duplicates'] = {
        k: v for k, v in report['rfc_duplicates'].items() if len(v) > 1
    }

    return report


def _validate_adjacency(
    id_set: Set[str],
    adjacency: Dict[str, List[str]],
) -> Dict[str, Any]:
    """Lightweight O(N+E) validation from streaming pass data."""
    report: Dict[str, Any] = {'cycles': [], 'dangling': []}

    visited: Set[str] = set()
    rec_stack: Set[str] = set()

    def has_cycle(node_id: str, path: Optional[List[str]] = None) -> bool:
        if path is None:
            path = []
        if node_id in rec_stack:
            report['cycles'].append(path + [node_id])
            return True
        if node_id in visited:
            return False
        visited.add(node_id)
        rec_stack.add(node_id)
        for dep in adjacency.get(node_id, []):
            if has_cycle(dep, path + [node_id]):
                return True
        rec_stack.remove(node_id)
        return False

    for node_id in id_set:
        if node_id not in visited:
            has_cycle(node_id)

    for node_id, deps in adjacency.items():
        for dep in deps:
            if dep not in id_set:
                report['dangling'].append({'chunk': node_id, 'missing': dep})

    return report


# ----------------------------------------------------------------------
# compute_diff (A2 fix: dict-based, handles added/removed)
# ----------------------------------------------------------------------

def compute_diff(
    old: List[Dict], new: List[Dict]
) -> Tuple[List[Dict], List[str], List[str]]:
    """
    A2: dict-keyed diff — correct when lists differ in length.
    Returns (modified_entries, added_ids, deleted_ids).
    """
    old_dict = {c['chunk_id']: c for c in old if 'chunk_id' in c}
    new_dict = {c['chunk_id']: c for c in new if 'chunk_id' in c}

    old_keys = set(old_dict)
    new_keys = set(new_dict)

    added = sorted(new_keys - old_keys)
    deleted = sorted(old_keys - new_keys)

    modified = []
    field_changes = 0
    for k in old_keys & new_keys:
        o, n = old_dict[k], new_dict[k]
        if o != n:
            changes = {}
            for field in set(o) | set(n):
                if o.get(field) != n.get(field):
                    changes[field] = {"old": o.get(field), "new": n.get(field)}
                    field_changes += 1
            modified.append({"id": k, "changes": changes})

    logger.info(
        f"✅ Diff: {len(modified)} modified, {len(added)} added, "
        f"{len(deleted)} deleted ({field_changes} field changes)"
    )
    return modified, added, deleted


# ----------------------------------------------------------------------
# Legacy loaders (used by validate/diff CLI commands)
# ----------------------------------------------------------------------

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    chunks = []
    with open(path, encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                chunks.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"JSON error at line {i}: {e}")
    logger.info(f"✅ Loaded {len(chunks)} chunks from {path}")
    return chunks


# ----------------------------------------------------------------------
# A1: Two-Pass Streaming helpers
# ----------------------------------------------------------------------

def _build_id_map_streaming(input_file: str) -> Dict[str, str]:
    """
    Pass 1: stream input, build Cyrillic→ASCII id_map.
    O(cyrillic_ids) memory — no chunk list held.
    """
    id_map: Dict[str, str] = {}
    used_ids: Set[str] = set()

    with open(input_file, encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                chunk = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"JSON error at line {line_num}: {e}")

            old_id = chunk.get("chunk_id", "")
            if old_id:
                used_ids.add(old_id)

            if old_id and _CYRILLIC_RE.search(old_id):
                new_id = safe_slug(old_id)
                counter = 1
                base_new_id = new_id
                while new_id in used_ids:
                    new_id = f"{base_new_id}_{counter}"
                    counter += 1
                id_map[old_id] = new_id
                used_ids.add(new_id)

    logger.info(f"✅ Pass 1 complete: {len(id_map)} ID translations")
    return id_map


def _stream_process(
    input_file: str,
    output_tmp: Optional[str],
    id_map: Dict[str, str],
    pattern: Optional[re.Pattern],
) -> Tuple[List[Dict], Dict[str, int], Dict[str, int], Set[str], Dict[str, List[str]]]:
    """
    Pass 2: transform each chunk, write to output_tmp (or skip if None=dry-run).
    Returns (diff, meta_stats, link_stats, id_set, adjacency).
    No full chunk list in memory — one chunk at a time.
    """
    diff: List[Dict] = []
    meta_stats = {'rfc_fixed': 0, 'status_updated': 0, 'layers_added': 0}
    link_stats = {'depends_on_updated': 0, 'content_refs_updated': 0}
    id_set: Set[str] = set()
    adjacency: Dict[str, List[str]] = {}

    fout = open(output_tmp, 'w', encoding='utf-8') if output_tmp else None
    try:
        with open(input_file, encoding='utf-8') as fin:
            for line in fin:
                raw = line.strip()
                if not raw:
                    continue

                chunk = json.loads(raw)
                original = json.loads(raw)  # snapshot for diff

                # Apply id_map to chunk_id
                old_id = chunk.get("chunk_id", "")
                if old_id in id_map:
                    chunk["chunk_id"] = id_map[old_id]

                # Metadata fixes
                title = chunk.get("title", "")
                rfc = extract_rfc(title)
                if rfc and not chunk.get("rfc"):
                    chunk["rfc"] = rfc
                    meta_stats['rfc_fixed'] += 1
                if "RFC0067" in title and chunk.get("rfc") != "RFC0067 v2.0":
                    chunk["rfc"] = "RFC0067 v2.0"
                    meta_stats['rfc_fixed'] += 1
                if len(chunk.get("content", "")) < 150 and chunk.get("status") != "deprecated":
                    chunk["status"] = "deprecated"
                    meta_stats['status_updated'] += 1
                if not chunk.get("layer"):
                    new_layer = None
                    if "L0" in title or "Ring Zero" in title:
                        new_layer = "L0"
                    elif "L1" in title or "session" in title.lower():
                        new_layer = "L1"
                    elif "L3" in title or "Neo4j" in title:
                        new_layer = "L3"
                    if new_layer:
                        chunk["layer"] = new_layer
                        meta_stats['layers_added'] += 1

                # Link updates
                deps = chunk.get("depends_on", [])
                if isinstance(deps, str):
                    deps = [deps]
                elif not isinstance(deps, list):
                    deps = []
                new_deps = [id_map.get(d, d) for d in deps]
                if new_deps != deps:
                    link_stats['depends_on_updated'] += 1
                chunk["depends_on"] = new_deps

                if "content" in chunk and pattern:
                    orig_content = chunk["content"]
                    chunk["content"] = replace_ids_safe(chunk["content"], id_map, pattern)
                    if chunk["content"] != orig_content:
                        link_stats['content_refs_updated'] += 1

                # Track for validation (ids + adjacency only — not full content)
                new_id = chunk.get("chunk_id", "")
                if new_id:
                    id_set.add(new_id)
                    adjacency[new_id] = chunk.get("depends_on", [])

                # Inline diff
                if chunk != original:
                    changes = {}
                    for k in set(original) | set(chunk):
                        if original.get(k) != chunk.get(k):
                            changes[k] = {"old": original.get(k), "new": chunk.get(k)}
                    diff.append({"id": old_id or new_id, "changes": changes})

                if fout:
                    fout.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    finally:
        if fout:
            fout.close()

    logger.info(
        f"✅ Pass 2 complete: meta={meta_stats}, links={link_stats}, "
        f"diff_entries={len(diff)}"
    )
    return diff, meta_stats, link_stats, id_set, adjacency


# ----------------------------------------------------------------------
# validate_all (used by validate CLI — loads full file)
# ----------------------------------------------------------------------

def validate_all(chunks: List[Dict], id_map: Dict[str, str]) -> bool:
    ids = [c["chunk_id"] for c in chunks if "chunk_id" in c]
    if len(ids) != len(set(ids)):
        dupes = [x for x in set(ids) if ids.count(x) > 1]
        logger.error(f"❌ Duplicate chunk_ids: {dupes}")
        return False

    dep_report = validate_dependency_chain(chunks)

    if dep_report['cycles']:
        logger.warning(f"⚠️  {len(dep_report['cycles'])} dependency cycles")
        for cycle in dep_report['cycles'][:5]:
            logger.warning(f"   {' → '.join(cycle)}")
    if dep_report['dangling']:
        logger.warning(f"⚠️  {len(dep_report['dangling'])} dangling references")
    if dep_report['rfc_duplicates']:
        logger.warning(
            f"⚠️  RFC duplicates (intentional multi-section): "
            f"{len(dep_report['rfc_duplicates'])} RFCs"
        )

    for c in chunks:
        try:
            json.dumps(c, ensure_ascii=False)
        except Exception as e:
            logger.error(f"❌ Invalid JSON in chunk {c.get('chunk_id')}: {e}")
            return False

    with open("migration_dependency_report.json", "w", encoding='utf-8') as f:
        json.dump(dep_report, f, indent=2, ensure_ascii=False)
    logger.info("✅ Dependency report: migration_dependency_report.json")

    if id_map:
        leftover = []
        leftover_re = compile_id_pattern(id_map)
        for c in chunks:
            if "content" in c and leftover_re and leftover_re.search(c["content"]):
                leftover.append(c.get("chunk_id"))
        if leftover:
            logger.warning(f"⚠️  {len(leftover)} chunks still contain old IDs")
        else:
            logger.info("✅ No leftover old IDs in content")

    return True


# ----------------------------------------------------------------------
# Atomic write, backup
# ----------------------------------------------------------------------

def write_atomic(data: List[Dict], output: str) -> None:
    temp = output + ".tmp"
    with open(temp, "w", encoding='utf-8') as f:
        for c in data:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    Path(temp).rename(output)
    logger.info(f"✅ Atomic write complete: {output}")


def create_rollback_backup(input_file: str) -> str:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup = f"{Path(input_file).stem}_backup_{timestamp}.jsonl"
    shutil.copy(input_file, backup)
    logger.info(f"✅ Backup: {backup}")
    return backup


# ----------------------------------------------------------------------
# A1: run_pipeline — two-pass streaming, no deepcopy
# ----------------------------------------------------------------------

def run_pipeline(input_file: str, dry_run: bool = False,
                 skip_backup: bool = False) -> bool:
    logger.info("🚀 Starting Velantrim migration v3.1")
    logger.info(f"   Input: {input_file}  dry-run: {dry_run}")

    # Pass 1: build id_map (stream, minimal RAM)
    logger.info("📝 Pass 1: building ID map (streaming)...")
    id_map = _build_id_map_streaming(input_file)

    # A3: compile regex once from id_map
    pattern = compile_id_pattern(id_map)

    input_path = Path(input_file)
    output = str(input_path.parent / (input_path.stem + "_migrated.jsonl"))
    output_tmp = output + ".tmp"

    # Pass 2: transform + write (or dry-run: skip writing)
    logger.info("📝 Pass 2: transforming chunks (streaming)...")
    diff, meta_stats, link_stats, id_set, adjacency = _stream_process(
        input_file,
        None if dry_run else output_tmp,
        id_map,
        pattern,
    )

    if dry_run:
        total = sum(len(d.get("changes", {})) for d in diff)
        logger.info(
            f"🔍 DRY RUN: {len(diff)} chunks would change, {total} field changes."
        )
        logger.info("   No files written.")
        return True

    # Lightweight validation from adjacency built during pass 2
    logger.info("✔️  Validating...")
    dep_report = _validate_adjacency(id_set, adjacency)
    if dep_report['cycles']:
        logger.warning(f"⚠️  {len(dep_report['cycles'])} dependency cycles")
    if dep_report['dangling']:
        logger.warning(f"⚠️  {len(dep_report['dangling'])} dangling references")

    # Atomic rename
    Path(output_tmp).rename(output)
    logger.info(f"✅ Output: {output}")

    # Backup (after successful write so we don't backup and then fail)
    if not skip_backup:
        create_rollback_backup(input_file)

    # Audit files (written alongside input)
    diff_file = str(input_path.parent / (input_path.stem + "_diff.json"))
    with open(diff_file, "w", encoding='utf-8') as f:
        json.dump(diff, f, indent=2, ensure_ascii=False)
    logger.info(f"   Diff: {diff_file}")

    if id_map:
        mapping_file = str(input_path.parent / (input_path.stem + "_id_map.json"))
        with open(mapping_file, "w", encoding='utf-8') as f:
            json.dump(id_map, f, indent=2, ensure_ascii=False)
        logger.info(f"   ID map: {mapping_file}")

    total_changes = sum(len(d.get("changes", {})) for d in diff)
    logger.info("=" * 60)
    logger.info("✅ MIGRATION COMPLETE")
    logger.info(f"   ID translations: {len(id_map)}")
    logger.info(f"   Metadata fixes:  {meta_stats}")
    logger.info(f"   Link updates:    {link_stats}")
    logger.info(f"   Field changes:   {total_changes}")
    logger.info("=" * 60)
    return True


# ----------------------------------------------------------------------
# CLI commands
# ----------------------------------------------------------------------

def validate_standalone(file_path: str) -> None:
    chunks = load_jsonl(file_path)
    ids = [c.get("chunk_id") for c in chunks if "chunk_id" in c]
    id_set = set(ids)
    print(f"Chunks: {len(chunks)}  Unique IDs: {len(id_set)}")

    if len(ids) != len(id_set):
        dupes = [x for x in id_set if ids.count(x) > 1]
        print(f"❌ Duplicate chunk_ids: {dupes}")
    else:
        print("✅ chunk_ids unique")

    dangling = [
        (c.get("chunk_id"), dep)
        for c in chunks
        for dep in c.get("depends_on", [])
        if dep not in id_set
    ]
    if dangling:
        print(f"⚠️  Dangling refs: {len(dangling)}")
        with open("validate_dangling.json", "w", encoding='utf-8') as f:
            json.dump(dangling, f, indent=2, ensure_ascii=False)
    else:
        print("✅ References intact")

    cyrillic = [c.get("chunk_id") for c in chunks
                if _CYRILLIC_RE.search(c.get("chunk_id", ""))]
    if cyrillic:
        print(f"⚠️  Cyrillic IDs: {len(cyrillic)}: {cyrillic[:5]}")
    else:
        print("✅ No Cyrillic IDs")

    stubs = sum(1 for c in chunks if len(c.get("content", "")) < 150)
    null_layers = sum(1 for c in chunks if not c.get("layer"))
    print(f"Stubs (<150 chars): {stubs}  Null layer: {null_layers}")


def diff_files(old_path: str, new_path: str) -> None:
    old = load_jsonl(old_path)
    new = load_jsonl(new_path)
    modified, added, deleted = compute_diff(old, new)
    print(f"Modified: {len(modified)}  Added: {len(added)}  Deleted: {len(deleted)}")
    with open("diff_report.json", "w", encoding='utf-8') as f:
        json.dump({"modified": modified, "added": added, "deleted": deleted},
                  f, indent=2, ensure_ascii=False)
    print("Report saved to diff_report.json")


def do_rollback(backup_file: str, target_file: str) -> None:
    if not Path(backup_file).exists():
        print(f"❌ Backup not found: {backup_file}")
        sys.exit(1)
    shutil.copy(backup_file, target_file)
    print(f"✅ Restored: {target_file}")


def main() -> None:
    # A8: logging configured here, not at module import time
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler('velantrim_migration.log'),
            logging.StreamHandler(),
        ]
    )

    parser = argparse.ArgumentParser(prog="velantrim-migrate")
    sub = parser.add_subparsers(dest="command", required=True)

    m = sub.add_parser("migrate")
    m.add_argument("file")
    m.add_argument("--dry-run", action="store_true")
    m.add_argument("--skip-backup", action="store_true")

    v = sub.add_parser("validate")
    v.add_argument("file")

    d = sub.add_parser("diff")
    d.add_argument("old_file")
    d.add_argument("new_file")

    r = sub.add_parser("rollback")
    r.add_argument("backup_file")
    r.add_argument("target_file")

    args = parser.parse_args()

    if args.command == "migrate":
        ok = run_pipeline(args.file, args.dry_run, args.skip_backup)
        sys.exit(0 if ok else 1)  # A7: sys.exit not exit()
    elif args.command == "validate":
        validate_standalone(args.file)
    elif args.command == "diff":
        diff_files(args.old_file, args.new_file)
    elif args.command == "rollback":
        do_rollback(args.backup_file, args.target_file)


if __name__ == "__main__":
    main()
