# 🇨🇳 简体中文文档 — Velantrim Crystal

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/README.md) · 🇫🇷 [Français](../fr/README.md) · 🇪🇸 [Español](../es/README.md) · 🇮🇹 [Italiano](../it/README.md) · 🇷🇺 [Русский](../ru/README.md) · 🇨🇳 **简体中文** · 🇸🇦 [العربية](../ar/README.md) · 🇯🇵 [日本語](../ja/README.md)

## 🔒 翻译与权威规则

这些页面是面向 reviewer、机构和贡献者的维护性简体中文阅读辅助。它们不会
改变 runtime 或 grant scope。

```text
GitHub main + 英文规范文档 = 权威来源
德语、法语、西班牙语、意大利语、俄语和简体中文文档 = 维护性翻译 / reviewer 辅助
```

如有差异，按以下顺序处理：

1. GitHub `main` 中实际已合并的代码；
2. [TEST_REPORT.md](../../TEST_REPORT.md) 中的测试与 coverage 结果；
3. [docs/STATUS.md](../STATUS.md) 中的当前实现状态；
4. 英文 grant 文档中的 scope、budget 与 deliverable。

翻译不得比英文来源更强地描述任何 capability。“面向 GDPR”“hardened”
“可验证”“本地”等词是技术描述，不是法律或安全认证。

---

## 🧭 推荐阅读顺序

| 顺序 | 文档 | 用途 |
|---:|---|---|
| 1 | [简体中文 README](../../README.zh-CN.md) | 项目、边界与架构概览 |
| 2 | [Reviewer 指南](./REVIEWER_GUIDE.md) | 外部 reviewer 的验证路线 |
| 3 | [快速开始](./QUICKSTART.md) | 安装、测试、CLI 与可选 API |
| 4 | [当前状态](./STATUS.md) | 实现与 public claim 边界 |
| 5 | [Grant 概览](./GRANT_OVERVIEW.md) | grant-safe 中文摘要 |
| 6 | [术语表](./GLOSSARY.md) | 一致的技术术语 |

---

## 📚 英文权威文档

| 文档 | 权威内容 |
|---|---|
| [README.md](../../README.md) | 公开入口与当前核心 claim |
| [TEST_REPORT.md](../../TEST_REPORT.md) | 可复现测试与 coverage baseline |
| [docs/STATUS.md](../STATUS.md) | 当前实现状态 |
| [docs/REVIEWER_GUIDE.md](../REVIEWER_GUIDE.md) | 英文 reviewer 路径 |
| [docs/ARCHITECTURE.md](../ARCHITECTURE.md) | 架构与 memory boundary |
| [docs/EVAL.md](../EVAL.md) | evaluation 方法 |
| [docs/GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md) | 已提交的 grant scope |
| [Baseline / Delta Matrix](../grants/baseline-funded-delta-matrix.md) | milestone 与 acceptance evidence |
| [Funding Use Plan](../grants/funding-use-plan.md) | budget 与优先级 |

---

## 🛠️ 维护约定

```text
1. 先更新并合并英文来源
2. 确认新的 main 状态
3. 在独立 docs-only PR 中同步翻译
4. 不在翻译中单独引入新数字或新 claim
```

本简体中文包基于 Crystal `main@14bc0659`。最后一个改变 runtime 的 checkpoint
仍是 PR #265 / `cd6fd44`。

---

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/README.md) · 🇫🇷 [Français](../fr/README.md) · 🇪🇸 [Español](../es/README.md) · 🇮🇹 [Italiano](../it/README.md) · 🇷🇺 [Русский](../ru/README.md) · 🇨🇳 **简体中文** · 🇸🇦 [العربية](../ar/README.md) · 🇯🇵 [日本語](../ja/README.md)