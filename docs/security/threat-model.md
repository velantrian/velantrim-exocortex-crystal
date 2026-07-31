# Velantrim Crystal — Threat Model (STRIDE)

> **Status:** docs-only. This file **expands** the threat summary in
> [`/SECURITY.md`](../../SECURITY.md); it is **not** a competing source of
> truth. `SECURITY.md` remains the canonical security policy and the canonical
> **vulnerability reporting** channel. Where the two overlap, `SECURITY.md`
> governs the short summary and reporting; this file provides the detailed
> STRIDE breakdown and code-grounded mitigation mapping.
>
> Updated after the non-configurable TruthPolicy hardening recorded in ADR-011.

## Root threat

> **Canon contains a factual claim that was not admitted by TruthGate or lacks
> a valid provenance / TRACE path.**

Velantrim is verifiable memory infrastructure: downstream systems may treat the
strict canonical projection as trusted, so canonical integrity and provenance
are primary security properties. Every threat below is ultimately a path toward
an unadmitted, unprovenanced or tampered claim being used as canonical — or a
path that degrades auditability.

## 1. Scope & assumptions

- **Default deployment is local-first and single-user** (see ADR-003 and
  `SECURITY.md`): no network listener and no outbound call requirement in the
  default configuration.
- **In scope:** Canon/L3 integrity, fact provenance and TRACE, the Epistemic
  State Machine (ESM), immutable core (Ring Zero), tamper-evident audit, and
  optional HTTP/backends as trust-boundary extensions.
- **Out of scope:** multi-tenant authentication/authorization beyond the
  opt-in review token guard; full field-level encryption of on-disk L3 backends;
  and hardening of explicitly enabled optional backends/generators.

## 2. Assets

| Asset | Why it matters | Anchor |
|---|---|---|
| Physical L3 graph / strict CanonicalView | Storage can be multi-status; the strict projection is the trusted answer surface | ADR-002 |
| Fact integrity (modality + origin) | Keeps subjective/model output from being laundered into world facts | `claim_type` / `source_status` |
| Immutable core | Foundational values must not be mutated | `VALUES_CORE`, `RING_ZERO`; invariant I6 |
| Provenance & TRACE | Origin and grounding must be recoverable | `source`, `source_status`, `core/trace.py` |
| Tamper-evident audit log | Governance events must be attributable | `core/audit.py` |
| Personal data | GDPR-oriented obligations | opt-in encryption, restriction, erasure |

## 3. Trust boundaries

1. **Ingestion boundary** — user/external input → `core/ingest.py` →
   `guardian()` → `truth_gate()` → caller performs an L3 write only on pass.
   TruthGate is an admission/decision function: it returns `(passed, reason)`
   and performs no database/Canon write (ADR-007). Its confidence threshold may
   read `core/adaptation` when no explicit threshold is supplied. The
   `LLM_OUTPUT` + `WORLD_FACT` rejection is non-configurable and cannot be
   weakened by process environment or runtime mode (ADR-011).
2. **Read-only query boundary** — HTTP `/ask`/`/receipt`, CLI `ask`/`receipt`
   and MCP search use `core.query_pipeline`; they must not create L0/L1 facts,
   transition ESM, mutate L3, touch the outbox, record episodes or initialize an
   unset embedding fingerprint.
3. **Optional HTTP surface** — the optional FastAPI service binds to
   `127.0.0.1` by default. Review endpoints carry an opt-in bearer-token guard
   (`VELANTRIM_API_TOKEN`, constant-time comparison).
4. **Optional extras** — enabling an external generator or remote Neo4j backend
   extends the trust boundary. Neo4j is optional/lazy and not in the default
   backend chain (ADR-009).

## 4. STRIDE analysis

### Spoofing (identity / source forgery)

| Threat | Mitigation in code |
|---|---|
| LLM-generated text presented as an independently sourced world fact | ADR-001 + ADR-011. `truth_gate()` unconditionally rejects `source_status=LLM_OUTPUT` + `claim_type=WORLD_FACT`; no environment flag disables the rule. |
| Fact admitted without any source | `truth_gate()` rejects empty/falsey `source`. **Caveat:** a literal value such as `"unknown"` is non-empty; the gate checks presence, not source authority or truthfulness. |
| Caller identity on the optional API | Review bearer-token guard when configured. No general multi-user identity layer otherwise. |

### Tampering (integrity)

| Threat | Mitigation in code |
|---|---|
| Direct L3 write bypassing the gate | Primary admission paths call TruthGate. Secondary sync paths reject pre-canonical ESM states via `memory.l3_secondary_sync_admissible()`. `Contradicted`/`Deprecated` sync only when the node already exists in L3. Residual: secondary sync does not re-run the full gate after every metadata update. |
| Process configuration weakens model-origin policy | Mitigated by removal of the `ENABLE_TRUTH_POLICY` read. Historical values (`off`, `false`, `0`, `legacy`) are inert and pinned in tests. |
| Mutating the immutable core | Invariant I6: `transition_esm` raises `ImmutableStateError` for Ring Zero IDs. Claim text is identity-locked after Supported/validated/terminal states; replacement requires a new fact plus explicit supersession. |
| Illegal ESM transition | `ESM_TRANSITIONS` is enforced by `transition_esm`; direct upsert does not overwrite persisted state. |
| Lost-update / stale-cache mutation | SQLite mutation/fresh read/L0 publish are serialized in-process; selected policy operations use `BEGIN IMMEDIATE`; `update_fact()` retains revision CAS. |
| Editing/truncating audit or provenance events | Hash-chain replay and chain checkpoints detect content edits, gaps, reordering and suffix deletion. Whole-database rollback still requires an externally held checkpoint/backup to detect. |

