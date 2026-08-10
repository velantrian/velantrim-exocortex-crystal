# Reader Core RC-0 Architecture Contract

**Status:** architecture contract only  
**Runtime status:** `NOT_IMPLEMENTED`  
**Tracking issue:** #355  
**Scope:** Crystal-only, docs-only architecture baseline  
**Machine-readable implementation status:** `docs/status/implementation-manifest.json` remains `dedicated_reader_core=false`

Reader Core RC-0 defines how Crystal may perform attentive, source-grounded reading of long documents without creating a second truth authority. It is a contract for a future implementation, not evidence that a Reader Core runtime, parser engine, semantic segmenter, model integration, storage schema, API, CLI, or background worker exists today.

## 1. Purpose

Crystal already has source/document identity, exact source-span evidence, import/review flows, admission controls, multi-status storage and strict read projections. The missing architectural capability is a dedicated reading layer that can preserve what was read, what remains unread, what needs re-reading, which source passages support an observation, and which ambiguities or contradictions remain unresolved across a long source.

Reader Core exists to make long-document reading explicit and auditable rather than reducing it to:

```text
split text
→ embeddings
→ top-k retrieval
```

Its purpose is attentive source reading for books, articles, research papers, documents, long dialogues and large textual corpora while preserving Crystal's existing authority boundaries.

## 2. Non-goals

RC-0 does **not** implement or claim:

- a Reader Core runtime or Semantic Reading runtime;
- a parser engine, semantic chunker or new segmentation runtime;
- OCR or multimodal extraction;
- embeddings, ANN, a vector database or a retrieval redesign;
- a new database table, index, migration or storage authority;
- a new public API, CLI command or background worker;
- active PostgreSQL runtime or automatic backend switching;
- a planner, autonomous research authority or belief-updating authority;
- human-level reading, perfect comprehension, zero hallucinations or arbitrary-book understanding;
- security, GDPR, production or native-speaker certification;
- integration with other Velantrim repositories.

RC-0 also does not redefine Guardian, TruthGate, Canon, contradiction resolution, TRACE, Receipt, evidence, query, ingest or storage contracts.

## 3. Architectural position

Reader Core is conceptually **upstream of epistemic admission** and downstream of source identity/provenance. Its outputs are source-linked reader artifacts and candidates, not trusted facts.

```text
Source / Document
        │
        ▼
Document identity + version/hash + exact source-span addressing
        │
        ▼
Structural map / reading-address space
        │
        ▼
┌──────────────────────────────────────┐
│              Reader Core             │
│                                      │
│  multi-pass reading                  │
│  coverage tracking                   │
│  segment understanding               │
│  bookmarks / re-read needs           │
│  exceptions / scope qualifiers       │
│  contradiction candidates            │
│  importance signals                  │
│  cross-reference candidates          │
│  unresolved questions                │
└──────────────────────────────────────┘
        │
        ▼
Evidence-linked Reader Artifacts / candidates
        │
        ▼
Existing explicit ingest / review / evidence path
        │
        ▼
Guardian / Immune safety-policy boundary
        │
        ▼
TruthGate
        │
        ▼
Operational state + physical multi-status L3
        │
        ▼
TrustSnapshot / CanonicalView strict read projection
```

This diagram defines **authority placement**, not a claim that the future implementation must be one literal middleware call immediately before TruthGate. A future implementation may use several services or passes, but no path from Reader Core may bypass the existing admission boundary.

## 4. Authority boundaries

The following invariants are normative:

```text
source text                  != fact
segment                      != claim
summary                      != evidence
importance                   != truth
retrieval score              != authority
Reader observation           != Canon admission
contradiction candidate      != confirmed contradiction
cross-document similarity    != identity
model interpretation         != source truth
coverage                     != comprehension proof
repetition                   != corroboration
```

Reader Core **MAY** detect, structure, annotate, compare, summarize and propose candidates. It **MUST NOT**:

