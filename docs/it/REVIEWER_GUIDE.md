<!-- translation-source: docs/REVIEWER_GUIDE.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: it -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# Guida per revisori — Velantrim Exo-Cortex Crystal

**Checkpoint inglese:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`  
Questa guida è un orientamento mantenuto. Le prove di implementazione restano codice in
`main`, test eseguibili, CI esatto, [TEST_REPORT.md](../../TEST_REPORT.md) e
[manifest](../status/implementation-manifest.json).

## 1. Oggetto della revisione

Crystal è infrastruttura pubblica, local-first, source-grounded e verificabile per memoria
di sistemi IA. La base comprende claim tipizzati, Guardian/TruthGate, proiezione strict Canon
sopra L3 multi-status, query pubbliche read-only, percorso ingest esplicito separato,
Receipts e provenance auditabile.

Non dichiara AGI, coscienza, verità universale, zero allucinazioni, runtime PostgreSQL attivo,
switching automatico, multi-tenancy produttivo, certificazione security/GDPR o grant NLnet
assegnato.

## 2. Riprodurre la baseline

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

Le metriche mutevoli sono mantenute solo nel report di test inglese.

## 3. Confine lettura/scrittura

```text
ask / receipt / MCP inspection → read-only
explicit ingest                → admission-capable write path
curator override               → esplicito, attribuito e auditato
```

Il `ask` pubblico usa `core.query_pipeline.query()` e non deve mutare facts, ESM, L3,
outbox, episode links, identità embedding o candidati sconosciuti. Un rifiuto limitato con
grounding insufficiente è comportamento sicuro previsto.

`ingest` scrive, ma admission dipende da evidence, tipo di claim, policy e TruthGate.
L’output del modello non può autocertificarsi come fatto mondiale verificato.

## 4. Storage e migrazione

SQLite è il profilo attivo local-first ordinario. Il primo `auto` durable può scegliere
LadybugDB opzionale se installato, altrimenti SQLite; scelta e locator non segreto vengono
bloccati. Il fallback silenzioso a Mock effimero è vietato.

PostgreSQL/pgvector è un percorso operatore separato: bundle verificato → preflight
versione/TLS → nuovo schema inattivo → import serializzabile → re-hash indipendente read-only
→ equivalenza esatta; il target resta `active=false`.

Import/equivalence non è activation, selection, TruthGate admission, strict Canon,
cutover, rollback, dual-write o production readiness.

## 5. Sicurezza e privacy

Il default non richiede cloud, LLM, telemetry o analytics. Neo4j remoto, Anthropic,
Wikidata, Redis, migrazione PostgreSQL, API ampia o copie backup/export estendono il confine
solo per scelta operatore.

`VELANTRIM_ENCRYPTION_KEY` protegge campi L1 selezionati, non automaticamente ogni L3,
backup, bundle, Receipt, log o temporaneo. Credentials e DSN segreti non devono entrare in
profiles, bundles, receipts, logs, issues o Notion.

La cancellazione dal local store attivo non elimina automaticamente backups, exports,
copie operatore, sistemi remoti o dati terzi.

## 6. Fallimenti fail-closed

- Claim non supportati bloccati, etichettati o rifiutati in modo limitato.
- Conflitti profile/locator falliscono prima della cache backend.
- Fallimento import esegue rollback e mantiene `active=false`.
- Evidence mismatch e manomissione Receipt/audit vengono rilevati.
- Input troppo grande fallisce ai limiti.
- Dependency opzionale assente non causa switch durable nascosto.
- Esposizione esterna richiede TLS, authentication, least privilege e monitoring.

## 7. Checklist

- [ ] `main` e CI esatto identificati.
- [ ] Query read-only distinta da ingest esplicito.
- [ ] L3 fisico distinto da strict Canon.
- [ ] Import PostgreSQL inattivo distinto da activation.
- [ ] Rete, secrets, encryption ed erasure verificati.
- [ ] Nessuna certification, production readiness o grant award dedotta.

Fonti inglesi: [Reviewer Guide](../REVIEWER_GUIDE.md), [Security](../../SECURITY.md),
[Privacy](../../PRIVACY.md), [Failure Modes](../FAILURE_MODES.md) e
[Safety Summary](../SAFETY_PRIVACY_AND_FAILURES.md).
