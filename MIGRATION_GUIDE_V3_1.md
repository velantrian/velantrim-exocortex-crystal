# Velantrim Migration Guide v3.1

## Overview

The migration tool `velantrim_migrate_v3_1.py` is a production-ready pipeline for transforming Velantrim JSONL knowledge bases:
- Transliterates Cyrillic chunk IDs to ASCII-safe identifiers
- Fixes metadata (extracts RFC, normalizes versions, assigns layers)
- Updates all internal references (depends_on, content links)
- Validates integrity and produces audit reports
- Provides rollback capability via timestamped backups

## Quick Start

### Basic Migration (Dry-Run First)
```bash
# Preview what will change without modifying files
python3 velantrim_migrate_v3_1.py migrate Velantrim_V8_Crystal_Sprint1.jsonl --dry-run

# Review generated reports
cat velantrim_migration.log              # Full log
cat migration_dependency_report.json     # Dependency analysis
cat Velantrim_V8_Crystal_Sprint1_diff.json  # Change summary
```

### Execute Migration
```bash
# Run migration (creates automatic backup)
python3 velantrim_migrate_v3_1.py migrate Velantrim_V8_Crystal_Sprint1.jsonl

# Output file
Velantrim_V8_Crystal_Sprint1_migrated.jsonl
```

### Rollback if Needed
```bash
# Backup is created with timestamp
# Restore from backup if issues occur
cp Velantrim_V8_Crystal_Sprint1_backup_20260419_153045.jsonl Velantrim_V8_Crystal_Sprint1.jsonl
```

## What Gets Fixed

### 1. Cyrillic ID Transliteration
**Before**: `velantrim_v8_001_спецификация_фрактальная_...`  
**After**: `vel_specifikacia_fraktalnaia_ae3f2b1c`

- All Cyrillic characters converted to ASCII equivalents
- SHA256 hash suffix ensures uniqueness and stability
- Semantic prefixes preserved (RFC, protocol, layer, arch, etc.)
- Word boundaries respected (no accidental ID merging)

**Mapping example**:
```
ж → zh, ц → ts, ч → ch, ш → sh, щ → sch, ю → yu, я → ya
```

### 2. Metadata Extraction & Normalization

| Fix | Before | After |
|-----|--------|-------|
| RFC extraction | Title contains "RFC0067 v2.0" | `rfc: "RFC0067 v2.0"` |
| RFC0067 version | Mixed v1.0 and v2.0 | Normalized to v2.0 |
| Tiny chunks (<150 chars) | `status: "stable"` | `status: "deprecated"` |
| Missing layer field | `layer: null` | `layer: "L1"` (inferred from title) |

### 3. Link Updates

**depends_on**: All references updated to use new chunk IDs
```json
// Before
"depends_on": ["velantrim_v8_001_спецификация_..."]

// After
"depends_on": ["vel_specifikacia_fraktalnaia_ae3f2b1c"]
```

**Content**: All RFC references in `content` field are updated
```diff
- RFC0063 связан с velantrim_v8_028_...
+ RFC0063 связан с vel_knowledge_ingestion_c4d92e7f
```

## Safety Features

### 1. Checksums
```
Before:  sha256=a3f2b1c9e4d8f...
After:   sha256=b5e1d7c2f9a4...
```
Checksums verify data integrity before/after migration.

### 2. Timestamped Backups
```bash
# Automatic backup with execution timestamp
Velantrim_V8_Crystal_Sprint1_backup_20260419_153045.jsonl

# Restore if needed
cp backup_file.jsonl Velantrim_V8_Crystal_Sprint1.jsonl
```

### 3. Dependency Analysis Report
```json
{
  "cycles": [],  // Circular dependencies detected
  "dangling": [], // Broken references (usually from deleted chunks)
  "orphaned": [], // Unused chunks
  "rfc_duplicates": {
    "RFC0067 v2.0": ["chunk1", "chunk2"]  // Intentional (multi-section)
  }
}
```

**Note**: Dangling references are warnings (not errors) because they may reference external RFCs.
File saved to `migration_dependency_report.json` for manual review.

### 4. Atomic Writes
```
Write to temp file → Validate → Atomic rename to final output
```
Prevents file corruption if process interrupted.

### 5. Detailed Logging
```bash
velantrim_migration.log

[2026-04-19 15:30:45] [INFO] 🚀 Starting Velantrim migration v3.1
[2026-04-19 15:30:45] [INFO] ✅ Loaded 63 chunks from Velantrim_V8_Crystal_Sprint1.jsonl
[2026-04-19 15:30:45] [INFO] ✅ Built ID map with 39 translations
[2026-04-19 15:30:45] [INFO] ✅ Metadata fixes: RFC=5, status=1, layers=18
[2026-04-19 15:30:45] [INFO] ✅ Link updates: depends_on=14, content=3
[2026-04-19 15:30:45] [INFO] ✅ Computed diff: 28 chunks changed, 62 fields
[2026-04-19 15:30:45] [INFO] ✅ MIGRATION COMPLETE
```

