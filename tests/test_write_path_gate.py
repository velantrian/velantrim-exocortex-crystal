"""Track 3B — write-path TruthGate behaviour pins.

These tests pin (do not change) the existing behaviour that the write paths
route through the TruthGate, and that a force-approve override records the
specific gate reason in its audit detail (`gate_reason`).

Scope note: there is no `/facts` POST endpoint and the major write paths
already route through TruthGate — this is behaviour pinning + audit detail, not
new architecture.
"""
import warnings

import pytest

from core import review, audit, kb_ingest
from core.ingest import ingest


def _blocked_world_fact(claim: str) -> str:
    """Ingest an LLM_OUTPUT WORLD_FACT → truth_gate blocks it deterministically
    (an LLM output can never be a WORLD_FACT on its own), so it stays Observed."""
    res = ingest(claim, claim_type="WORLD_FACT", source_status="LLM_OUTPUT")
    assert res["accepted"] is False, "expected the gate to block this fact"
    return res["fact"]["fact_id"]


# ─── 1. Force-approve still consults the TruthGate ────────────────────────────

def test_force_approve_still_calls_truth_gate(monkeypatch):
    """A force override must re-run the gate (diagnose), not bypass it silently.
    We wrap the gate with a call-recording spy and confirm it fires."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_world_fact("Zentar metal stays liquid at absolute zero")

    calls = []
    real_truth_gate = review.truth_gate

    def spy(facts_pack, *args, **kwargs):
        calls.append(facts_pack)
        return real_truth_gate(facts_pack, *args, **kwargs)

    monkeypatch.setattr(review, "truth_gate", spy)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        res = review.approve(fid, force=True, actor="curator-x",
                             reason="explicit override for the pin test")

    assert res["approved"] is True
    assert calls, "force-approve must call truth_gate (via _diagnose)"


# ─── 2. Force-approve audit detail carries gate_reason ────────────────────────

def test_force_approve_audit_includes_gate_reason(monkeypatch):
    """The override audit event must record WHY the gate blocked (gate_reason),
    not just the verdict — so the override is accountable against the gate."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_world_fact("Borium conducts electricity through vacuum")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        res = review.approve(fid, force=True, actor="curator-y",
                             reason="override with gate_reason audit")
    assert res["approved"] is True

    events = [e for e in audit.audit_log()
              if e["event"] == "review_force_approve" and e["fact_id"] == fid]
    assert len(events) == 1
    detail = events[0]["detail"]
    assert "gate_reason" in detail
    assert detail["gate_reason"], "gate_reason must be populated, not empty"
    assert "LLM_OUTPUT cannot be WORLD_FACT" in detail["gate_reason"]


# ─── 4. Bulk import dry-run blocks an LLM-origin world fact ────────────────────

def test_bulk_dry_run_blocks_llm_world_fact(monkeypatch):
    """A batch/manifest dry-run must predict a `blocked` verdict for an
    LLM_OUTPUT WORLD_FACT — the same gate decision as the live write path,
    without persisting anything."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    result = kb_ingest.dry_run_batch([
        {"claim": "Plurium reverses entropy in open systems",
         "claim_type": "WORLD_FACT", "source_status": "LLM_OUTPUT",
         "confidence": 0.9},
    ])
    assert result["total"] == 1
    assert result["would_block"] == 1
    item = result["items"][0]
    assert item["verdict"] == "blocked"
    assert "LLM_OUTPUT cannot be WORLD_FACT" in item["reason"]