- set, promote or otherwise mutate `truth_status` or ESM authority;
- write directly into strict Canon or bypass normal write-side admission;
- bypass Guardian, Immune policy checks, TruthGate or existing curator-controlled exception paths;
- present a summary or interpretation as if it were the source text;
- treat a generated explanation as independent evidence;
- hide unread, failed or stale regions of a document;
- present partial reading as full-document understanding;
- automatically resolve a contradiction or select a winning claim;
- infer claim identity from semantic similarity alone;
- create planner authority or autonomous belief-update authority;
- lower evidence requirements because an item is important, frequent or relevant.

These boundaries align with Crystal's existing separation of physical storage, strict Canon, retrieval ranking, model output and epistemic admission.

## 5. Reader Session

A **Reader Session** is one bounded reading attempt over one identified source version for a declared objective. It is an audit/replay unit, not a truth unit.

A future implementation must be able to represent, semantically, at least:

- source/document identity;
- source version or content hash;
- reading objective or question set;
- session start and completion/interruption state;
- passes attempted and passes completed;
- processed coverage and regions requiring review;
- unresolved sections/references/questions;
- failure or degraded state, when applicable;
- links to reader artifacts produced by the session.

RC-0 intentionally does not prescribe one database schema or one serialization format. The semantics are mandatory; the storage representation is an RC-1+ implementation decision.

A session against one source version must never be silently reused as proof of coverage for a different content hash.

## 6. Document Structural Map

Reader Core must address a document as a structure, not only as an undifferentiated token stream. The conceptual structural map may represent, when present and recoverable:

- document;
- section and subsection;
- paragraph;
- dialogue turn / speaker turn;
- list and list item;
- table and table region;
- code block;
- quotation;
- footnote / endnote / reference;
- figure/caption metadata **when already available from the source representation**;
- explicit structural boundaries and ordering relationships.

Structural identity must remain anchored to the document version and to source-span addressing wherever exact spans are available.

RC-0 does not claim OCR, image understanding, PDF-layout reconstruction or multimodal parsing. Unsupported or ambiguous structure must remain explicit rather than being invented.

## 7. Segment Card

A **Segment Card** is a source-linked reader artifact describing one bounded part of a document. It is a working observation, not a Canon fact.

A future Segment Card should be able to carry, as applicable:

- stable segment identity within a document version;
- document identity and version/hash;
- exact source span or replayable structural location;
- structural position and neighboring context;
- concise local meaning;
- entities/topics mentioned;
- propositions or claims mentioned by the source;
- evidence/reference pointers present in the source;
- uncertainty and ambiguity;
- questions raised;
- exceptions, counterpoints and contradiction candidates;
- importance/significance signals;
- links to bookmarks and cross-reference candidates;
- source-fidelity class for each meaningful derived statement.

A Segment Card must not silently collapse quoted speech, author opinion, hypothesis, example and factual assertion into one epistemic category.

```text
Segment Card != KnowledgeUnit
Segment Card != verified fact
Segment Card != Canon admission
```

If a meaningful Segment Card artifact cannot resolve back to a source span or an explicitly documented structural locator, it must be treated as invalid/degraded for evidence-linked use and marked for review rather than promoted by convenience.

## 8. Coverage Map

A **Coverage Map** answers: *what did this reading process actually touch, and what remains unresolved?*

RC-0 defines the following conceptual states:

| State | Meaning |
|---|---|
| `UNREAD` | No reader pass has semantically processed this region. |
| `SEEN` | The region was encountered for orientation/structure, but not substantively processed for the reading objective. |
| `PROCESSED` | The region received substantive reading for the current objective. |
| `REVISITED` | The region received a substantive re-read because of focus, ambiguity, cross-checking or new context. |
| `NEEDS_REVIEW` | The current reading state is insufficient or unsafe to rely on because of ambiguity, failure, staleness, truncation, unsupported structure or another explicit reason. |

`NEEDS_REVIEW` is not a claim of deeper processing than `REVISITED`; it is a fail-visible condition. A future schema may model it as a state or an orthogonal blocking flag, provided the semantics remain explicit.

Coverage rules:

- coverage must be version-specific;
- coverage must preserve gaps rather than infer them away;
- a changed source version invalidates affected coverage until re-read;
- `SEEN` must not be reported as `PROCESSED`;
- aggregate coverage must be derivable from lower-level regions rather than fabricated from a summary;
- a full-document reading claim must expose remaining `UNREAD`/`NEEDS_REVIEW` regions and the objective under which reading occurred.

