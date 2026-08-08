<!-- d2-source-contract: CURRENT -->
<!-- d2-source-scope: reviewer-security-privacy-failure -->
# Reviewer Guide — Velantrim Exo-Cortex Crystal

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](./fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](./es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](./it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](./ru/REVIEWER_GUIDE.md) · 🇨🇳 [简体中文](./zh-CN/REVIEWER_GUIDE.md) · 🇸🇦 [العربية](./ar/REVIEWER_GUIDE.md) · 🇯🇵 [日本語](./ja/REVIEWER_GUIDE.md) · 🇮🇳 [हिन्दी](./hi/REVIEWER_GUIDE.md)

**Status date:** 2026-08-08  
**Purpose:** a fast, evidence-linked review path.  
**Authority:** this guide summarizes; merged code, executable tests, exact CI,
[`TEST_REPORT.md`](../TEST_REPORT.md) and the
[implementation manifest](./status/implementation-manifest.json) are the evidence sources.

## 1. What Crystal is

Crystal is public, local-first, source-grounded and auditable memory infrastructure for AI
systems. Its current verified baseline includes:

- typed claims and explicit epistemic state;
- Guardian and TruthGate admission boundaries;
- a deny-dominant strict Canon read projection over multi-status physical L3 storage;
- read-only public query surfaces and a separate explicit ingest/write path;
- tamper-evident receipts, audit records and provenance mechanisms;
- SQLite as the ordinary active local-first profile;
- bounded logical export plus optional inactive PostgreSQL/pgvector import and exact-state
  equivalence with `active=false`.

## 2. What Crystal is not

Crystal does **not** claim:

- AGI, consciousness or biological-brain equivalence;
- universal truth or zero hallucinations;
- that every graph node belongs to strict Canon;
- an active PostgreSQL runtime backend;
- automatic backend switching, cutover, rollback or dual-write;
- production multi-tenancy, legal certification, security certification or GDPR certification;
- that NLnet funding has been awarded;
- that research/RFC concepts are current runtime capabilities.

