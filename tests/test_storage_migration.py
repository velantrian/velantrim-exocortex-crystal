from __future__ import annotations

import hashlib
import json
import os
import sqlite3
from pathlib import Path

import pytest

from core import storage_migration as m
from core.storage_common import StorageOperationError


def profile_payload(db: Path, *, backend: str = "sqlite") -> dict:
    configuration = {"path": str(db.resolve())}
    canonical = json.dumps(
        {"backend": backend, "configuration": configuration},
        sort_keys=True,
        separators=(",", ":"),
    )
    return {
        "schema_version": 1,
        "profile": "l3",
        "backend": backend,
        "durable": True,
        "configuration": configuration,
        "locator_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
    }


def make_store(tmp_path: Path, *, vectors: tuple[str, ...] = ("[0.1,0.2]",)):
    tmp_path.mkdir(parents=True, exist_ok=True)
    db = tmp_path / "l3.db"
    profile = tmp_path / "profile.json"
    connection = sqlite3.connect(db)
    connection.executescript(
        """
        CREATE TABLE nodes(fact_id TEXT PRIMARY KEY,data TEXT NOT NULL);
        CREATE TABLE vectors(fact_id TEXT PRIMARY KEY,vec TEXT NOT NULL);
        CREATE TABLE edges(src TEXT NOT NULL,rel_type TEXT NOT NULL,dst TEXT NOT NULL,props TEXT NOT NULL DEFAULT '{}',UNIQUE(src,rel_type,dst,props));
        CREATE TABLE entities(entity_id TEXT PRIMARY KEY,kind TEXT,label TEXT);
        CREATE TABLE mentions(fact_id TEXT NOT NULL,entity_id TEXT NOT NULL,rel TEXT NOT NULL,UNIQUE(fact_id,entity_id,rel));
        CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT);
        """
    )
    for fact_id in ("b", "a"):
        connection.execute(
            "INSERT INTO nodes VALUES (?,?)",
            (fact_id, json.dumps({"claim": fact_id.upper(), "fact_id": fact_id})),
        )
    for index, vector in enumerate(vectors):
        connection.execute("INSERT INTO vectors VALUES (?,?)", (("a", "b")[index], vector))
    connection.execute("INSERT INTO edges VALUES (?,?,?,?)", ("a", "LINK", "b", '{"z":1,"a":2}'))
    connection.execute("INSERT INTO entities VALUES (?,?,?)", ("e", "person", "E"))
    connection.execute("INSERT INTO mentions VALUES (?,?,?)", ("a", "e", "MENTIONS"))
    connection.execute("INSERT INTO meta VALUES (?,?)", ("embedder_fp", "hashing"))
    connection.execute("PRAGMA user_version=7")
    connection.commit()
    connection.close()
    profile.write_text(json.dumps(profile_payload(db), indent=2, sort_keys=True) + "\n")
    return profile, db


def export_bundle(tmp_path: Path) -> tuple[Path, Path, Path]:
    profile, db = make_store(tmp_path)
    bundle = tmp_path / "bundle"
    m.export_sqlite_logical(bundle, profile_path=profile)
    return bundle, profile, db


def load(path: Path):
    return json.loads(path.read_text())


