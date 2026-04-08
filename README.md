# 🧠 Velantrim Exocortex

**Velantrim** — это детерминированная, объяснимая когнитивная система (exocortex), в которой истина контролируется структурой, а не генерацией.

Система построена по принципу:
> **Trace → Validation → Answer**  
> (а не “сначала ответ → потом объяснение”)

---

# ⚙️ Core Pipeline

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
