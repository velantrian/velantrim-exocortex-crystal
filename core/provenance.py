# core/provenance.py
# Velantrim ExoCortex — Verifiable Answer Provenance (replayable receipts)
# v8.13.0-sprint2
#
# "Every answer can be replayed back to its sources." The pipeline already builds
# a trace; this layer turns an answer into a portable, tamper-evident *receipt*
# and lets anyone re-verify it against the canon later:
#
#   receipt = build_receipt(result)        # bind query+answer to the cited facts
#   report  = verify_receipt(receipt)      # replay: are those facts still standing?
#
# The receipt seals the query, the answer, and the exact facts it was built from
# under a SHA-256 digest:
#
#   digest = sha256(canonical(version | created_at | query | answer | citations))
#
# Editing the answer, the query, or any citation changes the digest — so a receipt
# is tamper-evident on its own. With VELANTRIM_PROVENANCE_KEY set, each receipt is
# also HMAC-signed (tamper-PROOF against anyone without the key), mirroring the
# audit log (core/audit.py).
#
# Each citation stores the SHA-256 of the claim text, not the text itself, so the
# receipt stays content-light: verify_receipt can prove a fact's claim is
# unchanged without the receipt re-exposing personal data.
#
# verify_receipt replays every citation against the current L3/L1 canon and
# reports drift, tying provenance to the GDPR machinery:
#   ok           — fact present, claim unchanged, still in a live ESM state
#   erased       — fact was physically erased (Art. 17 tombstone present)
#   restricted   — fact is under processing restriction (Art. 18)
#   modified     — the claim text changed since the answer was produced
#   invalidated  — fact dropped to Contradicted / Deprecated / Collapsed
#   missing      — fact is gone with no tombstone (unexpected)

import os
import json
import hmac
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from core import memory, evidence

RECEIPT_VERSION = 2  # v2 embeds source-span evidence in citations when present
_ENV_KEY = "VELANTRIM_PROVENANCE_KEY"

