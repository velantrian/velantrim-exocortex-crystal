# Velantrim Knowledge Base Roadmap

Velantrim Crystal is the verifiable memory core. The broader Velantrim project also includes an emerging curated knowledge-base effort designed to provide local AI systems with structured, source-aware knowledge that can work offline.

This document describes the intended direction honestly. The knowledge base is not yet part of the audited Crystal release boundary unless its contents are imported through Crystal's schema, provenance, TruthGate and receipt mechanisms.

---

## Goal

Build a curated offline graph of useful knowledge for weak and medium AI models.

```text
curated facts
→ nodes and edges
→ invariant science
→ context-dependent knowledge
→ practical knowledge
→ provenance and truth status
→ local graph retrieval
→ answers with trace
```

The purpose is not to create another huge encyclopedia. The purpose is to create a compact, structured and useful knowledge substrate that helps local AI systems reason from verified material instead of depending only on internet access or large cloud models.

---

## Knowledge resilience reserve

The knowledge base is also intended as a resilience layer: a local reserve of essential knowledge that remains usable when the internet is unavailable, degraded or politically, technically or economically unreliable.

This should not be framed as "all human knowledge". The realistic goal is a curated reserve of high-value knowledge that helps preserve access to important concepts, mechanisms, procedures, scientific facts and practical know-how even during network outages or failures of global information infrastructure.

In this sense, the KB can become a compact knowledge fallback for humans, schools, communities, research teams and local AI systems.

---

## Current status

The broader project-maintainer knowledge-base effort currently reports up to approximately **30,000 draft facts** under collection and refinement.

Important boundary:

- these draft facts are not automatically treated as canonical Crystal memory;
- they require schema validation, deduplication, provenance, relation typing and import through the Crystal memory pipeline;
- until validated, they should be described as a developing knowledge-base corpus, not as an audited released dataset.

---

## Scale and storage direction

The knowledge base should be able to grow from a compact gold core into a much larger corpus.

Suggested scaling path:

```text
1,000 gold facts
→ 5,000 clean facts
→ 10,000 high-value facts
→ 30,000 draft/refined facts
→ 50,000+ useful facts
→ larger domain packs when provenance and review workflows are stable
```

The goal is not maximum size for its own sake. The goal is maximum useful coverage under strict structure: typed claims, source references, relations, qualifiers, evidence spans and traceability.

Large future expansions should be organised as domain packs, for example science, education, medicine reference knowledge, engineering, agriculture, architecture, practical life and public-sector knowledge.

---

## Why not just Wikipedia?

Wikipedia is extremely valuable, but it is written primarily for human reading. It contains narrative context, pedagogy, historical discussion, style variation and long articles.

Velantrim KB aims to be different:

```text
Wikipedia = broad human encyclopedia
Velantrim KB = compact source-tracked graph of useful knowledge
```

The KB should distil useful claims, conditions, mechanisms, procedures and relations into a graph that is easier for local AI systems to retrieve and reason over.

The advantage is not that Velantrim replaces Wikipedia. The advantage is that it can transform selected knowledge into a more compact, typed and traceable graph:

```text
claim → qualifier → source → relation → evidence → trace
```

This makes it more suitable for weak and medium AI models running offline.

---

## Societal and professional coverage

Long-term, the KB should help different layers of society orient themselves in reliable knowledge.

Potential domains:

- foundational science;
- education and pedagogy;
- research support;
- medical reference knowledge and public-health education;
- engineering and mechanisms;
- construction and architecture;
- agriculture and ecology;
- practical household and safety knowledge;
- institutional procedures and public-sector knowledge;
- interdisciplinary knowledge for citizens, teachers, students, researchers and professionals.

Important boundary: medical and safety-related content must remain source-tracked, reviewable and clearly separated from professional advice or emergency decision-making.

---

## Knowledge types

Each knowledge unit should declare what kind of knowledge it represents.

