# 📌 Velantrim Crystal — Current Status

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./de/STATUS.md) · 🇫🇷 [Français](./fr/STATUS.md) · 🇪🇸 [Español](./es/STATUS.md) · 🇮🇹 [Italiano](./it/STATUS.md) · 🇷🇺 [Русский](./ru/STATUS.md) · 🇨🇳 [简体中文](./zh-CN/STATUS.md) · 🇸🇦 [العربية](./ar/STATUS.md) · 🇯🇵 [日本語](./ja/STATUS.md) · 🇮🇳 [हिन्दी](./hi/STATUS.md)

**Status date:** 2026-08-01  
**Verified runtime checkpoint:** `916097f` (`916097f049f2e71fa679571ac897e9d887957f4f`, merged PR #292)  
**Exact verification evidence:** [TEST_REPORT.md](../TEST_REPORT.md)  
**Machine-readable status:** [implementation-manifest.json](./status/implementation-manifest.json)

## Authority rule

```text
GitHub Crystal main = implementation truth
TEST_REPORT + manifest = exact verified evidence
Notion Crystal pages = synchronized strategy and grant map
Titan / Full Exo-Cortex = separate research track
```

A Notion page, translation, RFC, prototype or research branch is not a current
Crystal capability unless corresponding code and tests are merged into Crystal
`main`.

## Current verified baseline

```text
Python 3.11: 1780 passed / 12 skipped
Python 3.12: 1780 passed / 12 skipped
Failed:      0
Statements:  6484
Coverage:    100.00%
Mutation:    7/7 targeted Ring Zero mutants killed
```

The current repository topology contains **9 permanent CI jobs**:

1. `test (3.11)`;
2. `test (3.12)`;
3. `code-quality`;
4. `security`;
5. `docker-build`;
6. `eval-gate`;
7. `jsonl-integrity`;
8. `Ring Zero mutation gate`;
9. `docs-status`.

The ninth job validates consistency between the active README, this status page,
`TEST_REPORT.md`, `IMPLEMENTATION_STATUS.md` and the machine-readable manifest.

## Implemented trust-boundary hardening

### Unified public read-only query boundary

The public query surfaces now share the same zero-durable-mutation service:

```text
HTTP /ask and /receipt
CLI ask and receipt
MCP search
        ↓
core.query_pipeline
```

They do not create or update L0/L1 facts, transition ESM, write L3 graph objects,
operate the outbox, record episode links, initialize an unset embedding
fingerprint, store unknown candidates or mutate adaptive verification state.

`core.pipeline.run()` remains an explicit legacy/internal admission-capable
compatibility function, but public CLI query commands no longer call it.

### Non-configurable TruthGate invariant

The historical runtime bypass for the LLM-origin factual rule has been removed.
Environment values such as `ENABLE_TRUTH_POLICY=off`, `false`, `0` or `legacy` no
longer weaken the policy.

```text
LLM_OUTPUT + WORLD_FACT
        ↓
blocked from automatic VERIFIED admission
```

### Immutable read reconciliation

Read-time L3 content and deny-dominant L1 state are reconciled through a frozen,
slotted `TrustSnapshot` before a compatibility mapping reaches Guardian or
CanonicalView.

The snapshot preserves terminal-state and processing-restriction dominance,
records content-free conflict categories and treats malformed confidence as
unknown internally rather than silently converting it into trusted metadata.

### Ring Zero mutation gate

The targeted mutation gate executes seven declared semantic mutations covering:

- TruthGate threshold comparison;
- LLM-origin rejection;
- `VERIFIED` requirement;
- processing restriction;
- strict ESM allowlist;
- malformed-confidence conflict handling;
- Receipt digest verification.

All **7/7** declared mutants must be killed. Surviving mutants, source-fragment
drift, missing tests and pytest collection/internal errors fail the job.

## Public claim boundary

Crystal may be described as:

- local-first verifiable AI memory infrastructure;
- a source-, state- and provenance-oriented memory core;
- a system with explicit admission and strict read boundaries;
- a system with Guardian, TruthGate and CanonicalView where documented;
- a system with TRACE and replayable Receipts;
- a pure-stdlib default runtime with optional adapters and interfaces;
- an independently testable open-source research-grade baseline;
- a project with GDPR-relevant erasure and restriction mechanisms.

Crystal must not be described as:

- Titan or the Full Personal Exo-Cortex;
- an autonomous cognitive operating system;
- conscious, alive or biologically equivalent to a brain;
- a universal truth detector or hallucination-free system;
- legally GDPR-certified;
- security-certified;
- production multi-tenant ready without additional IAM and operational controls;
- dependent on a mandatory external model or cloud provider.

## Physical L3 and strict Canon

```text
Physical L3 graph ≠ strict Canon
```

The physical graph is multi-status memory. Strict Canon is a policy-allowed
projection that satisfies exact truth-status, ESM, provenance, confidence and
processing-restriction conditions. TruthGate controls admission; it does not
independently establish objective truth for every source statement.

## Current remaining engineering work

The next recommended packages remain separate changes:

1. **Contradiction decision contract** — typed reports and explicit
   coexist/supersede/contextualize/review outcomes.
2. **ESM transition specification** — one machine-checkable state-transition
   table and invariant checker.
3. **Performance history** — scheduled fixed-runner benchmark results and trend
   reporting rather than unstable PR latency thresholds.
4. **Advisory topic facets** — navigation-only multi-label metadata where topic
   score never influences truth or source authority.
5. **Roles and multi-curator hardening** — scoped authorization and accountable
   concurrent review workflows.

See [DOCUMENTATION_MAP.md](./DOCUMENTATION_MAP.md) and
[IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md).

## Grant status

The NLnet NGI0 Commons Fund proposal has been submitted and remains under review.
The repository does not claim that funding has been awarded.

```text
BASELINE TODAY
    +
MEASURABLE FUNDED DELTA
    =
INDEPENDENTLY VERIFIABLE DELIVERABLE
```

Already-merged work remains baseline and is not counted again as paid delivery.
Titan and broader cognitive research are not silently added to Crystal grant
scope.

- [Grant scope](./GRANT_NLNET_SCOPE.md)
- [Baseline/funded-delta matrix](./grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./grants/funding-use-plan.md)

## Reviewer path

1. [README](../README.md)
2. [Documentation map](./DOCUMENTATION_MAP.md)
3. [Reviewer guide](./REVIEWER_GUIDE.md)
4. [Reviewer demo](./REVIEWER_DEMO.md)
5. [Test report](../TEST_REPORT.md)
6. [Implementation status](./IMPLEMENTATION_STATUS.md)
7. [Architecture](./ARCHITECTURE.md)
8. [Grant scope](./GRANT_NLNET_SCOPE.md)

---

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./de/STATUS.md) · 🇫🇷 [Français](./fr/STATUS.md) · 🇪🇸 [Español](./es/STATUS.md) · 🇮🇹 [Italiano](./it/STATUS.md) · 🇷🇺 [Русский](./ru/STATUS.md) · 🇨🇳 [简体中文](./zh-CN/STATUS.md) · 🇸🇦 [العربية](./ar/STATUS.md) · 🇯🇵 [日本語](./ja/STATUS.md) · 🇮🇳 [हिन्दी](./hi/STATUS.md)
