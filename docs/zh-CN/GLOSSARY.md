# 📖 术语表 — Velantrim Crystal 简体中文

> 🌐 🇬🇧 [English](../ARCHITECTURE.md) · 🇩🇪 [Deutsch](../de/GLOSSARY.md) · 🇫🇷 [Français](../fr/GLOSSARY.md) · 🇪🇸 [Español](../es/GLOSSARY.md) · 🇮🇹 [Italiano](../it/GLOSSARY.md) · 🇷🇺 [Русский](../ru/GLOSSARY.md) · 🇨🇳 **简体中文**
>
> 本术语表统一简体中文技术表达，不替代英文 API、schema 或 code identifier。
> Code block 与 interface 中的名称保持不变。

## 总则

`TruthGate`、`Guardian`、`CanonicalView`、`TRACE` 与 `Receipt` 保留原名。
首次出现时可附中文解释，但代码合同名称不翻译。

| 英文术语 | 建议中文表达 | 含义与限制 |
|---|---|---|
| **admission** | 准入 / 进入决策 | 决定 claim 是否可进入更可信 memory state |
| **claim** | claim / 类型化断言 | 结构化陈述，不自动等于 verified fact |
| **Canon** | Canon / 规范事实投影 | TRACE 有效、policy 允许且已准入的严格投影 |
| **canonical graph** | canonical graph / 规范图 | 保存已准入对象与显式状态的 L3 graph |
| **Guardian** | Guardian / 结构与安全检查 | 前置检查，不替代 TruthGate |
| **TruthGate** | TruthGate / 认识论准入边界 | 根据类型、source、evidence 与 policy 控制自动准入 |
| **CanonicalView** | CanonicalView / 规范只读视图 | 用于严格 grounded answer 的 fail-closed 投影 |
| **TRACE** | TRACE / justification path | 机器可读的回答依据链 |
| **Receipt** | Receipt / sealed proof | 可 replay、可检测 tampering 的 fact 与 provenance proof |
| **receipt replay** | Receipt 重放 | 对当前 memory state 重新验证 Receipt |
| **trajectory replay** | trajectory 重放 | 为 evaluation 重复 execution path；不同于 Receipt replay |
| **provenance** | 来源链 / 可追踪来源 | claim 的 source、creation process 与 lifecycle |
| **evidence span** | Evidence Span / 证据片段 | source 中支撑 claim 的可引用片段 |
| **epistemic state** | 认识论状态 | 表示 claim 的资格状态，不只是 confidence score |
| **source status** | 来源状态 | external、user、model output 等来源类别 |
| **grounding** | 证据锚定 / grounding | 把 answer 连接到已准入 claim 与 source |
| **FactsPack** | FactsPack / 受控事实包 | 用于生成回答的紧凑、可追踪 context |
| **read-only query** | 只读查询 | 明确排除列出的 memory 与 state mutation |
| **fail-closed** | 不确定时拒绝 | 信任模糊或冲突时不静默准入 |
| **baseline** | baseline / 基线 | funded delta 前已实现并验证的工作 |
| **funded delta** | funded delta / 资助增量 | 通过 funding 交付的可测量新增工作 |
| **deliverable** | 可验证 deliverable | 具有 acceptance evidence 的公开 artifact |
| **local-first** | 本地优先 | 默认本地 data 与 execution；外部服务可选 |
| **stdlib-only runtime** | 默认标准库 runtime | 默认路径不强制第三方 runtime dependency |
| **restriction** | 处理限制 | 对 stored object 使用方式的技术限制 |
| **erasure** | 删除 | 按设计层级执行 removal，并保留必要 audit/tombstone 规则 |
| **review queue** | review queue / 审核队列 | curator decision 前的 pending 或 blocked claim 区域 |
| **curator override** | 显式 curator override | 可归因且可 audit 的人工决策，不是静默 bypass |
| **provider independence** | provider independence | 外部 model 可替换且可选，不具 truth authority |

## ⚠️ 谨慎使用的词

### “已验证”

不是 graph 中每个节点都是 verified Canon。只有 state、evidence、TRACE 与 policy
都支持时才使用该表述。

### “符合 GDPR”

建议表达：

```text
与 GDPR 相关的技术控制
面向 GDPR 的架构
```

没有法律依据时避免：

```text
GDPR 认证
保证完全法律合规
```

### “安全”或 “hardened”

“Hardened”表示有文档记录的技术措施与测试，不是 security certification，
也不证明不存在 vulnerability。

### “真相”

`TruthGate` 不是 universal truth detector，而是在定义明确的数据模型与 policy
中的 epistemic admission boundary。

### “Replay”

始终区分：

```text
Receipt replay    = 重新验证已有 proof
Trajectory replay = 为 evaluation 重复 execution path
```

### “认知”“生命”“意识”

这些词不描述当前 Crystal runtime capability。Bio-inspired 名称是 engineering
metaphor，不是生物或人格 claim。

## 中文文档风格

优先使用：

- 短句与可验证表述；
- backtick 中保持 code identifier 不变；
- 清晰区分“已实现”“可选”“计划”“研究”；
- 不让翻译比英文来源更强；
- 数字附权威来源；
- reviewer-oriented 语言而非模糊 marketing。

---

> 🌐 🇬🇧 [English](../ARCHITECTURE.md) · 🇩🇪 [Deutsch](../de/GLOSSARY.md) · 🇫🇷 [Français](../fr/GLOSSARY.md) · 🇪🇸 [Español](../es/GLOSSARY.md) · 🇮🇹 [Italiano](../it/GLOSSARY.md) · 🇷🇺 [Русский](../ru/GLOSSARY.md) · 🇨🇳 **简体中文**