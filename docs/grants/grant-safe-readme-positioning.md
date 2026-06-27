# 💠 Velantrim Crystal — Grant-Safe README Positioning Draft

**Status:** docs-only · grant-safe framing · not runtime expansion · not Research Mode · not a replacement for the canonical README

This document is a reviewer-facing positioning draft for improving or auditing the public `README.md` without weakening the repository's existing implementation claims.

It exists because the current repository already has a strong, tested implementation baseline. The purpose of this draft is not to replace that baseline, but to keep the public story clear, readable, visually navigable, and safe for grant review.

---

## 🧭 One-sentence positioning

> **Velantrim Crystal is an open-source, local-first verifiable memory layer for AI systems that separates raw input, explicit claim status, admitted knowledge, trace metadata, answer receipts, and current blocking/answer-generation behavior so applications can distinguish verified facts from unsupported context.**

---

## 🧠 The problem

Modern AI memory systems often optimize for recall, latency, personalization, and larger context. Those goals are useful, but they do not automatically solve the trust problem.

The central risk is **memory laundering**:

```text
unsupported claim
  ↓
stored without explicit status
  ↓
retrieved later as context
  ↓
spoken as if authoritative
  ↓
treated as trusted knowledge
```

Crystal's public framing should keep this distinction explicit:

```text
raw input          ≠ verified knowledge
user statement     ≠ externally verified fact
AI output          ≠ evidence
repetition         ≠ proof
importance         ≠ truth
retrieved context  ≠ authority
```

---

## 🗺️ Grant-safe mindmap

```text
                         💠 Velantrim Crystal
                                  │
       ┌──────────────────────────┼──────────────────────────┐
       │                          │                          │
  🧾 Provenance              🛡️ TruthGate              📦 FactsPack
  Where did it               What admission /           What evidence is
  come from?                 blocking rule applies?     allowed into context?
       │                          │                          │
       └──────────────┬───────────┴───────────┬──────────────┘
                      │                       │
              🗂️ Pending / Review       🏛️ Canonical Graph
              explicit status required   status-aware storage path
                      │                       │
                      └──────────┬────────────┘
                                 │
                         🗣️ Current answer policy
              blocking / answer generation / receipt replay today;
              named `response_policy` is grant-scope / planned terminology.
```

---

## ⚙️ Core public primitives

Use these terms in README, grant text, reviewer docs, and public technical summaries.

| Primitive | Public meaning | Safe reviewer wording |
|---|---|---|
| `pending / review path` | captured or imported information that still needs status discipline | Raw input may be useful, but it must keep explicit status and provenance. |
| `TruthGate` | admission / blocking boundary | Claims pass through implemented policy checks before or while entering the graph path. |
| `TRACE` | trace metadata / proof path | The system records how answers connect back to stored facts, metadata, and sources. |
| answer receipt | read-path receipt produced after an answered query | Receipts are answer/query artifacts, not current write-path admission receipts. |
| `FactsPack` | scoped evidence bundle | The answerer receives a bounded evidence context instead of arbitrary memory. |
| current answer behavior | implemented blocking / answer-generation behavior | Current runtime blocks or answers through the existing pipeline and receipts. |
| `response_policy` | future / grant-scope name for explicit speech-strength control | Use as planned terminology unless implemented and tested in GitHub main. |
| Canon / L3 | status-aware graph path | The graph can carry statuses such as verified, user-claimed, unverified, hypothesis, or subjective. |

---

## 🛡️ Claim discipline

The README should preserve the repository's existing honesty invariant:

```text
If it is implemented and tested:
  describe it as implemented.

If it is designed but not implemented:
  describe it as planned, proposed, or grant-scope.

If it is speculative:
  keep it out of Crystal runtime claims.
```

Implementation truth must come from:

```text
GitHub main
tests
auditable code paths
release notes
reviewer docs
```

Not from:

```text
private notes
conceptual diagrams
LLM-generated summaries
unreviewed drafts
```

---

## 🚫 Anti-goals for grant-facing README text

Do not describe Crystal as:

```text
❌ AGI
❌ digital brain
❌ consciousness model
❌ zero-hallucination guarantee
❌ replacement for LLMs
❌ personal companion
❌ therapeutic system
❌ private research runtime
```

Use this instead:

```text
✅ verifiable memory infrastructure
✅ local-first AI memory core
✅ provenance-aware retrieval
✅ status-aware storage
✅ auditable receipt path
✅ implemented blocking / answer-generation controls
✅ future explicit response-policy layer when implemented
✅ developer infrastructure for trustworthy AI applications
```

---

## 🧬 Public research boundary

The public repository should stay focused on Crystal's neutral engineering primitives.

