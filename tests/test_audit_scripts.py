"""Tests for the JSONL audit / duplicate-check scripts.

These were previously zero-coverage standalone scripts. We exercise their
library functions against synthetic JSONL fixtures rather than the real
~900KB corpus.
"""
import json

import pytest

import audit_metadata
import check_rfc_duplicates


def _write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            if isinstance(r, str):           # raw line (e.g. malformed JSON)
                f.write(r + "\n")
            else:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return path


def test_audit_jsonl_detects_every_issue_category(tmp_path):
    records = [
        # 0: RFC field vs title mismatch
        {"idx": 0, "chunk_id": "c0", "rfc": "RFC0010",
         "title": "RFC0099: mismatch", "content": "x" * 200, "layer": "L1",
         "depends_on": ["a"]},
        # 1 & 2: duplicate RFC number
        {"idx": 1, "chunk_id": "c1", "rfc": "RFC0067 v2.0", "title": "ok",
         "content": "y" * 200, "layer": "L1", "depends_on": ["a"]},
        {"idx": 2, "chunk_id": "c2", "rfc": "RFC0067 v2.0", "title": "ok2",
         "content": "y" * 200, "layer": "L1", "depends_on": ["a"]},
        # 3: cyrillic chunk_id + null layer + empty depends_on + empty stub
        {"idx": 3, "chunk_id": "чанк", "rfc": "", "title": "",
         "content": "short", "layer": None, "depends_on": []},
        # 4: mega blob
        {"idx": 4, "chunk_id": "c4", "rfc": "RFC0040", "title": "big",
         "content": "z" * 50001, "layer": "L2", "depends_on": ["a"]},
        # 5 & 6: duplicate chunk_id
        {"idx": 5, "chunk_id": "dup", "rfc": "RFC0041", "title": "d1",
         "content": "w" * 200, "layer": "L1", "depends_on": ["a"]},
        {"idx": 6, "chunk_id": "dup", "rfc": "RFC0042", "title": "d2",
         "content": "w" * 200, "layer": "L1", "depends_on": ["a"]},
        # 7: RFC0067 version inconsistency (field v1, title v2)
        {"idx": 7, "chunk_id": "c7", "rfc": "RFC0067 v1.0",
         "title": "RFC0067 v2.0 spec", "content": "q" * 200, "layer": "L1",
         "depends_on": ["a"]},
        # malformed line — exercises the JSONDecodeError branch
        "{not valid json",
    ]
    path = _write_jsonl(tmp_path / "synthetic.jsonl", records)

    chunks, issues = audit_metadata.audit_jsonl(path)

    assert len(chunks) == 8                      # malformed line skipped
    assert any(m["title_rfc"] == "RFC0099" for m in issues["rfc_mismatches"])
    assert "RFC0067 v2.0" in issues["duplicate_rfcs"]
    assert issues["cyrillic_chunk_ids"][0]["chunk_id"] == "чанк"
    assert 3 in issues["null_layers"]
    assert 3 in issues["empty_depends_on"]
    assert any(b["idx"] == 4 for b in issues["mega_blobs"])
    assert any(s["idx"] == 3 for s in issues["empty_stubs"])
    assert "dup" in issues["duplicate_chunk_ids"]
    assert any(v["issue"] == "rfc_field_v1_title_v2"
               for v in issues["rfc0067_versions"])


def test_audit_print_report_runs(tmp_path, capsys):
    path = _write_jsonl(tmp_path / "s.jsonl", [
        {"idx": 0, "chunk_id": "c0", "rfc": "RFC0001", "title": "t",
         "content": "x" * 200, "layer": "L1", "depends_on": ["a"]},
    ])
    chunks, issues = audit_metadata.audit_jsonl(path)
    audit_metadata.print_report(chunks, issues)
    out = capsys.readouterr().out
    assert "METADATA AUDIT REPORT" in out
    assert "Total chunks: 1" in out


def test_audit_jsonl_covers_remaining_rfc0067_and_blank_lines(tmp_path):
    records = [
        "",                                       # blank line is skipped
        # RFC0067: field v2.0 but title v1.0
        {"idx": 0, "chunk_id": "a", "rfc": "RFC0067 v2.0",
         "title": "RFC0067 v1.0 legacy", "content": "x" * 200, "layer": "L1"},
        # RFC0067: mixed versions present only in tags
        {"idx": 1, "chunk_id": "b", "rfc": "RFC0067",
         "title": "RFC0067 overview", "content": "y" * 200, "layer": "L1",
         "tags": ["v1.0", "v2.0"]},
    ]
    path = _write_jsonl(tmp_path / "v.jsonl", records)
    chunks, issues = audit_metadata.audit_jsonl(path)
    assert len(chunks) == 2                        # blank line skipped
    problems = {v["issue"] for v in issues["rfc0067_versions"]}
    assert "rfc_field_v2_title_v1" in problems
    assert "mixed_versions_in_tags" in problems