Most importantly:

```text
coverage != comprehension proof
100% processed spans != guaranteed correct interpretation
```

## 9. Multi-pass reading

Reader Core uses a **multi-pass strategy** as a conceptual reading pattern, not as a fixed number of model calls.

A compatible implementation may use passes such as:

1. **Orientation** — identify document identity, metadata, high-level structure, size, table of contents and structural map.
2. **Broad read** — establish section-level content and major lines of argument without pretending all details are resolved.
3. **Focused read** — revisit definitions, central arguments, evidence-bearing spans, exceptions, qualifications and high-importance regions.
4. **Cross-check** — compare earlier and later passages, references, negations, exceptions, contradiction candidates and unresolved questions.
5. **Targeted re-read** — return to selected regions because of a query, doubt, source change, cross-document comparison or missing context.

An implementation may merge, repeat or skip pass types when justified by the objective and source structure. It must record what it actually did rather than pretending a fixed ritual guarantees comprehension.

The architecture must not require a particular LLM, provider, model size, context window, embedding model or vector database.

## 10. Reader Bookmarks

A **Reader Bookmark** is a replayable, source-linked marker that records why a region deserves future attention.

Every meaningful bookmark must include or resolve to:

- the document identity and version/hash;
- a source span or structural location;
- a reason;
- the session or operation that created it, where available.

Typical reasons include:

- central thesis;
- definition;
- start/end of an argument;
- evidence-bearing passage;
- exception or scope limitation;
- warning or prerequisite;
- contradiction candidate;
- unresolved reference;
- re-read required.

Bookmarks are attention/replay artifacts only:

```text
bookmark != truth claim
bookmark priority != confidence
```

## 11. Exceptions and edge cases

Reader Core must preserve qualifiers that ordinary summaries often erase. At minimum it must be able to represent:

- "usually X, except Y" constructions;
- explicit author caveats and scope limits;
- negation;
- conditional and hypothetical examples;
- quotations of another person's position;
- disagreement reported by the author without endorsement;
- temporal qualifications and potentially outdated claims;
- uncertainty expressed by the author;
- exceptions tied to a particular population, jurisdiction, version or context.

A reader artifact must preserve the source speaker/owner of a proposition where that distinction matters.

The system must not transform:

```text
"in some cases X"
```

into:

```text
"X always"
```

merely to produce a shorter summary.

## 12. Contradiction candidates

Reader Core may identify possible tensions:

```text
same document:
Section A → X
Section F → not-X

cross-document:
Source A → X
Source B → Y
```

Its output is only a **contradiction candidate** that links the relevant source spans/propositions and explains the reason for suspicion.

Reader Core must not automatically:

- create a resolved contradiction;
- mark either side false;
- choose a winner;
- mutate existing claim state;
- replace Crystal's implemented contradiction classifier, `ContradictionReport` or curator decision contract.

When a reader-originated candidate is to become part of Crystal's executable contradiction workflow, the relevant propositions must first pass the existing source/evidence/admission path. Existing contradiction machinery then retains its own conservative detection limits and explicit resolution authority.

```text
Reader contradiction candidate
        !=
ContradictionReport resolution
```

## 13. Importance / significance

Reader Core may estimate **reading importance** to prioritize attention and re-reading. Useful categories include:

- central thesis;
- definition;
- causal explanation;
- evidence;
- exception;
- decision;
- warning;
- prerequisite;
- repeated concept;
- cross-reference.

The signal may be categorical or ranked in a future implementation, but it is never epistemic authority:

```text
importance != confidence
importance != truth
importance != evidence sufficiency
importance != authority
```

Reader importance may influence reading order or review priority. It must not directly set claim `significance`, `confidence`, `truth_status` or ESM state outside the existing contracts that own those fields.

## 14. Cross-document links

Reader Core may propose source-linked relationships between artifacts from different documents, including:

- `supports`;
- `contradicts`;
- `elaborates`;
- `references`;
- `defines`;
- `example-of`;
- `prerequisite-for`;
- `same-topic`;
- `possible-same-claim`.

These are **candidate semantic links**. A similarity score may motivate inspection but cannot prove identity or authority.