| Type | Meaning | Example |
|---|---|---|
| `INVARIANT_SCIENCE` | stable scientific knowledge that rarely changes | water consists of H2O; force has magnitude and direction |
| `VARIANT_KNOWLEDGE` | knowledge that depends on time, school, context, model or interpretation | historical interpretations; competing models; evolving classifications |
| `PRACTICAL_KNOWLEDGE` | applicable knowledge for life, work, education and operations | how to measure pH; how to purify water; how to use a tool safely |
| `PROCEDURAL_KNOWLEDGE` | step-by-step procedures | step 1 → step 2 → expected result |
| `WARNING_CONSTRAINT` | risks, constraints, safety boundaries or conditions | do not treat a claim as fact without evidence |

---

## Knowledge Unit Schema v1

A minimal knowledge unit should contain enough metadata to be useful for graph retrieval and audit.

```json
{
  "id": "fact_000001",
  "title": "Water boiling point",
  "claim": "Water boils at 100°C at 1 atm pressure.",
  "knowledge_type": "INVARIANT_SCIENCE",
  "claim_type": "WORLD_FACT",
  "truth_status": "FACT",
  "source_status": "EXTERNAL",
  "domain": "chemistry",
  "level": "basic",
  "qualifiers": ["at 1 atm", "pure water"],
  "relations": [
    {"type": "REQUIRES", "target": "atmospheric_pressure"},
    {"type": "RELATED_TO", "target": "phase_transition"}
  ],
  "source": "...",
  "evidence_span": "...",
  "confidence": 0.95,
  "significance": 0.8
}
```

---

## Relation vocabulary

The graph should store typed relations, not only isolated facts.

Recommended initial relation types:

```text
IS_A
PART_OF
MADE_OF
CAUSES
REQUIRES
USED_FOR
HAS_STEP
HAS_RISK
PREVENTS
SUPPORTS
CONTRADICTS
EXAMPLE_OF
RELATED_TO
```

This direction borrows useful ideas from commonsense graphs such as ConceptNet, but the Velantrim KB should not blindly import unverified facts. Relation types are reusable; claims still require provenance and review.

---

## Explanation chains

The knowledge base should support small explanation chains, inspired by science explanation graphs.

Example:

```text
plant needs water
→ water participates in photosynthesis
→ photosynthesis produces sugars
→ sugars provide energy for the plant
```

This helps weaker AI models answer with a causal path rather than a single disconnected sentence.

---

## Qualifiers and context

Many facts are only true under specific conditions.

Example:

```text
"Water boils at 100°C" is incomplete.
"Water boils at 100°C at 1 atm pressure" is scoped.
```

Knowledge units should therefore support:

- qualifiers;
- scope;
- time or era where relevant;
- location or jurisdiction where relevant;
- method or model where relevant;
- source references.

---

## Suggested folder structure

```text
Velantrim Knowledge Base
├── 01_Invariant_Science
│   ├── mathematics
│   ├── physics
│   ├── chemistry
│   ├── biology
│   └── logic
├── 02_Variant_Knowledge
│   ├── history
│   ├── medicine_contextual
│   ├── social_science
│   └── competing_models
├── 03_Practical_Knowledge
│   ├── health_basics
│   ├── home
│   ├── tools
│   ├── agriculture
│   └── safety
├── 04_Procedures
│   ├── step_by_step
│   └── troubleshooting
└── 05_Explanations
    ├── why_chains
    └── cause_effect_graphs
```

---

## Multilingual direction

The first presentation and grant-facing materials should be in English.

Longer term, after grant support and schema stabilisation, the knowledge base can be localised into major European languages and UN languages, including English, French, Spanish, Arabic, Chinese and Russian, with additional languages added according to community need.

The multilingual strategy should preserve stable IDs and relations while allowing labels, descriptions and examples to vary by language.

---

## Development order

Recommended order:

```text
1. schema_knowledge_unit_v1.json
2. relation_types_v1.json
3. first 1,000 gold-standard facts
4. source / provenance / evidence-span coverage
5. explanation chains
6. scale to 5k → 10k → 50k facts
7. multilingual labels and descriptions
```

Quality rule:

```text
5,000 clean facts with sources, relations and trace are better than
50,000 raw fragments without provenance or review.
```

---

## Relationship to Crystal

Crystal should remain the audited core:

```text
Crystal = memory engine + TruthGate + provenance + receipts + local-first controls
Knowledge Base = curated corpus that can be imported through Crystal
```

The KB should never bypass Crystal's evidence, epistemic state, TruthGate or receipt boundaries.