def dump(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def refresh_complete(bundle: Path) -> None:
    complete = load(bundle / m.MIGRATION_COMPLETE)
    complete["manifest_sha256"] = m._sha256_file(bundle / m.MIGRATION_MANIFEST)
    dump(bundle / m.MIGRATION_COMPLETE, complete)


def update_manifest(bundle: Path, mutator) -> None:
    manifest = load(bundle / m.MIGRATION_MANIFEST)
    mutator(manifest)
    dump(bundle / m.MIGRATION_MANIFEST, manifest)
    refresh_complete(bundle)


def update_dataset(bundle: Path, dataset: str, content: bytes, *, records: int | None = None) -> None:
    path = bundle / m.DATASET_FILES[dataset]
    path.write_bytes(content)
    manifest = load(bundle / m.MIGRATION_MANIFEST)
    metadata = manifest["datasets"][dataset]
    metadata["bytes"] = len(content)
    metadata["sha256"] = m._sha256_file(path)
    if records is not None:
        metadata["records"] = records
    dump(bundle / m.MIGRATION_MANIFEST, manifest)
    refresh_complete(bundle)


def assert_error(message: str, fn, *args, **kwargs):
    with pytest.raises(StorageOperationError, match=message):
        fn(*args, **kwargs)


def test_round_trip_is_deterministic_and_read_only(tmp_path):
    profile, db = make_store(tmp_path)
    before = (profile.read_bytes(), db.read_bytes())
    first, second = tmp_path / "first", tmp_path / "second"
    result = m.export_sqlite_logical(first, profile_path=profile)
    m.export_sqlite_logical(second, profile_path=profile)
    assert result["status"] == "PASS"
    verified = m.verify_logical_export(first)
    assert verified["datasets"] == {
        "nodes": 2, "vectors": 1, "edges": 1,
        "entities": 1, "mentions": 1, "meta": 1,
    }
    assert verified["vector_dimension"] == 2
    assert (profile.read_bytes(), db.read_bytes()) == before
    for filename in m.DATASET_FILES.values():
        assert (first / filename).read_bytes() == (second / filename).read_bytes()
    assert load(first / m.MIGRATION_MANIFEST) == load(second / m.MIGRATION_MANIFEST)
    assert [json.loads(line)["fact_id"] for line in (first / "nodes.jsonl").read_text().splitlines()] == ["a", "b"]
    assert json.loads((first / "edges.jsonl").read_text())["props"] == {"a": 2, "z": 1}


def test_empty_vectors_and_default_profile(tmp_path, monkeypatch):
    profile, _ = make_store(tmp_path, vectors=())
    monkeypatch.setenv(m.PROFILE_PATH_ENV, str(profile))
    result = m.export_sqlite_logical(tmp_path / "bundle")
    assert result["vector_dimension"] is None


def test_export_rejects_existing_symlinks_bad_source_and_dimension(tmp_path, monkeypatch):
    profile, db = make_store(tmp_path)
    output = tmp_path / "exists"
    output.mkdir()
    assert_error("already exists", m.export_sqlite_logical, output, profile_path=profile)
    broken = tmp_path / "broken"
    broken.symlink_to(tmp_path / "missing", target_is_directory=True)
    assert_error("symbolic link", m.export_sqlite_logical, broken, profile_path=profile)

    profile_link = tmp_path / "profile-link"
    profile_link.symlink_to(profile)
    assert_error("symbolic link", m.export_sqlite_logical, tmp_path / "p", profile_path=profile_link)
    monkeypatch.setenv(m.PROFILE_PATH_ENV, str(profile_link))
    assert_error("symbolic link", m.export_sqlite_logical, tmp_path / "p2")

    db_link = tmp_path / "db-link"
    db_link.symlink_to(db)
    linked = tmp_path / "linked.json"
    cfg = {"path": str(db_link)}
    canonical = json.dumps({"backend": "sqlite", "configuration": cfg}, sort_keys=True, separators=(",", ":"))
    linked_payload = profile_payload(db)
    linked_payload["configuration"] = cfg
    linked_payload["locator_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    linked.write_text(json.dumps(linked_payload, indent=2, sort_keys=True) + "\n")
    assert_error("symbolic link", m.export_sqlite_logical, tmp_path / "p3", profile_path=linked)

    missing = tmp_path / "missing-profile"
    assert_error("regular file", m.export_sqlite_logical, tmp_path / "p4", profile_path=missing)

    inconsistent, _ = make_store(tmp_path / "other", vectors=("[1,2]", "[1,2,3]"))
    assert_error("inconsistent dimensions", m.export_sqlite_logical, tmp_path / "p5", profile_path=inconsistent)


def test_export_cleanup_and_profile_mutation(tmp_path, monkeypatch):
    profile, _ = make_store(tmp_path)
    real_hash = m._sha256_file
    calls = {"profile": 0}

    def changed(path):
        value = real_hash(path)
        if Path(path) == profile:
            calls["profile"] += 1
            if calls["profile"] > 1:
                return "0" * 64
        return value

    monkeypatch.setattr(m, "_sha256_file", changed)
    output = tmp_path / "bundle"
    assert_error("profile changed", m.export_sqlite_logical, output, profile_path=profile)
    assert not output.exists()

    monkeypatch.setattr(Path, "mkdir", lambda *args, **kwargs: (_ for _ in ()).throw(OSError("no")))
    assert_error("cannot create migration bundle", m.export_sqlite_logical, tmp_path / "bad", profile_path=profile)


def test_strict_json_and_record_builders():
    assert m._strict_json('{"a":1}', "x") == {"a": 1}
    assert_error("JSON text", m._strict_json, 1, "x")
    for raw in ('{"a":1,"a":2}', '{"x":NaN}', '{'):
        assert_error("strict JSON", m._strict_json, raw, "x")
    assert_error("JSON object", m._json_object, "[]", "x")
    assert m._vector("[1,2.5]", "v") == [1, 2.5]
    for value, message in (([], "non-empty"), ([True], "non-numeric"), ([float("inf")], "non-finite")):
        assert_error(message, m._vector_value, value, "v")

    assert_error("nodes.fact_id", m._node_record, {"fact_id": "", "data": "{}"})
    assert_error("payload fact_id", m._node_record, {"fact_id": "a", "data": '{"fact_id":"b"}'})
    assert_error("vectors.fact_id", m._vector_record, {"fact_id": "", "vec": "[1]"})
    assert_error("edge identifiers", m._edge_record, {"src": "", "rel_type": "r", "dst": "d", "props": "{}"})
    assert_error("entities.entity_id", m._entity_record, {"entity_id": "", "kind": None, "label": None})
    assert_error("kind/label", m._entity_record, {"entity_id": "e", "kind": 1, "label": None})
    assert_error("mention identifiers", m._mention_record, {"fact_id": "", "entity_id": "e", "rel": "r"})
    assert_error("meta.key", m._meta_record, {"key": "", "value": None})
    assert_error("meta.value", m._meta_record, {"key": "k", "value": 1})


def test_schema_query_and_write_errors(tmp_path, monkeypatch):
    class Bad:
        def execute(self, query):
            raise sqlite3.OperationalError("bad")

    assert_error("inspect SQLite table", m._table_columns, Bad(), "nodes")
    assert_error("export SQLite dataset", m._export_records, Bad(), "nodes")

    profile, db = make_store(tmp_path)
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    connection.execute("ALTER TABLE nodes ADD COLUMN extra TEXT")
    assert_error("unsupported columns", m._require_schema, connection)
    connection.close()

    path = tmp_path / "dataset"
    monkeypatch.setattr(Path, "open", lambda *args, **kwargs: (_ for _ in ()).throw(OSError("bad")))
    assert_error("cannot write migration dataset", m._write_dataset, path, [])


def test_verify_rejects_root_and_required_files(tmp_path):
    file_path = tmp_path / "file"
    file_path.write_text("x")
    assert_error("must be a directory", m.verify_logical_export, file_path)
    link = tmp_path / "link"
    link.symlink_to(file_path)
    assert_error("symbolic link", m.verify_logical_export, link)

    bundle, _, _ = export_bundle(tmp_path / "one")
    (bundle / m.MIGRATION_MANIFEST).unlink()
    assert_error("manifest must be", m.verify_logical_export, bundle)
    bundle, _, _ = export_bundle(tmp_path / "two")
    (bundle / m.MIGRATION_COMPLETE).unlink()
    assert_error("completion marker must be", m.verify_logical_export, bundle)


def test_verify_completion_and_manifest_guards(tmp_path):
    cases = [
        (lambda b: dump(b / m.MIGRATION_COMPLETE, {"schema_version": 1}), "keys mismatch"),
        (lambda b: _mutate_complete(b, "schema_version", 2), "completion schema_version"),
        (lambda b: _mutate_complete(b, "bundle_type", "bad"), "completion bundle_type"),
        (lambda b: _mutate_complete(b, "completed_at", "bad"), "timestamp"),
        (lambda b: _mutate_complete(b, "manifest_sha256", "x"), "64-character"),
        (lambda b: _mutate_complete(b, "manifest_sha256", "z" * 64), "hexadecimal"),
        (lambda b: (b / m.MIGRATION_MANIFEST).write_text("{}"), "manifest SHA-256"),
    ]
    for index, (mutate, message) in enumerate(cases):
        bundle, _, _ = export_bundle(tmp_path / f"c{index}")
        mutate(bundle)
        assert_error(message, m.verify_logical_export, bundle)

    manifest_cases = [
        (lambda x: x.pop("source"), "manifest keys mismatch"),
        (lambda x: x.__setitem__("schema_version", 2), "manifest schema_version"),
        (lambda x: x.__setitem__("bundle_type", "bad"), "manifest bundle_type"),
        (lambda x: x.__setitem__("source", []), "source must be"),
        (lambda x: x["source"].pop("backend"), "source keys mismatch"),
        (lambda x: x["source"].__setitem__("backend", "ladybug"), "source backend"),
        (lambda x: x["source"].__setitem__("profile_sha256", "x"), "64-character"),
        (lambda x: x["source"].__setitem__("sqlite_user_version", True), "versions must be"),
        (lambda x: x.__setitem__("authority", {}), "authority boundary"),
        (lambda x: x.__setitem__("datasets", []), "dataset set"),
        (lambda x: x["datasets"].__setitem__("nodes", []), "metadata must be"),
        (lambda x: x["datasets"]["nodes"].pop("bytes"), "metadata keys mismatch"),
        (lambda x: x["datasets"]["nodes"].__setitem__("file", "bad"), "declared filename"),
        (lambda x: x["datasets"]["nodes"].__setitem__("records", -1), "non-negative"),
    ]
    for index, (mutate, message) in enumerate(manifest_cases):
        bundle, _, _ = export_bundle(tmp_path / f"m{index}")
        update_manifest(bundle, mutate)
        assert_error(message, m.verify_logical_export, bundle)


def _mutate_complete(bundle: Path, key: str, value) -> None:
    complete = load(bundle / m.MIGRATION_COMPLETE)
    complete[key] = value
    dump(bundle / m.MIGRATION_COMPLETE, complete)


def test_verify_bundle_file_and_dataset_guards(tmp_path):
    bundle, _, _ = export_bundle(tmp_path / "extra")
    (bundle / m.DATASET_FILES["meta"]).rename(bundle / "extra")
    assert_error("file set mismatch", m.verify_logical_export, bundle)

    bundle, _, _ = export_bundle(tmp_path / "size")
    with (bundle / "nodes.jsonl").open("ab") as handle:
        handle.write(b"{}\n")
    assert_error("byte-size mismatch", m.verify_logical_export, bundle)

    bundle, _, _ = export_bundle(tmp_path / "sha")
    path = bundle / "nodes.jsonl"
    content = path.read_bytes().replace(b'"a"', b'"x"', 1)
    path.write_bytes(content)
    manifest = load(bundle / m.MIGRATION_MANIFEST)
    manifest["datasets"]["nodes"]["bytes"] = len(content)
    dump(bundle / m.MIGRATION_MANIFEST, manifest)
    refresh_complete(bundle)
    assert_error("SHA-256 mismatch", m.verify_logical_export, bundle)

    bundle, _, _ = export_bundle(tmp_path / "newline")
    content = (bundle / "nodes.jsonl").read_bytes().rstrip(b"\n")
    update_dataset(bundle, "nodes", content)
    assert_error("end with a newline", m.verify_logical_export, bundle)

    bundle, _, _ = export_bundle(tmp_path / "json")
    update_dataset(bundle, "nodes", b'{"x":NaN}\n', records=1)
    assert_error("strict JSON", m.verify_logical_export, bundle)

    bundle, _, _ = export_bundle(tmp_path / "canonical")
    update_dataset(bundle, "nodes", b'{"payload":{"fact_id":"a"}, "fact_id":"a"}\n', records=1)
    assert_error("not canonical", m.verify_logical_export, bundle)

    bundle, _, _ = export_bundle(tmp_path / "order")
    lines = (bundle / "nodes.jsonl").read_bytes().splitlines(keepends=True)
    update_dataset(bundle, "nodes", b"".join(reversed(lines)), records=2)
    assert_error("strictly ordered", m.verify_logical_export, bundle)

    bundle, _, _ = export_bundle(tmp_path / "count")
    manifest = load(bundle / m.MIGRATION_MANIFEST)
    manifest["datasets"]["nodes"]["records"] = 3
    dump(bundle / m.MIGRATION_MANIFEST, manifest)
    refresh_complete(bundle)
    assert_error("record-count", m.verify_logical_export, bundle)

    bundle, _, _ = export_bundle(tmp_path / "symlink")
    path = bundle / "nodes.jsonl"
    target = tmp_path / "node-target"
    path.rename(target)
    path.symlink_to(target)
    assert_error("regular file", m.verify_logical_export, bundle)


def test_validate_record_guards():
    cases = [
        ("nodes", [], "JSON object"),
        ("nodes", {"fact_id": "a"}, "keys mismatch"),
        ("nodes", {"fact_id": "", "payload": {}}, "invalid fact_id"),
        ("nodes", {"fact_id": "a", "payload": {"fact_id": "b"}}, "payload fact_id"),
        ("vectors", {"fact_id": "a"}, "keys mismatch"),
        ("vectors", {"fact_id": "", "vector": [1]}, "fact_id is invalid"),
        ("vectors", {"fact_id": "a", "vector": []}, "non-empty"),
        ("edges", {"src": "a"}, "keys mismatch"),
        ("edges", {"src": "", "rel_type": "r", "dst": "b", "props": {}}, "identifiers"),
        ("edges", {"src": "a", "rel_type": "r", "dst": "b", "props": []}, "props"),
        ("entities", {"entity_id": "e"}, "keys mismatch"),
        ("entities", {"entity_id": "", "kind": None, "label": None}, "entity_id"),
        ("entities", {"entity_id": "e", "kind": 1, "label": None}, "kind/label"),
        ("mentions", {"fact_id": "a"}, "keys mismatch"),
        ("mentions", {"fact_id": "", "entity_id": "e", "rel": "r"}, "identifiers"),
        ("meta", {"key": "k"}, "keys mismatch"),
        ("meta", {"key": "", "value": None}, "key is invalid"),
        ("meta", {"key": "k", "value": 1}, "value must"),
    ]
    for dataset, record, message in cases:
        assert_error(message, m._validate_record, dataset, record)


def test_referential_and_dimension_guards(tmp_path):
    bundle, _, _ = export_bundle(tmp_path / "dangling")
    update_dataset(bundle, "vectors", m._canonical_record_bytes({"fact_id": "missing", "vector": [1, 2]}), records=1)
    assert_error("dangling references", m.verify_logical_export, bundle)

    bundle, _, _ = export_bundle(tmp_path / "edge")
    update_dataset(bundle, "edges", m._canonical_record_bytes({"src": "a", "rel_type": "r", "dst": "missing", "props": {}}), records=1)
    assert_error("dangling references", m.verify_logical_export, bundle)

    bundle, _, _ = export_bundle(tmp_path / "mention")
    update_dataset(bundle, "mentions", m._canonical_record_bytes({"fact_id": "a", "entity_id": "missing", "rel": "r"}), records=1)
    assert_error("dangling references", m.verify_logical_export, bundle)

    bundle, _, _ = export_bundle(tmp_path / "dims")
    content = b"".join([
        m._canonical_record_bytes({"fact_id": "a", "vector": [1, 2]}),
        m._canonical_record_bytes({"fact_id": "b", "vector": [1, 2, 3]}),
    ])
    update_dataset(bundle, "vectors", content, records=2)
    update_manifest(bundle, lambda x: x.__setitem__("vector_dimension", 2))
    assert_error("inconsistent dimensions", m.verify_logical_export, bundle)

    bundle, _, _ = export_bundle(tmp_path / "dimension-value")
    update_manifest(bundle, lambda x: x.__setitem__("vector_dimension", 3))
    assert_error("dimension mismatch", m.verify_logical_export, bundle)

    profile, _ = make_store(tmp_path / "bool-dimension", vectors=("[1]",))
    bundle = tmp_path / "bool-dimension" / "bundle"
    m.export_sqlite_logical(bundle, profile_path=profile)
    update_manifest(bundle, lambda x: x.__setitem__("vector_dimension", True))
    assert_error("positive integer", m.verify_logical_export, bundle)


def test_timestamp_and_sha_helpers():
    assert m._valid_completed_at("2026-08-07T12:00:00Z")
    assert not m._valid_completed_at(None)
    assert not m._valid_completed_at("badZ")
    assert m._require_sha256("a" * 64, "x") == "a" * 64
    assert_error("64-character", m._require_sha256, None, "x")
    assert_error("hexadecimal", m._require_sha256, "z" * 64, "x")


def test_remaining_source_and_transaction_guards(tmp_path, monkeypatch):
    profile, db = make_store(tmp_path / "missing-db")
    db.unlink()
    assert_error("SQLite storage file must be a regular file", m.export_sqlite_logical, tmp_path / "missing-db" / "bundle", profile_path=profile)

    class IntegrityBad:
        def execute(self, query):
            if query == "PRAGMA integrity_check":
                return [("corrupt",)]
            raise AssertionError(query)

    assert_error(
        "integrity_check failed",
        m._source_manifest,
        IntegrityBad(),
        {"schema_version": 1, "locator_sha256": "a" * 64},
        "b" * 64,
    )

    class InspectBad:
        def execute(self, query):
            raise sqlite3.OperationalError("bad")

    assert_error(
        "cannot inspect SQLite source",
        m._source_manifest,
        InspectBad(),
        {"schema_version": 1, "locator_sha256": "a" * 64},
        "b" * 64,
    )

    profile, _ = make_store(tmp_path / "tx")

    class TransactionBad:
        def execute(self, query):
            raise sqlite3.OperationalError("bad")
        def close(self):
            pass

    monkeypatch.setattr(m, "_connect_readonly", lambda _: TransactionBad())
    assert_error(
        "export transaction failed",
        m.export_sqlite_logical,
        tmp_path / "tx" / "bundle",
        profile_path=profile,
    )


def test_export_inconsistent_vectors_via_snapshot(tmp_path, monkeypatch):
    profile, _ = make_store(tmp_path)
    real = m._export_records

    def records(connection, dataset):
        if dataset == "vectors":
            return [
                {"fact_id": "a", "vector": [1, 2]},
                {"fact_id": "b", "vector": [1, 2, 3]},
            ]
        return real(connection, dataset)

    monkeypatch.setattr(m, "_export_records", records)
    assert_error(
        "inconsistent dimensions",
        m.export_sqlite_logical,
        tmp_path / "bundle",
        profile_path=profile,
    )


def test_read_dataset_direct_path_guards(tmp_path):
    target = tmp_path / "target"
    target.write_text("\n")
    link = tmp_path / "nodes.jsonl"
    link.symlink_to(target)
    assert_error(
        "regular file",
        m._read_dataset,
        link,
        "nodes",
        {"file": "nodes.jsonl", "records": 0, "bytes": 1, "sha256": m._sha256_file(target)},
    )
    wrong = tmp_path / "wrong.jsonl"
    wrong.write_bytes(b"")
    assert_error(
        "filename mismatch",
        m._read_dataset,
        wrong,
        "nodes",
        {"file": "nodes.jsonl", "records": 0, "bytes": 0, "sha256": m._sha256_file(wrong)},
    )


def test_safe_file_read_guards_identity_mutation_and_io(tmp_path, monkeypatch):
    path = tmp_path / "payload"
    path.write_bytes(b"original")
    real_open = m.os.open

    def replace_before_open(target, flags):
        replacement = tmp_path / "replacement"
        replacement.write_bytes(b"replacement")
        Path(target).unlink()
        replacement.rename(target)
        return real_open(target, flags)

    monkeypatch.setattr(m.os, "open", replace_before_open)
    assert_error("identity changed while opening", m._read_regular_bytes, path, "payload")

    monkeypatch.setattr(m.os, "open", lambda *args, **kwargs: (_ for _ in ()).throw(OSError("no")))
    assert_error("cannot open payload safely", m._read_regular_bytes, path, "payload")

    monkeypatch.setattr(m.os, "open", real_open)
    real_read = m.os.read
    changed = {"done": False}

    def mutate_during_read(fd, size):
        chunk = real_read(fd, size)
        if chunk and not changed["done"]:
            changed["done"] = True
            path.write_bytes(b"mutated-content")
        return chunk

    monkeypatch.setattr(m.os, "read", mutate_during_read)
    assert_error("changed while it was read", m._read_regular_bytes, path, "payload")

    monkeypatch.setattr(m.os, "read", lambda *args: b"")
    assert_error("byte-size changed while it was read", m._read_regular_bytes, path, "payload")

    monkeypatch.setattr(m.os, "read", lambda *args: (_ for _ in ()).throw(OSError("read")))
    assert_error("cannot read payload safely", m._read_regular_bytes, path, "payload")


def test_safe_rechecks_and_directory_guards(tmp_path):
    path = tmp_path / "payload"
    path.write_bytes(b"one")
    _, snapshot = m._read_regular_bytes(path, "payload")
    path.write_bytes(b"two")
    assert_error("changed during verification", m._require_unchanged_file, path, snapshot, "payload")
    path.unlink()
    assert_error("cannot recheck payload", m._require_unchanged_file, path, snapshot, "payload")

    missing = tmp_path / "missing"
    assert_error("cannot inspect bundle", m._directory_identity, missing, "bundle")
    directory = tmp_path / "bundle"
    directory.mkdir()
    directory_snapshot = m._directory_identity(directory, "bundle")
    (directory / "new").write_text("x")
    assert_error(
        "changed during verification",
        m._require_unchanged_directory,
        directory,
        directory_snapshot,
        "bundle",
    )


def test_verify_detects_file_set_change_after_initial_snapshot(tmp_path, monkeypatch):
    bundle, _, _ = export_bundle(tmp_path)
    real_read_dataset = m._read_dataset

    def mutate_after_last_dataset(path, dataset, expected):
        result = real_read_dataset(path, dataset, expected)
        if dataset == "meta":
            (bundle / "late-extra").write_text("x")
        return result

    monkeypatch.setattr(m, "_read_dataset", mutate_after_last_dataset)
    assert_error("file set changed", m.verify_logical_export, bundle)


def test_safe_file_read_reports_lstat_error(tmp_path, monkeypatch):
    path = tmp_path / "payload"
    path.write_bytes(b"x")
    real_lstat = Path.lstat

    def fail_lstat(self):
        if self == path:
            raise PermissionError("denied")
        return real_lstat(self)

    monkeypatch.setattr(Path, "lstat", fail_lstat)
    assert_error("cannot inspect payload", m._read_regular_bytes, path, "payload")
