# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-11  
**Retained verified runtime checkpoint:** `bbd816c` / PR #337  
**Machine-readable status:** [status/implementation-manifest.json](./status/implementation-manifest.json)

| Component | Status | Current boundary |
|---|---|---|
| Guardian / TruthGate / strict read projection | Implemented | Reader/storage artifacts cannot bypass authority |
| Read-only HTTP/CLI/MCP query boundary | Implemented | ordinary queries do not mutate Canon |
| SQLite backup/verify/inactive restore | Implemented and tested | restore is inactive and never admission |
| Bounded SQLite logical export/verify | Implemented and tested | backend-neutral verified bundle |
| PostgreSQL optional dependency/preflight | Implemented and tested | explicit extra, lazy load |
| Inactive PostgreSQL/pgvector import | Implemented and tested | target stays `active=false` |
| Exact target-state equivalence | Implemented and tested | operation evidence only |
| Active PostgreSQL runtime adapter | Not implemented | no normal PostgreSQL reads/writes |
| Automatic SQLite/PostgreSQL switching | Forbidden | availability/import success is not selection |
| Reader Core RC-0 architecture contract | Documented | normative authority/fidelity/coverage/privacy/non-claims contract |
| Reader Core RC-1 minimal skeleton | Implemented | `core/reader_core.py` |
| Reader Core RC-2 structural map | Implemented | `core/reader_structure.py` |
| Reader Core RC-3 multi-pass mechanics | Implemented | `core/reader_passes.py` |
| Reader Core RC-4 proposition extraction | Implemented pre-admission | `core/reader_extraction.py` |
| Reader Core RC-5 relation candidates | Implemented pre-admission | `core/reader_relations.py`; same-session/same-version explicit relation registry |
| Dedicated/full Semantic Reading runtime | Not implemented | `dedicated_reader_core=false` |

## Reader implementation chain

```text
RC-1 exact SourceVersion + provenance
↓
RC-2 version-bound structural regions
↓
RC-3 completed explicit pass targets + substantive coverage
↓
RC-4 registered EXTRACTED_PROPOSITION candidates
↓
RC-5 explicit relation candidates over exact RC-4 candidate IDs
```

### RC-4 input boundary

RC-4 validates a caller-supplied normalized proposition against a `COMPLETED` RC-3 pass whose declared target has both recorded and current matching `PROCESSED` or `REVISITED` coverage. It preserves source owner, presentation category, negation, qualifiers and primary/supporting replayable locators. `FACTUAL_ASSERTION` describes source presentation, not Crystal verification.

### RC-5 relation boundary

`ReaderRelationRegistry` is bound to one RC-4 `ReaderPropositionExtractor`, therefore one Reader session/source domain. It accepts only candidate IDs already registered by that extractor and re-validates that the session is OPEN, candidate session IDs match, every locator uses the same exact source version, and the candidate `SegmentCard` remains registered in the Reader session.

The minimal typed relation set is:

| Kind | Semantics | Direction |
|---|---|---|
| `POSSIBLE_CONTRADICTION` | explicit suspicion that two propositions may conflict | symmetric |
| `TENSION` | explicit tension without claiming contradiction | symmetric |
| `EXCEPTION` | right-hand proposition is registered as an exception to the left | directional |
| `QUALIFICATION` | right-hand proposition narrows/refines the left | directional |

Every relation keeps:

- explicit `relation_id` and `session_id`;
- both exact RC-4 `candidate_id` values;
- both pass IDs and structural node IDs;
- both primary locators and supporting locators;
- inherited exact source/version, restriction and sensitivity context;
- explicit non-empty rationale;
- count-by-kind telemetry only.

For symmetric kinds, candidate order is canonicalized deterministically and duplicate semantic re-registration fails closed. Directional exception/qualification ordering is preserved. No truth probability, confidence, evidence sufficiency, resolved flag or winner field exists on the RC-5 artifact.

## Authority isolation

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate      != admitted evidence
relation candidate    != admitted evidence
contradiction candidate != confirmed contradiction
```

RC-5 has no import from `core.evidence`, contradiction resolution modules, Guardian, TruthGate or ESM. It does not call `core.evidence.attach_evidence()`, write `evidence_spans`, mutate truth/Canon/ESM, promote confidence, choose a winner, create corroboration from repetition or enter an admission workflow.

RC-5 also does not add raw-text semantic comparison, automatic semantic equivalence, cross-document proposition identity, LLM/provider calls, parser/OCR/layout/multimodal processing, embeddings/ANN/vector DB, planner/research autonomy, public Reader API/CLI/worker, durable Reader persistence or PostgreSQL activation.

## Machine truth

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
dedicated_reader_core                  = false
```

Coverage, structure, pass, extraction and relation telemetry are process/count state only. None is a comprehension, truth, confidence or evidence-sufficiency score.

## Storage and grant boundaries

SQLite remains ordinary active local-first. PostgreSQL/pgvector remains an inactive target with `active=false`; RC-5 adds no schema migration or backend switching.

NLnet remains submitted / under review / not awarded. Approximate €50,000 is planning only and budget change is none. If RC-5 merges before an agreement, it is existing baseline and cannot later be presented as funded delta.

Crystal does not claim universal truth, zero hallucinations, AGI/consciousness, security/legal/GDPR certification, active PostgreSQL runtime or a dedicated/full autonomous Reader Core.
