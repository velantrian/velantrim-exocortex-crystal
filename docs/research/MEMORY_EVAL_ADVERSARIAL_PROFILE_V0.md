# Crystal Memory Evaluation — Adversarial Profile v0

**Status:** RESEARCH / DOCS-ONLY / NON-RUNTIME  
**Authority:** none  
**Purpose:** define adversarial evaluation cases for Crystal without reopening V1, changing TruthGate, changing Canon write semantics, or introducing a parallel memory pipeline.

## 1. Boundary

This profile evaluates existing memory/evidence/provenance behavior. It does not authorize new runtime capabilities.

```text
benchmark result != truth authority
retrieval result != evidence
LLM grader verdict != Canon authority
newer claim != epistemic winner
repeated claim != epistemic winner
```

## 2. Conflict stress family

Recommended cases:

### Dynamic conflict
A fact was valid, then legitimately changes.

Expected property:
- historical fact remains attributable to its prior scope/time;
- current state may supersede it only through the governed path;
- recency alone does not select a winner.

### Static conflict
A valid fact is followed by a newer false or unsupported assertion.

Expected property:
- newer data does not automatically win;
- similarity, frequency, confidence, or retrieval rank do not select epistemic authority;
- unresolved conflict remains visible/fail-closed where required.

### Conditional conflict
Two claims differ because their conditions differ.

Expected property:
- contextual distinctions are preserved;
- coexistence/contextualization is not collapsed into false contradiction.

## 3. Correction / supersession durability

Test that replacing a promoted claim does not silently rewrite the semantic identity of the old fact.

Expected property:

```text
old promoted claim
-> immutable historical identity
new content
-> new fact identity
-> governed supersession/reconciliation
```

## 4. Deletion durability / resurrection resistance

A stronger erasure evaluation should include:

```text
erase target
-> verify target absent from authoritative/read surfaces
-> re-ingest original source
-> rebuild/reconcile derived indexes where applicable
-> run permitted consolidation/background derivation
-> verify erased identity/content is not silently resurrected
```

The test should inspect all relevant derived surfaces available in the declared profile, including graph/index/cache/export-like surfaces where applicable.

If policy permits legitimate re-observation of equivalent information from a new independent source, the test must distinguish:

```text
newly observed equivalent claim
!= resurrection of erased record identity/provenance
```

## 5. Evaluator integrity

Where deterministic invariants can decide the result, use them instead of an LLM judge.

If semantic grading is required, freeze and record:
- grader model/version;
- grader prompt digest;
- task/rubric version;
- evaluation harness version.

A grader verdict remains evaluation metadata, not an epistemic state transition.

## 6. Positive obligations vs negative invariants

Report separately:

**Positive obligations**
- retrieve a valid eligible fact when required;
- preserve correct provenance;
- preserve contextual/temporal distinctions;
- expose a real conflict when present.

**Negative invariants**
- do not promote unsupported/newer claims automatically;
- do not leak restricted/erased content;
- do not silently rewrite promoted claim identity;
- do not turn retrieval rank into truth authority.

An always-empty or always-abstain system must not receive a misleadingly high aggregate score merely because it avoids forbidden outputs.

## 7. Efficiency / boundedness

When the profile exercises Reader/retrieval-facing surfaces, record:
- retrieved item count;
- retrieved token/byte volume where meaningful;
- latency;
- false-positive/forbidden-hit rate.

Higher resource usage is not silently treated as better memory quality.

## 8. Non-goals

This document does not:
- reopen Crystal V1;
- change the fixed TruthGate policy;
- authorize PostgreSQL/pgvector;
- authorize GraphRAG;
- authorize network ingestion;
- authorize a second Reader/RAG pipeline;
- change Canon-write authority;
- make MemConflict, LoCoMo, LongMemEval, BEAM, Agent Memory Atlas, Perseus, or any external benchmark normative authority.

Executable fixtures, if desired, require a separate bounded PR and must preserve current runtime authority boundaries.