```text
similar text != same claim
same topic != same proposition
cross-document link != Canon relation
```

Any durable authoritative relation must use the existing admitted data path appropriate to that relation.

## 15. Reader Questions / Open Loops

Attentive reading records not only what appears to have been learned, but also what remains unresolved.

Reader Core must be able to preserve open loops such as:

- unclear or ambiguous passages;
- missing context;
- unresolved references/citations;
- terms requiring definition;
- claims that need another source;
- contradictions requiring later resolution;
- structural regions requiring re-read;
- incomplete coverage;
- questions created by one pass for a later pass.

An open loop may schedule or motivate a future targeted re-read, but it is not planner authority and does not authorize writes to Canon.

## 16. Long-context strategy

Reader Core must support sources larger than any one model or processor working context through architecture, not by assuming a future infinite context window.

Permitted strategies include:

- hierarchical document reading;
- segment-level source-linked artifacts;
- rolling working sets;
- structural/source-span addressing;
- bookmarks and open loops;
- selective re-reading;
- progressive synthesis from lower-level artifacts;
- regeneration/checking of summaries against their supporting spans.

The contract is neutral with respect to OpenAI, Anthropic, Qwen or other providers; specific model context sizes; embeddings; and specific vector databases.

Progressive synthesis must not turn an intermediate summary into a provenance dead-end. Higher-level synthesis must retain a path back to the lower-level artifacts and ultimately to source spans.

## 17. Source fidelity classes

Reader Core must keep the source and its derived representations distinguishable. A future implementation must preserve the semantic equivalent of these classes:

| Class | Meaning | Authority boundary |
|---|---|---|
| `DIRECT_SOURCE_OBSERVATION` | Directly observable source/structure or a source statement anchored to the exact span. | The source says/shows this; that alone does not make it a verified world fact. |
| `EXTRACTED_PROPOSITION` | A normalized proposition extracted from one or more source spans. | Candidate representation; not automatically evidence-admitted. |
| `READER_INTERPRETATION` | Reader's interpretation of what the author likely means. | Must remain labeled as interpretation with uncertainty where applicable. |
| `SUMMARY` | Compressed representation of a larger region. | Never substitutes for the source span as evidence. |
| `INFERENCE` | A conclusion derived from multiple statements/spans or contextual reasoning. | Must identify supporting premises/spans and remain distinct from a direct source statement. |

A direct quotation may be stored/rendered according to existing privacy and copyright constraints, but quoting a source still does not prove the quoted proposition true.

## 18. Provenance

Every meaningful Reader artifact must remain replayable to its source context.

Conceptually:

```text
Reader Artifact
      │
      ▼
Document ID
      │
      ▼
Document version / content hash
      │
      ▼
Exact source span and/or replayable structural location
```

Where Crystal's existing `DocumentRecord` / `SourceSpan` evidence model can supply exact byte/character anchors and text hashes, a future Reader implementation should reuse that identity rather than inventing a competing provenance system.

Rules:

- summaries must not become provenance dead-ends;
- interpretations and inferences must link to the spans that motivated them;
- cross-document artifacts must preserve provenance for every contributing document;
- an artifact whose source locator is missing or cannot be replayed must expose degraded/invalid provenance;
- a provenance pointer is a locator, not authorization to disclose private source content;
- Reader provenance is distinct from the per-fact mutation provenance chain and from TRACE/Receipt answer proof; each keeps its existing responsibility.

## 19. Re-reading, source versioning and invalidation

Reading state belongs to a specific source identity/version. If the source content hash changes, Reader Core must not silently apply old coverage/artifacts to the new version.

Conceptual behavior:

1. preserve old Reader artifacts as historical artifacts tied to the old document version;
2. mark affected artifacts and coverage as stale for the new version;
3. identify affected spans/structural regions when a trustworthy mapping is available;
4. selectively re-read known affected regions;
5. widen invalidation conservatively when structural remapping is uncertain;
6. require full re-read when the system cannot safely determine what remained stable;
7. retain provenance history instead of rewriting the old reading record as if it had always referred to the new text.

```text
new hash + uncertain mapping
→ fail wider
→ do not assume old coverage is current
```

RC-0 defines no migration, diff engine or runtime invalidation algorithm.

