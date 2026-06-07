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
from core.reconcile import fact_history, find_conflicts
from core.observe import memory_report, format_report
from core.erasure import erase_fact, erasure_log
from core.compliance import (
    restrict_processing, unrestrict_processing, record_of_processing,
)
from core.audit import audit_log, verify_audit_log
from core import (pii, provenance, immune, fractal, neurogenesis, concept,
                  volition, velum, analogy, knowledge, neurocore, eval as _eval,
                  evidence)


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
    p_conf = sub.add_parser(
        "conflicts", help="find & classify canon facts conflicting with a claim")
    p_conf.add_argument("claim")
    # ─── Immune / CRISPR Memory Guard (RFC0072) ───────────────────────────────
    sub.add_parser("immune-report", help="immune layer status (threats, hits)")
    p_iblock = sub.add_parser(
        "immune-block", help="record a threat pattern to block on sight (CRISPR)")
    p_iblock.add_argument("pattern")
    p_iblock.add_argument("--type", default="manual", dest="threat_type",
                          help="threat type (e.g. hallucination, harmful)")
    p_iblock.add_argument("--severity", type=float, default=1.0,
                          help="severity 0..1 (block floor is 0.5 by default)")
    p_iallow = sub.add_parser(
        "immune-allow", help="revoke a recorded threat by pattern_id")
    p_iallow.add_argument("pattern_id")
    p_icheck = sub.add_parser(
        "immune-check", help="screen a claim against the immune guard (no write)")
    p_icheck.add_argument("claim")
    # ─── Fractal Memory Layer (RFC0070) ───────────────────────────────────────
    sub.add_parser(
        "fractal-reanchor", help="recompute fractal memory scales over the canon")
    sub.add_parser("fractal-report", help="fractal layer status (scales, capacities)")
    p_fanch = sub.add_parser(
        "fractal-anchors", help="list canonical facts by memory scale")
    p_fanch.add_argument(
        "--scale", choices=fractal.SCALES, default=None,
        help="filter to a single scale (SHORT/MEDIUM/LONG/CORE)")
    # ─── Neurogenesis Dynamic Growth (RFC0073) ────────────────────────────────
    sub.add_parser(
        "neuro-report", help="neurogenesis stats (plasticity, growth, capacity)")
    p_nprune = sub.add_parser(
        "neuro-prune-candidates",
        help="mature, weak, non-anchored facts that could be reclaimed (advisory)")
    p_nprune.add_argument(
        "--max-confidence", type=float, default=0.2,
        help="confidence below which a fact is prune-eligible (default 0.2)")
    # ─── Concept Emergence (RFC0066) ──────────────────────────────────────────
    sub.add_parser(
        "concepts", help="ProtoConcepts emerging from Hebbian co-activation")
    sub.add_parser(
        "concepts-emerge", help="materialise emergent concepts into the canon")
    p_cfor = sub.add_parser(
        "concepts-for", help="concepts a fact belongs to")
    p_cfor.add_argument("fact_id")
    # ─── Memory Volition (RFC0065) ────────────────────────────────────────────
    p_vwrite = sub.add_parser(
        "volition-write", help="system voluntarily writes a fact (through the gates)")
    p_vwrite.add_argument("claim")
    sub.add_parser(
        "volition-focus", help="the system's self-selected attention set (salient facts)")
    sub.add_parser(
        "volition-cycle", help="VolitionWorker: rehearse the most salient memories")
    sub.add_parser("volition-report", help="volition state (voluntary writes, focus)")
    # ─── L1.5 Velum synaptic pre-graph (RFC0016) ──────────────────────────────
    sub.add_parser("velum-report", help="Velum synaptic pre-graph status (edges, signals)")
    p_vn = sub.add_parser(
        "velum-neighbors", help="synaptically connected entities (context hint)")
    p_vn.add_argument("entity")
    p_vn.add_argument("--min-weight", type=float, default=0.3)
    # ─── Analogy Graph / Semantic Bridges / CREATIVE mode (RFC0067) ───────────
    p_alink = sub.add_parser("analogy-link", help="record an analogy/metaphor edge")
    p_alink.add_argument("src")
    p_alink.add_argument("dst")
    p_alink.add_argument("--kind", choices=[analogy.REL_ANALOGOUS_TO,
                                            analogy.REL_METAPHOR_OF],
                         default=analogy.REL_ANALOGOUS_TO)
    p_alink.add_argument("--weight", type=float, default=1.0)
    p_aof = sub.add_parser("analogy-of", help="analogies/metaphors of a node")
    p_aof.add_argument("node")
    p_asug = sub.add_parser(
        "analogy-suggest", help="structural analogy candidates (review, no write)")
    p_asug.add_argument("node")
    p_abr = sub.add_parser(
        "analogy-bridges", help="semantic bridges between two nodes")
    p_abr.add_argument("a")
    p_abr.add_argument("b")
    # ─── External knowledge ingestion (RFC0063) ───────────────────────────────
    p_learn = sub.add_parser(
        "learn", help="import a knowledge file (.txt/.md/.json/.jsonl/.csv) via the TruthGate")
    p_learn.add_argument("path")
    p_learn.add_argument("--source", default=None, help="provenance label (default: filename)")
    # ─── NeuroCore Phase 0 passive tracker (RFC0068) ───────────────────────────
    sub.add_parser(
        "neurocore-report", help="RFC0068 NeuroCore Phase 0 plasticity telemetry")
    # ─── Evaluation harness (baseline) ─────────────────────────────────────────
    sub.add_parser(
        "eval", help="run the baseline evaluation harness (retrieval/trace/receipt metrics)")
    # ─── Evidence spans (WP1) ──────────────────────────────────────────────────
    p_ev = sub.add_parser(
        "evidence", help="list source-span evidence attached to a fact")
    p_ev.add_argument("fact_id")
    p_ev.add_argument("--verify", action="store_true",
                      help="replay each span against the current canon")

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
            **({"reason": res["reason"]} if not res["accepted"] else {}),
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
    elif args.cmd == "conflicts":
        print(json.dumps(find_conflicts(args.claim), ensure_ascii=False))
    elif args.cmd == "immune-report":
        print(json.dumps(immune.immunity_report(), ensure_ascii=False, indent=2))
    elif args.cmd == "immune-block":
        print(json.dumps(
            immune.record_threat(args.pattern, threat_type=args.threat_type,
                                 severity=args.severity, actor="cli"),
            ensure_ascii=False))
    elif args.cmd == "immune-allow":
        print(json.dumps({"forgotten": immune.forget_threat(args.pattern_id,
                                                            actor="cli")},
                         ensure_ascii=False))
    elif args.cmd == "immune-check":
        print(json.dumps(immune.screen(args.claim), ensure_ascii=False))
    elif args.cmd == "fractal-reanchor":
        print(json.dumps(fractal.reanchor(), ensure_ascii=False))
    elif args.cmd == "fractal-report":
        print(json.dumps(fractal.fractal_report(), ensure_ascii=False, indent=2))
    elif args.cmd == "fractal-anchors":
        print(json.dumps(fractal.anchors(args.scale), ensure_ascii=False))
    elif args.cmd == "neuro-report":
        print(json.dumps(neurogenesis.growth_report(), ensure_ascii=False, indent=2))
    elif args.cmd == "neuro-prune-candidates":
        print(json.dumps(
            neurogenesis.prune_candidates(max_confidence=args.max_confidence),
            ensure_ascii=False))
    elif args.cmd == "concepts":
        print(json.dumps(concept.concept_report(), ensure_ascii=False, indent=2))
    elif args.cmd == "concepts-emerge":
        print(json.dumps(concept.emerge_concepts(), ensure_ascii=False))
    elif args.cmd == "concepts-for":
        print(json.dumps(concept.concepts_for_fact(args.fact_id), ensure_ascii=False))
    elif args.cmd == "volition-write":
        res = volition.write_voluntary(args.claim)
        print(json.dumps({
            "accepted": res["accepted"], "volition": True,
            "fact_id": res["fact"]["fact_id"],
            **({"reason": res["reason"]} if not res["accepted"] else {}),
        }, ensure_ascii=False))
    elif args.cmd == "volition-focus":
        print(json.dumps(volition.volition_focus(), ensure_ascii=False))
    elif args.cmd == "volition-cycle":
        print(json.dumps(volition.volition_cycle(), ensure_ascii=False))
    elif args.cmd == "volition-report":
        print(json.dumps(volition.volition_report(), ensure_ascii=False, indent=2))
    elif args.cmd == "velum-report":
        print(json.dumps(velum.get_velum().report(), ensure_ascii=False, indent=2))
    elif args.cmd == "velum-neighbors":
        print(json.dumps(
            velum.get_velum().get_neighbors(args.entity, min_weight=args.min_weight),
            ensure_ascii=False))
    elif args.cmd == "analogy-link":
        print(json.dumps(
            analogy.link_analogy(args.src, args.dst, kind=args.kind,
                                 weight=args.weight, source="cli"),
            ensure_ascii=False))
    elif args.cmd == "analogy-of":
        print(json.dumps(analogy.analogies_for(args.node), ensure_ascii=False))
    elif args.cmd == "analogy-suggest":
        print(json.dumps(analogy.suggest_analogies(args.node), ensure_ascii=False))
    elif args.cmd == "analogy-bridges":
        print(json.dumps(analogy.find_bridges(args.a, args.b), ensure_ascii=False))
    elif args.cmd == "learn":
        print(json.dumps(knowledge.ingest_file(args.path, source=args.source),
                         ensure_ascii=False))
    elif args.cmd == "neurocore-report":
        print(json.dumps(neurocore.report(), ensure_ascii=False))
    elif args.cmd == "eval":
        print(json.dumps(_eval.run_baseline(), ensure_ascii=False))
    elif args.cmd == "evidence":
        if args.verify:
            print(json.dumps(evidence.verify_evidence(args.fact_id), ensure_ascii=False))
        else:
            print(json.dumps(evidence.evidence_for(args.fact_id), ensure_ascii=False))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
