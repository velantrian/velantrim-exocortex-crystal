# Velantrim Crystal — Reviewer Checkpoint after Audit Hardening

> **Status of this doc:** docs-only checkpoint. It summarizes work already
> merged to `main`; it does not itself implement, propose new runtime
> behaviour, or supersede `docs/STATUS.md` / `TEST_REPORT.md` as the
> authoritative status pages — see those for the live source of truth if
> this checkpoint ages.
>
> **As of:** `main` at commit `4f4d8b0`, July 2026.

---

## 1. Executive summary

- Crystal is a **local-first, verifiable memory infrastructure for AI
  systems**, designed to separate stored, evidence-backed knowledge from
  generated language.
- It is **not a chatbot** and **not simple RAG** — retrieval feeds a gated
  admission path (TruthGate), not a direct answer.
- It makes **no claim** to be an AGI, a digital mind, or conscious.
- The **graph/canon is the truth boundary, by design**: only the
  `VERIFIED`, trace-valid subgraph is meant to count as canon; the physical
  graph may hold other epistemic/truth states (pending, `USER_CLAIMED`,
  hypothetical, subjective) alongside it. **This separation is not yet a
  read-time filter today** — `core.pipeline.retrieve()` reads L3 by
  similarity and does not filter on `truth_status == VERIFIED` or trace
  validity, so a `USER_CLAIMED` fact is retrievable, not only a `VERIFIED`
  one. Closing that gap with a trusted-only read projection is exactly
  what CanonicalView (section 3, RFC-only) proposes.
- The **LLM is an optional speech layer** — it can phrase an answer from
  admitted facts, but it is never itself a source of truth.
- **TruthGate, Trace/Receipt, and per-fact provenance** enforce epistemic
  discipline: what enters canon, and how a caller can verify why.
- The cycle summarized here improved **correctness** (8 audit-confirmed
  bugs fixed across two PRs, plus 2 more caught and fixed via review on
  those same PRs), **documentation clarity**
  (contradiction/immune-layer behaviour documented, a read-path RFC added),
  and **benchmark visibility** (a real, honest retrieval-latency baseline
  where there was previously none).
- This checkpoint is written to be **reviewer-safe**: it names what changed
  precisely, marks proposals as proposals, and does not round up.

## 2. What changed in the completed cycle

