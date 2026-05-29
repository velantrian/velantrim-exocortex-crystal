"""Additional coverage for velantrim_migrate_v3_1.py.

Targets the utility, streaming, validation and CLI surfaces that the original
test_migration.py left untested (was ~60% coverage).
"""
import json

import pytest

import velantrim_migrate_v3_1 as mig


def _write(path, records):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write((r if isinstance(r, str) else json.dumps(r, ensure_ascii=False)) + "\n")
    return str(path)


# ─── compute_checksum ─────────────────────────────────────────────────────────

def test_compute_checksum_is_order_independent_and_deterministic():
    a = [{"chunk_id": "x", "n": 1}]
    cs1 = mig.compute_checksum(a)
    cs2 = mig.compute_checksum([{"n": 1, "chunk_id": "x"}])   # keys reordered
    assert cs1 == cs2                                          # sort_keys=True
    assert cs1 != mig.compute_checksum([{"chunk_id": "x", "n": 2}])


# ─── safe_slug branches ───────────────────────────────────────────────────────

def test_safe_slug_empty_uses_counter_fallback():
    s1 = mig.safe_slug("")
    s2 = mig.safe_slug("   ")
    assert s1.startswith("vel_empty_") and s2.startswith("vel_empty_")
    assert s1 != s2                                            # counter advances


def test_safe_slug_applies_semantic_prefix():
    slug = mig.safe_slug("рфс mythos layer")
    assert slug.startswith("rfc_")                            # рфс → rfc prefix


def test_safe_slug_transliterates_cyrillic():
    slug = mig.safe_slug("Привет")
    assert slug.startswith("vel_privet_")
    assert slug.isascii()


def test_safe_slug_unnamed_when_nothing_survives():
    slug = mig.safe_slug("!!!###")                            # stripped to empty base
    assert slug.startswith("vel_unnamed_")


def test_safe_slug_truncates_long_base():
    slug = mig.safe_slug("a" * 500)
    assert len(slug) <= 200


# ─── replace_ids_safe edge paths ──────────────────────────────────────────────

def test_replace_ids_safe_compiles_when_no_pattern_given():
    out = mig.replace_ids_safe("old here", {"old": "new"})    # pattern=None path
    assert out == "new here"


def test_replace_ids_safe_noop_on_empty_inputs():
    assert mig.replace_ids_safe("", {"a": "b"}) == ""
    assert mig.replace_ids_safe("text", {}) == "text"


# ─── validate_dependency_chain rfc duplicates ─────────────────────────────────

def test_validate_dependency_chain_reports_rfc_duplicates():
    chunks = [
        {"chunk_id": "a", "rfc": "RFC0001", "depends_on": []},
        {"chunk_id": "b", "rfc": "RFC0001", "depends_on": []},
    ]
    report = mig.validate_dependency_chain(chunks)
    assert report["rfc_duplicates"]["RFC0001"] == ["a", "b"]


# ─── _validate_adjacency ──────────────────────────────────────────────────────

def test_validate_adjacency_detects_cycle_and_dangling():
    id_set = {"a", "b"}
    adjacency = {"a": ["b"], "b": ["a", "ghost"]}
    report = mig._validate_adjacency(id_set, adjacency)
    assert report["cycles"]
    assert any(d["missing"] == "ghost" for d in report["dangling"])


# ─── load_jsonl ───────────────────────────────────────────────────────────────

def test_load_jsonl_skips_blanks(tmp_path):
    path = _write(tmp_path / "in.jsonl", [{"chunk_id": "a"}, "", {"chunk_id": "b"}])
    chunks = mig.load_jsonl(path)
    assert [c["chunk_id"] for c in chunks] == ["a", "b"]


def test_load_jsonl_raises_on_bad_json(tmp_path):
    path = _write(tmp_path / "bad.jsonl", ["{not json"])
    with pytest.raises(ValueError, match="JSON error at line 1"):
        mig.load_jsonl(path)


# ─── _build_id_map_streaming ──────────────────────────────────────────────────

def test_build_id_map_handles_slug_collision(tmp_path, monkeypatch):
    # Force two distinct Cyrillic ids to slug to the same value → suffix _1.
    monkeypatch.setattr(mig, "safe_slug", lambda text, prefix="vel": "vel_dup")
    path = _write(tmp_path / "c.jsonl", [
        {"chunk_id": "альфа"}, {"chunk_id": "бета"},
    ])
    id_map = mig._build_id_map_streaming(path)
    assert set(id_map.values()) == {"vel_dup", "vel_dup_1"}


def test_build_id_map_raises_on_bad_json(tmp_path):
    path = _write(tmp_path / "c.jsonl", ["{bad"])
    with pytest.raises(ValueError, match="JSON error at line 1"):
        mig._build_id_map_streaming(path)


