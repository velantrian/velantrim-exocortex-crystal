# core/cli.py
# Velantrim ExoCortex — Command-line interface
# v8.8.0-sprint2
#
# Тонкая обёртка над ядром: ingest / ask / history / report.
#   python -m core.cli ingest "Water boils at 100C"
#   python -m core.cli ask    "how does water behave"
#   python -m core.cli history <fact_id>
#   python -m core.cli report

import argparse
import json
from typing import Optional, List

from core.ingest import ingest
from core.pipeline import run
from core.reconcile import fact_history
from core.observe import memory_report, format_report


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="velantrim", description="Velantrim ExoCortex memory CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ing = sub.add_parser("ingest", help="принять реплику в память")
    p_ing.add_argument("text")
    p_ask = sub.add_parser("ask", help="спросить (retrieve → gate → answer)")
    p_ask.add_argument("query")
    p_hist = sub.add_parser("history", help="truth-провенанс факта")
    p_hist.add_argument("fact_id")
    sub.add_parser("report", help="сводка по канонической памяти L3")

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
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
