# Implementation Status: Crystal vs Full Exo-Cortex

This page prevents implemented Crystal behavior from being mixed with RFC,
roadmap, Titan or broader Exo-Cortex concepts.

**Status date:** 2026-08-01  
**Verified runtime checkpoint:** `916097f`  
**Exact test evidence:** [TEST_REPORT.md](../TEST_REPORT.md)  
**Machine-readable status:** [status/implementation-manifest.json](./status/implementation-manifest.json)

## Status vocabulary

- **Implemented** — code and behavior-pinning tests are merged.
- **Implemented baseline** — usable slice exists; broader lifecycle integration or
  policy hardening remains.
- **Partial** — some mechanisms exist, but the complete contract is not yet
  implemented.
- **RFC / roadmap** — documented design; no current runtime claim.
- **Vision / research** — long-term direction outside the current public core.
- **Out of scope** — intentionally not part of Crystal.

## Three distinct project surfaces

1. **Crystal Core** — this repository: local-first verifiable memory,
   admission/read boundaries, provenance, review and evaluation.
2. **Titan / Full Exo-Cortex** — broader cognitive architecture and experimental
   integrations. Separate research track unless a capability is explicitly
   migrated through an RFC and tested Crystal PR.
3. **Velantrim Culture** — symbolic, linguistic and creative materials outside
   the Crystal engineering and grant core.

## Current implementation table

| Component | Status | Current boundary |
|---|---|---|
| Local-first L0/L1 storage | Implemented | in-process L0 plus SQLite/WAL operational state |
| Pluggable L3 graph storage | Implemented baseline | SQLite dependency-free default; optional adapters have different maturity levels |
| TruthGate | Implemented | admission policy; automatic L3 admission boundary, not an objective-truth oracle |
| Non-configurable LLM-origin rule | Implemented | runtime TruthPolicy bypass removed; `LLM_OUTPUT + WORLD_FACT` cannot automatically become `VERIFIED` |
| Guardian | Implemented baseline | structural detect/pass/block contract before admission and on strict read grounding |
| CanonicalView | Implemented | strict read projection; physical L3 membership is not strict Canon |
| **Unified public read-only query boundary** | **Implemented** | HTTP `/ask`/`receipt`, CLI `ask`/`receipt`, MCP search use `core.query_pipeline`; zero durable mutation contract |
| Legacy `core.pipeline.run()` | Compatibility residual | explicit internal/admission-capable path; no longer used by public CLI query commands |
| **Immutable TrustSnapshot** | **Implemented baseline** | frozen L3/L1 read reconciliation for `core.query_pipeline`; legacy write path migration is separate work |
| TRACE | Implemented | answer grounding trace |
| Receipt and replay | Implemented | tamper-evident digest, optional HMAC, citation replay and source-span support |
| Per-fact provenance chain | Implemented baseline | append-only hash chain; broader ingest/promote/restrict lifecycle wiring remains |
| Evidence spans | Implemented baseline | source URI/kind, chunk, offsets and hashes; institutional hardening remains |
| Import sessions and dry run | Implemented baseline | import accountability and preview behavior |
| Review queue and web UI | Implemented | token-guarded review surface; role model remains limited |
| Resumable review sessions | Implemented | create, resume, record decision and complete session |
| RRF retrieval fusion | Implemented | ranking only; never assigns truth status or bypasses policy |
| Exact duplicate occurrence tracking | Implemented | frequency metadata only; does not increase confidence or count as independent evidence |
| Memory observability | Implemented | read-only reports over states, statuses and contradictions |
| Deterministic eval gate | Implemented | retrieval, grounding, contradiction and refusal controls |
| **Ring Zero mutation gate** | **Implemented** | seven declared semantic mutants; all must be killed; collection/internal errors fail closed |
| Documentation status manifest | Implemented baseline | active README/STATUS/TEST_REPORT consistency checked by CI |
| GDPR-relevant controls | Partial | erasure, restriction, record of processing, audit, redaction and opt-in encryption; not certification |
| Contradiction detection | Implemented baseline | detection exists; complete typed decision contract remains future work |
| Contradiction decision policy | Partial / RFC needed | no complete coexist/supersede/contextualize/review contract yet |
| Roles and multi-curator authorization | Partial | current token boundary is not a production multi-tenant IAM model |
| Retrieval scale benchmark | Implemented baseline | local benchmark exists; scheduled fixed-runner history is not yet implemented |
| Fractal Memory anchoring baseline | Implemented baseline | SHORT→MEDIUM→LONG→CORE anchoring; not cognitive Fractal Attention |

If a component is absent from this table, assume it is not an implemented Crystal
feature until matching code and tests demonstrate otherwise.

## Current trust topology

```text
explicit ingest
→ pending L0/L1 state
→ Guardian
→ TruthGate
→ contradiction/restriction checks
→ physical L3 multi-status graph

public query/search
→ read-only candidate retrieval
→ immutable TrustSnapshot
→ Guardian + CanonicalView STRICT
→ FactsPack + TRACE
→ answer / bounded refusal / Receipt
```

