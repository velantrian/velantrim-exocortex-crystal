# core/storage_ops.py
# Operator CLI for durable SQLite lifecycle and governed storage migration.

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

from core.postgresql_migration import (
    DEFAULT_DSN_ENV,
    import_logical_export_to_postgresql,
    verify_postgresql_import,
)
from core.storage_backup import create_backup, verify_backup
from core.storage_common import StorageOperationError
from core.storage_lock import lock_report, recover_stale_lock, status_report
from core.storage_migration import export_sqlite_logical, verify_logical_export
from core.storage_restore import restore_backup


def _postgresql_options(command: argparse.ArgumentParser) -> None:
    command.add_argument("bundle", type=Path)
    command.add_argument("--target-schema", required=True)
    command.add_argument("--dsn-env", default=DEFAULT_DSN_ENV)
    command.add_argument(
        "--allow-insecure-local-test",
        action="store_true",
        help="allow plaintext PostgreSQL only for an explicit local integration test",
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="velantrim-storage")
    commands = parser.add_subparsers(dest="command", required=True)

    status = commands.add_parser("status")
    status.add_argument("--profile", type=Path)

    backup = commands.add_parser("backup")
    backup.add_argument("output", type=Path)
    backup.add_argument("--profile", type=Path)

    verify = commands.add_parser("verify")
    verify.add_argument("bundle", type=Path)

    restore = commands.add_parser("restore")
    restore.add_argument("bundle", type=Path)
    restore.add_argument("--target-database", type=Path, required=True)
    restore.add_argument("--target-profile", type=Path, required=True)
    restore.add_argument("--receipt", type=Path)

    inspect_lock = commands.add_parser("inspect-lock")
    inspect_lock.add_argument("--profile", type=Path)

    recover = commands.add_parser("recover-lock")
    recover.add_argument("--profile", type=Path)
    recover.add_argument("--expected-mtime-ns", type=int, required=True)
    recover.add_argument("--expected-sha256", required=True)
    recover.add_argument("--min-age-seconds", type=float, default=300.0)
    recover.add_argument("--confirm-no-writer", action="store_true")

    export_logical = commands.add_parser("export-logical")
    export_logical.add_argument("output", type=Path)
    export_logical.add_argument("--profile", type=Path)

    verify_logical = commands.add_parser("verify-logical")
    verify_logical.add_argument("bundle", type=Path)

    import_postgresql = commands.add_parser("import-postgresql-inactive")
    _postgresql_options(import_postgresql)
    import_postgresql.add_argument("--receipts", type=Path, required=True)

    verify_postgresql = commands.add_parser("verify-postgresql-inactive")
    _postgresql_options(verify_postgresql)
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "status":
            report = status_report(profile_path=args.profile)
        elif args.command == "backup":
            report = create_backup(args.output, profile_path=args.profile)
        elif args.command == "verify":
            report = verify_backup(args.bundle)
        elif args.command == "restore":
            report = restore_backup(
                args.bundle,
                target_database=args.target_database,
                target_profile=args.target_profile,
                receipt_path=args.receipt,
            )
        elif args.command == "inspect-lock":
            report = lock_report(profile_path=args.profile)
        elif args.command == "recover-lock":
            report = recover_stale_lock(
                profile_path=args.profile,
                expected_mtime_ns=args.expected_mtime_ns,
                expected_sha256=args.expected_sha256,
                min_age_seconds=args.min_age_seconds,
                confirm_no_writer=args.confirm_no_writer,
            )
        elif args.command == "export-logical":
            report = export_sqlite_logical(args.output, profile_path=args.profile)
        elif args.command == "verify-logical":
            report = verify_logical_export(args.bundle)
        elif args.command == "import-postgresql-inactive":
            report = import_logical_export_to_postgresql(
                args.bundle,
                args.receipts,
                target_schema=args.target_schema,
                dsn_env=args.dsn_env,
                require_tls=not args.allow_insecure_local_test,
                allow_insecure_test_connection=args.allow_insecure_local_test,
            )
        else:
            report = verify_postgresql_import(
                args.bundle,
                target_schema=args.target_schema,
                dsn_env=args.dsn_env,
                require_tls=not args.allow_insecure_local_test,
                allow_insecure_test_connection=args.allow_insecure_local_test,
            )
    except StorageOperationError as exc:
        print(json.dumps({"schema_version": 1, "status": "FAIL", "error": str(exc)}))
        return 2
    print(json.dumps(report, sort_keys=True))
    return 0 if report.get("status") == "PASS" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
