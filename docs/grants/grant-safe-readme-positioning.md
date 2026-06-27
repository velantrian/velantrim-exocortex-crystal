# 💠 Velantrim Crystal — Grant-Safe README Positioning Draft

**Status:** docs-only · grant-safe framing · not runtime expansion · not Research Mode · not a replacement for the canonical README

This document is a reviewer-facing positioning draft for improving or auditing the public `README.md` without weakening the repository's existing implementation claims.

It exists because the current repository already has a strong, tested implementation baseline. The purpose of this draft is not to replace that baseline, but to keep the public story clear, readable, visually navigable, and safe for grant review.

---

## 🧭 One-sentence positioning

> **Velantrim Crystal is an open-source, local-first verifiable memory layer for AI systems that separates raw input, pending candidates, admitted knowledge, provenance receipts, and response policy so applications can distinguish verified facts from unsupported context.**

---

## 🧠 The problem

Modern AI memory systems often optimize for recall, latency, personalization, and larger context. Those goals are useful, but they do not automatically solve the trust problem.

The central risk is **memory laundering**:

```text
unsupported claim
  ↓
stored as memory
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
user statement     ≠ source-backed fact
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
  Where did it               Can this claim             What evidence is
  come from?                 enter trusted memory?      allowed into context?
       │                          │                          │
       └──────────────┬───────────┴───────────┬──────────────┘
                      │                       │
              🗂️ Pending / Review       🏛️ Canonical Graph
              not trusted by default     admitted knowledge path
                      │                       │
                      └──────────┬────────────┘
                                 │
                         🗣️ response_policy
                  How strongly may the system speak?
```

---

## ⚙️ Core public primitives

Use these terms in README, grant text, reviewer docs, and public technical summaries.

| Primitive | Public meaning | Safe reviewer wording |
|---|---|---|
| `pending candidate` | captured information not yet admitted as trusted knowledge | Raw input may be useful, but it is not trusted by default. |
| `TruthGate` | admission boundary | Claims must pass policy checks before entering the canonical path. |
| `TRACE / receipt` | audit path | Answers can be connected back to stored facts, metadata, and sources. |
| `FactsPack` | scoped evidence bundle | The answerer receives a bounded evidence context instead of arbitrary memory. |
| `response_policy` | speech-strength control | The system can assert, hedge, speculate, cite/limit, or refuse based on evidence status. |
| `Canon / L3` | admitted graph path | The trusted path is narrower than raw storage. |

---

## 🛡️ Claim discipline

The README should preserve the repository's existing honesty invariant:

```text
If it is implemented and tested:
  describe it as implemented.

If it is designed but not implemented:
  describe it as planned, proposed, or grant-scope.

If it is speculative:
  keep it in Research Mode, not in Crystal runtime claims.
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
Research Mode
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
❌ Research Mode runtime
```

Use this instead:

```text
✅ verifiable memory infrastructure
✅ local-first AI memory core
✅ provenance-aware retrieval
✅ admission-controlled storage
✅ auditable receipt path
✅ response-strength policy layer
✅ developer infrastructure for trustworthy AI applications
```

---

## 🧬 Research Mode boundary

The broader private Velantrim Research Mode may explore cognitive metaphors, personal exocortex models, working-memory interfaces, and future architecture hypotheses.

Those concepts should not enter public Crystal README language unless converted into neutral engineering primitives and verified by implementation.

Safe path:

```text
Research idea
  → neutral primitive
  → RFC
  → invariants
  → tests
  → implementation
  → audit
  → GitHub main
```

Public translation rule:

```text
Velaris      → L1/L2 working context
Workdesk     → pending candidate / candidate envelope
Aktaris      → admission step / TruthGate path
Karin        → Canon / canonical graph
Archive      → supersede-store / append-only history
Observer     → counter-classifier / drift signal
ResponseGate → response_policy
Anti-Cyc     → architecture review checklist
```

---

## 🧾 Reviewer-friendly ASCII architecture

```text
WRITE PATH
──────────
raw input
  ↓
pending candidate
  ↓
admission policy
  ↓
Guardian + TruthGate
  ↓
TRACE / receipt
  ↓
canonical graph path

READ PATH
─────────
user query
  ↓
retrieval scope
  ↓
FactsPack
  ↓
status merge / evidence boundary
  ↓
response_policy
  ↓
answer / refusal / citation-limited output
```

---

## 🧪 Minimal demo story

The strongest public demo should show one simple contrast:

```text
unsupported claim → HEDGE / REFUSE
verified claim    → ASSERT + receipt
```

Example reviewer narrative:

```text
1. A user or model introduces a claim without source support.
2. Crystal stores it only as pending or advisory context.
3. A factual query cannot turn that claim into a strong assertion.
4. A source-backed version is admitted through TruthGate.
5. A later answer can assert the claim and show a receipt path.
```

This explains Crystal in under one minute without overclaiming that it eliminates all hallucinations.

---

## ⚖️ Ecosystem positioning

| Dimension | Ordinary RAG | Long-term AI memory | Agent memory | Velantrim Crystal |
|---|---|---|---|---|
| Main goal | retrieve relevant text | remember useful context | maintain agent state | enforce memory trust boundaries |
| Admission boundary | often external | varies | often agent-driven | explicit TruthGate path |
| Claim status | usually implicit | varies | varies | explicit status discipline |
| Provenance | document/chunk-level | varies | varies | receipt-oriented audit path |
| Output strength | mostly prompt-based | mostly prompt-based | mostly prompt-based | response_policy discipline |
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
AI systems should not silently convert generated text, user speculation, or unsupported notes into trusted memory.
Crystal provides an open-source memory boundary that keeps raw, pending, admitted, and evidenced knowledge separate.
```

---

## ✅ Suggested README improvement pattern

If this draft is used to improve the canonical README, prefer small edits:

```text
1. Keep the existing tested status and reviewer validation sections.
2. Add a short positioning block near the top.
3. Add a compact visual mindmap only if it improves readability.
4. Preserve all implemented/tested claims that are already supported by TEST_REPORT and reviewer docs.
5. Keep Research Mode outside runtime claims.
6. Do not replace precise implementation sections with broad marketing language.
```

---

## 🧭 Final formula

```text
Useful memory is not enough.
AI systems need verifiable memory.

Velantrim Crystal provides the boundary:
what is raw,
what is pending,
what is admitted,
what is evidenced,
and what may be safely said.
```
