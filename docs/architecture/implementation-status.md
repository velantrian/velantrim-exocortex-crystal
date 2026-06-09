# Velantrim ExoCortex — Implementation Status

> **Purpose of this document.** This is the canonical bridge between the
> [Notion Canonical Index / Status Map](https://notion.so) and the GitHub
> codebase. It answers one question: *for every architecture concept in the
> Notion canon, what code exists today, and what is still planned?*
>
> **Honesty rule** (same as README): this document describes implemented and
> tested behaviour only. Planned work is clearly labelled `PLANNED`. Nothing
> is implied to be done that is not done.
>
> **Sync discipline**: when a new module is implemented, update the table below
> and remove it from the "Planned" section. This file is the single truth for
> the canon ↔ code mapping.

---

## Status legend

| Label | Meaning |
|---|---|
| `CANONICAL / P0` | Fully implemented, tested, stable. Core of the audited release boundary. |
| `CANONICAL / P1` | Implemented and tested, but at an earlier maturity level. Next hardening priority. |
| `RESEARCH / P2` | Implemented as a research or opt-in module. Off by default. Not part of the audited release boundary. |
| `PLANNED / P0` | Not yet implemented. High priority — blocks measurement and reliability work. |
| `PLANNED / P1` | Not yet implemented. Next self-diagnosis layer after P0 is stable. |
| `PLANNED / P2+` | Not yet implemented. Future work, not blocking current priorities. |

---

## Table 1 — Core reliability layer (P0)

These modules form the audited, dependency-free, grant-ready release boundary.

| Canon concept | Code file(s) | Status | Notes |
|---|---|---|---|
| **TruthGate** | `core/pipeline.py`, `core/ingest.py` | `CANONICAL / P0` | Only automatic entry into L3 (sole exception: explicit, audited curator override in `core/review.py`). `claim_type`, `source_status`, `epistemic_state` enforced. Direct unaudited L3 writes are bugs. |
| **Guardian** | `core/immune.py` + `core/pipeline.py` | `CANONICAL / P0` | CRISPR Guard — blocks hallucination patterns, unsafe writes, Ring Zero violations. |
| **L0 / L1 memory + 8-state ESM** | `core/memory.py` | `CANONICAL / P0` | In-RAM cache + SQLite/WAL. Full ESM: Observed → Supported → Validated → … |
| **L3 canonical graph** | `core/l3_graph.py` | `CANONICAL / P0` | Swappable backend: `auto` → LadybugDB / SQLite / mock. Optional Neo4j. Graph = Truth. |
| **Trace / Receipt** | `core/trace.py`, `core/provenance.py` | `CANONICAL / P0` | Tamper-evident trace chain + replayable receipts. `verify_receipt` re-checks against live canon. |
| **Audit log** | `core/audit.py` | `CANONICAL / P0` | Hash-chained, tamper-evident. Every gate decision and write is logged. |
| **Evaluation Harness (baseline)** | `core/eval.py`, `docs/EVAL.md` | `CANONICAL / P0` | Retrieval hit@1/3/5, MRR, trace completeness, metadata completeness, source-span coverage, receipt replay survival, contradiction P/R. Quality gate with floor/ceiling thresholds. |
| **Ingest / claim classification** | `core/ingest.py` | `CANONICAL / P0` | Utterance → claim type → Guardian + TruthGate → L3. |
| **Evidence store** | `core/evidence.py` | `CANONICAL / P0` | Source-span evidence: `source_uri` / chunk / span + content-light hashes. |
| **GDPR erasure** | `core/erasure.py` | `CANONICAL / P0` | Art. 17 physical erasure across L0/L1/L3 + tombstone. |
| **PII detection** | `core/pii.py` | `CANONICAL / P0` | PII detection and redaction. |
| **Compliance / Record-of-Processing** | `core/compliance.py` | `CANONICAL / P0` | Art. 18 restriction + Art. 30 record-of-processing. |
| **Crypto (opt-in)** | `core/crypto.py` | `CANONICAL / P0` | Art. 32 opt-in encryption at rest for L1 personal-data fields. |
| **External knowledge ingestion** | `core/knowledge.py` | `CANONICAL / P0` | `.txt`, `.md`, `.json`, `.jsonl`, `.csv` → TruthGate path. |
| **Import sessions / dry-run** | `core/imports.py` | `CANONICAL / P0` | Batch import with dry-run, review, restrict/erase. |
| **Read-only MCP server** | `core/mcp_server.py` | `CANONICAL / P0` | `search`, `memory_report`, `get_fact`, `fact_history`, `find_conflicts`, `verify_receipt`. No write path that bypasses TruthGate. |

---

## Table 2 — Self-diagnosis layer (P1)

Implemented and tested, but ongoing hardening. The next priority tier.

| Canon concept | Code file(s) | Status | Notes |
|---|---|---|---|
| **Contradiction classifier** | `core/contradiction.py` | `CANONICAL / P1` | Deterministic. Detects CONTRADICTION, SUPERSEDED, DUPLICATE. Measured in eval via P/R/FPR. |
| **Reconcile / conflict handling** | `core/reconcile.py` | `CANONICAL / P1` | Reinforce, supersede, contradict, find_conflicts. Structured conflict — not magical truth resolution. |
| **L2 review queue** | `core/review.py` | `CANONICAL / P1` | Pre-canonical zone for `Observed` / advisory-quarantined claims. Full review queue is grant scope WP2. |
| **FSRS decay + adaptive threshold** | `core/consolidate.py`, `core/adaptation.py` | `CANONICAL / P1` | FSRS-style decay (attention, not truth). Adaptive TruthGate threshold. |

---

## Table 3 — Research / intelligence layer (P2)

Implemented as optional, off-by-default research modules. Not part of the
audited release boundary. Under Observer + TruthGate control.

| Canon concept | Code file(s) | Status | Notes |
|---|---|---|---|
| **Hebbian / Adaptive Association** | `core/concept.py` | `RESEARCH / P2` | ProtoConcepts from co-activation. `association_weight ≠ truth`. Adaptive navigation only. |
| **Fractal Memory** | `core/fractal.py` | `RESEARCH / P2` | Multi-scale anchoring, CORE anchors resist forgetting. Decay affects attention, not truth. |
| **Neurogenesis / Plasticity** | `core/neurogenesis.py` | `RESEARCH / P2` | Pattern separation, lifelong capacity. Off by default. |
| **NeuroCore (passive plasticity)** | `core/neurocore.py` | `RESEARCH / P2` | RFC0068 Phase 0 passive tracker. **Never writes L3.** Off by default. |
| **Velum / Synaptic pre-graph** | `core/velum.py` | `RESEARCH / P2` | L1.5 entity co-occurrence layer. Does not promote facts. |
| **Analogy graph** | `core/analogy.py` | `RESEARCH / P2` | Semantic bridges. Association weight ≠ evidence. |
| **Volition / Voluntary writes** | `core/volition.py` | `RESEARCH / P2` | Voluntary writes and rehearsal — still passes through all gates. |
| **Epigenetic adaptation** | `epigenetic_adaptation_module.py` | `RESEARCH / P2` | Prototype-level. Not in core release boundary. |

---

## Table 4 — Planned P0 (not yet implemented)

**These are the highest-priority missing pieces.** Without them the system
cannot measure its own errors, explain its own decisions, or prove reliability.

| Canon concept | Planned location | What is missing |
|---|---|---|
| **Black Box Decision Record** | `core/decision_record.py` | A single per-decision record: `decision_id`, `timestamp`, `input_hash`, `claim_type`, `source_status`, `guardian_result`, `truthgate_result`, `contradiction_result`, `esm_before`, `esm_after`, `action_taken`, `reason`, `trace_id`, `audit_id`. Today Trace shows the path; Audit proves the write; Black Box must explain *why* the system decided. |
| **`run_context` enum** | `core/run_context.py` or field in pipeline | Values: `PRODUCTION`, `EVAL_HARNESS`, `CHAOS_SIM`, `RED_TEAM`, `REPLAY`, `SAFE_MODE`. Set only by the system — never by the user. Required to isolate chaos/eval runs from production L3. |
| **Failure Simulator / Chaos** | `tests/chaos/` | Controlled anomaly scenarios: broken JSONL, missing `source_ref`, missing `trace_id`, false FACT promotion attempt (`GENERATED → FACT`, `USER_STATED → WORLD_FACT`), conflicting claims, corrupted metadata, broken rollback target, partial ingestion abort. Strictly sandbox / shadow L3 only — never touches production Core Graph. |
| **Shadow L3 / sandbox testing** | Test fixtures + `run_context` | Eval currently runs against shared in-memory state. Shadow L3 creates an isolated copy of the canon for chaos and red-team tests, then discards it. |
| **Extended eval metrics** | Extend `core/eval.py` | `false_fact_promotion_rate` (most critical — must stay at 0), `rollback_success_rate`, `guardian_false_alarm_rate`, `observer_false_alarm_rate`. These are not yet in `run_baseline()`. |

### Why these are P0 (not P1)

```text
Without Black Box Recorder:   cannot explain why a fact was accepted or rejected.
Without run_context:          chaos tests could corrupt production L3.
Without Failure Simulator:    cannot prove the system survives broken inputs.
Without extended eval metrics: cannot measure false_fact_promotion_rate — the most critical safety number.
```

The canonical formula:

```text
false_fact_promotion_rate > 0  →  architectural danger
rollback_success_rate < 1.0    →  recovery not reliable
guardian_false_alarm_rate > 0  →  useful claims are being blocked
```

---

## Table 5 — Planned P1 (self-diagnosis layer)

After the P0 measurement layer is stable.

| Canon concept | Planned location | Notes |
|---|---|---|
| **Gap Detector** | `core/gap.py` | Scans corpus for structural gaps: `missing_source`, `missing_date`, `missing_definition`, `missing_evidence`, `low_confidence_area`, `contradiction_without_resolution`. Makes the system know *what it does not know*. Not a curiosity engine — no hypothesis generation. |
| **Temporal Policy** | Extend `core/memory.py` / `core/reconcile.py` | Fields: `valid_from`, `valid_until`, `observed_at`, `review_after`, `superseded_by`, `time_scope`. Facts are not deleted when superseded — they receive temporal context. Implement as a policy layer, not a separate large module. |
| **Provenance / import quality evaluation** | Extend `core/eval.py` | Measure quality of external ingestion: schema completeness, source_status distribution, provenance gap rate per import session. |

---

## Table 6 — Planned P2+ (future)

Not blocking current priorities. Build only after the measurement layer is solid.

| Canon concept | Notes |
|---|---|
| **Human Review Console** | UI for reviewing contested claims, rollback events, blocked imports, low-confidence areas. Needs Black Box Recorder first — otherwise it shows an incomplete picture. |
| **Causal Reasoning layer** | `CAUSES`, `ENABLES`, `BLOCKS`, `PREVENTS`. Dangerous before TruthGate strictly separates `WORLD_FACT` from `INTERPRETATION`, `HYPOTHESIS`, `CORRELATION`. Risk: `A before B → A caused B`. Build only after Contradiction Resolver is mature. |
| **Task / Goal Manager** | Operational goals, subgoals, next steps, dependencies. Useful once the core memory is stable and measurable. |
| **Source Authority Model** | Source reputation / domain authority. **`authority_score ≠ truth`.** Keep as metadata (`source_tier`, `source_type`, `source_license`) — never let it override TruthGate. |
| **Full Schema Migration Manager** | Minimal `schema_version` discipline needed now (already has `pyproject.toml` versioning). Full migration manager after the schema stabilises. |
| **Morphology / Multilingual layer** | Lemmatization, entity normalization, alias map, synonym map for Russian and other languages. Part of ingestion/retrieval pipeline — not a separate "cognitive organ". |

---

## Evaluation Harness — current vs. target metrics

### Currently measured (`core/eval.py` `run_baseline()`)

| Metric | Description |
|---|---|
| `retrieval.hit@1/3/5` | Does the expected fact appear in top-k results? |
| `retrieval.mrr` | Mean Reciprocal Rank |
| `trace_completeness` | Share of answers with a non-empty trace |
| `metadata_completeness` | Share of facts with full `source`, `source_status`, `claim_type`, `epistemic_state` |
| `source_span_coverage` | Share of facts with at least one source-span evidence record |
| `unsupported_provenance` | VERIFIED facts with no source-span evidence (must be 0) |
| `receipt_replay_survival` | Share of receipts that re-verify against unchanged canon |
| `contradiction.precision/recall/fpr` | Deterministic classifier on labelled pairs |

### Not yet measured (planned P0 extensions)

| Metric | Why critical |
|---|---|
| `false_fact_promotion_rate` | **Most critical.** Rate at which false or unsupported claims pass through TruthGate into L3. Must be 0. |
| `rollback_success_rate` | Rate at which corrupted-import rollbacks complete cleanly. |
| `guardian_false_alarm_rate` | Rate at which Guardian blocks legitimate claims. |
| `observer_false_alarm_rate` | Rate at which Observer raises alerts on normal claims. |
| `corruption_containment_rate` | Rate at which broken/malformed inputs are contained without L3 mutation. |
| `contradiction_detection_rate` | Rate at which known contradictions in the corpus are surfaced (recall on a larger labelled set). |

---

## Canon rules (invariants)

These rules must not change without architectural review:

```text
Graph = Truth                    One canonical L3 graph is the single source of truth.
TruthGate is the only automatic L3 entry   Sole exception: explicit, audited curator override (review queue). Direct unaudited L3 writes are bugs, not shortcuts.
Provenance for every fact        source, source_status, trace, receipt — non-negotiable.
run_context is system-only       Users cannot set PRODUCTION / EVAL_HARNESS / CHAOS_SIM.
Chaos never touches production   Failure Simulator runs in sandbox / shadow L3 only.
Black Box ≠ Trace ≠ Audit        Trace = path. Audit = tamper-proof record. Black Box = decision reason.
association_weight ≠ truth       Hebbian strength does not promote facts.
authority_score ≠ truth          Source reputation does not override TruthGate.
false_fact_promotion_rate = 0    Any value above 0 is an architectural emergency.
```

---

*Last updated: 2026-06-09. Branch: `claude/admiring-keller-0k7xdv`.*  
*Maintained alongside the Notion Canonical Index / Status Map.*
