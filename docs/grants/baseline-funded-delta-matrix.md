# Crystal baseline → funded delta → acceptance matrix

**Status date:** 2026-08-12  
**Grant state:** submitted / under review / not awarded — **no award/budget change**.

Anything merged before an agreement is existing baseline and **cannot be counted again as future paid work**.

## Existing verified / pre-agreement baseline

| Area | Existing baseline | Authority/non-claim |
|---|---|---|
| Trust/evidence | Guardian, TruthGate, strict read projection, evidence/provenance | physical L3 != strict Canon |
| Query | HTTP/CLI/MCP read-only query pipeline | query != ingest |
| SQLite | ordinary active local-first + lifecycle/export | operation evidence != truth evidence |
| PostgreSQL target | inactive import/equivalence | target remains `active=false` |
| Reader RC-1 | source/session/provenance skeleton | no truth authority |
| Reader RC-2 | caller-supplied structural map | structure != truth |
| Reader RC-3 | explicit multi-pass ledger | pass completion != comprehension |
| Reader RC-4 | source-linked proposition candidates | `EXTRACTED_PROPOSITION != verified fact`; `Reader candidate != admitted evidence` |
| Reader RC-5 | same-session/same-version typed relation candidates | `contradiction candidate != confirmed contradiction` |

Machine Reader boundary:

```text
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
dedicated_reader_core                  = false
```

## Potential funded delta after RC-5

RC-6 is the currently authorized pre-agreement candidate under issue #369 / PR #370. Until merge it is not yet established merged baseline. Its acceptance boundary is deliberately narrow:

| Potential/current delta | Minimum independent acceptance evidence |
|---|---|
| RC-6 long-context strategy | deterministic same-session/same-version working-set contract + direct leaf provenance + tests + final exact-head CI + signed merge + post-merge CI; no comprehension/evidence/truth overclaim |
| RC-7 cross-document reading | **not started/not authorized**; exact cross-source provenance/identity rules + adversarial tests; similarity != identity |
| retrieval experiments | versioned corpus + measured thresholds; no authority from similarity alone |
| cutover/rollback | explicit fencing/receipts/crash tests |
| PostgreSQL lifecycle | backup/restore/upgrade/roles/observability evidence |
| release/audit hardening | reproducible artifacts, checksums, SBOM, independent findings |

RC-6 artifact boundaries:

```text
working-set coverage != comprehension proof
summary              != source text
summary              != evidence
summary              != verified fact
summary              != Canon admission
```

Reader work beyond RC-5 cannot silently gain evidence-admission, Canon/ESM, contradiction-resolution or planner authority. RC-6 also cannot add automatic summarization/model routing, parser/OCR, embeddings/ANN, RC-7 cross-document semantic identity, Reader persistence/API/worker or PostgreSQL activation.

If RC-6 merges before an agreement, the accounting boundary advances immediately:

```text
pre-agreement RC-0..RC-6 = existing baseline
future agreement          = only measurable delta after RC-6
```

The older phrase **after RC-5** remains useful for audit history because RC-6 was selected from that position; it does not mean merged RC-6 may later be rebilled.

Approximate €50,000 is planning only and does not represent an approved budget or payment commitment.
