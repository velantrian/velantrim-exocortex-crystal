# 📌 Velantrim Crystal — 現在の状態

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 [Español](../es/STATUS.md) · 🇮🇹 [Italiano](../it/STATUS.md) · 🇷🇺 [Русский](../ru/STATUS.md) · 🇨🇳 [简体中文](../zh-CN/STATUS.md) · 🇸🇦 [العربية](../ar/STATUS.md) · 🇯🇵 **日本語**

**翻訳同期基準:** `main@14bc0659`  
**audited runtime checkpoint:** `cd6fd44`  
**正本となる evidence:** [TEST_REPORT.md](../../TEST_REPORT.md)

## Reading rule

```text
GitHub Crystal main = 公開実装の正本
Notion Crystal      = 同期された grant / strategy map
Titan / Full        = 別の研究トラック
```

文書、Notion note、prototype branch、Titan component は、Crystal `main` に実装・test・merge されていない限り、
現在の Crystal capability ではありません。

## 現在の verified checkpoint

PR #265 は strict read-only HTTP query boundary を導入しました。

```text
POST /ingest  → Guardian + TruthGate を通る admission
POST /ask     → strict read-only canonical query
GET /receipt  → strict read-only canonical query + Receipt
```

HTTP `/ask` と `/receipt` は、L0/L1 または L3 への write、ESM transition、outbox operation、
episode link 記録、embedding fingerprint 初期化、adaptive verification state mutation を行いません。

## 明示された残余スコープ

- CLI `ask` と `receipt` は `core.pipeline.run()` compatibility path を使用します;
- `core.pipeline.run()` は admission-capable path として残っています;
- MCP には明示的な canonical write tool はありませんが、search が未設定の embedding fingerprint を初期化する可能性があります。

これらは follow-up scope であり、隠された capability claim ではありません。

## Verification baseline

正確な test count、skip、coverage、CI evidence は [TEST_REPORT.md](../../TEST_REPORT.md) が正本です。
CI の permanent gate は以下を含みます。

- Python 3.11 / 3.12 test;
- Ruff code quality;
- secret / security scan;
- Docker build;
- evaluation gate;
- JSONL integrity。

## 現在許可される public claim

Crystal は次のように説明できます。

- local-first で検証可能な AI memory infrastructure;
- source / provenance oriented memory core;
- wiring 済み path における Guardian / TruthGate admission control;
- wiring 済み path における CanonicalView、TRACE、replayable Receipt;
- optional adapter を持つ standard-library default runtime;
- GDPR 関連の erasure / restriction mechanism;
- independently testable open-source research-grade baseline。

Crystal は次のようには説明できません。

- Titan または完全な Personal Exo-Cortex;
- autonomous cognitive OS;
- conscious、alive、biological brain equivalent;
- universally truthful または hallucination-free;
- legally GDPR-certified;
- security-certified または production multi-tenant ready;
- mandatory external LLM / cloud provider dependent。

## Grant status

NLnet NGI0 Commons Fund proposal は提出済みで review 中です。repository は funding award を主張しません。

```text
BASELINE TODAY
    +
MEASURABLE FUNDED DELTA
    =
INDEPENDENTLY VERIFIABLE DELIVERABLE
```

すでに merge 済みの作業は baseline であり、paid milestone として再計上されません。

## Replay decision

Titan の deterministic replay implementation は prior art として review されていますが、
この同期で Crystal runtime にコピーされてはいません。

```text
REVIEWED_PRIOR_ART
DOCUMENTED_ONLY
M4_CANDIDATE
NO_RUNTIME_CHANGE
NO_CANON_WRITE
NO_BUDGET_CHANGE
BASELINE_NOT_MOVED
```

将来の実装は既存の `core/eval.py` と `scripts/eval_gate.py` を拡張し、別 RFC/PR、offline、
non-authoritative、grant baseline 固定後という条件を守る必要があります。

## Canonical reviewer path

1. [REVIEWER_GUIDE.md](./REVIEWER_GUIDE.md)
2. [QUICKSTART.md](./QUICKSTART.md)
3. [../../TEST_REPORT.md](../../TEST_REPORT.md)
4. [../ARCHITECTURE.md](../ARCHITECTURE.md)
5. [../EVAL.md](../EVAL.md)
6. [../GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)

---

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 [Español](../es/STATUS.md) · 🇮🇹 [Italiano](../it/STATUS.md) · 🇷🇺 [Русский](../ru/STATUS.md) · 🇨🇳 [简体中文](../zh-CN/STATUS.md) · 🇸🇦 [العربية](../ar/STATUS.md) · 🇯🇵 **日本語**
