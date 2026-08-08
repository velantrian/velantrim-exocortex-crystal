<!-- translation-source: docs/STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: it -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# Velantrim Crystal — stato attuale

**Data:** 2026-08-08  
**Checkpoint runtime verificato:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Tree verificato:** `f57e58a6f4d1954b649ba324996fcde42ac287b8`  
**Head validato:** `d7af7c80722274f9217bc5545d150f92e9363f37`  
**PR / CI:** #337 / `31256316536`  
**CI PostgreSQL:** `31256316532`

## Verifica

- Python 3.11: **2078 passed / 13 skipped / 0 failed**;
- Python 3.12: **2078 passed / 13 skipped / 0 failed**;
- **9756 statements / 100.00% line coverage**;
- `core/postgresql_migration.py`: **44/44 statements**;
- `core/postgresql_migration_impl.py`: **336/336 statements**;
- **7/7** mutanti Ring Zero eliminati;
- **9/9** job CI permanenti riusciti;
- **1/1** integrazione reale PostgreSQL/pgvector riuscita.

Evidenza: [TEST_REPORT.md](../../TEST_REPORT.md) e
[manifest](../status/implementation-manifest.json).

## Confine verificato delle capacità

Crystal conserva SQLite local-first e implementa la fase 1 dell’issue #332:

```text
verified completed logical bundle
→ PostgreSQL 16 / pgvector 0.8.2 preflight
→ new inactive target schema
→ serializable import
→ independent read-only canonical target re-hash
→ exact count / byte / SHA-256 equivalence
→ non-secret receipts
```

Il driver PostgreSQL è opzionale e caricato lazy solo da comandi operatore espliciti.
L’installazione predefinita resta standard library pura. Il target importato non entra
nella composizione runtime normale, rimane `active=false` e non serve letture o scritture.

## Confine di autorità

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
migration/import        != TruthGate admission
successful equivalence  != backend activation
```

Guardian, TruthGate, restrictions, TrustSnapshot e CanonicalView restano invariati.

## Ancora assente

- runtime PostgreSQL attivo read/write;
- valutazione exact-vs-ANN e soglie ANN accettate;
- attivazione, cutover, fencing, rollback o dual-write;
- ciclo backup/restore/upgrade, pooling produttivo e fencing distribuito;
- IdP/multi-tenancy produttivo o certificazione legale, sicurezza o GDPR;
- Reader Core verificato dedicato.

## Stato del grant

Il progetto è stato presentato ed è in revisione. **Non viene dichiarata alcuna
assegnazione né modifica del budget.** PR #337 e issue #332 sono già baseline unita e
non possono essere conteggiati di nuovo come lavoro futuro finanziato.
