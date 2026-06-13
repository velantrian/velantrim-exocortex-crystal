# core/trace_visualize.py
# Velantrim ExoCortex — TRACE Visualization (reviewer tooling, read-only)
#
# Converts a receipt/trace JSON into Markdown or DOT format for reviewer
# inspection. Pure read-only formatter — no writes, no TruthGate calls,
# no L3 access, no truth verification.

from typing import Any, Dict, List, Tuple, Union


def _extract_receipt_and_verify(
    data: Union[Dict[str, Any], List[Any]],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Extract receipt and verify dicts from a combined, plain, or trace-array input.

    Handles three forms:
    - list (trace array from build_trace): uses data[0] as the receipt dict.
    - dict with "receipt" key (combined receipt+verify): returns (receipt, verify).
    - plain receipt dict: returns (data, {}).
    """
    if isinstance(data, list):
        data = data[0] if data else {}
    if "receipt" in data:
        return data["receipt"], data.get("verify", {})
    return data, {}


def to_markdown(data: Dict[str, Any]) -> str:
    """Convert a receipt (or combined receipt+verify) dict to a Markdown string.

    Parameters
    ----------
    data:
        Either a plain receipt dict or a combined dict with ``"receipt"`` and
        optional ``"verify"`` keys.

    Returns
    -------
    str
        Markdown document suitable for reviewer inspection.
    """
    receipt, verify = _extract_receipt_and_verify(data)

    query = receipt.get("query") or "(none)"
    answer = receipt.get("answer") or "(none)"
    digest = receipt.get("digest")
    digest_short = digest[:16] if digest else "absent"

    # Verification fields — show value if verify dict is present, else "—"
    if verify:
        digest_valid = verify.get("digest_valid", "—")
        signature_valid = verify.get("signature_valid", "—")
        verified = verify.get("verified", "—")
    else:
        digest_valid = "—"
        signature_valid = "—"
        verified = "—"

    citations = receipt.get("citations") or []

    # Build per-citation verify-status lookup from verify["citations"] (if present).
    verify_citations = verify.get("citations") or []
    verify_map: Dict[str, str] = {
        str(c["fact_id"]): c.get("status", "")
        for c in verify_citations
        if "fact_id" in c
    }

    lines: list = [
        "# TRACE Visualization",
        "",
        "## Query",
        query,
        "",
        "## Answer",
        answer,
        "",
        "## Evidence Path",
        "",
        "- Receipt",
        f"  - digest: {digest_short}",
        f"  - digest_valid: {digest_valid}",
        f"  - signature_valid: {signature_valid}",
        f"  - verified: {verified}",
        "",
        f"- Citations ({len(citations)} total)",
    ]

    for cit in citations:
        raw_fact_id = cit.get("fact_id")
        if raw_fact_id is None:
            fact_id_display = "(unknown)"
            verify_status = ""
        else:
            fact_id_str = str(raw_fact_id)
            verify_status = verify_map.get(fact_id_str, "")
            if len(fact_id_str) > 20:
                fact_id_display = fact_id_str[:20] + "…"
            else:
                fact_id_display = fact_id_str

        truth_status = cit.get("truth_status", "")
        source = cit.get("source", "")
        evidence_list = cit.get("evidence")
        evidence_present = "present" if evidence_list else "absent"

        line = (
            f"  - {fact_id_display}: truth_status={truth_status},"
            f" source={source}, evidence={evidence_present}"
        )
        if verify_status:
            line += f", verify={verify_status}"
        lines.append(line)

    lines += [
        "",
        "## Boundary Notes",
        "- Retrieval candidates are not trusted until boundary checks pass.",
        "- TruthGate and receipt verification determine trusted use.",
        "- This visualization does not modify memory or canon.",
    ]

    return "\n".join(lines) + "\n"


def to_dot(data: Dict[str, Any]) -> str:
    """Convert a receipt (or combined receipt+verify) dict to a DOT digraph string.

    Parameters
    ----------
    data:
        Either a plain receipt dict or a combined dict with ``"receipt"`` and
        optional ``"verify"`` keys.

    Returns
    -------
    str
        A DOT language digraph suitable for rendering with Graphviz.
    """
    receipt, verify = _extract_receipt_and_verify(data)

    citations = receipt.get("citations") or []

    # Build receipt node label
    if verify and "verified" in verify:
        receipt_label = f'Receipt\\nverified: {verify["verified"]}'.replace('"', '\\"')
    else:
        receipt_label = "Receipt"

    def _escape(s: str) -> str:
        return str(s).replace("\\", "\\\\").replace('"', '\\"')

    lines = [
        "digraph trace {",
        "  rankdir=LR;",
        '  query [label="Query", shape=ellipse];',
        '  answer [label="Answer", shape=ellipse];',
        f'  receipt [label="{receipt_label}", shape=diamond];',
        "  query -> answer;",
        "  answer -> receipt;",
    ]

    for i, cit in enumerate(citations):
        raw_fact_id = cit.get("fact_id")
        if raw_fact_id is None:
            fact_id_str = "(unknown)"
        else:
            fact_id_str = str(raw_fact_id)

        if len(fact_id_str) > 20:
            short_fact_id = fact_id_str[:20] + "…"
        else:
            short_fact_id = fact_id_str

        truth_status = cit.get("truth_status", "")
        label = f"Claim {_escape(truth_status)}\\n{_escape(short_fact_id)}"

        ts_upper = truth_status.upper()
        is_blocked = "BLOCK" in ts_upper or "UNVERIFIED" in ts_upper
        if is_blocked:
            node_line = f'  claim_{i} [label="{label}", shape=box, style=dashed];'
        else:
            node_line = f'  claim_{i} [label="{label}", shape=box];'

        lines.append(node_line)
        lines.append(f"  answer -> claim_{i};")
        lines.append(f"  claim_{i} -> receipt;")

    lines.append("}")

    return "\n".join(lines) + "\n"
