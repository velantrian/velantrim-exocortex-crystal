<!-- translation-source: docs/REVIEWER_GUIDE.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: zh-CN -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# Reviewer Guide — Velantrim Exo-Cortex Crystal

**英语源 checkpoint：** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`  
本指南是持续维护的审查入口。实现证据仍是 `main` 中的代码、可执行测试、精确 CI、
[TEST_REPORT.md](../../TEST_REPORT.md) 和
[manifest](../status/implementation-manifest.json)。

## 1. 审查对象

Crystal 是面向 AI 系统的公开、local-first、source-grounded、可审计 memory
infrastructure。已验证基线包括 typed claims、Guardian/TruthGate、multi-status L3 上的
strict Canon read projection、read-only public query、分离的 explicit ingest path、
Receipts 与可审计 provenance。

不声称 AGI、意识、普遍真理、零幻觉、active PostgreSQL runtime、automatic switching、
production multi-tenancy、security/GDPR certification 或已获 NLnet grant。

## 2. 复现基线

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

可变 metrics 只从英语测试报告获取。

## 3. Read/write boundary

```text
ask / receipt / MCP inspection → read-only
explicit ingest                → admission-capable write path
curator override               → explicit, attributed, audited
```

公开 `ask` 使用 `core.query_pipeline.query()`，不得修改 facts、ESM、L3、outbox、
episode links、embedding identity 或 unknown candidates。严格 grounding 不足时的
bounded refusal 是预期安全行为。

`ingest` 会写入，但 admission 仍取决于 evidence、claim type、policy 与 TruthGate。
模型输出不能自行认证为 verified world fact。

## 4. Storage 与 migration

SQLite 是普通 active local-first profile。首次 durable `auto` 可在已安装时选择
optional LadybugDB，否则选择 SQLite，并锁定 choice 与 non-secret locator。禁止静默
fallback 到 ephemeral Mock。

PostgreSQL/pgvector 是独立 operator path：verified bundle → version/TLS preflight →
new inactive schema → serializable import → independent read-only re-hash → exact
equivalence；target 保持 `active=false`。

Import/equivalence 不等于 activation、selection、TruthGate admission、strict Canon、
cutover、rollback、dual-write 或 production readiness。

## 5. Security 与 privacy

默认运行不要求 cloud、LLM、telemetry 或 analytics。Remote Neo4j、Anthropic、
Wikidata、Redis、PostgreSQL migration、wider API 或 copied backup/export 仅通过明确
operator choice 扩展边界。

`VELANTRIM_ENCRYPTION_KEY` 保护 selected L1 fields，不自动覆盖全部 L3、backup、
bundle、Receipt、log 或 temporary file。Credentials 与 secret DSN 不得进入 profiles、
bundles、receipts、logs、issues 或 Notion。

从 active local store erasure 不会自动删除 backups、exports、operator copies、remote
systems 或 third-party data。

## 6. Fail-closed checks

- Unsupported claims 被 block、label 或 bounded refusal。
- Profile/locator conflict 在 backend cache 前失败。
- Import failure rollback 并保持 `active=false`。
- Evidence mismatch 与 Receipt/audit tampering 被检测。
- Oversized input 在 limits 处失败。
- Missing optional dependency 不触发 hidden durable switch。
- External exposure 需要 TLS、authentication、least privilege 与 monitoring。

## 7. Checklist

- [ ] 已识别 current `main` 与 exact CI。
- [ ] Read-only query 与 explicit ingest 分离。
- [ ] Physical L3 与 strict Canon 分离。
- [ ] Inactive PostgreSQL import 与 activation 分离。
- [ ] 已审查 network、secrets、encryption 与 erasure limits。
- [ ] 未推断 certification、production readiness 或 grant award。

英语来源：[Reviewer Guide](../REVIEWER_GUIDE.md)、[Security](../../SECURITY.md)、
[Privacy](../../PRIVACY.md)、[Failure Modes](../FAILURE_MODES.md) 与
[Safety Summary](../SAFETY_PRIVACY_AND_FAILURES.md)。