## 20. Failure model

Reader Core must fail visibly. If it cannot establish sufficient reading coverage or provenance, it must report an incomplete/degraded state rather than manufacture full understanding.

| Failure / condition | Required conceptual response |
|---|---|
| malformed document | preserve failure reason; do not invent structure; mark affected coverage `NEEDS_REVIEW` |
| unsupported structure | retain source as far as safely addressable; expose unsupported regions |
| encoding problem | fail/mark affected spans; do not silently substitute corrupted text |
| truncated source | mark truncation and remaining coverage incomplete |
| interrupted read | preserve completed partial coverage and interruption state |
| model/provider failure | preserve source state; mark affected pass incomplete; allow replay with another compatible backend |
| insufficient working context | narrow working set or defer/re-read; never claim full processing from omitted spans |
| unresolved reference | record an open loop; do not fabricate target content |
| internally contradictory summary | mark summary invalid/needs review and return to supporting spans |
| stale document version | invalidate affected current coverage/artifacts until re-read |
| incomplete coverage | expose it explicitly in session/coverage outputs |
| reader artifact without source span/locator | treat as degraded/invalid for evidence-linked use; require review |
| source unavailable during replay | preserve artifact history but report provenance replay unavailable |

No failure state may silently promote a Reader artifact into authoritative memory.

## 21. Privacy and security boundaries

Reader Core inherits Crystal's existing privacy, erasure, restricted-processing, secret-handling and fail-closed boundaries. RC-0 introduces no new certification or security mechanism.

A source may contain PII or other sensitive material. Derived artifacts can be equally or more sensitive:

- Segment Cards may repeat identifying details;
- summaries may concentrate sensitive content;
- bookmarks can reveal what the reader considered important;
- open questions may disclose private context;
- provenance can reveal source existence/location even without copying text.

Therefore a future implementation must:

- treat Reader artifacts according to the sensitivity of their source and derived content;
- avoid treating a provenance pointer as permission to publish the underlying source;
- preserve existing processing restrictions and erasure semantics where applicable;
- minimize copied sensitive source text when a reference is sufficient, without breaking provenance;
- avoid credentials/secrets in logs, receipts or public artifacts;
- fail closed when a required privacy/restriction decision cannot be established.

RC-0 does not add encryption, authentication, authorization, telemetry, remote upload, GDPR certification or security certification.

## 22. Integration and responsibility boundaries

The matrix below is grounded in current Crystal contracts. It describes responsibility, not a requirement that every component be one Python class.

| Component / boundary | Existing or proposed responsibility | Reader Core must not take over |
|---|---|---|
| **Reader Core** | attentive source reading, coverage, re-read state, source-linked observations/candidates | truth admission, strict Canon writes, automatic contradiction resolution |
| **DocumentRecord / SourceSpan / EvidenceStore + import/review flow** | document identity, content hash, exact source addressing, source-first candidate evidence | attentive whole-document synthesis or Reader coverage state |
| **Guardian / Immune safety-policy boundary** | structural/safety checks and threat/policy pre-screening before normal admission where applicable | summarization, reading objectives or document comprehension claims |
| **TruthGate** | epistemic admissibility and evidence/source requirements | document reading, importance ranking or summary generation |
| **Contradiction detection / ContradictionReport / curator decisions** | conservative conflict classification/reporting and explicit resolution authority | Reader only proposes pre-authority contradiction candidates |
| **L1 + physical multi-status L3** | operational state and stored multi-status memory | Reader workspace must not masquerade as strict Canon |
| **TrustSnapshot / CanonicalView** | deny-dominant reconciliation and strict trusted read projection | raw Reader artifacts or partial-reading state |
| **Read-only query / retrieval** | find/render existing admitted or status-labeled material without write-side effects | declaring a retrieved item true or proving a source was fully read |
| **TRACE / Receipt / provenance contracts** | answer/source proof, audit and replay evidence in their existing scopes | becoming the Reader's semantic state or comprehension authority |
| **Staged working-memory architecture (future)** | non-authoritative candidate workspace before admission | Reader Core must not turn reading artifacts into an alternate promotion path |

Reader Core should reuse existing source identity and authority contracts wherever possible. RC-1 must justify any new runtime object on the basis of a missing semantic responsibility, not convenience.

