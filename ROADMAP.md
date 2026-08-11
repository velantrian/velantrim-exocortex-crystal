<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Retained runtime baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

## ✅ Delivered Reader baseline through RC-5

RC-0 defines the normative Reader contract. RC-1 through RC-5 are bounded pre-admission layers:

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
dedicated_reader_core                  = false
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

No contradiction resolution, winner selection, evidence admission, truth/Canon/ESM mutation, confidence promotion, LLM/provider, parser/OCR, embeddings/ANN, public Reader API/worker, Reader DB migration or PostgreSQL activation was added.

## ⏭️ Later Reader phases — separate authorization required

RC-5 completion does not automatically authorize the next phase.

```text
RC-6 long-context strategy
→ RC-7 cross-document reading
→ only then reassess semantic/vector retrieval needs
```

Cross-document relation identity must not be smuggled into RC-5. Any later stage must preserve the Reader authority firewall and existing admission path.

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

## ✅ Localization position

English is source. Russian Reader-dependent public/detail documentation is current against the immutable RC-5 English checkpoint recorded in the translation ledger. Eight other Reader-dependent locales remain `REFRESH_NEEDED` with rich translations preserved. D2 and Quick Start remain current in all nine locales.

## Grant boundary

Anything merged before a grant agreement is existing baseline and cannot be counted again as future paid work. Reader RC-0/RC-1/RC-2/RC-3/RC-4/RC-5, when merged pre-agreement, are therefore baseline.

```text
verified existing baseline
+
new measurable funded delta
=
independently verifiable public deliverable
```

No award/budget change is claimed. Approximate €50,000 remains planning only. Potential funded delta after RC-5 must be genuinely new work beyond the merged baseline.

## Related documents

- [Project, grant and governance overview](./docs/PROJECT_GRANT_AND_GOVERNANCE.md)
- [Grant scope](./docs/GRANT_NLNET_SCOPE.md)
- [Baseline-funded delta matrix](./docs/grants/baseline-funded-delta-matrix.md)
- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
- [Reader architecture contract](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
