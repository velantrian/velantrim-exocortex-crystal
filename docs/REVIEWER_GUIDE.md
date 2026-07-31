# Reviewer Guide — Velantrim ExoCortex (Crystal)

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](./fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](./es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](./it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](./ru/REVIEWER_GUIDE.md) · 🇨🇳 [简体中文](./zh-CN/REVIEWER_GUIDE.md)

> A fast, honest path for a reviewer to understand what Crystal is, verify it
> runs, and check its core epistemic guarantees. Reflects the audit-hardening
> work completed in this cycle (Tracks 1–3B).
>
> Status of this doc: docs-only. It points to the authoritative status pages and
> does not itself make new runtime claims.

---

## 1. What Crystal is

Crystal is the **public, minimal, verifiable memory core** of Velantrim:
local-first, source-grounded, auditable AI memory infrastructure.

- Local-first storage (SQLite/WAL by default; no cloud or external LLM required).
- Typed claims with a **TruthGate** as the only automatic entry into the L3 canon.
- **Trace / Receipt** — sealed, replayable provenance for answers.
- **Per-fact ProvenanceChain** — append-only, hash-chained lifecycle log.
- GDPR-oriented controls (erasure, restriction, record-of-processing, tamper-evident audit, PII redaction).
- Dependency-free runtime (`pip install .`); optional extras are opt-in.

## 2. What Crystal is *not*

Crystal makes **no** claim to be (see [`docs/STATUS.md`](./STATUS.md)):

- AGI, consciousness, an autonomous mind, or a biological-brain implementation;
- a "zero hallucinations" guarantee;
- a production-ready Titan console / Research PWA;
- NoeticCore / AttentionRouter / BICA as current runtime;
- Graphiti, Neo4j, OpenAI, or cloud LLMs as *mandatory* dependencies;
- a verified universal World Knowledge Core (graph entries are gated, not
  presumed-true canon);
- the full Personal Research Mode / Full Velantrim Exo-Cortex (tracked separately
  in Notion and local research builds) as current Crystal runtime or a grant
  deliverable. The bio-inspired modules that *are* in `core/` are tested baseline
  mechanisms / engineering metaphors, not biological cognition and not that full
  research mode.

Research-Mode / cognitive concepts are **research / RFC-level**, not Crystal
runtime. The canonical separation lives in
[`docs/STATUS.md`](./STATUS.md) and [`docs/IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md).

## 3. Current implementation status

Authoritative, per-component status (not roadmap ambition):

- [`docs/STATUS.md`](./STATUS.md) — high-level status + reality matrix
- [`docs/IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md) — detailed map
- [`docs/IMPLEMENTATION_REALITY_MATRIX.md`](./IMPLEMENTATION_REALITY_MATRIX.md) — track-by-track matrix
- [`../TEST_REPORT.md`](../TEST_REPORT.md) — audited test/coverage baseline

If a capability is not listed as `IMPLEMENTED` there, treat it as not implemented.

## 4. How to run the tests

