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
