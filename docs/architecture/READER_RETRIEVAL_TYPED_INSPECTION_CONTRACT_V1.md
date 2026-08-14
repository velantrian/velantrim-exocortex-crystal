# Reader Retrieval Typed Inspection Contract v1

**Status:** FROZEN ARCHITECTURE CONTRACT  
**Tracking issue:** #391  
**Starting main:** `d8bc98cb7643019b34ffacde2e87c3e81a5556ba`  
**Runtime authorization:** false

## Purpose

Comparator v1 recovered the measured lexical recall ceiling but retained excessive hard-negative leakage. The preregistered NLI neutral-filter v1 materially improved discrimination but lost useful Reader candidates. The combined evidence shows a relation-contract mismatch: retrieval usefulness is broader than strict proposition equivalence or bidirectional entailment.

RRTIC-v1 therefore freezes a retrieval-side inspection envelope. Its job is to describe a candidate pair as a **typed suspicion with explicit qualifier diagnostics**. It does not decide whether the pair should be accepted, rejected, admitted as evidence, treated as identical, or adjudicated as contradictory.

```text
broad retrieval candidate
        |
        v
typed inspection diagnostic
        |
        +-- relation-family suspicion
        +-- structural qualifier states
        +-- unresolved dimensions
        |
        v
inspection candidate
        |
        v
explicit downstream review / existing authority layers
```

The contract is intentionally model-free. It defines the output shape before any future diagnostic provider is selected.

## Frozen relation families

RRTIC-v1 contains exactly six relation-family values:

1. `EQUIVALENCE_SUSPECT`
2. `RELATED_SUSPECT`
3. `CONTRADICTION_SUSPECT`
4. `QUALIFICATION_SUSPECT`
5. `TOPIC_ONLY_SUSPECT`
6. `UNKNOWN`

`SUSPECT` is normative wording. These labels are inspection hypotheses, not verified semantic relations.

## Frozen qualifier dimensions

RRTIC-v1 contains exactly ten qualifier dimensions:

- `entity_binding`
- `predicate_binding`
- `argument_roles`
- `polarity`
- `modality_quantifier`
- `temporal_version`
- `jurisdiction`
- `condition_direction`
- `units_thresholds`
- `attribution_causality`

Each dimension has only four states:

```text
MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE
```

A state describes the diagnostic observation available to an inspection provider. It is not a probability or confidence score.

## Required authority flags

Every conforming envelope is non-authoritative:

```text
identity_claimed        = false
evidence_admitted       = false
adjudication_performed  = false
runtime_authorization   = false
```

The contract has no scalar truth score, identity score, evidence score, accept/reject decision, or reranking decision.

## Why a typed envelope is required

The frozen research chain exposed several distinct candidate relations that cannot safely collapse into one relevance score or three generic NLI labels:

- a causal-chain claim can be useful without being an entailment;
- a low-overlap paraphrase can be useful even when generic NLI is neutral;
- condition direction can differ while the pair remains useful for inspection;
- an entity-sense collision can look topically similar while referring to a different entity;
- a polarity mismatch can be highly similar lexically and semantically while being structurally important.

The examples in `eval/reader_retrieval_typed_inspection_contract_v1.json` are synthetic representability examples. Historical RC-8/v2/NLI cases remain explanatory provenance only. They are not a new performance qualification surface and no new benchmark score is claimed here.

## RC-5 compatibility boundary

Crystal already has `core/reader_relations.py`, where RC-5 records explicit pre-admission relation candidates such as `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, and `TENSION`.

RRTIC-v1 does **not** replace or extend that runtime module in this milestone.

```text
RRTIC diagnostic
      != RC-5 registered relation
      != resolved semantic identity
      != adjudicated contradiction
      != admitted evidence
```

No automatic mapping from RRTIC relation families into `ReaderRelationKind` is authorized. A future architecture milestone would have to justify any bridge independently and preserve RC-5 provenance and authority semantics.

## Frozen non-goals

This milestone does not authorize or implement:

- changes under `core/**`;
- a CrossEncoder;
- another NLI or embedding model;
- threshold tuning;
- hard filtering;
- reranking;
- qrel modification;
- a new performance metric or qualification result;
- semantic or hybrid Reader runtime;
- FTS, ANN, FAISS, HNSW, vector DB, PostgreSQL, or pgvector Reader activation;
- automatic proposition identity;
- automatic contradiction adjudication;
- evidence admission;
- Canon mutation;
- Guardian or TruthGate responsibility changes;
- work on issues #155, #165, or #214.

## Authority firewall

The following distinctions remain invariant:

```text
retrieval match          != evidence
similarity               != identity
NLI label                != proposition identity
NLI contradiction        != contradiction adjudication
relation-family suspect  != adjudicated relation
qualifier mismatch       != truth decision
candidate discovery      != candidate adjudication
evaluation evidence      != runtime authorization
```

## Validation contract

RRTIC-v1 is valid only if repository evidence verifies all of the following:

1. exactly six relation families are frozen;
2. exactly ten qualifier dimensions are frozen;
3. qualifier states are exactly `MATCH`, `MISMATCH`, `UNKNOWN`, `NOT_APPLICABLE`;
4. all authority flags are false;
5. no accept/reject or reranking decision exists;
6. no truth, identity, or evidence score exists;
7. no model, network access, dependency, or runtime change is required;
8. synthetic examples demonstrate representability of related causal, paraphrase, condition-direction, entity-collision, and polarity cases;
9. existing RC-5 kinds remain unchanged;
10. prior frozen evaluation surfaces are explanatory only and no performance qualification is authorized.

## STOP gate

Stop and open a new architecture decision rather than silently expanding RRTIC-v1 if any proposed design requires:

- more than six relation families;
- more than ten qualifier dimensions;
- an implicit or explicit accept/reject policy;
- a scalar authority-like score;
- a runtime/model dependency;
- automatic RC-5 registration.

Any future discriminator must have a new experiment identity, preregistration, and fresh validation design before a qualifying result. RRTIC-v1 itself authorizes no such experiment and no runtime mechanism.