CI enforces a **100% coverage gate**. From a clean clone:

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
python -m pytest                     # full suite, 100% coverage gate
```

See [`../TEST_REPORT.md`](../TEST_REPORT.md) for the canonical current baseline
(passing tests, skips, coverage). It and the README badge are the only places
that carry the exact count; this guide intentionally does not repeat the number
so it cannot drift.

## 5. How to run Crystal securely with Docker

Fail-closed by design (see [`../SECURITY.md`](../SECURITY.md) and
[`docs/security/DEPLOYMENT_SECURITY.md`](./security/DEPLOYMENT_SECURITY.md)):

```bash
# A token is REQUIRED — compose fails fast if it is unset.
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
docker compose up --build
curl http://127.0.0.1:8000/health     # {"status":"ok",...}
```

Security properties (Track 2, #170 + #171):

- **Fail-closed**: no default/fallback API token; without `VELANTRIM_API_TOKEN`
  the service refuses to start.
- **Loopback-only**: published on `127.0.0.1:8000:8000` (host loopback), never a
  routable interface by default. The image default host is `127.0.0.1`; compose
  binds the container to `0.0.0.0` *only behind* that loopback publish.
- **Non-root** `velantrim` user; **named-volume** data default (works out of the box).
- No secrets / local DBs / tests / dev extras baked into the image (`.[api]` only).

## 6. How to verify the core epistemic behaviour

All commands are stdlib-only CLI (`velantrim …` after `pip install .`):

**TruthGate (strict by default — Track 3A, #172).**
The strict policy is the production default; only `ENABLE_TRUTH_POLICY=off` opts
into the legacy bypass. Under the strict policy an `LLM_OUTPUT` cannot become a
`WORLD_FACT` on its own. This admission behaviour (on/off/unset) is pinned by
`tests/test_truth_gate.py` — that is the authoritative proof, not a CLI command.

```bash
velantrim invariant-check          # read-only at-rest scan of existing L3 facts
```

Note: `invariant-check` is a read-only at-rest scan of the current L3 state; it
does **not** call TruthGate or exercise `ENABLE_TRUTH_POLICY`, so it does not by
itself prove that an `LLM_OUTPUT` write is blocked (see `tests/test_truth_gate.py`
for that).

**Receipt (sealed, replayable provenance).**

```bash
velantrim receipt "your question"          # emit a tamper-evident receipt (JSON)
velantrim verify-receipt receipt.json      # replay it against the canon
velantrim verify-receipt receipt.json --strict-provenance
```

**Per-fact provenance & audit (Track 1, #168).**

```bash
velantrim history <fact_id>     # truth-maintenance history (supersede/contradict edges)
velantrim audit                 # tamper-evident audit log (erase/restrict/override)
velantrim audit-verify          # verify the audit hash chain + signatures
```

Note: `velantrim history` reads truth-maintenance graph edges via `fact_history`
(`core/reconcile.py`); it does **not** read the per-fact `ProvenanceChain`
(`core/provenance_chain.py`, wired into the erase path under #168).

**Write-path gate + accountable overrides (Track 3B, #175).**
Curator force-overrides of a blocked fact are recorded under
`review_force_approve` with a `gate_reason` (the specific reason the gate
blocked) — overrides are never silent. See `tests/test_write_path_gate.py`.

A hands-on, reproducible walkthrough lives in
[`docs/REVIEWER_DEMO.md`](./REVIEWER_DEMO.md) and [`docs/DEMO.md`](./DEMO.md).

## 7. Audit-hardening tracks merged this cycle

| Track | What | PR(s) |
|---|---|---|
| **1** | Per-fact, append-only, hash-chained `ProvenanceChain` (`core/provenance_chain.py`), wired into the erase path | #168 |
| **2** | Fail-closed Docker stack from scratch (`Dockerfile`, `docker-compose.yml`, `.dockerignore`) + review fixes | #170, #171 |
| **3A** | Strict TruthPolicy production default via `ENABLE_TRUTH_POLICY` (on/off/unset pinned) | #172 |
| **3B** | Write-path TruthGate behaviour pins + `gate_reason` in the force-approve audit | #175 |

Status pages were synced to match merged behaviour in #173 and #174.

## 8. Limitations and deferred work

Explicitly **not** done in this cycle (and not claimed):

- **ProvenanceChain lifecycle wiring** beyond the erase path — other state
  transitions are follow-up.
- **Knowledge-graph data verifier** — graph/autolinker data is labelled
  unverified-unless-sourced; a source/evidence-coverage verifier is future work.
- **Canonical write-path expansion** beyond the current gated paths.
- **RRF rank fusion** exists as a standalone helper, **not** wired into `retrieve()`.
- Research-Mode / Noetic / AttentionRouter / Graphiti / Titan console / PWA /
  BICA remain research / RFC-level, not runtime.

For the authoritative deferred list, see
[`docs/security/AUDIT_RESPONSE_2026_06_17.md`](./security/AUDIT_RESPONSE_2026_06_17.md)
and [`docs/STATUS.md`](./STATUS.md).

---

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](./fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](./es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](./it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](./ru/REVIEWER_GUIDE.md) · 🇨🇳 [简体中文](./zh-CN/REVIEWER_GUIDE.md)