### Repudiation (deniability)

| Threat | Mitigation in code |
|---|---|
| "This claim was never reviewed / approved" | Curator force-override is explicit, attributed and audited with actor/reason/gate reason (ADR-004). |
| Silent automatic promotion/deprecation | Reconcile occurrence/conflict detection is advisory; state-changing supersede/contradict operations are explicit caller decisions (ADR-008). |

### Information disclosure

| Threat | Mitigation in code |
|---|---|
| Personal data readable on disk | Opt-in L1 field encryption. **Non-claim:** on-disk L3 backends are not covered by that field-level encryption; use full-disk encryption and erasure/restriction controls. |
| Restricted fact returned by search | Public read-only search resolves restrictions deny-dominantly and excludes restricted rows before claim/source serialization. |
| Error messages leak internals | Deployment guidance forbids exposing raw exceptions, SQL, stack traces or paths. This remains an operational requirement, not a universal runtime guarantee. |
| Accidental API exposure | Loopback bind by default; public exposure requires explicit deployment changes. |

### Denial of service

| Threat | Status |
|---|---|
| Unbounded ingestion / oversized input | Partially bounded by validation; no general rate limiting in the default single-user local library. |
| Archive / zip-bomb style inputs | Not a current default-runtime mitigation claim. |

DoS remains the weakest-covered STRIDE category in the current baseline.

### Elevation of privilege

| Threat | Mitigation in code |
|---|---|
| Unsanctioned promotion into Canon | Automatic admission remains gated. The only sanctioned exception is an explicit, attributed, audited curator force-override (ADR-004); it does not alter the original TruthGate decision. |
| Optional optimizer relaxes safety | ADR-005: any future optimizer may suggest but cannot relax TruthGate/Guardian/TRACE or self-promote. |

## 5. Mitigation map

- **Admission boundary:** `core/truth_gate.py` — side-effect-free decision over
  the evidence package plus the adaptive threshold context. ADR-011 fixes the
  model-origin policy as non-configurable.
- **Read-only boundary:** `core/query_pipeline.py`, `core/cli.py`,
  `core/mcp_server.py`, `core/api.py` — query/search surfaces do not become
  admission paths.
- **L3 write callers:** `core/pipeline.py`, `core/ingest.py`, `core/review.py` —
  merge after admission or explicit audited governance action.
- **Immutable core & ESM:** `core/memory.py` — Ring Zero protection,
  `ESM_TRANSITIONS`, revision/CAS and transactional checks.
- **Provenance/TRACE:** per-fact origin metadata, evidence spans, receipts,
  `core/trace.py`, `core/provenance.py`, `core/provenance_chain.py`.
- **Audit chain:** `core/audit.py` — append-only hash chain, checkpoint replay,
  optional HMAC.
- **Reconcile discipline:** `core/reconcile.py` — detection is advisory;
  supersede/contradict are explicit state-changing calls.

## 6. Residual risks & explicit non-claims

1. **No environment TruthPolicy bypass remains.** This closes the former
   deployment-configuration risk, but it does not make TruthGate an oracle of
   objective truth. A non-empty independent source can still be wrong,
   misleading or low quality; source authority/evidence quality require broader
   verification policy and human review.
2. **Adaptive threshold context remains.** When `min_confidence` is omitted,
   `core/adaptation` supplies the threshold, so otherwise identical low-margin
   claims can receive different confidence decisions as adaptive state changes.
3. **Fact-writer serialization is scoped to one SQLite database.** It is not a
   distributed lock across copied/replicated databases.
4. **On-disk L3 plaintext.** Field-level encryption covers selected L1 data only
   when enabled; L3 requires deployment-level disk protection or explicit data
   lifecycle controls.
5. **No general authentication/authorization.** Beyond the optional review token,
   Crystal is a single-user local library; do not expose it as a multi-user
   service without an authn/z layer.
6. **DoS is not a primary mitigation target** in the default local runtime.
7. **Optional extras extend the trust boundary.** External generators/backends
   may move data and trust outside the local process.
8. **Bio-named modules are engineering metaphors only** (ADR-006, ADR-010), not
   biological, neuroplastic or conscious implementations.
9. **AdmissionToken** is a possible future defense-in-depth mechanism, not an
   implemented feature or emergency requirement.

## 7. Out of scope

- General multi-tenant authentication and authorization.
- L3 field-level encryption beyond deployment-level protection.
- Distributed consensus/locking across replicated databases.
- Hardening of every explicitly enabled third-party backend/generator.

## 8. References

- [`/SECURITY.md`](../../SECURITY.md) — canonical security policy and reporting.
- [`./DEPLOYMENT_SECURITY.md`](./DEPLOYMENT_SECURITY.md) — deployment defaults.
- [`../ADR.md`](../ADR.md) — core Architecture Decision Records.
- [`../adr/ADR-011-NON_CONFIGURABLE_TRUTH_POLICY.md`](../adr/ADR-011-NON_CONFIGURABLE_TRUTH_POLICY.md) — fixed TruthPolicy decision.
- [`../METAPHOR_VS_MECHANISM.md`](../METAPHOR_VS_MECHANISM.md) — metaphor mapping.
- [`../IMPLEMENTATION_STATUS.md`](../IMPLEMENTATION_STATUS.md) — implementation status.
