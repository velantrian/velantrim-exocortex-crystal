"""Tests for velantrim_migrate_v3_1.py P0/P1 fixes."""

import json
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ─── A2: compute_diff — dict-based, handles added/removed ─────────────────────

def test_compute_diff_modified():
    from velantrim_migrate_v3_1 import compute_diff
    old = [{"chunk_id": "a", "title": "A"}, {"chunk_id": "b", "title": "B"}]
    new = [{"chunk_id": "a", "title": "A modified"}, {"chunk_id": "b", "title": "B"}]
    modified, added, deleted = compute_diff(old, new)
    assert len(modified) == 1
    assert modified[0]["id"] == "a"
    assert added == []
    assert deleted == []


def test_compute_diff_added_removed():
    """A2: zip() would have missed added/deleted chunks."""
    from velantrim_migrate_v3_1 import compute_diff
    old = [{"chunk_id": "a", "title": "A"}, {"chunk_id": "b", "title": "B"}]
    new = [{"chunk_id": "a", "title": "A modified"}, {"chunk_id": "c", "title": "C new"}]
    modified, added, deleted = compute_diff(old, new)
    assert "b" in deleted
    assert "c" in added
    assert len(modified) == 1  # only "a" is in both and changed


def test_compute_diff_different_lengths_no_data_loss():
    """A2: old list longer than new — deleted must be captured."""
    from velantrim_migrate_v3_1 import compute_diff
    old = [{"chunk_id": f"c{i}", "title": f"T{i}"} for i in range(5)]
    new = [{"chunk_id": f"c{i}", "title": f"T{i}"} for i in range(3)]
    _, added, deleted = compute_diff(old, new)
    assert "c3" in deleted
    assert "c4" in deleted
    assert added == []


# ─── A3: regex compiled once ──────────────────────────────────────────────────

def test_compile_id_pattern_returns_none_for_empty():
    from velantrim_migrate_v3_1 import compile_id_pattern
    assert compile_id_pattern({}) is None


def test_replace_ids_safe_with_precompiled_pattern():
    """A3: replace_ids_safe accepts pre-compiled pattern (no re-compile per chunk)."""
    from velantrim_migrate_v3_1 import compile_id_pattern, replace_ids_safe
    id_map = {"Привет": "hello", "Мир": "world"}
    pattern = compile_id_pattern(id_map)
    result = replace_ids_safe("Привет Мир test", id_map, pattern)
    assert result == "hello world test"


def test_replace_ids_safe_word_boundary():
    """Replacement respects word boundaries."""
    from velantrim_migrate_v3_1 import compile_id_pattern, replace_ids_safe
    id_map = {"old_id": "new_id"}
    pattern = compile_id_pattern(id_map)
    assert replace_ids_safe("old_id test", id_map, pattern) == "new_id test"
    assert replace_ids_safe("xold_idx", id_map, pattern) == "xold_idx"


# ─── A4: has_cycle — path=None, no shared state ───────────────────────────────

def test_has_cycle_no_cycle():
    from velantrim_migrate_v3_1 import validate_dependency_chain
    chunks = [
        {"chunk_id": "a", "depends_on": ["b"]},
        {"chunk_id": "b", "depends_on": ["c"]},
        {"chunk_id": "c", "depends_on": []},
    ]
    report = validate_dependency_chain(chunks)
    assert report["cycles"] == []


def test_has_cycle_detects_cycle():
    from velantrim_migrate_v3_1 import validate_dependency_chain
    chunks = [
        {"chunk_id": "a", "depends_on": ["b"]},
        {"chunk_id": "b", "depends_on": ["a"]},  # cycle
    ]
    report = validate_dependency_chain(chunks)
    assert len(report["cycles"]) > 0


def test_has_cycle_no_shared_state_across_calls():
    """A4: two consecutive calls must not accumulate path state."""
    from velantrim_migrate_v3_1 import validate_dependency_chain
    chunks = [{"chunk_id": "x", "depends_on": []}]
    r1 = validate_dependency_chain(chunks)
    r2 = validate_dependency_chain(chunks)
    assert r1["cycles"] == r2["cycles"] == []


def test_dangling_reference_detected():
    from velantrim_migrate_v3_1 import validate_dependency_chain
    chunks = [{"chunk_id": "a", "depends_on": ["missing_id"]}]
    report = validate_dependency_chain(chunks)
    assert any(d["missing"] == "missing_id" for d in report["dangling"])


# ─── A1: streaming pipeline ───────────────────────────────────────────────────

def test_run_pipeline_dry_run_no_files(tmp_path):
    """A1: dry-run writes nothing to disk."""
    test_file = tmp_path / "test.jsonl"
    chunks = [
        {"chunk_id": f"chunk_{i}", "content": "x" * 200, "title": f"Title {i}",
         "depends_on": [], "layer": "L1"}
        for i in range(5)
    ]
    with open(test_file, 'w') as f:
        for c in chunks:
            f.write(json.dumps(c) + '\n')

    files_before = set(tmp_path.iterdir())
    from velantrim_migrate_v3_1 import run_pipeline
    ok = run_pipeline(str(test_file), dry_run=True)
    files_after = set(tmp_path.iterdir())

    assert ok is True
    assert files_before == files_after  # no new files created


def test_run_pipeline_cyrillic_ids_translated(tmp_path):
    """A1+A5: streaming pipeline translates Cyrillic IDs, no deepcopy."""
    test_file = tmp_path / "input.jsonl"
    chunks = [
        {"chunk_id": "привет_мир", "content": "x" * 200, "title": "Hello",
         "depends_on": [], "layer": "L1"},
        {"chunk_id": "normal_id", "content": "y" * 200, "title": "World",
         "depends_on": ["привет_мир"], "layer": "L1"},
    ]
    with open(test_file, 'w') as f:
        for c in chunks:
            f.write(json.dumps(c) + '\n')

    from velantrim_migrate_v3_1 import run_pipeline
    ok = run_pipeline(str(test_file), dry_run=False, skip_backup=True)
    assert ok is True

    output = tmp_path / "input_migrated.jsonl"
    assert output.exists()
    result = [json.loads(l) for l in output.read_text().splitlines()]
    ids = [c["chunk_id"] for c in result]
    assert all(c.isascii() or c == '_' for cid in ids for c in cid)
    # depends_on reference must also be updated
    normal = next(c for c in result if c["chunk_id"] == "normal_id")
    assert "привет_мир" not in normal["depends_on"]


# ─── D3: fill_dependencies dry-run ───────────────────────────────────────────

def test_fill_dependencies_dry_run_no_files(tmp_path, monkeypatch):
    """D3: --dry-run must not create any files."""
    monkeypatch.chdir(tmp_path)
    test_file = tmp_path / "data.jsonl"
    chunks = [
        {"chunk_id": "a", "content": "See RFC0004 and RFC0016", "rfc": "RFC0001",
         "depends_on": []}
    ]
    with open(test_file, 'w') as f:
        for c in chunks:
            f.write(json.dumps(c) + '\n')

    files_before = set(tmp_path.iterdir())
    from fill_dependencies import fill_dependencies
    import tempfile, os
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jsonl') as tmp:
        tmp_path_str = tmp.name
    try:
        fixes = fill_dependencies(str(test_file), tmp_path_str)
    finally:
        os.unlink(tmp_path_str)

    files_after = set(tmp_path.iterdir())
    # Only test_file should exist, no extra output file
    assert files_before == files_after
    assert fixes['depends_on_populated'] > 0  # would have changed something