| PR | Area | Result | Runtime impact |
|---|---|---|---|
| [#206](https://github.com/velantrian/velantrim-exocortex-crystal/pull/206) | Audit hardening | Ring Zero sync guards, HTTP API token coverage extended to `/ingest` and other endpoints, ingest path sandboxing, RRF wired into `retrieve()`, force-override metadata | Yes — merged runtime hardening |
| [#216](https://github.com/velantrian/velantrim-exocortex-crystal/pull/216) | P0 integrity follow-up | Fixed 3 audit-confirmed bugs: `store_fact()` L0-cache poisoning on upsert, a write-lock race in the audit/provenance append-only logs, an import-session bug that let a duplicate-only session erase a fact it never created | Yes — correctness fixes |
| [#217](https://github.com/velantrian/velantrim-exocortex-crystal/pull/217) | Status sync | Synced `docs/STATUS.md` test baseline and PR #216 record; corrected a stale PR #202 status line | No — docs-only |
| [#221](https://github.com/velantrian/velantrim-exocortex-crystal/pull/221) | Contradiction / immune-layer docs | Added `docs/CONTRADICTION_POLICY.md` and `docs/IMMUNE_LAYER.md`, documenting implemented behaviour, current limitations, and the safe conflict-handling policy for `core/contradiction.py`, `core/reconcile.py`, and `core/immune.py` | No — docs-only |
| [#222](https://github.com/velantrian/velantrim-exocortex-crystal/pull/222) | Correctness hardening | Fixed 5 more small, independent bugs: `truth_gate()`'s `KeyError` on missing confidence, `volition.write_voluntary()`'s implicit `source_status`, `erase_fact()` fabricating tombstones for facts that never existed (plus a follow-up fix for an L3-only orphan case), a raw traceback in the `retrieval-config-set` CLI, and a PII false-positive on ISO dates | Yes — correctness fixes |
| [#223](https://github.com/velantrian/velantrim-exocortex-crystal/pull/223) | Status sync | Synced `docs/STATUS.md`/`TEST_REPORT.md`/`README.md` test baseline after #222 | No — docs-only |
| [#224](https://github.com/velantrian/velantrim-exocortex-crystal/pull/224) | CanonicalView RFC (issue #220) | Specifies a proposed read-path contract distinguishing the physical L3 graph from a trusted-only, `VERIFIED` + trace-valid read projection | **No — RFC-only, not implemented.** No code, CLI flag, or API parameter exists for it |
| [#225](https://github.com/velantrian/velantrim-exocortex-crystal/pull/225) | L3 retrieval benchmark (issue #218) | Adds a dependency-free smoke benchmark and a real local baseline for `core.l3_graph`'s SQLite-backend retrieval latency | **No — benchmark/report only.** Measures current behaviour; does not change or optimize it |

## 3. Current implementation reality

| Capability | Status |
|---|---|
| TruthGate write boundary | **Implemented** |
| Trace / Receipt discipline | **Implemented** |
| GDPR erasure / restriction paths | **Implemented, within project scope** (see Non-goals — not a legal certification) |
| Contradiction policy | **Documented** (`docs/CONTRADICTION_POLICY.md`) — detection and safe-surfacing behaviour described; a persistent "contested" marker and a curator-facing resolution command are noted as future work, not yet built |
| Immune layer | **Documented** (`docs/IMMUNE_LAYER.md`) — threat-memory screening and advisory/strict contradiction handling described as implemented |
| CanonicalView | **RFC-only, not implemented** (`docs/CANONICAL_VIEW_RFC.md`, issue #220) |
| L3 retrieval benchmark | **Benchmark baseline exists** (`docs/benchmarks/L3_RETRIEVAL_SCALE.md`, issue #218) |
| L3 retrieval optimization | **Not implemented** — the benchmark measures current behaviour, including an observed near-linear latency scaling characteristic; no algorithm change has been made |
| Property-based invariant suite | **Future work** — not started |

## 4. Current verified baseline

**1307 passed / 12 skipped / 100% coverage.**

This is the current repository test baseline as of this checkpoint (`main`
at `4f4d8b0`), reproducible via:

```bash
pytest tests/ --cov=. --cov-fail-under=100 -q
```

See [`TEST_REPORT.md`](../TEST_REPORT.md) for the authoritative, exact
count — that file and the `README.md` badge are the only places that carry
it, precisely so it cannot silently drift out of sync with this checkpoint
or any other document.

## 5. Benchmark baseline summary

Issue #218 added a dependency-free retrieval-scale smoke benchmark:

- Script: [`scripts/bench_l3_retrieval.py`](../scripts/bench_l3_retrieval.py).
- Report: [`docs/benchmarks/L3_RETRIEVAL_SCALE.md`](./benchmarks/L3_RETRIEVAL_SCALE.md).
- Measures `core.l3_graph`'s **SQLite backend** `vector_search()` latency
  **directly** — not the full retrieval pipeline, not Guardian/TruthGate,
  not the optional LadybugDB/Neo4j backends.
- Uses a **synthetic, deterministic corpus** (fixed seed, predictable claim
  text) — no network, no external fixture file.
- Documented local baseline at **100 / 1,000 / 10,000 facts**; **30,000 is
  opt-in** and was not run for the documented baseline (10,000 alone took
  ~8.5 minutes in the sandboxed container used to measure it).
- The baseline showed **near-linear latency scaling** with corpus size in
  that sandbox, traced in the report to a specific, disclosed mechanism:
  `vector_search()` issues a separate point-query for every candidate that
  clears a similarity threshold, not only a single scan.
- **This is a local smoke baseline, not a production performance
  guarantee.** Numbers depend on hardware, Python version, filesystem, and
  machine load.

**The benchmark exposes current retrieval behaviour; it does not optimize
it.** No retrieval algorithm, schema, or TruthGate change was made as part
of this work.

## 6. Why this matters for reviewers

- **Implemented vs. proposed is now explicit**, not left to be inferred: a
  reviewer can check section 3 (or `docs/STATUS.md`) rather than guess
  whether `trusted_only` reads or L3 performance tuning already exist.
- **The benchmark gives an honest performance baseline** — including a
  disclosed scaling characteristic — instead of an unverified performance
  claim or silence on the topic.
- **The CanonicalView RFC prevents a specific, real confusion**: that
  "the L3 graph contains it" and "it is trusted canon" are not the same
  claim, before any code makes that distinction load-bearing.
- **The contradiction/immune-layer docs make safety boundaries legible**:
  what is detected, what is not, and — importantly — that today's
  contradiction handling is advisory-surfacing, not silent
  auto-resolution, with the exact code paths cited.
- **The correctness-hardening PRs (#216, #222) reduced audit-discovered
  failure modes** in the integrity/erasure/audit-log/PII paths, each with
  a regression test that failed before its fix.
- **Documentation now separates "what exists" from "what is planned"**
  more consistently across `docs/STATUS.md`, the two new policy docs, the
  RFC, and the benchmark report, rather than in one file alone.

## 7. Remaining roadmap

1. **CanonicalView implementation** — only after the RFC (#220) is reviewed
   and its open questions (default conflict behaviour, mode-selection
   surface) are answered.
2. **L3 retrieval optimization** — informed by the benchmark baseline
   (#218), not started yet.
3. **Property/invariant test suite** — a stronger correctness-proof surface
   beyond example-based tests.
4. **Reviewer smoke guide** — an easier, more guided path for an external
   party to reproduce the claims in this checkpoint themselves.
5. **Grant / SOTA narrative** — a public explanation and comparison,
   building on `docs/COMPARISON.md` and the grant-facing docs already in
   `docs/grants/`.

None of these is started by this checkpoint document.

## 8. Non-goals

This checkpoint does not claim, and no document it summarizes claims:

- legal certification of any kind;
- full GDPR compliance certification — the project describes its controls
  as **GDPR-oriented**, not GDPR-certified;
- EU AI Act compliance;
- a "zero hallucinations" guarantee;
- AGI;
- consciousness or a digital mind;
- a replacement for human judgment or human curator review;
- a production-scale performance guarantee (see section 5 — the benchmark
  is a local smoke baseline).

## 9. Suggested reviewer quote

> Velantrim Crystal treats LLM output as candidate speech, not truth. Its
> truth boundary is the verified graph/canon plus traceable evidence, with
> TruthGate and provenance controls mediating what can become trusted
> memory.

---

*This checkpoint reflects PRs #206, #216, #217, #221, #222, #223, #224, and
#225. For anything not covered here, or if this document appears to
disagree with a more recent state of `main`, `docs/STATUS.md` and
`TEST_REPORT.md` are the authoritative sources.*
