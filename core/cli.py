# core/cli.py
# Velantrim ExoCortex — Command-line interface
# v8.8.0-sprint2
#
# A thin wrapper over the core: ingest / ask / history / report.
#   python -m core.cli ingest "Water boils at 100C"
#   python -m core.cli ask    "how does water behave"
#   python -m core.cli history <fact_id>
#   python -m core.cli report
#   python -m core.cli erase  <fact_id> [--reason ...]   # GDPR Art. 17
#   python -m core.cli erasures                          # deletion log

import argparse
import json
from typing import Optional, List

from core.ingest import ingest
from core.pipeline import run
from core.reconcile import fact_history
from core.observe import memory_report, format_report
from core.erasure import erase_fact, erasure_log
from core.compliance import (
    restrict_processing, unrestrict_processing, record_of_processing,
)
from core.audit import audit_log, verify_audit_log
from core import pii, provenance


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="velantrim", description="Velantrim ExoCortex memory CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ing = sub.add_parser("ingest", help="accept an utterance into memory")
    p_ing.add_argument("text")
    p_ask = sub.add_parser("ask", help="ask (retrieve → gate → answer)")
    p_ask.add_argument("query")
    p_hist = sub.add_parser("history", help="truth provenance of a fact")
    p_hist.add_argument("fact_id")
    sub.add_parser("report", help="summary of L3 canonical memory")
    p_erase = sub.add_parser(
        "erase", help="physically delete a fact across all fabrics (GDPR Art. 17)")
    p_erase.add_argument("fact_id")
    p_erase.add_argument(
        "--reason", default="data_subject_request",
        help="reason for deletion (for tombstone / Art. 30)")
    p_erase.add_argument(
        "--cascade", action="store_true",
        help="also delete facts derived from this one (DERIVED_FROM)")
    sub.add_parser("erasures", help="deletion log (tombstones, Art. 30)")
    p_restrict = sub.add_parser(
        "restrict", help="restrict processing of a fact (GDPR Art. 18)")
    p_restrict.add_argument("fact_id")
    p_unrestrict = sub.add_parser(
        "unrestrict", help="lift the processing restriction (GDPR Art. 18)")
    p_unrestrict.add_argument("fact_id")
    sub.add_parser("ropa", help="record of processing (GDPR Art. 30)")
    sub.add_parser("audit", help="tamper-evident audit log (erase/restrict events)")
    sub.add_parser("audit-verify", help="verify audit-log integrity (hash chain + signatures)")
    p_redact = sub.add_parser("redact", help="detect & redact PII in text (GDPR Art. 5)")
    p_redact.add_argument("text")
    p_receipt = sub.add_parser(
        "receipt", help="ask, then emit a tamper-evident provenance receipt (JSON)")
    p_receipt.add_argument("query")
    p_verify = sub.add_parser(
        "verify-receipt", help="replay a provenance receipt against the canon")
    p_verify.add_argument(
        "file", nargs="?", default="-",
        help="receipt JSON file, or '-'/omitted to read from stdin")

    args = parser.parse_args(argv)

    if args.cmd == "ingest":
        res = ingest(args.text)
        fact = res["fact"]
        print(json.dumps({
            "accepted": res["accepted"],
            "reinforced": res.get("reinforced", False),
            "fact_id": fact["fact_id"],
            "claim_type": fact.get("claim_type"),
            "truth_status": fact.get("truth_status"),
            "conflicts": [c["fact_id"] for c in res.get("conflicts", [])],
        }, ensure_ascii=False))
    elif args.cmd == "ask":
        res = run(args.query)
        print(res.get("answer") or f"[blocked] {res.get('error')}")
    elif args.cmd == "history":
        print(json.dumps(fact_history(args.fact_id), ensure_ascii=False))
    elif args.cmd == "report":
        print(format_report(memory_report()))
    elif args.cmd == "erase":
        print(json.dumps(
            erase_fact(args.fact_id, reason=args.reason, cascade=args.cascade),
            ensure_ascii=False))
    elif args.cmd == "erasures":
        print(json.dumps(erasure_log(), ensure_ascii=False))
    elif args.cmd == "restrict":
        print(json.dumps(restrict_processing(args.fact_id), ensure_ascii=False))
    elif args.cmd == "unrestrict":
        print(json.dumps(unrestrict_processing(args.fact_id), ensure_ascii=False))
    elif args.cmd == "ropa":
        print(json.dumps(record_of_processing(), ensure_ascii=False, indent=2))
    elif args.cmd == "audit":
        print(json.dumps(audit_log(), ensure_ascii=False))
    elif args.cmd == "audit-verify":
        print(json.dumps(verify_audit_log(), ensure_ascii=False))
    elif args.cmd == "redact":
        redacted, found = pii.redact(args.text)
        print(json.dumps({"redacted": redacted, "found": pii.summary(found)},
                         ensure_ascii=False))
    elif args.cmd == "receipt":
        res = run(args.query)
        if res.get("answer") is None:
            print(json.dumps({"error": res.get("error")}, ensure_ascii=False))
            return 1
        print(json.dumps(provenance.build_receipt(res), ensure_ascii=False, indent=2))
    elif args.cmd == "verify-receipt":
        import sys
        raw = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
        print(json.dumps(provenance.verify_receipt(json.loads(raw)), ensure_ascii=False))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
