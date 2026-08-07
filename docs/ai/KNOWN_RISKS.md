# ⚠️ Crystal Known Risks and Open Boundaries

**Status date:** 2026-08-08  
**Verified runtime checkpoint:** `f03e24c85922d0bb46d6d9dfee98338972135908`  
**Validated implementation head / CI:** `17ce10ffe12da93be50434c73d08f05a70a5922b` / `31224184351`

This register is an orientation layer. GitHub `main`, executable tests, exact CI, current issues and accepted ADRs remain authoritative.

## P1 — PostgreSQL/pgvector runtime remains absent (#332)

- SQLite is the verified local-first runtime profile.
- PostgreSQL/pgvector is a proposed optional institutional profile only.
- No driver, target schema, inactive importer, exact target-equivalence implementation, activation, cutover, rollback or dual-write exists.
- Backend reachability, package availability, profile editing or successful import must never cause automatic switching.
- Credentials, credential-bearing DSNs and secrets must not enter profiles, bundles, receipts, logs, issues or Notion.

## P1 — Current migration evidence is bounded local-first evidence

Issue #331 is implemented by PR #335. The production path now uses fixed cursor batches, disk-backed canonical edge ordering, same-descriptor hash-first parsing and disk-backed referential checks instead of complete datasets or global identifier sets in memory.

Remaining limits and risks:

- source and dataset files remain limited to 64 MiB;
- aggregate JSONL remains limited to 384 MiB;
- temporary-disk capacity is required and must be monitored;
- hard process or host interruption can still leave operating-system-managed temporary remnants for investigation;
- benchmark `31224005804` covers 1,025 and 8,193-record synthetic corpora only;
- benchmark evidence is not a production SLO, arbitrary-scale proof or institution-scale certification;
- increasing limits requires separate reproducible memory, disk, time, cleanup and adversarial evidence.

## P1 — Production identity, tenancy and distributed coordination remain external

- curator leases are process-local;
- there is no bundled production IdP;
- there is no complete multi-tenant isolation proof;
- TLS termination, network policy, credential rotation and distributed fencing remain deployment responsibilities;
- no distributed exactly-once behavior is claimed.

## P1 — Supply-chain hardening is incomplete

- the default runtime remains pure standard library;
- optional dependencies require explicit extras and version bounds;
- immutable action pinning, reviewed dependency constraints, checksums, SBOM and scheduled update policy remain future work;
- a green dependency audit does not establish full supply-chain assurance.

## P2 — Reader Core remains research, not runtime

Crystal does not yet implement a dedicated multi-pass Reader Core or Semantic Reading Layer. Any future implementation must preserve source spans, coverage and contradictions, remain upstream of Guardian/TruthGate and never become a second Canon owner.

## Claim and legal boundaries

- physical L3 is multi-status storage, not strict Canon;
- migration bundles and receipts are operational evidence, not claim evidence;
- retrieval or ANN quality cannot override exact-state mismatch;
- GDPR language means **GDPR-oriented technical controls**, not legal compliance or certification;
- no universal truth, zero hallucinations, AGI, consciousness or production certification is claimed;
- the project is submitted and under review; no grant award or budget change is claimed.

## Next actions

1. Implement #332 only as inactive PostgreSQL/pgvector import plus exact-state equivalence.
2. Review exact-vs-ANN evaluation separately.
3. Require explicit source/target fencing before any cutover phase.
4. Add rollback proof and server backup/restore/upgrade lifecycle in later reviewed phases.
5. Preserve GitHub/Notion synchronization and exact-head CI for every material boundary change.
