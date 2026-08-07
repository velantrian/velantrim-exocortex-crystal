# core/storage_ops.py
# Pure-stdlib operator CLI for durable SQLite lifecycle and logical export.

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

from core.storage_backup import create_backup, verify_backup
from core.storage_common import StorageOperationError
from core.storage_lock import lock_report, recover_stale_lock, status_report
from core.storage_migration import export_sqlite_logical, verify_logical_export
from core.storage_restore import restore_backup


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
        else:
            report = verify_logical_export(args.bundle)
    except StorageOperationError as exc:
        print(json.dumps({"schema_version": 1, "status": "FAIL", "error": str(exc)}))
        return 2
    print(json.dumps(report, sort_keys=True))
    return 0 if report.get("status") == "PASS" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
