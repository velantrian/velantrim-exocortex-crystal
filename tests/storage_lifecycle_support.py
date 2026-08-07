from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import sqlite3
import stat
import time
from pathlib import Path

import pytest

from core import storage_backup as backup
from core import storage_common as common
from core import storage_lock as lockmod
from core import storage_ops as ops
from core import storage_restore as restore


def _profile_payload(path: Path, backend: str = "sqlite") -> dict:
    if backend in {"sqlite", "ladybug"}:
        configuration = {"path": str(path.resolve())}
    else:
        configuration = {"uri": "bolt://localhost:7687", "database": "neo4j"}
    canonical = json.dumps(
        {"backend": backend, "configuration": configuration},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return {
        "schema_version": 1,
        "profile": "l3",
        "backend": backend,
        "durable": True,
        "configuration": configuration,
        "locator_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
    }


def _write_profile(path: Path, db: Path, backend: str = "sqlite") -> dict:
    payload = _profile_payload(db, backend)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def _create_db(path: Path, *, rows: int = 2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.executescript(
        """
        CREATE TABLE nodes(fact_id TEXT PRIMARY KEY, data TEXT NOT NULL);
        CREATE TABLE vectors(fact_id TEXT PRIMARY KEY, vec TEXT NOT NULL);
        CREATE TABLE edges(src TEXT, rel_type TEXT, dst TEXT, props TEXT);
        CREATE TABLE entities(entity_id TEXT PRIMARY KEY, kind TEXT, label TEXT);
        CREATE TABLE mentions(fact_id TEXT, entity_id TEXT, rel TEXT);
        CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);
        """
    )
    for index in range(rows):
        fact_id = f"f{index}"
        conn.execute(
            "INSERT INTO nodes VALUES(?, ?)",
            (fact_id, json.dumps({"fact_id": fact_id, "claim": f"claim {index}"})),
        )
        conn.execute("INSERT INTO vectors VALUES(?, ?)", (fact_id, "[0.1, 0.2]"))
    conn.execute("INSERT INTO edges VALUES('f0', 'LINK', 'f1', '{}')")
    conn.execute("INSERT INTO entities VALUES('e1', 'person', 'One')")
    conn.execute("INSERT INTO mentions VALUES('f0', 'e1', 'MENTIONS')")
    conn.execute("INSERT INTO meta VALUES('embedder_fp', 'hashing')")
    conn.execute("PRAGMA user_version=7")
    conn.commit()
    conn.close()


@pytest.fixture
def store(tmp_path: Path) -> tuple[Path, Path]:
    db = tmp_path / "active" / "l3.db"
    profile = tmp_path / "profiles" / "l3.json"
    _create_db(db)
    _write_profile(profile, db)
    return profile, db


def _copy_bundle(bundle: Path, tmp_path: Path, name: str) -> Path:
    target = tmp_path / name
    shutil.copytree(bundle, target)
    return target


def _refresh_completion(bundle: Path) -> None:
    receipt_path = bundle / common.BUNDLE_RECEIPT
    completion_path = bundle / common.BUNDLE_COMPLETE
    completion = json.loads(completion_path.read_text())
    completion["receipt_sha256"] = common._sha256_file(receipt_path)
    completion_path.write_text(json.dumps(completion))


def _old_empty_lock(profile: Path) -> dict:
    lock = profile.with_name(f"{profile.name}.lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_bytes(b"")
    old = time.time() - 600
    os.utime(lock, (old, old))
    return lockmod.lock_report(profile_path=profile)




__all__ = [
    'hashlib',
    'io',
    'json',
    'os',
    'shutil',
    'sqlite3',
    'stat',
    'time',
    'Path',
    'pytest',
    'backup',
    'common',
    'lockmod',
    'ops',
    'restore',
    'store',
    '_profile_payload',
    '_write_profile',
    '_create_db',
    '_copy_bundle',
    '_refresh_completion',
    '_old_empty_lock',
]
