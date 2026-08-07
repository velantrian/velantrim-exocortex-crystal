# core/storage_ops.py
# Public CLI for fail-closed SQLite storage lifecycle operations.

from __future__ import annotations

import argparse
import json
import sys
from typing import Optional, Sequence

from core.backend_profiles import StorageProfileError
from core.storage_backup import create_backup, verify_backup
from core.storage_common import StorageOperationError
from core.storage_lock import lock_report, recover_stale_lock, status_report
from core.storage_restore import restore_backup


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="velantrim-storage")
    sub = parser.add_subparsers(dest="command", required=True)

    status_cmd = sub.add_parser("status")
    status_cmd.add_argument("--profile")

    backup_cmd = sub.add_parser("backup")
    backup_cmd.add_argument("output")
    backup_cmd.add_argument("--profile")

    verify_cmd = sub.add_parser("verify")
    verify_cmd.add_argument("bundle")

    restore_cmd = sub.add_parser("restore")
    restore_cmd.add_argument("bundle")
    restore_cmd.add_argument("--target-database", required=True)
    restore_cmd.add_argument("--target-profile", required=True)

    inspect_cmd = sub.add_parser("inspect-lock")
    inspect_cmd.add_argument("--profile")

    recover_cmd = sub.add_parser("recover-lock")
    recover_cmd.add_argument("--profile")
    recover_cmd.add_argument("--expected-mtime-ns", required=True, type=int)
    recover_cmd.add_argument("--expected-sha256", required=True)
    recover_cmd.add_argument("--min-age-seconds", type=float, default=300.0)
    recover_cmd.add_argument("--confirm-no-writer", action="store_true")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run one operator action and emit exactly one JSON result."""

    args = _parser().parse_args(list(sys.argv[1:] if argv is None else argv))
    try:
        if args.command == "status":
            result = status_report(profile_path=args.profile)
        elif args.command == "backup":
            result = create_backup(args.output, profile_path=args.profile)
        elif args.command == "verify":
            result = verify_backup(args.bundle)
        elif args.command == "restore":
            result = restore_backup(
                args.bundle,
                target_database=args.target_database,
                target_profile=args.target_profile,
            )
        elif args.command == "inspect-lock":
            result = lock_report(profile_path=args.profile)
        else:
            result = recover_stale_lock(
                profile_path=args.profile,
                expected_mtime_ns=args.expected_mtime_ns,
                expected_sha256=args.expected_sha256,
                min_age_seconds=args.min_age_seconds,
                confirm_no_writer=args.confirm_no_writer,
            )
    except (StorageOperationError, StorageProfileError) as exc:
        result = {
            "schema_version": 1,
            "status": "FAIL",
            "operation": args.command,
            "error": str(exc),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("status") == "PASS" else 1

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
