# Crystal Reader Product Bridge v0.1

**Status:** IMPLEMENTED IN DRAFT PR · NOT MERGED  
**Scope:** pass-bounded foreground orchestration over existing RC-1..RC-3  
**Documentation impact:** `GITHUB_AND_NOTION`

## Purpose

Crystal already contains source-bound Reader sessions, structural maps, explicit multi-pass mechanics, proposition candidates, relation candidates, long-context working sets and cross-document candidate links. What it does not contain is one small foreground orchestration path that turns the RC-1..RC-3 primitives into a bounded product-style run.

Reader Product Bridge v0.1 closes only that orchestration gap.

```text
caller-provided source/version + structural map
                    ↓
             ReaderSession
                    ↓
          ReaderProductBridge
                    ↓
             BROAD_READ
                    ↓
        visible NEEDS_REVIEW gaps?
              /             \
            no               yes
            ↓                 ↓
        COMPLETE      one TARGETED_REREAD
                              ↓
                    unresolved gaps remain?
                       /             \
                     no               yes
                     ↓                 ↓
                 COMPLETE          DEGRADED
```

## Deliberate non-goals

v0.1 adds no:

- parser, chunker, OCR or PDF-layout engine;
- file ingestion path;
- LLM/model/provider integration;
- automatic proposition extraction or summarization;
- semantic/hybrid/vector retrieval;
- public CLI/API;
- persistence or Reader database;
- background worker, planner or autonomous retry loop;
- TruthGate, Guardian, ingest, memory or Canon write path;
- evidence admission or contradiction adjudication;
- PostgreSQL/pgvector activation;
- cross-project runtime dependency on Titan.

## Execution contract

The bridge receives an existing `ReaderSession`, an existing `DocumentStructuralMap`, and a caller-supplied `RegionExecutor`.

The executor is the only component allowed to claim that actual reading/processing happened. The bridge never converts scheduling into `PROCESSED` coverage by itself.

The run is pass-bounded to:

1. exactly one `BROAD_READ` pass over non-document structural nodes;
2. at most one `TARGETED_REREAD` pass over bridge-target nodes still marked `NEEDS_REVIEW`;
3. no recursive reread loop;
4. `COMPLETED` only when no session-visible `UNREAD` or `NEEDS_REVIEW` coverage remains;
5. otherwise `DEGRADED` with `reader_product_incomplete_after_bounded_reread`.

This v0.1 contract bounds orchestration depth, not total input size or executor cost. `DocumentStructuralMap` remains caller-supplied and does not impose a target-count or character budget, and `RegionExecutor` remains caller-supplied. A future product resource budget (for example max targets, max reread tasks or character ceilings) would be a separate explicitly reviewed stage; it is not implied by the word `bounded` here.

Existing RC-3 transition validation remains authoritative. Ambiguous or unsupported structure cannot be silently marked processed.

## Authority boundary

```text
scheduled region != processed region
processed coverage != comprehension proof
Reader result != evidence admission
Reader result != verified fact
Reader result != Canon
Reader completion != production authorization
```

The module imports no TruthGate, Guardian, memory, ingest, pipeline, embedding, LLM-router or remote-egress authority/runtime component.

## Relationship to Titan

Titan's Reader product path demonstrated the value of a small bounded orchestration bridge. Crystal does not copy Titan's implementation or types. This implementation reuses Crystal-native RC-1..RC-3 semantics and preserves Crystal's stricter coverage/version boundaries.

```text
cross-project pattern reuse != code/runtime/authority transfer
```

## Exit state for v0.1

If merged after review and CI, the truthful capability statement would be:

```text
bounded_reader_product_bridge_v0_1 = true
dedicated_reader_core = false
semantic_hybrid_reader_runtime = false
public_reader_cli = false
reader_model_provider_integration = false
```

A later stage may separately decide whether to add a local file-ingestion/CLI surface, an opt-in semantic executor, or explicit product resource budgets. This v0.1 does not authorize any of them.
