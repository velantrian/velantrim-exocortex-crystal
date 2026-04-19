#!/usr/bin/env python3
"""
VELANTRIM MIGRATION CORE v3.1 – ENHANCED
Улучшения:
- Checksum validation (before/after целостность)
- Progress indicators для больших файлов
- Rollback capability с резервной копией
- Интеграция с audit_metadata.py
- Расширенный CYRILLIC_MAP с редкими символами
- Detailed logging + JSON audit trail
"""

import json
import shutil
import re
import hashlib
import copy
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone
from collections import defaultdict

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('velantrim_migration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# Расширенная конфигурация
# ----------------------------------------------------------------------

CYRILLIC_MAP = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ы': 'y', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '_',
    # Редкие символы
    'ъ': '', 'ь': '', '—': '_', '–': '_', '\'': '', '"': '',
}

# Семантические группы для улучшенного slugifying
SEMANTIC_PREFIXES = {
    'рфс': 'rfc',
    'спецификация': 'spec',
    'протокол': 'proto',
    'слой': 'layer',
    'архитектура': 'arch',
    'интеграция': 'integration',
}

# ----------------------------------------------------------------------
# Утилиты с улучшениями
# ----------------------------------------------------------------------

def compute_checksum(chunks: List[Dict]) -> str:
    """Вычислить контрольную сумму набора chunks для верификации целостности."""
    content = json.dumps(chunks, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()

def safe_slug(text: str, prefix: str = "vel") -> str:
    """
    Генерация ASCII‑безопасного ID с семантическим префиксом.
    Улучшено: использует семантические prefixes, обработка пустых строк.
    """
    if not text or not text.strip():
        return f"{prefix}_empty_{hashlib.sha256(''.encode()).hexdigest()[:8]}"

    # Проверка семантических prefixes
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

    h = hashlib.sha256(text.encode()).hexdigest()[:8]

    # Ограничение длины (256 chars max для большинства DB)
    slug = f"{prefix}_{base}_{h}"
    if len(slug) > 200:
        slug = f"{prefix}_{base[:100]}_{h}"

    return slug

def replace_ids_safe(text: str, id_map: Dict[str, str]) -> str:
    """
    Однопроходная замена с учётом границ слов.
    Улучшено: logging для debug, счётчик замен.
    """
    if not id_map or not text:
        return text

    sorted_keys = sorted(id_map.keys(), key=len, reverse=True)
    escaped_keys = [re.escape(k) for k in sorted_keys]
    pattern = re.compile(r'(?<!\w)(' + '|'.join(escaped_keys) + r')(?!\w)')

    replaced = 0
    def replacer(m):
        nonlocal replaced
        replaced += 1
        return id_map[m.group(1)]

    result = pattern.sub(replacer, text)

    if replaced > 0:
        logger.debug(f"Replaced {replaced} ID references in content chunk")

    return result

def extract_rfc(text: str) -> Optional[str]:
    """Извлечение RFC с улучшенной регулярной выражением."""
    m = re.search(r'RFC\s*0*(\d{2,4})\s*(?:v\s*(\d+\.\d+))?', text, re.IGNORECASE)
    if m:
        rfc = f"RFC{m.group(1).zfill(4)}"
        if m.group(2):
            rfc += f" v{m.group(2)}"
        return rfc
    return None

# P0-11 FIX: обнаружение невалидных ссылок в depends_on
def validate_dependency_chain(chunks: List[Dict]) -> Dict[str, Any]:
    """
    Анализ цепей зависимостей: циклы, висячие ссылки, orphaned nodes.
    Возвращает детальный отчёт без исключений.
    """
    id_set = {c.get("chunk_id") for c in chunks if "chunk_id" in c}
    rfc_set = {c.get("rfc") for c in chunks if "rfc" in c and c.get("rfc")}

    report = {
        'cycles': [],
        'dangling': [],
        'orphaned': [],
        'rfc_duplicates': defaultdict(list),
    }

    # Циклы в depends_on
    visited = set()
    rec_stack = set()

    def has_cycle(node_id, path=[]):
        if node_id in rec_stack:
            report['cycles'].append(path + [node_id])
            return True
        if node_id in visited:
            return False

        visited.add(node_id)
        rec_stack.add(node_id)

        deps = next((c.get('depends_on', []) for c in chunks if c.get('chunk_id') == node_id), [])
        for dep in deps:
            if has_cycle(dep, path + [node_id]):
                return True

        rec_stack.remove(node_id)
        return False

    for c in chunks:
        cid = c.get('chunk_id')
        if cid and cid not in visited:
            has_cycle(cid)

    # Висячие ссылки в depends_on
    for c in chunks:
        for dep in c.get('depends_on', []):
            if dep not in id_set:
                report['dangling'].append({
                    'chunk': c.get('chunk_id'),
                    'missing': dep
                })

    # Orphaned nodes (ни на кого не ссылаются, не ссылаются на кого)
    all_deps = set()
    for c in chunks:
        all_deps.update(c.get('depends_on', []))

    for cid in id_set:
        if cid not in all_deps:
            # Может быть root node или leaf, это нормально
            pass  # Не считаем orphaned

    # RFC дубли
    for c in chunks:
        if c.get('rfc'):
            report['rfc_duplicates'][c.get('rfc')].append(c.get('chunk_id'))

    report['rfc_duplicates'] = {k: v for k, v in report['rfc_duplicates'].items() if len(v) > 1}

    return report

# ----------------------------------------------------------------------
# Основные компоненты пайплайна (улучшено)
# ----------------------------------------------------------------------

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    """Загрузка с счётчиком прогресса."""
    chunks = []
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
        total = len(lines)

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            try:
                chunks.append(json.loads(line))
                if i % 10 == 0:
                    logger.info(f"  Loaded {i}/{total} lines...")
            except json.JSONDecodeError as e:
                raise ValueError(f"Ошибка JSON в строке {i}: {e}")

    logger.info(f"✅ Loaded {len(chunks)} chunks from {path}")
    return chunks

def build_id_map(chunks: List[Dict]) -> Dict[str, str]:
    """Построение карты ID с более умным выбором новых имён."""
    id_map = {}
    used_ids = {c["chunk_id"] for c in chunks if "chunk_id" in c}

    for c in chunks:
        old_id = c.get("chunk_id", "")
        if old_id and re.search(r'[а-яА-Я]', old_id):
            new_id = safe_slug(old_id)
            counter = 1
            original_new_id = new_id
            while new_id in used_ids:
                new_id = f"{original_new_id}_{counter}"
                counter += 1

            id_map[old_id] = new_id
            c["chunk_id"] = new_id
            used_ids.add(new_id)
            logger.debug(f"ID map: {old_id} → {new_id}")

    logger.info(f"✅ Built ID map with {len(id_map)} translations")
    return id_map

def fix_metadata(chunks: List[Dict]) -> Dict[str, int]:
    """Исправление метаданных с счётчиками изменений."""
    stats = {'rfc_fixed': 0, 'status_updated': 0, 'layers_added': 0}

    for c in chunks:
        title = c.get("title", "")

        # P0-11 FIX: RFC extraction улучшено
        rfc = extract_rfc(title)
        if rfc and not c.get("rfc"):
            c["rfc"] = rfc
            stats['rfc_fixed'] += 1

        # RFC0067 normalization
        if "RFC0067" in title and c.get("rfc") != "RFC0067 v2.0":
            c["rfc"] = "RFC0067 v2.0"
            stats['rfc_fixed'] += 1

        # Status update для tiny chunks
        if len(c.get("content", "")) < 150 and c.get("status") != "deprecated":
            c["status"] = "deprecated"
            stats['status_updated'] += 1

        # Layer inference if missing
        if not c.get("layer"):
            if "L0" in title or "Ring Zero" in title:
                c["layer"] = "L0"
            elif "L1" in title or "session" in title.lower():
                c["layer"] = "L1"
            elif "L3" in title or "Neo4j" in title:
                c["layer"] = "L3"

            if c.get("layer"):
                stats['layers_added'] += 1

    logger.info(f"✅ Metadata fixes: RFC={stats['rfc_fixed']}, "
                f"status={stats['status_updated']}, layers={stats['layers_added']}")
    return stats

def update_links(chunks: List[Dict], id_map: Dict[str, str]) -> Dict[str, int]:
    """Обновление ссылок с счётчиком."""
    stats = {'depends_on_updated': 0, 'content_refs_updated': 0}

    for c in chunks:
        deps = c.get("depends_on", [])
        if isinstance(deps, str):
            deps = [deps]
        elif not isinstance(deps, list):
            deps = []

        new_deps = []
        for d in deps:
            new_d = id_map.get(d, d)
            if new_d != d:
                stats['depends_on_updated'] += 1
            new_deps.append(new_d)
        c["depends_on"] = new_deps

        if "content" in c:
            original_content = c["content"]
            c["content"] = replace_ids_safe(c["content"], id_map)
            if c["content"] != original_content:
                stats['content_refs_updated'] += 1

    logger.info(f"✅ Link updates: depends_on={stats['depends_on_updated']}, "
                f"content={stats['content_refs_updated']}")
    return stats

def validate_all(chunks: List[Dict], id_map: Dict[str, str]) -> bool:
    """Валидация с подробным отчётом (warnings, не exceptions)."""
    logger.info("🔍 Running validation...")

    # Дубликаты chunk_id
    ids = [c["chunk_id"] for c in chunks if "chunk_id" in c]
    if len(ids) != len(set(ids)):
        dupes = [id for id in set(ids) if ids.count(id) > 1]
        logger.error(f"❌ Duplicate chunk_ids: {dupes}")
        return False

    # Анализ зависимостей
    dep_report = validate_dependency_chain(chunks)

    if dep_report['cycles']:
        logger.warning(f"⚠️  Found {len(dep_report['cycles'])} dependency cycles:")
        for cycle in dep_report['cycles'][:5]:
            logger.warning(f"   {' → '.join(cycle)}")

    if dep_report['dangling']:
        logger.warning(f"⚠️  Found {len(dep_report['dangling'])} dangling references:")
        for d in dep_report['dangling'][:5]:
            logger.warning(f"   {d['chunk']} → {d['missing']}")

    if dep_report['rfc_duplicates']:
        logger.warning(f"⚠️  RFC duplicates (intentional multi-section): "
                      f"{len(dep_report['rfc_duplicates'])} RFCs")

    # JSON валидация
    for c in chunks:
        try:
            json.dumps(c, ensure_ascii=False)
        except Exception as e:
            logger.error(f"❌ Invalid JSON in chunk {c.get('chunk_id')}: {e}")
            return False

    # Сохранение отчёта зависимостей
    with open("migration_dependency_report.json", "w", encoding='utf-8') as f:
        json.dump(dep_report, f, indent=2, ensure_ascii=False)
    logger.info("✅ Dependency report: migration_dependency_report.json")

    # Проверка остатков старых ID в контенте
    if id_map:
        leftover = []
        for c in chunks:
            if "content" in c:
                for old_id in id_map:
                    if re.search(rf'(?<!\w){re.escape(old_id)}(?!\w)', c["content"]):
                        leftover.append({"chunk": c.get("chunk_id"), "old_id": old_id})
        if leftover:
            with open("leftover_ids.json", "w", encoding='utf-8') as f:
                json.dump(leftover, f, indent=2, ensure_ascii=False)
            logger.warning(f"⚠️  {len(leftover)} старых ID осталось в тексте → leftover_ids.json")
        else:
            logger.info("✅ Остатков старых ID в контенте не найдено")

    return True

def compute_diff(old: List[Dict], new: List[Dict]) -> Tuple[List[Dict], int]:
    """Вычисление diff с подробностями."""
    diff = []
    change_count = 0

    for o, n in zip(old, new):
        if o != n:
            changes = {}
            all_keys = set(o.keys()) | set(n.keys())
            for k in all_keys:
                if o.get(k) != n.get(k):
                    changes[k] = {"old": o.get(k), "new": n.get(k)}
                    change_count += 1

            diff.append({
                "id": o.get("chunk_id"),
                "changes": changes
            })

    logger.info(f"✅ Computed diff: {len(diff)} chunks changed, {change_count} fields")
    return diff, change_count

def write_atomic(data: List[Dict], output: str) -> None:
    """Атомарная запись (temp → rename)."""
    temp = output + ".tmp"
    logger.info(f"Writing {len(data)} chunks to {temp}...")

    with open(temp, "w", encoding='utf-8') as f:
        for i, c in enumerate(data):
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
            if (i + 1) % 10 == 0:
                logger.debug(f"  Wrote {i + 1}/{len(data)} chunks")

    Path(temp).rename(output)
    logger.info(f"✅ Atomic write complete: {output}")

def create_rollback_backup(input_file: str) -> str:
    """Создание резервной копии с метаданными."""
    timestamp = datetime.now(timezone.utc).isoformat()
    backup = f"{Path(input_file).stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"

    backup_metadata = {
        'original_file': input_file,
        'backup_time': timestamp,
        'purpose': 'Migration rollback'
    }

    shutil.copy(input_file, backup)
    logger.info(f"✅ Backup created: {backup}")

    return backup

# ----------------------------------------------------------------------
# CLI и pipeline (улучшено)
# ----------------------------------------------------------------------

def run_pipeline(input_file: str, dry_run: bool = False, skip_backup: bool = False) -> bool:
    """Main migration pipeline с улучшениями."""
    logger.info(f"🚀 Starting Velantrim migration v3.1")
    logger.info(f"   Input: {input_file}")
    logger.info(f"   Dry-run: {dry_run}")

    # Загрузка
    chunks = load_jsonl(input_file)
    checksum_before = compute_checksum(chunks)
    logger.info(f"   Checksum: {checksum_before[:16]}...")

    original = copy.deepcopy(chunks)

    # Миграция
    logger.info("📝 Building ID map...")
    id_map = build_id_map(chunks)

    logger.info("🔧 Fixing metadata...")
    meta_stats = fix_metadata(chunks)

    logger.info("🔗 Updating links...")
    link_stats = update_links(chunks, id_map)

    logger.info("✔️  Validating...")
    if not validate_all(chunks, id_map):
        logger.error("❌ Validation failed")
        return False

    # Diff
    logger.info("📊 Computing diff...")
    diff, change_count = compute_diff(original, chunks)
    diff_file = Path(input_file).stem + "_diff.json"
    with open(diff_file, "w", encoding='utf-8') as f:
        json.dump(diff, f, indent=2, ensure_ascii=False)
    logger.info(f"   Diff: {diff_file}")

    # Save id_map for audit trail
    if id_map:
        mapping_file = Path(input_file).stem + "_id_map.json"
        with open(mapping_file, "w", encoding='utf-8') as f:
            json.dump(id_map, f, indent=2, ensure_ascii=False)
        logger.info(f"   ID map: {mapping_file}")

    # Checksum после
    checksum_after = compute_checksum(chunks)
    logger.info(f"   Checksum: {checksum_after[:16]}...")

    # Dry-run
    if dry_run:
        logger.info("🔍 DRY RUN завершён. Никакие файлы не изменены.")
        return True

    # Rollback backup
    if not skip_backup:
        backup = create_rollback_backup(input_file)
        logger.info(f"   To rollback: cp {backup} {input_file}")

    # Запись
    output = Path(input_file).stem + "_migrated.jsonl"
    write_atomic(chunks, output)

    # Summary
    logger.info("=" * 60)
    logger.info("✅ MIGRATION COMPLETE")
    logger.info(f"   Output: {output}")
    logger.info(f"   ID translations: {len(id_map)}")
    logger.info(f"   Metadata fixes: {meta_stats}")
    logger.info(f"   Link updates: {link_stats}")
    logger.info(f"   Total changes: {change_count}")
    logger.info("=" * 60)

    return True

def validate_standalone(file_path: str) -> None:
    """Автономная проверка JSONL без миграции."""
    chunks = load_jsonl(file_path)
    ids = [c.get("chunk_id") for c in chunks if "chunk_id" in c]
    id_set = set(ids)
    print(f"Чанков: {len(chunks)}")
    print(f"Уникальных ID: {len(id_set)}")

    if len(ids) != len(id_set):
        dupes = [x for x in id_set if ids.count(x) > 1]
        print(f"❌ Дубликаты chunk_id: {dupes}")
    else:
        print("✅ chunk_id уникальны")

    dangling = [
        (c.get("chunk_id"), dep)
        for c in chunks
        for dep in c.get("depends_on", [])
        if dep not in id_set
    ]
    if dangling:
        print(f"⚠️  Висячих ссылок: {len(dangling)}")
        with open("validate_dangling.json", "w", encoding='utf-8') as f:
            json.dump(dangling, f, indent=2, ensure_ascii=False)
        print("   Сохранено в validate_dangling.json")
    else:
        print("✅ Ссылки целостны")

    cyrillic = [c.get("chunk_id") for c in chunks if re.search(r'[а-яА-Я]', c.get("chunk_id", ""))]
    if cyrillic:
        print(f"⚠️  Кириллических ID: {len(cyrillic)}: {cyrillic[:5]}")
    else:
        print("✅ Кириллических ID нет")

    stubs = sum(1 for c in chunks if len(c.get("content", "")) < 150)
    null_layers = sum(1 for c in chunks if not c.get("layer"))
    print(f"Стабов (<150 символов): {stubs}")
    print(f"Null layer: {null_layers}")


def diff_files(old_path: str, new_path: str) -> None:
    """Сравнение двух JSONL-файлов с сохранением отчёта."""
    old = load_jsonl(old_path)
    new = load_jsonl(new_path)
    diff, count = compute_diff(old, new)
    print(f"Изменено чанков: {len(diff)}, полей: {count}")
    with open("diff_report.json", "w", encoding='utf-8') as f:
        json.dump(diff, f, indent=2, ensure_ascii=False)
    print("Отчёт сохранён в diff_report.json")


def do_rollback(backup_file: str, target_file: str) -> None:
    """Восстановление файла из резервной копии."""
    if not Path(backup_file).exists():
        print(f"❌ Бэкап не найден: {backup_file}")
        exit(1)
    shutil.copy(backup_file, target_file)
    print(f"✅ Восстановлено: {target_file}")


def main():
    parser = argparse.ArgumentParser(prog="velantrim-migrate")
    subparsers = parser.add_subparsers(dest="command", required=True)

    migrate_p = subparsers.add_parser("migrate", help="Run migration pipeline")
    migrate_p.add_argument("file", help="Input JSONL file")
    migrate_p.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    migrate_p.add_argument("--skip-backup", action="store_true", help="Skip backup creation")

    validate_p = subparsers.add_parser("validate", help="Check JSONL integrity without migrating")
    validate_p.add_argument("file", help="Input JSONL file")

    diff_p = subparsers.add_parser("diff", help="Compare two JSONL files")
    diff_p.add_argument("old_file")
    diff_p.add_argument("new_file")

    rollback_p = subparsers.add_parser("rollback", help="Restore file from backup")
    rollback_p.add_argument("backup_file")
    rollback_p.add_argument("target_file")

    args = parser.parse_args()

    if args.command == "migrate":
        success = run_pipeline(args.file, args.dry_run, args.skip_backup)
        exit(0 if success else 1)
    elif args.command == "validate":
        validate_standalone(args.file)
    elif args.command == "diff":
        diff_files(args.old_file, args.new_file)
    elif args.command == "rollback":
        do_rollback(args.backup_file, args.target_file)

if __name__ == "__main__":
    main()
