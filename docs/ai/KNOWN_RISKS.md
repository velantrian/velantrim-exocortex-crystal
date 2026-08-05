# ⚠️ Crystal Known Risks and Open Boundaries

**Status date:** 2026-08-05

This register is an orientation layer. It does not replace issues, security documents,
ADRs, tests or current code inspection.

## Severity model

- **P0:** can invalidate core trust, safety or durable-state claims.
- **P1:** materially limits production, scale, interoperability or reviewer confidence.
- **P2:** maintainability, governance, documentation or research debt.

A risk closes only with merged implementation/doc changes and explicit evidence.

## P0 — trust-boundary regressions to prevent

No new confirmed P0 defect was introduced by this documentation work. These remain
permanent audit targets because a regression would invalidate Crystal's core purpose.

### P0.1 TruthGate or Guardian bypass

**Risk:** a new API, adapter, import path, review helper or background process writes
trusted/canonical state without the established admission and safety boundaries.

**Closure/protection evidence:**

- explicit authority owner;
- adversarial tests for all public/internal write paths;
- fail-closed behavior when policy/evidence dependencies fail;
- CI coverage and mutation proof for the changed boundary.

### P0.2 Query-to-write contamination

**Risk:** read/query/retrieval paths reinforce, promote, create or mutate canonical
claims.

**Required proof:** public HTTP, CLI and MCP query surfaces remain read-only, including
error, retry and optional-provider paths.

### P0.3 Strict Canon leakage

**Risk:** restricted, erased, unverified or contested physical L3 records enter strict
grounding because physical graph presence is mistaken for Canon membership.

**Required proof:** deny-dominant immutable reconciliation tests and consumer-level
integration tests.

### P0.4 Proof/state split

**Risk:** a canonical mutation commits without the required provenance/audit/receipt
record, or a failed mutation leaves a success-looking proof artifact.

**Required proof:** atomicity/idempotency analysis, crash-window tests and replay
verification.

## P1 — current engineering and operational limitations

### P1.1 Distributed curator coordination is absent

The included decision lease registry is process-local. Multiple processes require an
external lease adapter and a separately reviewed failure model.

**Do not claim:** distributed locking or cross-process exactly-once conflict decisions.

**Closure proof:** adapter contract, fencing/CAS semantics, expiry/recovery tests,
operator metrics and multi-process integration evidence.

### P1.2 Production identity provider and multi-tenancy are incomplete

Crystal has scoped curator principals/capabilities and host-authenticated actor binding,
but not a complete production IdP, tenant-isolation and policy-administration surface.

**Closure proof:** tenant model, authenticated identity mapping, authorization matrix,
isolation tests, revocation/audit behavior and deployment documentation.

### P1.3 Broader provenance lifecycle wiring

Status documents list broader provenance lifecycle wiring as future work.

**Risk:** proof may be strong on verified paths but inconsistent across less central
lifecycle operations or future adapters.

**Closure proof:** inventory of all mutation/read surfaces, common receipt/provenance
contract, replay tests and no orphaned state/proof windows.

### P1.4 Performance SLO policy is not a production guarantee

Benchmark history exists, but controlled-runner SLO policy and operational capacity
claims require a stable environment, thresholds and regression handling.

**Closure proof:** versioned workload, controlled hardware/runtime metadata, p50/p95/p99
budgets, storage growth limits and CI/operations policy.

### P1.5 Mutation testing scope is targeted, not repository-wide

The checkpoint proves 7/7 declared Ring Zero mutants killed. This does not mean all
semantic mutations across the repository are covered.

**Closure proof:** expanded mutation inventory, bounded execution policy and documented
scope/limitations.

### P1.6 Legacy normalized-ID migration gap (#165)

New normalized ingest IDs do not fully deduplicate case/whitespace variants against
pre-normalization rows unless the re-ingested raw text matches the old ID path.

**Risk:** duplicate logical claims in upgraded stores.

**Closure proof:** reviewed migration or persistent normalized-claim index, collision
policy, occurrence preservation and backwards-compatibility tests.

### P1.7 Dedicated long-document Reader Core is absent

Crystal has evidence spans and strong admission/proof boundaries, but no verified
multi-pass reading subsystem with structural maps, coverage tracking, bookmarks,
exception/contradiction passes and selective re-reading.

**Risk:** downstream adapters may overcompress long documents or lose rare but important
source details before claim review.

**Safe direction:** source-linked candidate cards upstream of ordinary Guardian and
TruthGate; no second Canon owner.

## P2 — governance, maintenance and research debt

### P2.1 i18n governance and link validation (#285, #286)

Ten localized top-level READMEs increase drift risk.

**Closure proof:** authoritative-language policy, localization manifest, sync metadata,
link/selector validation and conservative claim comparison.

### P2.2 Secret-scanning and fixture hygiene (#214)

Current security CI exists, but lightweight secret scanning and systematic review of
large fixtures/data remain additive hygiene work.

**Closure proof:** deterministic scan policy, false-positive handling, fixture provenance
and no weakening of existing security/coverage gates.

### P2.3 Research PR accumulation

Open research/documentation PRs #245, #249, #261 and #262 can become stale against
`main`, overlap, or be mistaken for current runtime.

**Closure proof:** periodic rebase/review, explicit status headers, conflict-free
reconciliation and closure/merge decisions.

### P2.4 Stale issues after implementation

Some older open issues describe capabilities later implemented through other PRs.

**Risk:** agents may report a false gap by trusting issue state instead of code/status.

**Closure proof:** issue triage linked to the implementing PR/checkpoint or a clear note
explaining what remains.

### P2.5 Documentation/context drift

This AI pack can itself become stale.

**Closure proof:** every material PR completes the documentation synchronization block
and updates `CURRENT_STATE`, `KNOWN_RISKS`, `COMPONENT_MAP` or `WORK_LOG` when affected.

## Research-only boundaries

The following must remain `PROPOSED`/research unless separately implemented and merged:

- Essence Workdesk / dialogue-board experiments;
- cognitive state, planning and user-intent hypotheses;
- Native Kernel compatibility and event substrate concepts;
- Personal Exo-Cortex, Mentaury and Full Exo-Cortex modules;
- ASR/Small Core active-state recovery;
- any artificial-consciousness or digital-person claim.

## Risk closure template

When closing a risk, record:

```text
risk id
exact PR and merge SHA
affected authority boundary
implementation summary
tests and CI run
runtime wiring/default state
migration/recovery behavior
remaining limitations
documentation and Notion updates
```