Important invariants:

```text
Physical L3 ≠ strict Canon
retrieval score ≠ truth
confidence ≠ independent evidence
topic/domain score ≠ epistemic confidence
LLM output ≠ independent factual source
query ≠ ingest
```

## Implemented public query surfaces

The read-only guarantee applies to:

- HTTP `POST /ask`;
- HTTP `GET /receipt`;
- CLI `velantrim ask`;
- CLI `velantrim receipt`;
- direct `python -m core.cli ask/receipt`;
- MCP search.

These surfaces must not create/update L0/L1 facts, transition ESM, write L3,
operate the outbox, add episodic links, initialize an unset embedding fingerprint,
store unknown candidates or mutate adaptive verification state.

MCP search is an inspection surface, not a strict-Canon declaration. Confident
factual answers additionally require Guardian and CanonicalView strict grounding.

## Mutation evidence boundary

The targeted mutation gate currently covers seven load-bearing conditions:

1. TruthGate confidence threshold comparison;
2. LLM-origin factual rejection;
3. exact `VERIFIED` requirement;
4. processing restriction exclusion;
5. strict ESM allowlist;
6. malformed-confidence store conflict;
7. Receipt digest equality.

This is executable evidence that assigned tests detect those semantic changes. It
is not a claim of repository-wide mutation adequacy.

## Partial work and next engineering packages

### 1. Contradiction decision contract

Needed artifacts:

- typed `ContradictionReport`;
- explicit outcomes: `COEXIST`, `SUPERSEDE`, `CONTEXTUALIZE`, `REVIEW_REQUIRED`;
- temporal and scope-difference representation;
- evidence comparison without automatic winner-by-confidence;
- review queue integration and accountable curator decision.

### 2. ESM transition specification

One machine-checkable transition table should be shared by admission, review and
reconciliation. It must define allowed transitions, terminal states, authority,
side effects and invalid-transition behavior.

### 3. Performance history

The existing L3 retrieval benchmark should gain scheduled execution on a stable
runner, historical JSON output and trend reporting. Shared PR runner latency
should not become a brittle hard SLO.

### 4. Advisory topic facets

A future domain classifier must be multi-label, optional and non-authoritative.

```text
topic_score ≠ truth
               ≠ evidence quality
               ≠ source authority
               ≠ epistemic confidence
```

It must not assign `VERIFIED`, change ESM, write directly to L3, erase facts or
resolve contradictions.

### 5. Roles and multi-curator hardening

Production shared-service use requires scoped identity, accountable review
actors, concurrent decision safety and auditable authorization boundaries.

## RFC / roadmap only

| Component | Status | Boundary |
|---|---|---|
| Observer action policy | RFC / roadmap | read-only observability exists; automatic flag→action routing does not |
| Mode Layer and Mode Router | RFC / roadmap | no current runtime mode authority |
| Imagination Mode / Spark | RFC / roadmap | must remain sandboxed and non-authoritative |
| Temporal / bi-temporal claims | RFC / roadmap | no complete current schema or reasoning engine |
| Provenance grades | RFC / roadmap | BRONZE/SILVER/GOLD are not current schema fields |
| KnownUnknown / research-question objects | RFC / roadmap | should be review/research objects, not strict facts |
| Autonomous question generation | Research | no current autonomous runtime |
| Advanced causal contradiction resolution | Research | no current causal resolver |
| Distributed replication | Research | not current Crystal baseline |
| Titan cognitive integration | Separate research track | outside current grant-facing runtime |
| Artificial consciousness claims | Out of scope | no such implementation claim |
| Velantrim Culture | Out of scope | intentionally separate from Crystal engineering core |

## Graph backend role summary

| Backend | Role |
|---|---|
| SQLite | dependency-free verified baseline |
| LadybugDB | optional embedded graph adapter/candidate |
| Kuzu lineage | legacy/reference context, not mandatory runtime |
| Neo4j | optional inspection/demo integration |
| Mock | contract and test support |

Backend choice must not weaken TruthGate, CanonicalView, restrictions or Receipt
contracts.

## Grant and public-claim rule

The NLnet NGI0 Commons Fund proposal is submitted and under review. Funding is
not claimed as awarded.

Already-merged work remains baseline. Future RFCs, Titan mechanisms and research
ideas are not silently counted as funded Crystal deliverables.

## Documentation routes

- [README](../README.md)
- [Documentation map](./DOCUMENTATION_MAP.md)
- [Current status](./STATUS.md)
- [Architecture](./ARCHITECTURE.md)
- [ADR index](./ADR.md)
- [Test report](../TEST_REPORT.md)
- [Failure modes](./FAILURE_MODES.md)
- [Evaluation](./EVAL.md)
- [Grant scope](./GRANT_NLNET_SCOPE.md)
- [Metaphor vs mechanism](./METAPHOR_VS_MECHANISM.md)