# ESM states in which a cited fact still "stands" behind the answer.
_LIVE_STATES = {"Validated", "Supported", "ImmutableCore"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _prov_key() -> Optional[bytes]:
    value = os.environ.get(_ENV_KEY)
    return value.encode("utf-8") if value else None


def claim_digest(claim: str) -> str:
    """SHA-256 of a claim's text — lets a receipt commit to content without storing it."""
    return hashlib.sha256((claim or "").encode("utf-8")).hexdigest()


def _canonical(receipt: Dict[str, Any]) -> str:
    """Deterministic serialisation of the sealed fields (digest/signature excluded)."""
    sealed = {k: receipt[k] for k in ("version", "created_at", "query", "answer", "citations")}
    return json.dumps(sealed, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _digest(receipt: Dict[str, Any]) -> str:
    return hashlib.sha256(_canonical(receipt).encode("utf-8")).hexdigest()


def _sign(digest: str, key: Optional[bytes] = None) -> Optional[str]:
    key = key if key is not None else _prov_key()
    if key is None:
        return None
    return hmac.new(key, digest.encode("utf-8"), hashlib.sha256).hexdigest()


def build_receipt(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Turn a pipeline result (from pipeline.run / generate_answer) into a portable,
    tamper-evident provenance receipt. Raises ValueError on a blocked result
    (no answer to attest to).
    """
    if result.get("answer") is None:
        raise ValueError("build_receipt: result has no answer (blocked?)")

    citations: List[Dict[str, Any]] = []
    for f in result.get("facts", []):
        cit: Dict[str, Any] = {
            "fact_id":         f.get("fact_id"),
            "claim_sha256":    claim_digest(f.get("claim", "")),
            "source":          f.get("source", "unknown"),
            "epistemic_state": f.get("epistemic_state", "Observed"),
            "truth_status":    f.get("truth_status", "UNVERIFIED"),
        }
        # Receipt v2: seal any source-span evidence attached to the cited fact, so
        # the receipt can later replay against exact sources — not only fact hashes.
        # Added only when present, keeping evidence-free citations byte-identical.
        fid = f.get("fact_id")
        spans = evidence.evidence_for(fid) if fid else []
        if spans:
            cit["evidence"] = [{
                "evidence_id":   s["evidence_id"],
                "source_uri":    s["source_uri"],
                "source_kind":   s["source_kind"],
                "chunk_id":      s["chunk_id"],
                "span_start":    s["span_start"],
                "span_end":      s["span_end"],
                "source_sha256": s["source_sha256"],
                "claim_sha256":  s["claim_sha256"],
            } for s in spans]
        citations.append(cit)

    receipt = {
        "version":    RECEIPT_VERSION,
        "created_at": _now(),
        "query":      result.get("query", ""),
        "answer":     result["answer"],
        "citations":  citations,
    }
    receipt["digest"] = _digest(receipt)
    signature = _sign(receipt["digest"])
    if signature is not None:
        receipt["signature"] = signature
    return receipt


def _citation_status(cit: Dict[str, Any], tombstoned: set) -> str:
    """Replay a single citation against the current canon."""
    fid = cit.get("fact_id")
    if fid in tombstoned:
        return "erased"
    fact = memory.get_fact(fid)
    if fact is None:
        return "missing"
    if int(fact.get("restricted", 0)):
        return "restricted"
    if claim_digest(fact.get("claim", "")) != cit.get("claim_sha256"):
        return "modified"
    if fact.get("epistemic_state") not in _LIVE_STATES:
        return "invalidated"
    return "ok"


def verify_receipt(receipt: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verify a receipt and replay its citations against the current canon.

    Returns:
      digest_valid    — the sealed fields still hash to receipt["digest"]
      signature_valid — HMAC checked against VELANTRIM_PROVENANCE_KEY
                        (True/False), or None if unsigned / no key configured
      citations       — [{fact_id, status}] per citation (see module docstring)
      summary         — counts by status
      verified        — digest_valid AND signature not failed AND every citation "ok"
    """
    digest_valid = (
        "digest" in receipt and _digest(receipt) == receipt["digest"]
    )

    signature_valid: Optional[bool] = None
    key = _prov_key()
    if receipt.get("signature") is not None and key is not None:
        expected = _sign(receipt.get("digest", ""), key)
        signature_valid = hmac.compare_digest(receipt["signature"], expected or "")

    tombstoned = {t["fact_id"] for t in memory.get_tombstones()}
    citations, summary = [], {}
    for cit in receipt.get("citations", []):
        status = _citation_status(cit, tombstoned)
        out_cit: Dict[str, Any] = {"fact_id": cit.get("fact_id"), "status": status}
        # Receipt v2: replay sealed source-span evidence against the live store.
        sealed_spans = cit.get("evidence")
        if sealed_spans:
            live_ids = {s["evidence_id"] for s in evidence.evidence_for(cit.get("fact_id"))}
            ev_report = []
            for span in sealed_spans:
                if span.get("evidence_id") not in live_ids:
                    ev_status = "evidence_missing"   # the source link was removed
                elif status in ("modified", "erased", "missing"):
                    ev_status = status               # the underlying fact drifted
                else:
                    ev_status = "ok"
                ev_report.append({"evidence_id": span.get("evidence_id"),
                                  "source_uri": span.get("source_uri"),
                                  "status": ev_status})
            out_cit["evidence"] = ev_report
            # A citation is only fully "ok" if its evidence still stands.
            if status == "ok" and any(e["status"] != "ok" for e in ev_report):
                out_cit["status"] = status = "evidence_missing"
        citations.append(out_cit)
        summary[status] = summary.get(status, 0) + 1

    verified = (
        digest_valid
        and signature_valid is not False
        and all(c["status"] == "ok" for c in citations)
        and len(citations) > 0
    )

    return {
        "digest_valid":    digest_valid,
        "signature_valid": signature_valid,
        "citations":       citations,
        "summary":         summary,
        "verified":        verified,
    }