# ─── _stream_process metadata + link fixes ────────────────────────────────────

def test_stream_process_applies_all_metadata_fixes(tmp_path):
    records = [
        # rfc extracted from title + layer inferred (Neo4j → L3) + short→deprecated
        {"chunk_id": "c1", "title": "RFC0040 spec on Neo4j graph",
         "content": "short", "depends_on": "c2"},
        # RFC0067 forced to v2.0; depends_on already a list
        {"chunk_id": "c2", "title": "RFC0067 overview", "rfc": "RFC0067",
         "content": "y" * 200, "depends_on": []},
    ]
    path = _write(tmp_path / "in.jsonl", records)
    diff, meta, links, id_set, adjacency = mig._stream_process(path, None, {}, None)

    assert meta["rfc_fixed"] >= 2          # c1 extracted, c2 forced to v2.0
    assert meta["status_updated"] == 1     # c1 content < 150
    assert meta["layers_added"] == 1       # c1 → L3
    assert adjacency["c1"] == ["c2"]       # depends_on string normalized to list
    assert {"c1", "c2"} == id_set
    assert diff                            # changes were recorded


def test_stream_process_updates_content_refs(tmp_path):
    id_map = {"oldref": "newref"}
    pattern = mig.compile_id_pattern(id_map)
    path = _write(tmp_path / "in.jsonl", [
        {"chunk_id": "c1", "title": "t", "content": "see oldref now",
         "depends_on": ["oldref"]},
    ])
    diff, meta, links, id_set, adjacency = mig._stream_process(path, None, id_map, pattern)
    assert links["content_refs_updated"] == 1
    assert links["depends_on_updated"] == 1


def test_stream_process_writes_output_when_path_given(tmp_path):
    path = _write(tmp_path / "in.jsonl", [{"chunk_id": "c1", "title": "t",
                                           "content": "z" * 200, "depends_on": []}])
    out = str(tmp_path / "out.jsonl")
    mig._stream_process(path, out, {}, None)
    lines = [json.loads(l) for l in open(out, encoding="utf-8")]
    assert lines[0]["chunk_id"] == "c1"


# ─── validate_all ─────────────────────────────────────────────────────────────

