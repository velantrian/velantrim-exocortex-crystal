<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Retained runtime baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

## ✅ Delivered Reader baseline through RC-5

RC-0 defines the normative Reader contract. RC-1 through RC-5 are merged bounded pre-admission layers:

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
```

### ✅ RC-1 — Minimal Evidence-Linked Reading Skeleton

Exact source/version identity, replayable locators, Reader sessions, fidelity, coverage, bookmarks/open loops and fail-visible stale/privacy semantics.

### ✅ RC-2 — Structural Document Map

Caller-supplied version-bound hierarchy/order with explicit `RECOVERED`, `AMBIGUOUS`, `UNSUPPORTED` state. No parser/OCR/layout authority.

### ✅ RC-3 — Explicit Multi-Pass Reading Mechanics

`ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK`, `TARGETED_REREAD`; explicit targets/outcomes/state; partial progress preservation; count-only telemetry.

### ✅ RC-4 — Source-Linked Proposition Extraction

Completed substantive RC-3 context may produce source-linked `EXTRACTED_PROPOSITION` candidates with attribution/category/negation/qualifiers and exact provenance.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate      != admitted evidence
```

### ✅ RC-5 — Exceptions / Contradiction Candidate Detection

`core/reader_relations.py` adds explicit PRE-ADMISSION relation registration over valid RC-4 candidates only:

- `POSSIBLE_CONTRADICTION`;
- `EXCEPTION`;
- `QUALIFICATION`;
- `TENSION`.

RC-5 is same-session/same-exact-source-version and within-document. It keeps exact candidate IDs, both-side provenance and explicit rationale. Symmetric relations canonicalize pair order; directional exception/qualification preserve order. Stale/mismatched/fabricated Reader context fails closed.

```text
contradiction candidate != confirmed contradiction
similarity              != identity
repetition              != corroboration
```

## 🚧 RC-6 — Bounded Long-Context Strategy — authorized / implementation in progress

Tracking issue: #369. Draft implementation PR: #370.

RC-6 is intentionally model-neutral and remains inside one OPEN ReaderSession / exact SourceVersion. The bounded design is:

```text
registered RC-4 proposition candidates
→ RC-2 structural order + stable candidate-ID tie-break
→ bounded rolling working sets
   ├─ max candidates per set
   ├─ max direct source locators per set
   ├─ candidate atomicity
   └─ optional RC-5 relation carry-through only when both sides are in-set
→ optional caller-supplied SUMMARY artifact
   └─ direct RC-4 leaf IDs + replayable source provenance retained
```

Primary non-equalities:

```text
working-set coverage != comprehension proof
summary              != source text
summary              != evidence
summary              != verified fact
summary              != Canon admission
```

RC-6 does not add automatic summarization, LLM/provider/model routing, token-context claims, parser/OCR, embeddings/ANN/vector DB, evidence admission, contradiction resolution, truth/Canon/ESM mutation, planner authority, Reader persistence/API/CLI/worker or PostgreSQL activation.

Machine truth after RC-6 implementation is represented as:

```text
reader_core_rc6_long_context_strategy = true
dedicated_reader_core                 = false
```

Final implementation truth is not established until exact-head CI, guarded merge, verified merge signature and exact post-merge push CI all succeed.

## ⏭️ RC-7 and later — separate authorization required

RC-6 does not automatically authorize RC-7.

```text
RC-6 long-context strategy
→ RC-7 cross-document reading
→ only then reassess semantic/vector retrieval needs
```

Cross-document relation identity must not be smuggled into RC-6. RC-7 must preserve exact cross-source provenance and treat similarity as a candidate signal rather than identity proof.

## ✅ Storage baseline remains unchanged

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL inactive import/equivalence
→ active=false
```

### Future storage work

- exact-vs-ANN evaluation with measured thresholds;
- explicit source/target fencing, cutover and rollback proof;
- PostgreSQL server lifecycle, least-privilege roles and observability;
- no reachability-based automatic backend selection.

## 🌍 Localization position during RC-6

English is source. RC-6 first advances the English public/machine surfaces and records an immutable source checkpoint. Russian Reader-dependent root + D1/D3/D4/D5 surfaces are then refreshed to that exact checkpoint. Eight other Reader-dependent locales remain rich `REFRESH_NEEDED` translations; D2 and Quick Start remain current across all nine locales because RC-6 does not change those contracts.

## Grant boundary

Anything merged before a grant agreement is existing baseline and cannot be counted again as future paid work. Reader RC-0 through RC-5 are already existing baseline. If RC-6 merges pre-agreement, RC-6 also becomes existing baseline.

```text
verified existing baseline
+
new measurable funded delta
=
independently verifiable public deliverable
```

No award/budget change is claimed. Approximate €50,000 remains planning only. Any potential funded Reader delta after a pre-agreement RC-6 merge must begin after RC-6.

## Related documents

- [Project, grant and governance overview](./docs/PROJECT_GRANT_AND_GOVERNANCE.md)
- [Grant scope](./docs/GRANT_NLNET_SCOPE.md)
- [Baseline-funded delta matrix](./docs/grants/baseline-funded-delta-matrix.md)
- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
- [Reader architecture contract](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
