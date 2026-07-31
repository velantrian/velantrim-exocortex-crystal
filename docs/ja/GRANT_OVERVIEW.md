# 💶 Grant 概要 — Velantrim Crystal

> 🌐 🇬🇧 [English](../GRANT_NLNET_SCOPE.md) · 🇩🇪 [Deutsch](../de/GRANT_OVERVIEW.md) · 🇫🇷 [Français](../fr/GRANT_OVERVIEW.md) · 🇪🇸 [Español](../es/GRANT_OVERVIEW.md) · 🇮🇹 [Italiano](../it/GRANT_OVERVIEW.md) · 🇷🇺 [Русский](../ru/GRANT_OVERVIEW.md) · 🇨🇳 [简体中文](../zh-CN/GRANT_OVERVIEW.md) · 🇸🇦 [العربية](../ar/GRANT_OVERVIEW.md) · 🇯🇵 **日本語**

この文書は、日本語 reviewer のための概要です。法的・契約上・grant scope の正本は英語文書です。

## 現在の status

Velantrim Crystal は NLnet NGI0 Commons Fund に提出され、review 中です。
repository は funding award、契約成立、支払確定を主張しません。

## Governing formula

```text
BASELINE TODAY
    +
MEASURABLE FUNDED DELTA
    =
INDEPENDENTLY VERIFIABLE DELIVERABLE
```

すでに merge 済みの機能、test、documentation、security hardening は baseline です。
それらを将来の paid deliverable として二重計上しません。

## Baseline の例

現在の public baseline には、英語の正本に記載された範囲で次が含まれます。

- local-first L0/L1 memory;
- local L3 backend;
- Guardian / TruthGate admission control;
- CanonicalView、TRACE、Receipt;
- evidence span、review queue、import session;
- GDPR 関連の erasure / restriction mechanism;
- deterministic evaluation / CI gate;
- optional FastAPI / MCP surface;
- strict read-only HTTP query path。

この一覧は新しい scope を作りません。現在の `main` と英語 status の要約です。

## Funded delta の要件

funded delta は次を満たす必要があります。

- baseline と明確に区別される;
- measurable acceptance criterion を持つ;
- independent reviewer が再現できる;
- test / evaluation evidence がある;
- TruthGate、provenance、query boundary を弱めない;
- 別 issue / RFC / PR で change control される;
- budget と milestone の正本に一致する。

## Scope に自動追加されないもの

次は、文書や研究 note に存在するだけでは funded scope になりません。

- Titan / Full Personal Exo-Cortex;
- autonomous cognitive OS;
- NoeticCore / AttentionRouter / BICA;
- neuromorphic / biological cognition claim;
- self-modifying agent;
- universal World Knowledge Core;
- production multi-tenant service;
- legal GDPR certification;
- security certification。

## Replay work の分類

Titan の deterministic replay work は prior art として review されています。

```text
REVIEWED_PRIOR_ART
DOCUMENTED_ONLY
M4_CANDIDATE
NO_RUNTIME_CHANGE
NO_CANON_WRITE
NO_BUDGET_CHANGE
BASELINE_NOT_MOVED
```

将来の Crystal implementation は既存 evaluation stack を拡張し、offline、non-authoritative、
separate RFC/PR、baseline fixed の条件を守る必要があります。

## Reviewer が確認する英語正本

1. [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)
2. [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
3. [funding-use-plan.md](../grants/funding-use-plan.md)
4. [evaluation-replay-adoption.md](../grants/evaluation-replay-adoption.md)
5. [STATUS.md](../STATUS.md)
6. [TEST_REPORT.md](../../TEST_REPORT.md)

## 禁止される表現

日本語版でも、英語正本にない次の表現を追加しません。

- 「funding が award された」;
- 「milestone が承認された」;
- 「certified / compliant が保証された」;
- 「production-ready である」;
- 「すべての回答が真実である」;
- 「grant に Titan 全体が含まれる」。

---

> 🌐 🇬🇧 [English](../GRANT_NLNET_SCOPE.md) · 🇩🇪 [Deutsch](../de/GRANT_OVERVIEW.md) · 🇫🇷 [Français](../fr/GRANT_OVERVIEW.md) · 🇪🇸 [Español](../es/GRANT_OVERVIEW.md) · 🇮🇹 [Italiano](../it/GRANT_OVERVIEW.md) · 🇷🇺 [Русский](../ru/GRANT_OVERVIEW.md) · 🇨🇳 [简体中文](../zh-CN/GRANT_OVERVIEW.md) · 🇸🇦 [العربية](../ar/GRANT_OVERVIEW.md) · 🇯🇵 **日本語**
