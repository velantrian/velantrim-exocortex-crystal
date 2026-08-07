#!/usr/bin/env bash
set -euo pipefail

records="${1:-1025}"
output="${2:-storage-migration-benchmark-${records}.json}"

python - "$records" "$output" <<'PY'
from __future__ import annotations

import hashlib
import json
import os
import platform
import resource
import sqlite3
import sys
import tempfile
import time
import tracemalloc
from pathlib import Path

from core import storage_migration as migration

record_count = int(sys.argv[1])
output_path = Path(sys.argv[2])
if record_count < 2 or record_count > migration.MAX_RECORDS_PER_DATASET:
    raise SystemExit("record count must be between 2 and MAX_RECORDS_PER_DATASET")


def batches(total: int, size: int = 512):
    for start in range(0, total, size):
        yield range(start, min(total, start + size))


with tempfile.TemporaryDirectory(prefix="velantrim-migration-benchmark-") as raw:
    root = Path(raw)
    database = root / "source.db"
    profile = root / "profile.json"
    bundle = root / "bundle"

    setup_started = time.perf_counter()
    connection = sqlite3.connect(database)
    connection.executescript(
        """
        CREATE TABLE nodes(fact_id TEXT PRIMARY KEY,data TEXT NOT NULL);
        CREATE TABLE vectors(fact_id TEXT PRIMARY KEY,vec TEXT NOT NULL);
        CREATE TABLE edges(
            src TEXT NOT NULL,rel_type TEXT NOT NULL,dst TEXT NOT NULL,
            props TEXT NOT NULL DEFAULT '{}',UNIQUE(src,rel_type,dst,props)
        );
        CREATE TABLE entities(entity_id TEXT PRIMARY KEY,kind TEXT,label TEXT);
        CREATE TABLE mentions(
            fact_id TEXT NOT NULL,entity_id TEXT NOT NULL,rel TEXT NOT NULL,
            UNIQUE(fact_id,entity_id,rel)
        );
        CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT);
        """
    )
    for batch in batches(record_count):
        connection.executemany(
            "INSERT INTO nodes VALUES (?,?)",
            (
                (
                    f"f{index:08d}",
                    json.dumps(
                        {
                            "fact_id": f"f{index:08d}",
                            "claim": f"synthetic-{index:08d}",
                        },
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                )
                for index in batch
            ),
        )
    for batch in batches(record_count):
        connection.executemany(
            "INSERT INTO vectors VALUES (?,?)",
            ((f"f{index:08d}", "[0.125,0.25,0.5]") for index in batch),
        )
    for batch in batches(record_count - 1):
        connection.executemany(
            "INSERT INTO edges VALUES (?,?,?,?)",
            (
                (
                    f"f{index:08d}",
                    "NEXT",
                    f"f{index + 1:08d}",
                    '{"weight":1}',
                )
                for index in batch
            ),
        )
    for batch in batches(record_count):
        connection.executemany(
            "INSERT INTO entities VALUES (?,?,?)",
            (
                (f"e{index:08d}", "synthetic", f"Entity {index:08d}")
                for index in batch
            ),
        )
    for batch in batches(record_count):
        connection.executemany(
            "INSERT INTO mentions VALUES (?,?,?)",
            (
                (f"f{index:08d}", f"e{index:08d}", "MENTIONS")
                for index in batch
            ),
        )
    connection.executemany(
        "INSERT INTO meta VALUES (?,?)",
        (("benchmark", "bounded-streaming"), ("records", str(record_count))),
    )
    connection.commit()
    connection.close()

    configuration = {"path": str(database.resolve())}
    locator_payload = json.dumps(
        {"backend": "sqlite", "configuration": configuration},
        sort_keys=True,
        separators=(",", ":"),
    )
    profile.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "profile": "l3",
                "backend": "sqlite",
                "durable": True,
                "configuration": configuration,
                "locator_sha256": hashlib.sha256(
                    locator_payload.encode("utf-8")
                ).hexdigest(),
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    setup_seconds = time.perf_counter() - setup_started

    tracemalloc.start()
    export_started = time.perf_counter()
    export_report = migration.export_sqlite_logical(bundle, profile_path=profile)
    export_seconds = time.perf_counter() - export_started
    verify_started = time.perf_counter()
    verify_report = migration.verify_logical_export(bundle)
    verify_seconds = time.perf_counter() - verify_started
    current_python_bytes, peak_python_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if export_report["resource_mode"] != "bounded-streaming":
        raise SystemExit("export did not report bounded-streaming mode")
    if verify_report["resource_mode"] != "bounded-streaming":
        raise SystemExit("verify did not report bounded-streaming mode")

    bundle_bytes = sum(path.stat().st_size for path in bundle.iterdir())
    max_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result = {
        "schema_version": 1,
        "classification": "local-first resource evidence; not a production SLO",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "records_per_primary_dataset": record_count,
        "batch_size": migration.MIGRATION_BATCH_SIZE,
        "source_sqlite_bytes": database.stat().st_size,
        "bundle_bytes": bundle_bytes,
        "setup_seconds": round(setup_seconds, 6),
        "export_seconds_including_internal_verify": round(export_seconds, 6),
        "independent_verify_seconds": round(verify_seconds, 6),
        "python_traced_current_bytes": current_python_bytes,
        "python_traced_peak_bytes": peak_python_bytes,
        "process_max_rss_kib_linux": max_rss,
        "datasets": verify_report["datasets"],
        "vector_dimension": verify_report["vector_dimension"],
        "limits": {
            "source_sqlite_bytes": migration.MAX_SOURCE_SQLITE_BYTES,
            "dataset_bytes": migration.MAX_DATASET_BYTES,
            "records_per_dataset": migration.MAX_RECORDS_PER_DATASET,
            "aggregate_jsonl_bytes": migration.MAX_BUNDLE_DATA_BYTES,
            "record_bytes": migration.MAX_RECORD_BYTES,
        },
    }
    output_path.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
PY
