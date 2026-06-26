# Velantrim Crystal — Threat Model (STRIDE)

> **Status:** docs-only. This file **expands** the threat summary in
> [`/SECURITY.md`](../../SECURITY.md); it is **not** a competing source of
> truth. `SECURITY.md` remains the canonical security policy and the canonical
> **vulnerability reporting** channel. Where the two overlap, `SECURITY.md`
> governs the short summary and reporting; this file provides the detailed
> STRIDE breakdown and code-grounded mitigation mapping.
>
> Grounded in the read-only repository audit performed after PR #190. No
> runtime change is implied or made by this document.

## Root threat

> **Canon contains a factual claim that was not admitted by TruthGate or lacks
> a valid provenance / TRACE path.**

Velantrim is verifiable memory infrastructure: downstream systems treat Canon
as *true*, so the integrity and provenance of the canonical store is itself the
primary security property. Every threat below is ultimately a path toward this
root threat — an unadmitted, unprovenanced, or tampered claim becoming
canonical — or a path that degrades the auditability of how a claim got there.

## 1. Scope & assumptions

- **Default deployment is local-first and single-user** (see ADR-003 and
  `SECURITY.md`): no network listener, no outbound calls in the default
  configuration.
- **In scope:** Canon / L3 integrity, fact provenance and TRACE, the Epistemic
  State Machine (ESM), the immutable core (Ring Zero), the tamper-evident audit
  log, and the optional HTTP service / optional backends as trust-boundary
  extensions.
- **Out of scope (mirrors `SECURITY.md`, no contradiction):** multi-tenant
  authentication / authorization (beyond the opt-in review token guard);
  full field-level encryption of on-disk L3 backends (opt-in L1 field
  encryption exists; see `SECURITY.md` §"Out of scope"); hardening of
  explicitly-enabled optional backends/generators.

## 2. Assets

| Asset | Why it matters | Anchor |
|-------|----------------|--------|
| Canonical graph (L3) / Canon | The trusted, verified subset other systems treat as true | ADR-002 |
| Fact integrity (modality axis) | Keeps subjective / LLM output from being laundered into world-facts | `claim_type` / `source_status` in `core/memory.py` |
| Immutable core | Foundational values must not be mutated | `VALUES_CORE`, `RING_ZERO`; invariant I6 |
| Provenance & TRACE | "Where did this come from" must be recoverable | `source` + `source_status` per fact; `core/trace.py` |
| Tamper-evident audit log | Compliance events must be non-repudiable | `core/audit.py` (GDPR Art. 5(2)/24/30) |
| Personal data | GDPR obligations | opt-in encryption `core/crypto.py`; erasure path |

## 3. Trust boundaries

1. **Ingestion boundary** — user/external input → `core/ingest.py` →
   `guardian()` → `truth_gate()` → (on pass) caller performs the L3 write.
   TruthGate is an **admission / decision function**: it returns `(passed, reason)`
   and does not itself write to the DB or mutate Canon (ADR-007). It is *not*
   pure over the evidence package alone — its threshold reads `core/adaptation`
   and `ENABLE_TRUTH_POLICY` at call time (see §4–§6) — so the decision is not
   guaranteed replayable as that context changes. The write is performed by the
   caller (pipeline / ingest / review) only on admission.
2. **Optional HTTP surface** — the optional FastAPI service
   (`pip install ".[api]"`) binds to `127.0.0.1` by default and is a
   localhost-trust surface. `/review/*` endpoints carry an opt-in bearer-token
   guard (`VELANTRIM_API_TOKEN`, constant-time compare). See `SECURITY.md`
   §"Optional HTTP service layer".
3. **Optional extras** — enabling the optional Claude generator or a remote
   **Neo4j** backend extends the trust boundary to those services. Neo4j is
   **optional / lazy and is not in the default backend chain** (the default
   chain falls back to embedded / SQLite / in-memory backends; the Neo4j driver
   is imported lazily and only when that backend is explicitly selected) —
   ADR-009.

## 4. STRIDE analysis

Each row maps a category to the relevant manifestation and the **in-repo,
audit-verified** control. Controls are stated as what the code does today, not
as guarantees beyond that (see §6 for residual risk and non-claims).

### Spoofing (identity / source forgery)

| Threat | Mitigation in code |
|--------|--------------------|
| LLM-generated text presented as an independently-sourced world-fact | ADR-001 (LLM is speech, not a canon writer). Type-aware `truth_gate()` blocks `LLM_OUTPUT` + `WORLD_FACT` without an independent source under the strict policy (`core/truth_gate.py`). |
| Fact admitted without any source | `truth_gate()` rejects a fact whose `source` is empty/falsey (returns `(False, reason)`). **Caveat:** `store_fact` defaults an *omitted* source to the literal `"unknown"` (`core/memory.py`), which is truthy and passes this check — the gate enforces a non-empty source, not a *meaningful / verifiable* one. |
| Caller identity on the optional API | `/review/*` bearer-token guard when `VELANTRIM_API_TOKEN` is set (constant-time compare). No general authn layer otherwise (see §7). |

