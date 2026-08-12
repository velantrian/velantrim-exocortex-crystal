# Reader Core RC-7 — Bounded Cross-Document Candidate Links

**Status:** implementation/test milestone tracked by issue #371 / PR #372  
**Normative parent:** [Reader Core Architecture](./READER_CORE_ARCHITECTURE.md)

## Purpose

RC-7 adds an auditable cross-document comparison layer without turning comparison into epistemic admission. It records explicit caller-supplied candidate links between current RC-4 proposition candidates from different document identities and preserves exact provenance on both sides.

## Inputs

`ReaderCrossDocumentRegistry` is constructed from explicit `ReaderPropositionExtractor` instances. It requires:

- at least two extractors and no more than 32;
- unique OPEN Reader session IDs;
- at least two distinct `document_id` values;
- current registered RC-4 `EXTRACTED_PROPOSITION` candidates only.

Every registration revalidates candidate/session/source/pass/structure/coverage/card state before acceptance.

## Candidate link vocabulary

```text
SUPPORTS
CONTRADICTS
ELABORATES
REFERENCES
DEFINES
EXAMPLE_OF
PREREQUISITE_FOR
SAME_TOPIC
POSSIBLE_SAME_CLAIM
```

Symmetric candidates:

```text
CONTRADICTS
SAME_TOPIC
POSSIBLE_SAME_CLAIM
```

They canonicalize side order using source document, source URI, source SHA-256, session ID and candidate ID. All other kinds are directional and preserve caller-declared left/right meaning.

## Exact provenance snapshot

Each link side stores:

```text
session_id
candidate_id
pass_id
node_ids
SourceVersion(document_id + source_uri + SHA-256 + privacy binding)
primary SourceLocator
supporting SourceLocator values
```

RC-7 rejects same-document links and mismatched source/privacy provenance. It also rejects duplicate semantic link candidates rather than interpreting repetition as corroboration.

## Inspection basis

Optional caller-supplied inspection metadata may say why a human/system chose to compare the candidates:

```text
EXPLICIT_SOURCE_REFERENCE
CALLER_COMPARISON
LEXICAL_SIMILARITY_SIGNAL
SHARED_TOPIC_SIGNAL
OTHER
```

This field is descriptive only. There is no similarity score, identity probability, confidence promotion or evidence-sufficiency field.

## Authority firewall

```text
cross-document link       != Canon relation
cross-document support    != admitted evidence
cross-document contradiction candidate != confirmed contradiction
same-topic                != same proposition
possible-same-claim       != claim identity
similarity signal         != identity proof
repetition across sources != corroboration
```

RC-7 does not:

- call `core.evidence.attach_evidence()`;
- mutate truth status, ESM or strict Canon;
- bypass Guardian or TruthGate;
- resolve contradictions or choose a winner;
- perform automatic semantic matching, entity resolution or deduplication;
- use embeddings, ANN or vector databases;
- call an LLM/provider or parse/OCR documents;
- create a Reader database/API/CLI/background worker;
- activate PostgreSQL or automatic backend switching;
- create planner/autonomous-research/belief-update authority.

## Privacy

Each side retains its exact source restriction/sensitivity metadata. `restricted` is conservatively true when either side is restricted; sensitivity labels remain visible as a unique ordered tuple rather than being collapsed into a confidence/permission score.

## Telemetry

Telemetry is count-only:

- total links;
- restricted link count;
- counts by link kind;
- counts by inspection basis.

No telemetry field means comprehension, truth, confidence, identity, corroboration or admission.

## Verification

The first runtime/test commit `b75811e09323adbe2c74184ae0470dfb703fcf4c` passed exact-head CI `31568205231` 9/9. That is pre-merge evidence only. Final RC-7 implementation truth requires final exact-head CI, guarded merge from the exact validated head, verified merge signature and exact post-merge push CI.
