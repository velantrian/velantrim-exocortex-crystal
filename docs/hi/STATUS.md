# 📌 Velantrim Crystal — वर्तमान स्थिति

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 [Español](../es/STATUS.md) · 🇮🇹 [Italiano](../it/STATUS.md) · 🇷🇺 [Русский](../ru/STATUS.md) · 🇨🇳 [简体中文](../zh-CN/STATUS.md) · 🇸🇦 [العربية](../ar/STATUS.md) · 🇯🇵 [日本語](../ja/STATUS.md) · 🇮🇳 **हिन्दी**

**Translation synchronization marker:** `main@c5a34a64`  
**Audited runtime checkpoint:** `cd6fd44`  
**Authoritative evidence:** [TEST_REPORT.md](../../TEST_REPORT.md)

## Reading rule

```text
GitHub Crystal main = सार्वजनिक implementation का authoritative source
Notion Crystal      = synchronized grant / strategy map
Titan / Full        = अलग research track
```

कोई document, Notion note, prototype branch या Titan component वर्तमान Crystal capability नहीं है,
जब तक वह Crystal `main` में implemented, tested और merged न हो।

## वर्तमान verified checkpoint

PR #265 ने strict read-only HTTP query boundary जोड़ा।

```text
POST /ingest  → Guardian + TruthGate से गुजरने वाला admission
POST /ask     → strict read-only canonical query
GET /receipt  → strict read-only canonical query + Receipt
```

HTTP `/ask` और `/receipt` L0/L1 या L3 write, ESM transition, outbox operation,
episode link recording, embedding fingerprint initialization या adaptive verification state mutation नहीं करते।

## स्पष्ट residual scope

- CLI `ask` और `receipt`, `core.pipeline.run()` compatibility path का उपयोग करते हैं;
- `core.pipeline.run()` admission-capable path के रूप में उपलब्ध है;
- MCP में explicit canonical write tool नहीं है, लेकिन search unset embedding fingerprint initialize कर सकता है।

ये follow-up scope हैं, छिपे capability claims नहीं।

## Verification baseline

सटीक test count, skips, coverage और CI evidence के लिए [TEST_REPORT.md](../../TEST_REPORT.md) authoritative है।
Permanent CI gates में शामिल हैं:

- Python 3.11 / 3.12 tests;
- Ruff code quality;
- secret / security scans;
- Docker build;
- evaluation gate;
- JSONL integrity।

## वर्तमान अनुमत public claim

Crystal को इस प्रकार वर्णित किया जा सकता है:

- local-first, सत्यापनीय AI memory infrastructure;
- source / provenance-oriented memory core;
- wired paths में Guardian / TruthGate admission control;
- wired paths में CanonicalView, TRACE और replayable Receipt;
- optional adapters वाला standard-library default runtime;
- GDPR-संबंधित erasure / restriction mechanisms;
- independently testable open-source research-grade baseline।

Crystal को इस प्रकार वर्णित नहीं किया जा सकता:

- Titan या पूर्ण Personal Exo-Cortex;
- autonomous cognitive OS;
- conscious, alive या biological brain equivalent;
- universally truthful या hallucination-free;
- legally GDPR-certified;
- security-certified या production multi-tenant ready;
- mandatory external LLM / cloud provider dependent।

## Grant status

NLnet NGI0 Commons Fund proposal submit हो चुका है और review में है। Repository funding award का दावा नहीं करती।

```text
BASELINE TODAY
    +
MEASURABLE FUNDED DELTA
    =
INDEPENDENTLY VERIFIABLE DELIVERABLE
```

पहले से merged कार्य baseline है; उसे paid milestone के रूप में फिर से नहीं गिना जाता।

## Replay decision

Titan deterministic replay implementation को prior art के रूप में review किया गया है,
लेकिन इस synchronization में उसे Crystal runtime में copy नहीं किया गया।

```text
REVIEWED_PRIOR_ART
DOCUMENTED_ONLY
M4_CANDIDATE
NO_RUNTIME_CHANGE
NO_CANON_WRITE
NO_BUDGET_CHANGE
BASELINE_NOT_MOVED
```

भविष्य implementation को मौजूदा `core/eval.py` और `scripts/eval_gate.py` extend करना होगा,
अलग RFC/PR, offline, non-authoritative और grant baseline fixed जैसी शर्तें बनाए रखनी होंगी।

## Canonical reviewer path

1. [REVIEWER_GUIDE.md](./REVIEWER_GUIDE.md)
2. [QUICKSTART.md](./QUICKSTART.md)
3. [../../TEST_REPORT.md](../../TEST_REPORT.md)
4. [../ARCHITECTURE.md](../ARCHITECTURE.md)
5. [../EVAL.md](../EVAL.md)
6. [../GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)

---

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 [Español](../es/STATUS.md) · 🇮🇹 [Italiano](../it/STATUS.md) · 🇷🇺 [Русский](../ru/STATUS.md) · 🇨🇳 [简体中文](../zh-CN/STATUS.md) · 🇸🇦 [العربية](../ar/STATUS.md) · 🇯🇵 [日本語](../ja/STATUS.md) · 🇮🇳 **हिन्दी**
