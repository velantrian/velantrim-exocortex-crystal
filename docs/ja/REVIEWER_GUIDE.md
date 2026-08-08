<!-- translation-source: docs/REVIEWER_GUIDE.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: ja -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# Reviewer Guide — Velantrim Exo-Cortex Crystal

**英語 source checkpoint:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`  
このガイドは保守された案内です。実装 evidence は `main` の code、実行可能 test、
exact CI、[TEST_REPORT.md](../../TEST_REPORT.md)、
[manifest](../status/implementation-manifest.json) です。

## 1. Review 対象

Crystal は AI system 向けの public、local-first、source-grounded、auditable memory
infrastructure です。verified baseline は typed claims、Guardian/TruthGate、multi-status
L3 上の strict Canon read projection、read-only public query、分離された explicit
ingest path、Receipts、auditable provenance を含みます。

AGI、consciousness、universal truth、zero hallucinations、active PostgreSQL runtime、
automatic switching、production multi-tenancy、security/GDPR certification、awarded
NLnet grant は主張しません。

## 2. Baseline 再現

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

変動する metrics は英語 test report から確認します。

## 3. Read/write boundary

```text
ask / receipt / MCP inspection → read-only
explicit ingest                → admission-capable write path
curator override               → explicit, attributed, audited
```

公開 `ask` は `core.query_pipeline.query()` を使い、facts、ESM、L3、outbox、episode
links、embedding identity、unknown candidates を変更しません。strict grounding 不足時の
bounded refusal は期待される安全動作です。

`ingest` は write ですが、admission は evidence、claim type、policy、TruthGate に依存。
model output は自身を verified world fact と認定できません。

## 4. Storage と migration

SQLite は通常の active local-first profile。最初の durable `auto` は optional
LadybugDB があれば選択し、なければ SQLite を選択して choice と non-secret locator
を lock します。ephemeral Mock への silent fallback は禁止です。

PostgreSQL/pgvector は別の operator path: verified bundle → version/TLS preflight →
new inactive schema → serializable import → independent read-only re-hash → exact
equivalence。target は `active=false` のままです。

Import/equivalence は activation、selection、TruthGate admission、strict Canon、
cutover、rollback、dual-write、production readiness ではありません。

## 5. Security と privacy

Default operation は cloud、LLM、telemetry、analytics を必須としません。Remote
Neo4j、Anthropic、Wikidata、Redis、PostgreSQL migration、wide API、backup/export copy
は explicit operator choice で boundary を広げます。

`VELANTRIM_ENCRYPTION_KEY` は selected L1 fields を保護しますが、すべての L3、
backup、bundle、Receipt、log、temporary file を自動保護しません。credentials と
secret DSN を profiles、bundles、receipts、logs、issues、Notion に入れてはいけません。

Active local store の erasure は backups、exports、operator copies、remote systems、
third-party data を自動削除しません。

## 6. Fail-closed checks

- Unsupported claim は block、label、bounded refusal。
- Profile/locator conflict は backend cache 前に failure。
- Import failure は rollback し `active=false` を維持。
- Evidence mismatch、Receipt/audit tampering を検出。
- Oversized input は limits で failure。
- Missing optional dependency は hidden durable switch を起こさない。
- External exposure は TLS、authentication、least privilege、monitoring が必要。

## 7. Checklist

- [ ] Current `main` と exact CI を確認。
- [ ] Read-only query と explicit ingest を分離。
- [ ] Physical L3 と strict Canon を分離。
- [ ] Inactive PostgreSQL import と activation を分離。
- [ ] Network、secrets、encryption、erasure limits を確認。
- [ ] Certification、production readiness、grant award を推論しない。

English sources: [Reviewer Guide](../REVIEWER_GUIDE.md), [Security](../../SECURITY.md),
[Privacy](../../PRIVACY.md), [Failure Modes](../FAILURE_MODES.md),
[Safety Summary](../SAFETY_PRIVACY_AND_FAILURES.md).
