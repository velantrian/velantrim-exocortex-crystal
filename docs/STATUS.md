# Velantrim Crystal — Current Status

> Date: 2026-06-17
> Scope: public Crystal repository status note
> Status: docs-only integrity map; does not change runtime behaviour

## Reading rule

Crystal is the public, minimal, verifiable memory core. Titan / Full Exo-Cortex is the broader private research laboratory.

```text
GitHub Crystal = implementation truth for the public core.
Notion Crystal = grant and strategy map.
Titan / Full = research laboratory and future architecture.
```

Do not treat Titan, V9, V10, Noetic, Research PWA, BICA, or private Full Exo-Cortex notes as current Crystal runtime unless a feature is implemented, tested, and listed here or in `TEST_REPORT.md`.

## Status vocabulary

| Status | Meaning |
|---|---|
| `IMPLEMENTED` | Present in the Crystal runtime and covered by tests or reviewer tooling. |
| `FEATURE_FLAGGED` | Code exists but is off by default or requires explicit configuration. |
| `DOCUMENTED_ONLY` | Architecture/specification only; no runtime claim. |
| `RESEARCH` | Private or future research direction; not a public Crystal deliverable. |
| `LEGACY` | Historical material retained for context. |
| `SUPERSEDED` | Old statement replaced by newer repository status. |

## Current public claim boundary

Crystal may safely claim:

- local-first verifiable AI memory infrastructure;
- source-grounded / provenance-oriented memory boundaries;
- TruthGate / Guardian / TRACE / Receipt-oriented design where implemented;
- explicit separation of memory, evidence, retrieval, truth, reasoning, and speech;
- LLM output is not treated as truth by default;
- research directions are separated from current runtime claims.

Crystal must not claim:

- AGI, consciousness, autonomous mind, or biological brain implementation;
- zero hallucinations as a guarantee;
- production-ready Titan console;
- NoeticCore / AttentionRouter / Research PWA as current Crystal runtime;
- Graphiti, Neo4j, OpenAI, or cloud LLMs as mandatory Crystal dependencies;
- verified World Knowledge Core unless source/evidence requirements are met.

## Implementation reality matrix

| Component / area | Current status | Public claim | Risk / note | Next action |
|---|---|---|---|---|
| Crystal public core | IMPLEMENTED | local-first verifiable memory core | Keep narrow; avoid Titan scope creep | Maintain `TEST_REPORT.md` as source of truth |
| TruthGate / epistemic boundary | IMPLEMENTED / evolving | verifies admissibility where wired | Ensure no read/write bypasses are introduced | Add contract tests when changing write/read paths |
| TRACE / Receipt | IMPLEMENTED | replayable proof path where generated | Keep receipt semantics stable | Document threat model and replay assumptions |
| Claim type / origin type | CANDIDATE FOR PORT / FEATURE DESIGN | separates fact, opinion, experience, LLM output | Do not imply all Crystal paths already enforce it unless verified | Add dedicated docs/spec before runtime changes |
| Ingest schema | DOCUMENTED / CANDIDATE | source-first ingestion contract | No source must mean no confident answer | Add `docs/core/INGEST_SCHEMA.md` |
| Dedup / scale design | DOCUMENTED / CANDIDATE | exact/semantic dedup roadmap | Frequency is not independent evidence | Add `docs/core/DEDUP_AND_SCALE.md` |
| Titan console | RESEARCH / TITAN ONLY | demo/research UI | Not production Crystal UI | Keep outside Crystal runtime claim |
| Noetic Orchestration | RESEARCH | future external attention / cognitive routing | Not wired into `/query` as Crystal runtime | Keep as RFC only |
| BICA Alignment | RESEARCH / GRANT LANGUAGE | BICA-informed mapping only | Not a BICA implementation | Use only as cautious framing |
| Graphiti / Neo4j | OPTIONAL / RESEARCH | optional advanced backend inspiration | Not Crystal truth authority | Keep stdlib/local-first Crystal core |
| Knowledge graph / WSC data | RESEARCH / UNVERIFIED unless sourced | draft graph / autolinker prototype if no evidence | Do not call verified canon without real sources/evidence_refs | Add `docs/data/KNOWLEDGE_GRAPH_STATUS.md` |
| Docker / deployment defaults | NEEDS HARDENING REVIEW | local deployment should fail closed | Known dev-key defaults or public bind would weaken auth | Track in `docs/security/DEPLOYMENT_SECURITY.md` |
| Provenance chain | NEEDS CODE VERIFICATION | hash-chain provenance where tests pass | Recent audit claims possible actor/reason regression in Titan | Claude Code must verify/fix with tests |

## Immediate Crystal hardening sequence

1. Keep this status page and future Reality Matrix current.
2. Add deployment security documentation and then patch Docker/compose if needed.
3. Add claim type / origin type documentation before runtime changes.
4. Add ingest schema and dedup/scale docs.
5. Verify provenance-chain contract in code and tests.
6. Decide production profile for TruthPolicy / strict epistemic enforcement.
7. Add knowledge graph status and data-quality verifier rules before claiming verified graph knowledge.

## Relationship to Titan

Titan is valuable as a donor of ideas, UI, research modules and future architecture. Crystal should extract only:

- invariants;
- epistemic contracts;
- evidence/source requirements;
- security lessons;
- minimal dependency-free mechanisms;
- reviewer-safe documentation.

Crystal should not absorb Titan wholesale.