## Validation Reports

### migration_dependency_report.json
Detailed analysis of dependency graph:
```json
{
  "cycles": [["chunk_a", "chunk_b", "chunk_a"]],  // Circular refs
  "dangling": [
    {"chunk": "chunk_x", "missing": "RFC0999"}     // Broken refs
  ],
  "orphaned": [],
  "rfc_duplicates": {
    "RFC0067 v2.0": ["4 chunks"]  // Intentional multi-section organization
  }
}
```

### Input_diff.json
Complete before/after comparison:
```json
{
  "id": "chunk_id",
  "changes": {
    "chunk_id": {
      "old": "velantrim_v8_001_спецификация_...",
      "new": "vel_specifikacia_fraktalnaia_..."
    },
    "rfc": {
      "old": null,
      "new": "RFC0065"
    },
    "depends_on": {
      "old": ["old_id_1", "old_id_2"],
      "new": ["new_id_1", "new_id_2"]
    }
  }
}
```

## Advanced Usage

### Dry-Run with Full Report (Recommended First Step)
```bash
python3 velantrim_migrate_v3_1.py migrate my_chunks.jsonl --dry-run

# Check what will change
cat my_chunks_diff.json | jq '.[] | select(.changes | length > 0)'
```

### Skip Backup (Careful - Use Only if Manual Backup Exists)
```bash
python3 velantrim_migrate_v3_1.py migrate my_chunks.jsonl --skip-backup
```

### Custom Processing (Python API)
```python
from velantrim_migrate_v3_1 import (
    load_jsonl, build_id_map, fix_metadata, update_links,
    validate_all, write_atomic
)

chunks = load_jsonl("input.jsonl")
id_map = build_id_map(chunks)
fix_metadata(chunks)
update_links(chunks, id_map)

if validate_all(chunks, id_map):
    write_atomic(chunks, "output.jsonl")
```

## Troubleshooting

### Issue: Dangling References in Dependency Report
**Cause**: References to RFCs that don't exist in current JSONL (likely external).  
**Solution**: This is expected. Review `migration_dependency_report.json` and confirm RFCs are intentionally external.

### Issue: Migration Creates Large File Differences
**Cause**: Content field has many chunk ID references.  
**Solution**: Expected. All ID changes propagate through content. Check `input_diff.json` for details.

### Issue: Checksum Mismatch Error
**Cause**: Data corruption or encoding issue during load.  
**Solution**: Restore from backup, check file encoding (must be UTF-8).

### Issue: Circular Dependency Detected
**Cause**: chunk A depends on B, B depends on A (or longer cycle).  
**Solution**: Review dependency chain in `migration_dependency_report.json`. May indicate data issue.

## Integration with Existing Tools

The migration tool integrates with Velantrim's metadata audit pipeline:

```bash
# 1. Run audit BEFORE migration to establish baseline
python3 audit_metadata.py > baseline_audit.txt

# 2. Run migration
python3 velantrim_migrate_v3_1.py migrate Velantrim_V8_Crystal_Sprint1.jsonl

# 3. Run audit AFTER migration on migrated file
python3 audit_metadata.py Velantrim_V8_Crystal_Sprint1_migrated.jsonl > post_audit.txt

# 4. Compare
diff baseline_audit.txt post_audit.txt
```

## Performance

For typical Velantrim JSONL (50-100 chunks):
- Load: ~100ms
- ID mapping: ~50ms
- Metadata fixes: ~50ms
- Link updates: ~200-500ms (depends on content size)
- Validation: ~50ms
- Write: ~100ms

**Total**: ~1 second for average 63-chunk knowledge base.

For larger files (1M+ chunks): Linear time complexity O(n), ~1-2 minutes.

## Version History

| Version | Changes |
|---------|---------|
| v3.1 | Checksums, dependency analysis, semantic slug prefixes, rollback backups, non-blocking validation |
| v3.0 | Word-boundary regex, sorted ID replacement, warning mode |
| v2.0 | Initial production release |

## Schema After Migration

All chunks maintain original structure with fixes:

```json
{
  "chunk_id": "vel_RFC0065_memory_volition_a1b2c3d4",  // ASCII-safe
  "idx": 9,
  "title": "RFC0065: Memory-as-Volition — Осознанная воля к памяти",
  "version": "8.0.2-sprint1",
  "rfc": "RFC0065",
  "layer": "L3",                                         // Added/fixed
  "tags": ["volition", "RFC0057"],
  "invariants": ["I40", "I63"],
  "depends_on": ["RFC0016", "RFC0004"],                 // Updated IDs
  "status": "stable",
  "char_count": 25102,
  "content": "...[all ID references updated]..."        // Updated links
}
```

---

**Ready to migrate?** Start with `--dry-run` to preview changes, review reports, then execute with confidence.