Use [`STATUS.md`](./STATUS.md) and
[`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md) for the canonical implemented/future
split. If a capability is absent there, treat it as not implemented.

## 3. Reproduce the verified baseline

From a clean clone:

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

Exact mutable counts belong only in [`TEST_REPORT.md`](../TEST_REPORT.md) and the manifest;
this guide intentionally does not duplicate them.

## 4. Verify the read/write authority boundary

```text
ask / receipt / MCP inspection → read-only
explicit ingest                → admission-capable write path
curator override               → explicit, attributed and audited governance action
```

Public `ask` routes through `core.query_pipeline.query()` and must not mutate facts, ESM,
L3, outbox state, episode links, embedding identity or unknown candidates. A bounded refusal
when strict grounding is insufficient is expected safety behaviour.

`ingest` is a write path. Admission still depends on evidence, claim type, policy and
TruthGate; model output cannot certify itself as a verified world fact.

Useful checks:

```bash
velantrim invariant-check
velantrim receipt "your question" > receipt.json
velantrim verify-receipt receipt.json --strict-provenance
velantrim audit-verify
```

`invariant-check` scans at-rest state; it is not by itself proof of admission-time rejection.
The behaviour pins live in executable tests such as `tests/test_truth_gate.py` and
`tests/test_read_only_query_boundary.py`.

## 5. Verify storage and migration boundaries

The ordinary documented profile is SQLite. A first durable `auto` selection may choose the
optional LadybugDB backend when installed, otherwise SQLite, and then persists the winner in
a durable storage profile. It must not silently fall back to ephemeral Mock.

PostgreSQL/pgvector support is a separate operator migration path:

```text
verified logical bundle
→ supported-version/TLS preflight
→ new inactive target schema
→ serializable import
→ independent read-only canonical re-hash
→ exact equivalence receipt
→ target remains active=false
```

Successful import or equivalence is operation evidence, not activation, backend selection,
TruthGate admission, strict Canon membership or production readiness.

Read:

- [Durable storage profile](./architecture/DURABLE_STORAGE_PROFILE.md)
- [SQLite lifecycle](./architecture/SQLITE_STORAGE_LIFECYCLE.md)
- [Inactive PostgreSQL import](./architecture/POSTGRESQL_INACTIVE_IMPORT.md)

## 6. Review security and deployment

For the optional HTTP service:

```bash
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
docker compose up --build
curl http://127.0.0.1:8000/health
```

Check that:

- startup fails closed without the required token;
- the published default is host-loopback only;
- the container runs as a non-root user;
- secrets and local databases are excluded from the image and repository;
- wider network exposure is fronted by TLS, authentication, least privilege and monitoring;
- PostgreSQL credentials or credential-bearing DSNs never enter profiles, bundles, receipts,
  logs, issues or Notion;
- test-only localhost `trust` authentication is not copied into deployment guidance.

Read [`SECURITY.md`](../SECURITY.md),
[the threat model](./security/threat-model.md) and
[deployment security](./security/DEPLOYMENT_SECURITY.md).

## 7. Review privacy and data lifecycle

Default operation has no telemetry, analytics or phone-home behaviour. Data leaves the local
trust boundary only when an operator explicitly enables an external/networked adapter,
remote backend, API exposure or migration target.

Review:

- what is stored in L0/L1/L3, receipts, audit records, bundles and backups;
- optional encryption coverage and its limits;
- access, rectification, restriction and erasure operations;
- copies outside the active store, including backups, exports and remote systems;
- network exposure and optional third-party processing.

Read [`PRIVACY.md`](../PRIVACY.md), [`GDPR.md`](../GDPR.md) and the
[D2 safety/privacy/failure summary](./SAFETY_PRIVACY_AND_FAILURES.md).

## 8. Review failure behaviour

A reviewer should test fail-closed outcomes, not only successful paths:

- unsupported or self-certified claims are blocked, labelled or refused;
- malformed storage profiles and locator conflicts fail before backend caching;
- import errors roll back before activation and do not expose raw credentials;
- incomplete evidence produces abstention rather than invented grounding;
- receipt or audit tampering is detected;
- resource and size limits reject oversized migration input;
- unavailable optional dependencies fail with explicit bounded errors;
- privacy-sensitive network or storage expansion requires operator action.

The current matrix is [`FAILURE_MODES.md`](./FAILURE_MODES.md).

## 9. Grant and evidence boundary

The project is submitted and under review. It is **not awarded**, and no budget change is
claimed. Merged baseline work cannot be counted again as future funded delivery.

Read [`GRANT_NLNET_SCOPE.md`](./GRANT_NLNET_SCOPE.md) and the
[baseline/funded-delta matrix](./grants/baseline-funded-delta-matrix.md).

## 10. Review checklist

- [ ] Current `main` and exact CI evidence identified.
- [ ] Tests and docs-status reproduced or independently inspected.
- [ ] Read-only query boundary distinguished from explicit ingest.
- [ ] Physical L3 distinguished from strict Canon.
- [ ] Inactive PostgreSQL import distinguished from runtime activation.
- [ ] Optional network adapters and deployment exposure identified.
- [ ] Privacy copies, erasure limits and encryption coverage reviewed.
- [ ] Failure-mode and rollback behaviour inspected.
- [ ] Security/GDPR/production certification not inferred.
- [ ] Grant award or budget change not inferred.

---

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](./fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](./es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](./it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](./ru/REVIEWER_GUIDE.md) · 🇨🇳 [简体中文](./zh-CN/REVIEWER_GUIDE.md) · 🇸🇦 [العربية](./ar/REVIEWER_GUIDE.md) · 🇯🇵 [日本語](./ja/REVIEWER_GUIDE.md) · 🇮🇳 [हिन्दी](./hi/REVIEWER_GUIDE.md)