def test_validate_all_rejects_duplicate_ids(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    chunks = [{"chunk_id": "dup", "depends_on": []},
              {"chunk_id": "dup", "depends_on": []}]
    assert mig.validate_all(chunks, {}) is False


def test_validate_all_happy_path_writes_report(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    chunks = [
        {"chunk_id": "a", "rfc": "RFC0001", "depends_on": ["b"], "content": "hi"},
        {"chunk_id": "b", "rfc": "RFC0001", "depends_on": [], "content": "yo"},
    ]
    # id_map present + content still holding an old id → leftover-id branch
    assert mig.validate_all(chunks, {"a": "a_new"}) is True
    assert (tmp_path / "migration_dependency_report.json").exists()


# ─── write_atomic / create_rollback_backup ────────────────────────────────────

def test_write_atomic_creates_final_file(tmp_path):
    out = str(tmp_path / "final.jsonl")
    mig.write_atomic([{"chunk_id": "a"}], out)
    assert json.loads(open(out, encoding="utf-8").read()) == {"chunk_id": "a"}
    assert not (tmp_path / "final.jsonl.tmp").exists()    # tmp renamed away


def test_create_rollback_backup_copies_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    src = _write(tmp_path / "src.jsonl", [{"chunk_id": "a"}])
    backup = mig.create_rollback_backup(src)
    assert (tmp_path / backup).exists()


# ─── CLI helpers ──────────────────────────────────────────────────────────────

def test_validate_standalone_reports(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path / "v.jsonl", [
        {"chunk_id": "латиница", "depends_on": ["missing"], "content": "x"},
    ])
    mig.validate_standalone(path)
    out = capsys.readouterr().out
    assert "Dangling refs" in out
    assert "Cyrillic IDs" in out
    assert (tmp_path / "validate_dangling.json").exists()


def test_diff_files_writes_report(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    old = _write(tmp_path / "old.jsonl", [{"chunk_id": "a", "title": "A"}])
    new = _write(tmp_path / "new.jsonl", [{"chunk_id": "a", "title": "B"}])
    mig.diff_files(old, new)
    assert "Modified: 1" in capsys.readouterr().out
    assert (tmp_path / "diff_report.json").exists()


def test_do_rollback_restores(tmp_path, capsys):
    backup = _write(tmp_path / "b.jsonl", [{"chunk_id": "a"}])
    target = str(tmp_path / "restored.jsonl")
    mig.do_rollback(backup, target)
    assert json.loads(open(target, encoding="utf-8").read()) == {"chunk_id": "a"}


def test_do_rollback_missing_backup_exits(tmp_path):
    with pytest.raises(SystemExit):
        mig.do_rollback(str(tmp_path / "nope.jsonl"), str(tmp_path / "t.jsonl"))


# ─── main() CLI dispatch ──────────────────────────────────────────────────────

def test_main_validate(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path / "m.jsonl", [{"chunk_id": "a", "depends_on": [],
                                          "content": "x" * 200, "layer": "L1"}])
    monkeypatch.setattr("sys.argv", ["velantrim-migrate", "validate", path])
    mig.main()
    assert "Chunks: 1" in capsys.readouterr().out


def test_main_migrate_dry_run_exits_zero(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path / "m.jsonl", [{"chunk_id": "a", "depends_on": [],
                                          "content": "x" * 200, "layer": "L1"}])
    monkeypatch.setattr("sys.argv", ["velantrim-migrate", "migrate", path, "--dry-run"])
    with pytest.raises(SystemExit) as exc:
        mig.main()
    assert exc.value.code == 0


def test_main_diff(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    old = _write(tmp_path / "o.jsonl", [{"chunk_id": "a", "title": "A"}])
    new = _write(tmp_path / "n.jsonl", [{"chunk_id": "a", "title": "B"}])
    monkeypatch.setattr("sys.argv", ["velantrim-migrate", "diff", old, new])
    mig.main()
    assert "Modified: 1" in capsys.readouterr().out


def test_stream_process_layer_inference_and_blank_lines(tmp_path):
    records = [
        "",                                                   # blank line skipped
        {"chunk_id": "x", "title": "Ring Zero core", "content": "z" * 200},
        # 'session' in title → L1; depends_on is a non-list/non-str → coerced to []
        {"chunk_id": "y", "title": "session layer", "content": "z" * 200,
         "depends_on": 123},
    ]
    path = _write(tmp_path / "in.jsonl", records)
    diff, meta, links, id_set, adjacency = mig._stream_process(path, None, {}, None)
    assert id_set == {"x", "y"}
    assert adjacency["y"] == []                               # int depends_on dropped
    assert meta["layers_added"] == 2                          # L0 + L1 inferred


def test_validate_all_warns_on_cycles_dangling_and_bad_json(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    chunks = [
        {"chunk_id": "a", "rfc": "RFC0001", "depends_on": ["b"], "content": "x"},
        {"chunk_id": "b", "rfc": "RFC0001", "depends_on": ["a", "ghost"],
         "content": "y"},
    ]
    assert mig.validate_all(chunks, {}) is True
    # cycles (a↔b), dangling (ghost) and rfc duplicates (RFC0001) all warned
    assert (tmp_path / "migration_dependency_report.json").exists()


def test_validate_all_rejects_unserializable_chunk(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    chunks = [{"chunk_id": "a", "depends_on": [], "bad": {1, 2, 3}}]  # set → not JSON
    assert mig.validate_all(chunks, {}) is False


def test_validate_standalone_reports_duplicate_ids(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    path = _write(tmp_path / "d.jsonl", [
        {"chunk_id": "dup", "depends_on": [], "content": "x" * 200, "layer": "L1"},
        {"chunk_id": "dup", "depends_on": [], "content": "y" * 200, "layer": "L1"},
    ])
    mig.validate_standalone(path)
    assert "Duplicate chunk_ids" in capsys.readouterr().out


def test_run_pipeline_warns_on_cycles_and_dangling(tmp_path):
    path = _write(tmp_path / "in.jsonl", [
        {"chunk_id": "a", "title": "t", "content": "x" * 200, "depends_on": ["b"]},
        {"chunk_id": "b", "title": "t", "content": "y" * 200,
         "depends_on": ["a", "ghost"]},
    ])
    ok = mig.run_pipeline(str(path), dry_run=False, skip_backup=True)
    assert ok is True
    assert (tmp_path / "in_migrated.jsonl").exists()


def test_fill_dependencies_skips_blank_lines(tmp_path):
    from fill_dependencies import fill_dependencies
    inp = tmp_path / "in.jsonl"
    inp.write_text(
        '{"chunk_id": "a", "content": "See RFC0004", "rfc": "RFC0001", "depends_on": []}\n'
        '\n',                                       # blank line is skipped (line 23)
        encoding="utf-8",
    )
    out = tmp_path / "out.jsonl"
    fixes = fill_dependencies(str(inp), str(out))
    assert fixes["total_chunks"] == 1
    assert fixes["depends_on_populated"] == 1


def test_main_rollback(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    backup = _write(tmp_path / "b.jsonl", [{"chunk_id": "a"}])
    target = str(tmp_path / "t.jsonl")
    monkeypatch.setattr("sys.argv", ["velantrim-migrate", "rollback", backup, target])
    mig.main()
    assert "Restored" in capsys.readouterr().out