### Tampering (integrity)

| Threat | Mitigation in code |
|--------|--------------------|
| Direct L3 write bypassing the gate | **Primary entry point**: admission / ingest writes go through `truth_gate()`; `store_fact` writes L0/L1 only, never L3. Most other L3 merges are metadata re-syncs of an already-admitted fact. **Caveat:** those sync paths do not re-check the gate, and some do not require `Validated` — e.g. `compliance._sync_restriction()` (`core/compliance.py`) merges a restricted fact, and `reconcile.reinforce()` (`core/reconcile.py`) calls `_sync_l3()` after a confidence/metadata change; either can merge an `Observed` fact into L3. Treat "no unguarded L3 writes" as scoped to the admission/ingest paths, not an absolute guarantee. |
| Mutating the immutable core | Invariant **I6**: `transition_esm` raises `ImmutableStateError` for Ring Zero IDs (`VALUES_CORE`, `RING_ZERO`) — this blocks *state transitions* only. **Caveat:** `update_fact()` has no immutable-id guard, so claim/source/metadata of those IDs can still be changed; I6 is not blanket immutability. |
| Illegal epistemic transition (e.g. Collapsed → Validated) | `ESM_TRANSITIONS` matrix validated in `transition_esm`. `store_fact` preserves the existing `epistemic_state` in the DB on conflict (the `ON CONFLICT` clause omits `epistemic_state`); L0 is updated only after the DB write using the persisted state. A re-`store_fact` can no longer bypass the transition matrix — use `transition_esm()` to advance state. |
| Lost-update / stale-cache state change | `transition_esm` uses a compare-and-swap (`WHERE fact_id = ? AND epistemic_state = ?`) and evicts stale L0 on a CAS miss (PR #190). This is **defense-in-depth correctness hardening**, not a full atomic state-machine guarantee. |
| Editing past audit entries | Append-only hash chain in `core/audit.py`; `verify_audit_log()` detects edits/reordering; optional per-entry HMAC (`VELANTRIM_AUDIT_KEY`). |

### Repudiation (deniability)

| Threat | Mitigation in code |
|--------|--------------------|
| "This claim was never reviewed / I never approved it" | Curator override is an explicit, attributed, audited event (ADR-004); recorded with actor + reason. |
| Silent automatic promotion/deprecation | Reconcile's *occurrence / conflict* surface is **append-only / advisory** (ADR-008): `record_occurrence` is a frequency signal (not independent evidence) and never changes confidence/truth_status/ESM; `find_conflicts` returns candidates, not verdicts. State-changing operations (`supersede`/`contradict`) are explicit and caller-invoked, never automatic. |

### Information disclosure

| Threat | Mitigation in code |
|--------|--------------------|
| Personal data readable on disk | Opt-in field-level encryption of L1 personal-data columns (`core/crypto.py`, `VELANTRIM_ENCRYPTION_KEY`). **Non-claim:** on-disk L3 backends store claims in plaintext and are **not yet** covered by field-level encryption — use full-disk encryption or the Art. 17 erasure path (see `SECURITY.md`). |
| Error messages leaking internals | Production guidance: responses must not leak raw exceptions, SQL fragments, stack traces, or filesystem paths (`docs/security/DEPLOYMENT_SECURITY.md`). This is a deployment requirement, not an automatic runtime guarantee. |
| Accidental public exposure of the API | Loopback bind by default; explicit override required for public exposure (`SECURITY.md`, `DEPLOYMENT_SECURITY.md`). |

### Denial of service

| Threat | Status |
|--------|--------|
| Unbounded ingestion / oversized input | Partially bounded by validation in `store_fact`; no dedicated rate limiting in the default local library (single-user assumption). |
| Archive / zip-bomb style inputs | **Not a current in-scope mitigation target** for the default local runtime; noted here for completeness, not claimed as mitigated. |

> DoS is the weakest-covered STRIDE category in the current code and is stated
> as such — see §6.

### Elevation of privilege

| Threat | Mitigation in code |
|--------|--------------------|
| Unsanctioned promotion into Canon | The only sanctioned exception to the automatic gate is the explicit, attributed, audited curator override in the review queue (ADR-004). |
| Optional optimizer relaxing safety boundaries | ADR-005: any future optimizer is constrained and cannot relax TruthGate / Guardian / TRACE; optimization may suggest, only a human curator may promote. (RFC-aligned / documentation-only today.) |

## 5. Mitigation map (verified references)

- **Admission boundary:** `core/truth_gate.py` — `(passed, reason)` decision
  function with no DB write / no Canon mutation (ADR-007); caller performs
  writes. Note its threshold reads `core/adaptation` and `ENABLE_TRUTH_POLICY`
  at call time, so the decision depends on contextual state, not the evidence
  package alone.
- **Single L3 entry:** `core/pipeline.py` / `core/ingest.py` /
  `core/review.py` — L3 merges occur only after admission, or on
  already-Validated facts.
- **Immutable core & ESM:** `transition_esm` in `core/memory.py` — I6 Ring Zero
  protection, `ESM_TRANSITIONS` validation, CAS guard (PR #190).
- **Provenance/TRACE:** per-fact `source` + `source_status`; `core/trace.py`.
- **Audit chain:** `core/audit.py` — append-only hash chain, `verify_audit_log()`,
  optional HMAC.
- **Encryption at rest (opt-in):** `core/crypto.py`.
- **Reconcile discipline:** `core/reconcile.py` — the occurrence/conflict
  surface is append-only/advisory; `supersede()`/`contradict()` are explicit,
  caller-invoked operations that *do* transition state, sync L3 and add edges (ADR-008).

## 6. Residual risks & explicit non-claims

These are stated openly to avoid overclaiming:

1. **`ENABLE_TRUTH_POLICY=off` is a documented legacy bypass / opt-in risk —
   not an active exploit.** With the strict policy disabled, the
   `LLM_OUTPUT` + `WORLD_FACT` block is skipped and such a claim is judged on
   source + confidence alone. **However**, it does **not** elevate
   `truth_status` to `VERIFIED` (an `LLM_OUTPUT` world-claim resolves to
   `UNVERIFIED`). Strict policy is the default (unset / `on`); operators who set
   `off` knowingly opt into the legacy behavior.
2. **CAS in `transition_esm` is defense-in-depth, not full atomicity.** It
   catches lost-update / stale-cache divergence; it is not a thread/process lock.
   The `store_fact` upsert path no longer overwrites `epistemic_state` on
   conflict: the `ON CONFLICT` clause omits `epistemic_state`, and L0 is
   populated from the persisted DB state after the write. A re-`store_fact`
   cannot bypass the transition matrix. Use `transition_esm()` to advance
   epistemic state explicitly.
3. **On-disk L3 plaintext.** Field-level encryption covers L1 personal-data
   columns only when enabled; on-disk L3 claims are plaintext (mitigate with
   full-disk encryption or Art. 17 erasure).
4. **No general authentication / authorization.** Beyond the opt-in review
   token guard, Velantrim is a single-user local library; do not expose it as a
   network service without adding an authn/z layer.
5. **DoS is not a primary mitigation target** in the default local runtime.
6. **Optional extras extend the trust boundary.** Enabling the Claude generator
   or a remote Neo4j backend moves data/trust to those services. Neo4j is
   optional/lazy and not in the default backend chain.
7. **Bio-named modules are engineering metaphors only** (ADR-006, ADR-010):
   `neurogenesis`, `immune`, `neurocore`, `fractal`, `salience`, `adaptation`
   describe deterministic, auditable mechanisms over the existing canon. They
   are **not** biological, neuroplastic, or conscious implementations, and carry
   no such claim. Disclaimers stay synchronized with
   [`../METAPHOR_VS_MECHANISM.md`](../METAPHOR_VS_MECHANISM.md).
8. **AdmissionToken** (a stronger, token-bound admission proof) is a potential
   **future defense-in-depth** hardening, **not** an emergency fix; no active
   vulnerability requires it today.

## 7. Out of scope (mirrors `SECURITY.md`)

- Authentication / multi-tenant access control beyond the opt-in review token.
- Encryption at rest beyond the opt-in L1 field encryption.
- Hardening of explicitly-enabled optional backends/generators.

## 8. References

- [`/SECURITY.md`](../../SECURITY.md) — canonical security policy and
  vulnerability reporting (governs the summary and reporting channel).
- [`./DEPLOYMENT_SECURITY.md`](./DEPLOYMENT_SECURITY.md) — deployment hardening
  defaults.
- [`../ADR.md`](../ADR.md) — Architecture Decision Records (ADR-001…010).
- [`../METAPHOR_VS_MECHANISM.md`](../METAPHOR_VS_MECHANISM.md) — metaphor →
  mechanism mapping.
- [`../IMPLEMENTATION_STATUS.md`](../IMPLEMENTATION_STATUS.md) — the source of
  truth for implementation status.
