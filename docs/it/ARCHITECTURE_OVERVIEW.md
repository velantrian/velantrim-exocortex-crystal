<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: it -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Crystal — panoramica dell’architettura

Questa traduzione è uno strato di orientamento. In caso di conflitto prevalgono codice merged, test eseguibili, CI esatto e contratti inglesi.

## Modello centrale

```text
fonti + ingest esplicito
→ provenienza + normalizzazione
→ controlli Guardian
→ decisione TruthGate
→ stato operativo L1 + physical L3 multi-stato
→ proiezione di lettura strict Canon deny-dominant
→ retrieval read-only / risposta / rifiuto limitato
```

Un record in physical L3 non appartiene automaticamente a strict Canon. Punteggio di retrieval, similarità vettoriale e testo del modello non sono prove indipendenti.

## Livelli di memoria e revisione

- **L0:** contesto effimero del processo.
- **L1:** SQLite/WAL per stato operativo, evidenze, audit, receipts, sessioni import/review e outbox.
- **L2:** staging pending/review per candidati o quarantena; non è uno strato di verità finale.
- **L3:** storage a grafo multi-stato; distinto da strict Canon.
- **TrustSnapshot / CanonicalView:** superficie di lettura affidabile deny-dominant.

## Separazione lettura/scrittura

`HTTP /ask`, `CLI ask` e MCP passano read-only da `core.query_pipeline.query()`. Una query non può creare o rafforzare fatti né modificare ESM, L3, outbox, legami episodici o identità dell’embedder. Solo `ingest` esplicito entra nel percorso di scrittura governato da Guardian e TruthGate.

## Profili e portabilità

SQLite è il profilo attivo local-first ordinario. Al primo `auto` durevole può essere scelto LadybugDB opzionale oppure SQLite, quindi backend e locator non segreto vengono bloccati. Il fallback silenzioso a Mock effimero è vietato.

Il percorso PostgreSQL/pgvector verificato termina in un target inattivo:

```text
bundle SQLite verificato
→ import PostgreSQL transazionale
→ re-hash indipendente read-only
→ equivalenza esatta
→ active=false
```

Import o equivalenza non sono activation, scelta backend, ammissione TruthGate, cutover, rollback o dual-write. PostgreSQL non è nella normale composizione runtime.

## Lettura dei documenti

Source spans, record documento, sessioni di import e flussi dry-run/review sono baseline implementata. Non è implementato un Reader Core dedicato multi-pass con mappe di copertura, rilettura sensibile alle contraddizioni e sintesi documentale.

## Non-rivendicazioni

Crystal non dichiara AGI, coscienza, zero allucinazioni, runtime PostgreSQL attivo, switching automatico, ANN accettato per produzione, cutover/rollback/dual-write, certificazione sicurezza/legale/GDPR o grant NLnet assegnato.

## Fonti inglesi

- [Architettura completa](../ARCHITECTURE.md)
- [Limiti storage/autorità](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Stato di implementazione](../IMPLEMENTATION_STATUS.md)
- [Import PostgreSQL inattivo](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