def test_print_report_emits_every_section(capsys):
    # Hand-build a fully populated issues dict so every conditional block in
    # print_report runs (including the ">10 cyrillic" truncation branch).
    issues = {
        "rfc_mismatches": [{"idx": 0, "chunk_id": "c0", "rfc_field": "RFC0001",
                            "title_rfc": "RFC0002", "title": "mismatch"}],
        "duplicate_rfcs": {"RFC0001": [0, 1]},
        "cyrillic_chunk_ids": [{"idx": i, "chunk_id": f"чанк{i}"} for i in range(12)],
        "null_layers": [3],
        "empty_depends_on": [4],
        "mega_blobs": [{"idx": 5, "chunk_id": "c5", "char_count": 60000,
                        "title": "big"}],
        "empty_stubs": [{"idx": 6, "chunk_id": "c6", "char_count": 10,
                         "title": "tiny"}],
        "duplicate_chunk_ids": {"dup": [7, 8]},
        "rfc0067_versions": [{"idx": 9, "chunk_id": "c9", "rfc": "RFC0067 v2.0",
                              "title": "t", "issue": "rfc_field_v2_title_v1"}],
    }
    audit_metadata.print_report([{}, {}], issues)
    out = capsys.readouterr().out
    assert "RFC MISMATCHES" in out
    assert "DUPLICATE RFC NUMBERS" in out
    assert "RFC0067 VERSION INCONSISTENCIES" in out
    assert "CYRILLIC CHUNK_IDS" in out
    assert "... and 2 more" in out               # >10 truncation branch
    assert "MEGA-BLOBS" in out
    assert "EMPTY STUBS" in out
    assert "DUPLICATE CHUNK_IDS" in out


def test_check_duplicates_smoke(tmp_path, capsys):
    # check_duplicates indexes up to 62, so provide 63 minimal chunks.
    records = [
        {"chunk_id": f"chunk-{i}", "title": f"Title {i}", "char_count": 100,
         "status": "ok", "tags": ["t1", "t2"], "content": f"content {i}"}
        for i in range(63)
    ]
    path = _write_jsonl(tmp_path / "dups.jsonl", records)
    check_rfc_duplicates.check_duplicates(path)
    out = capsys.readouterr().out
    assert "RFC0067 v2.0" in out
    assert "chunks at indices" in out


# ── Hardening tests (C1) ────────────────────────────────────────────────────

def test_check_duplicates_short_jsonl_does_not_crash(tmp_path, capsys):
    """Short JSONL: out-of-range indices are warned, not raised."""
    records = [
        {"chunk_id": f"c{i}", "title": f"T{i}", "content": f"x{i}"}
        for i in range(5)  # max index in duplicates dict is 62; all OOB
    ]
    path = _write_jsonl(tmp_path / "short.jsonl", records)
    # Must not raise IndexError or KeyError
    check_rfc_duplicates.check_duplicates(path)
    err = capsys.readouterr().err
    assert "out of range" in err


def test_check_duplicates_missing_chunk_id_does_not_crash(tmp_path, capsys):
    """Chunks with no chunk_id field must not raise KeyError."""
    records = [
        {"title": f"T{i}", "content": f"x{i}"}  # no chunk_id
        for i in range(63)
    ]
    path = _write_jsonl(tmp_path / "no_id.jsonl", records)
    check_rfc_duplicates.check_duplicates(path)
    out = capsys.readouterr().out
    assert "<missing>" in out


def test_check_duplicates_missing_title_does_not_crash(tmp_path, capsys):
    """Chunks with no title field must not raise KeyError."""
    records = [
        {"chunk_id": f"c{i}", "content": f"x{i}"}  # no title
        for i in range(63)
    ]
    path = _write_jsonl(tmp_path / "no_title.jsonl", records)
    check_rfc_duplicates.check_duplicates(path)
    out = capsys.readouterr().out
    assert "<missing>" in out


def test_check_duplicates_malformed_json_reports_line_number(tmp_path, capsys):
    """A malformed JSON line should be reported with its line number."""
    records = [
        {"chunk_id": f"c{i}", "title": f"T{i}", "content": f"x{i}"}
        for i in range(5)
    ]
    records.insert(2, "{bad json")  # raw string → malformed line
    path = _write_jsonl(tmp_path / "mal.jsonl", records)
    # load_chunks prints to stderr on bad lines but should not raise
    check_rfc_duplicates.load_chunks(path)
    err = capsys.readouterr().err
    assert "Line 3" in err or "line" in err.lower()


def test_check_duplicates_missing_input_raises(tmp_path):
    """Missing input file must raise FileNotFoundError, not a raw open() error."""
    with pytest.raises(FileNotFoundError):
        check_rfc_duplicates.load_chunks(tmp_path / "nonexistent.jsonl")


def test_load_chunks_skips_blank_lines(tmp_path):
    """Blank lines in JSONL must be skipped silently."""
    p = tmp_path / "blanks.jsonl"
    p.write_text(
        '\n{"chunk_id": "a", "title": "T"}\n\n{"chunk_id": "b", "title": "T2"}\n',
        encoding="utf-8",
    )
    chunks = check_rfc_duplicates.load_chunks(p)
    assert len(chunks) == 2