## 23. RC-1 test and validation plan

RC-1 may begin only after this architecture contract is accepted and merged. It should start with the smallest evidence-linked skeleton that can prove the contract without pretending to solve long-document understanding.

Minimum validation targets for a future RC-1 include:

### Identity and provenance

- a Reader artifact resolves to document identity, exact source version/hash and source span/structural location;
- source-version changes make affected Reader state stale rather than silently current;
- missing source location fails visibly.

### Coverage

- legal coverage transitions preserve `UNREAD`, `SEEN`, `PROCESSED`, `REVISITED` and `NEEDS_REVIEW` semantics;
- interrupted/partial reads cannot be reported as complete;
- stale regions invalidate aggregate coverage.

### Fidelity

- direct source observation, extracted proposition, interpretation, summary and inference remain distinguishable;
- quoted opinions and hypotheticals are not collapsed into author-endorsed world facts;
- exceptions, negation and scope qualifiers survive the reader artifact path.

### Non-authority invariants

Tests must prove the Reader skeleton cannot, merely by producing a Reader artifact:

- mutate `truth_status` or ESM state;
- write directly into strict Canon;
- bypass Guardian/Immune/TruthGate admission;
- resolve a `ContradictionReport`;
- convert importance/repetition/retrieval score into truth authority;
- equate cross-document claims solely from similarity.

### Failure and replay

- model/provider interruption preserves partial coverage;
- unavailable source replay is explicit;
- contradictory summaries return to supporting spans/`NEEDS_REVIEW`;
- malformed/truncated sources remain visibly incomplete.

### Privacy/security

- restricted/sensitive source handling does not become less restrictive because a Reader artifact was derived;
- logs/receipts do not gain source content or credentials merely to support Reader Core;
- no new certification claim appears.

RC-1 must remain backend/model neutral unless a later accepted decision deliberately narrows that boundary.

## 24. Explicit implementation status

At RC-0:

```text
Reader Core RC-0 architecture contract = DEFINED_IN_DOCUMENTATION
Reader Core runtime                  = NOT_IMPLEMENTED
dedicated_reader_core                = false
new runtime wiring                   = none
new public API / CLI                 = none
new dependency                       = none
new storage schema / migration       = none
PostgreSQL active runtime            = false
```

This architecture document is not implementation evidence. The authoritative machine-readable implementation manifest must remain unchanged by RC-0 unless an independent repository validator requires a docs-only metadata update that preserves `dedicated_reader_core=false`.

## 25. Grant and claim boundary

RC-0 is a documentation/architecture baseline. It does not change Crystal's grant state and must not be described as funded Reader runtime implementation.

Current claim boundary remains:

- NLnet: submitted / under review / not awarded;
- approximately €50,000: planning only;
- approved budget/payment commitment: absent;
- budget change: none;
- pre-agreement merged work: existing baseline.

If this RC-0 contract merges before a grant agreement exists, it becomes part of that existing pre-agreement baseline.

## 26. Related current Crystal contracts

- [`../ARCHITECTURE.md`](../ARCHITECTURE.md)
- [`../STORAGE_AND_AUTHORITY_BOUNDARIES.md`](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [`../CONTRADICTION_POLICY.md`](../CONTRADICTION_POLICY.md)
- [`../CLAIM_METADATA_GLOSSARY.md`](../CLAIM_METADATA_GLOSSARY.md)
- [`../core/INGEST_SCHEMA.md`](../core/INGEST_SCHEMA.md)
- [`../core/PROVENANCE_CHAIN_CONTRACT.md`](../core/PROVENANCE_CHAIN_CONTRACT.md)
- [`read-only-query-boundary.md`](./read-only-query-boundary.md)
- [`STAGED_WORKING_MEMORY_ADMISSION.md`](./STAGED_WORKING_MEMORY_ADMISSION.md)
- [`../IMMUNE_LAYER.md`](../IMMUNE_LAYER.md)
- [`../PRIVACY.md`](../../PRIVACY.md)
- [`../../SECURITY.md`](../../SECURITY.md)

These documents keep their existing authority and implementation status. RC-0 adds a bounded reading contract; it does not replace them.