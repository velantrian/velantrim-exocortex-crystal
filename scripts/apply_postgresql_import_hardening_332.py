from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "core/postgresql_migration.py"
text = PATH.read_text(encoding="utf-8")

text = text.replace("import shutil\n", "")
text = text.replace("from typing import Any, Callable, Iterable, Mapping, Optional", "from typing import Any, Iterable, Mapping, Optional")

old = '''def _preflight(
    connection: Any,
    *,
    driver_version: str,
    target_schema: str,
    require_tls: bool,
    allow_insecure_test_connection: bool,
    require_absent_schema: bool,
) -> dict[str, Any]:'''
new = '''def _preflight(
    connection: Any,
    *,
    driver_version: str,
    target_schema: str,
    require_tls: bool,
    allow_insecure_test_connection: bool,
    require_absent_schema: bool,
    require_writable: bool,
) -> dict[str, Any]:'''
assert text.count(old) == 1
text = text.replace(old, new, 1)

old = '''    create_allowed, read_only, in_recovery = _fetch_one(
        connection,
        "SELECT has_database_privilege(current_user, current_database(), 'CREATE'), "
        "current_setting('transaction_read_only')::boolean, pg_is_in_recovery()",
    )
    if not bool(create_allowed) or bool(read_only) or bool(in_recovery):
        raise StorageOperationError(
            "PostgreSQL target is not writable by the explicit migration role"
        )'''
new = '''    in_recovery = bool(_fetch_one(connection, "SELECT pg_is_in_recovery()")[0])
    if in_recovery:
        raise StorageOperationError("PostgreSQL target is in recovery")
    if require_writable:
        create_allowed, read_only = _fetch_one(
            connection,
            "SELECT has_database_privilege(current_user, current_database(), 'CREATE'), "
            "current_setting('transaction_read_only')::boolean",
        )
        if not bool(create_allowed) or bool(read_only):
            raise StorageOperationError(
                "PostgreSQL target is not writable by the explicit migration role"
            )'''
assert text.count(old) == 1
text = text.replace(old, new, 1)

old = '''def _exact_equivalence(
    cursor: Any,
    *,
    target_schema: str,
    datasets: Mapping[str, Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:'''
new = '''def _exact_equivalence(
    cursor: Any,
    *,
    target_schema: str,
    datasets: Mapping[str, Mapping[str, Any]],
    write_evidence: bool,
) -> dict[str, dict[str, Any]]:'''
assert text.count(old) == 1
text = text.replace(old, new, 1)

old = '''        try:
            cursor.execute(
                f"UPDATE {schema}.dataset_evidence SET "
                "actual_records=%s,actual_bytes=%s,actual_sha256=%s,exact_match=%s "
                "WHERE dataset=%s",
                (
                    actual["records"],
                    actual["bytes"],
                    actual["sha256"],
                    exact,
                    dataset,
                ),
            )
        except Exception as exc:
            raise _database_failure("equivalence evidence write", exc) from exc'''
new = '''        if write_evidence:
            try:
                cursor.execute(
                    f"UPDATE {schema}.dataset_evidence SET "
                    "actual_records=%s,actual_bytes=%s,actual_sha256=%s,exact_match=%s "
                    "WHERE dataset=%s",
                    (
                        actual["records"],
                        actual["bytes"],
                        actual["sha256"],
                        exact,
                        dataset,
                    ),
                )
            except Exception as exc:
                raise _database_failure("equivalence evidence write", exc) from exc'''
assert text.count(old) == 1
text = text.replace(old, new, 1)

old = '''    manifest = _load_manifest(bundle_path)
    root = _receipt_root(receipt_directory)
    schema = _target_schema(target_schema)
    driver = _load_psycopg()
    dsn = _dsn_from_environment(dsn_env)
    connection: Any = None
    try:'''
new = '''    manifest = _load_manifest(bundle_path)
    schema = _target_schema(target_schema)
    driver = _load_psycopg()
    dsn = _dsn_from_environment(dsn_env)
    root = _receipt_root(receipt_directory)
    connection: Any = None
    try:'''
assert text.count(old) == 1
text = text.replace(old, new, 1)

text = text.replace(
    '''            require_absent_schema=True,
        )''',
    '''            require_absent_schema=True,
            require_writable=True,
        )''',
    1,
)
text = text.replace(
    '''                datasets=datasets,
            )''',
    '''                datasets=datasets,
                write_evidence=True,
            )''',
    1,
)

old = '''    except StorageOperationError as exc:
        _write_failure(root, stage, exc)
        raise'''
new = '''    except StorageOperationError as exc:
        try:
            _write_failure(root, stage, exc)
        except StorageOperationError:
            pass
        raise'''
assert text.count(old) == 1
text = text.replace(old, new, 1)

text = text.replace(
    '''            require_absent_schema=False,
        )''',
    '''            require_absent_schema=False,
            require_writable=False,
        )''',
    1,
)

old = '''    connection = _connect(driver, dsn, autocommit=True)
    try:
        preflight = _preflight('''
new = '''    connection = _connect(driver, dsn, autocommit=False)
    try:
        try:
            connection.execute("SET TRANSACTION READ ONLY")
        except Exception as exc:
            raise _database_failure("read-only verification setup", exc) from exc
        preflight = _preflight('''
assert text.count(old) == 1
text = text.replace(old, new, 1)

text = text.replace(
    '''                datasets=manifest["datasets"],
            )''',
    '''                datasets=manifest["datasets"],
                write_evidence=False,
            )''',
    1,
)

old = '''        return {
            "schema_version": POSTGRESQL_IMPORT_SCHEMA_VERSION,'''
new = '''        after = verify_logical_export(bundle_path)
        if after["manifest_sha256"] != verified["manifest_sha256"]:
            raise StorageOperationError(
                "migration bundle changed during PostgreSQL verification"
            )
        connection.rollback()
        return {
            "schema_version": POSTGRESQL_IMPORT_SCHEMA_VERSION,'''
# The first occurrence belongs to import success; replace the final occurrence only.
index = text.rfind(old)
assert index != -1
text = text[:index] + text[index:].replace(old, new, 1)

PATH.write_text(text, encoding="utf-8")
Path(__file__).unlink()