Broader private research may explore cognitive metaphors, personal exocortex models, working-memory interfaces, and future architecture hypotheses, but those names and metaphors should not appear in public grant-facing README guidance.

Safe path:

```text
research idea
  → neutral primitive
  → RFC
  → invariants
  → tests
  → implementation
  → audit
  → GitHub main
```

Public documentation should prefer neutral language:

```text
working context
pending / review path
admission step
canonical graph
status-aware storage
trace metadata
answer receipt
blocking behavior
answer generation
future explicit response policy
architecture review checklist
```

---

## 🧾 Reviewer-friendly ASCII architecture

```text
WRITE / INGEST PATH TODAY
─────────────────────────
raw input
  ↓
claim classification + source/status metadata
  ↓
Guardian + TruthGate / implemented blocking rules
  ↓
transient trace + merge behavior
  ↓
status-aware graph path
  ├─ externally supported / verified claims may be used as stronger evidence
  └─ user-reported claims may be stored with explicit USER_CLAIMED status

READ / ANSWER PATH TODAY
────────────────────────
user query
  ↓
retrieval scope
  ↓
FactsPack / supporting facts
  ↓
implemented blocking + answer-generation behavior
  ↓
answer or refusal / limitation
  ↓
answer receipt / receipt replay where requested

GRANT-SCOPE EXTENSION
─────────────────────
explicit response_policy layer
  ↓
ASSERT / HEDGE / SPECULATIVE / REFUSE / CITE_OR_LIMIT
```

---

## 🧪 Minimal demo story

The strongest public demo should show one simple contrast without overstating current runtime behavior:

```text
unsupported or low-confidence generated claim → blocked, limited, or not used as strong evidence
source-backed claim                         → stronger answer path + trace / receipt support
```

Example reviewer narrative:

```text
1. A model-generated or low-confidence claim is introduced without source support.
2. Crystal keeps explicit status and does not present it as externally verified evidence.
3. User-reported claims may be stored with USER_CLAIMED status, but should not be described as externally verified facts.
4. A source-backed version can pass the implemented gate / evidence path.
5. A later answer can be supported by trace metadata and an answer receipt where requested.
```

This explains Crystal in under one minute without claiming that all unsupported user statements always remain outside the graph or that the system eliminates all hallucinations.

---

## ⚖️ Ecosystem positioning

| Dimension | Ordinary RAG | Long-term AI memory | Agent memory | Velantrim Crystal |
|---|---|---|---|---|
| Main goal | retrieve relevant text | remember useful context | maintain agent state | enforce memory trust boundaries |
| Admission / blocking boundary | often external | varies | often agent-driven | implemented Guardian / TruthGate path |
| Claim status | usually implicit | varies | varies | explicit status discipline |
| Provenance | document/chunk-level | varies | varies | trace + answer receipt orientation |
| Output control | mostly prompt-based | mostly prompt-based | mostly prompt-based | implemented blocking / answer behavior today; explicit response_policy is future terminology |
| Core risk addressed | missing context | forgotten context | continuity | unsupported context becoming trusted knowledge |

This is a positioning map, not a benchmark claim. Formal comparison requires reproducible tests and documented criteria.

---

## 🏛️ Grant-safe value proposition

Crystal is strongest for grant review when framed as:

```text
open-source local-first infrastructure
for verifiable AI memory,
provenance-aware retrieval,
auditable source trails,
and evidence-bounded factual answers.
```

The best public-interest framing:

```text
AI systems should not silently convert generated text, user speculation, or unsupported notes into externally verified knowledge.
Crystal provides an open-source memory boundary that keeps raw, user-claimed, unverified, hypothesis, subjective, and verified knowledge statuses explicit.
```

---

## ✅ Suggested README improvement pattern

If this draft is used to improve the canonical README, prefer small edits:

```text
1. Keep the existing tested status and reviewer validation sections.
2. Add only a short positioning block near the top.
3. Add a compact visual mindmap only if it improves readability.
4. Preserve all implemented/tested claims that are already supported by TEST_REPORT and reviewer docs.
5. Keep private research names outside public Crystal README guidance.
6. Mark response_policy as planned/grant-scope until implemented and tested.
7. Do not show answer receipts as current write-path admission receipts.
8. Do not promise that all user claims remain outside the graph; describe USER_CLAIMED status accurately.
9. Do not replace precise implementation sections with broad marketing language.
```

---

## 🧭 Final formula

```text
Useful memory is not enough.
AI systems need verifiable memory.

Velantrim Crystal provides the boundary:
what is raw,
what is user-claimed,
what is unverified,
what is hypothesized,
what is externally supported,
what is verified,
and what may be safely said today.
```
