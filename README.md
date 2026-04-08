# 🧠 Velantrim Exocortex

---

## 🇬🇧 EN

**Velantrim** is a truth-first, explainable cognitive system (exocortex) where truth is controlled by structure, not by generation.

The system follows the principle:

> **Trace → Validation → Answer**  
> not “first answer, then explain”.

---

### ⚙️ Core Pipeline

```text
Query
 ↓
Tokenize
 ↓
Retrieve (scoring / BM25-lite)
 ↓
Facts Pack (confidence)
 ↓
TRACE (provenance)
 ↓
Guardian (structure validation)
 ↓
Truth Gate (truth validation)
 ↓
Answer + Trace
