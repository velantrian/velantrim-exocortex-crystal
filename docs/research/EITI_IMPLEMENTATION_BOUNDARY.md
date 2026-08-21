# EITI Implementation Evidence — Crystal Research Boundary

Status: **RESEARCH INPUT · NOT CRYSTAL CURRENT TRUTH · NO AUTHORITY TRANSFER**  
Recorded: 2026-08-21  
EITI evidence source: `velantrian/velantrim-eiti@586cff46b47110847913ea3dea1c33a46cb03f13`

## Why this exists

EITI already implements local retrieval/memory dynamics such as MOSC, ranking/salience, decay/accessibility, local learning analysis and context assembly. Crystal may study compatibility with those mechanisms, but Crystal remains the owner of trusted evidence/memory admission inside Crystal.

```text
EITI retrieval signal != Crystal evidence
EITI association != Crystal canonical relation
EITI local learning != Crystal admission
EITI receipt != objective truth
integration != authority transfer
```

## Relevant research questions for Crystal

1. **Proposal transport** — how can EITI send a typed `ProposalEnvelope` without gaining write authority?
2. **Evidence references** — what minimum `EvidenceRef` fields are required so provenance, lineage and resolvability survive transport?
3. **Target-controlled admission** — how does Crystal issue ALLOW/DENY, a bounded CapabilityLease where appropriate, and immutable receipts?
4. **Derived retrieval signals** — how can MOSC/PKG/salience/decay help candidate retrieval while remaining excluded from evidence quality and truth promotion?
5. **Erasure and replay** — how are derived indexes and proposals invalidated when source material is erased, superseded or loses permission?

## Hard invariants

- association strength cannot raise epistemic status;
- salience cannot substitute for provenance;
- decay/accessibility cannot revise whether evidence exists;
- duplicate/same-lineage evidence cannot increase independent support;
- model output and EITI learning proposals cannot directly write Crystal canonical state;
- Crystal controls admission to Crystal state only; it is not a system-wide sovereign.

## Promotion criteria

No EITI-derived integration becomes Current in Crystal until Crystal itself has:
- a versioned contract and target-owned validator;
- negative tests for replay, scope inflation, delegation and provenance loss;
- fail-closed authorization behavior;
- canonical transaction/rollback semantics where writes are involved;
- Decision/Consumption receipts bound to the exact operation;
- evidence that retrieval assistance does not become implicit epistemic promotion.

EITI is an implementation reference and research input, not a delegated authority source.
