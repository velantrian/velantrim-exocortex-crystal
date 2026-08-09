<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: it -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Limiti dello storage e dell’autorità

## Identità separate

```text
storage profile = identità di deployment
physical L3 = stato a grafo multi-stato
strict Canon = proiezione di lettura affidabile
migration bundle = prova di integrità operativa
retrieval score = segnale di ranking
model output = testo generato
```

Nessuna identità conferisce automaticamente l’autorità di un’altra.

## Profilo durevole

SQLite è il profilo attivo local-first ordinario. Un primo `auto` durevole può scegliere LadybugDB opzionale o SQLite e bloccare backend e locator non segreto. I conflitti successivi falliscono in modalità fail-closed. Mock resta solo uno stato esplicito di sviluppo/CI.

## physical L3 e strict Canon

physical L3 può contenere VERIFIED, USER_CLAIMED, UNVERIFIED, HYPOTHESIS, SUBJECTIVE, contested, superseded o restricted. strict Canon è una proiezione deny-dominant basata su evidenze e policy correnti. Storage, retrieval o punteggio alto non bastano.

## Lettura e scrittura

Le query pubbliche passano read-only da `core.query_pipeline.query()`. `ingest` esplicito è il percorso capace di scrivere; Guardian e TruthGate applicano poi i limiti strutturali ed epistemici.

## Ciclo SQLite e migrazione

Sono implementati backup, verifica indipendente, inactive restore, logical export deterministico limitato e verifica del bundle. I dataset physical-L3 approvati possono essere importati in un nuovo schema PostgreSQL inattivo e confrontati esattamente; il target resta `active=false`.

Non è una migrazione completa di L1, audit/outbox, metadati di cifratura, configurazione o copie indipendenti. Non esistono runtime PostgreSQL attivo, accettazione ANN, switching automatico, cutover, fencing, rollback o dual-write.

## Segreti e copie

Password, token, chiavi private e DSN con credenziali non devono entrare in profiles, bundles, receipts, logs, GitHub o Notion. Backup, export e migrazioni creano altre copie; cancellare lo store attivo non le elimina automaticamente. La cifratura selettiva dei campi L1 non è universale.

## Evidenza operativa

| Evento | Prova | Non prova |
|---|---|---|
| record in L3 | persistenza fisica | appartenenza a strict Canon |
| risultato retrieval | rilevanza candidata | evidenza sufficiente |
| backup verificato | integrità backup | verità del claim |
| import riuscito | integrità import | activation o selezione runtime |
| exact equivalence | uguaglianza dataset approvati | prontezza produttiva o cutover |

Il Reader Core dedicato non è implementato; NLnet resta submitted / under review / not awarded.

## Contratti inglesi dettagliati

- [Architettura completa](../ARCHITECTURE.md)
- [Profilo storage durevole](../architecture/DURABLE_STORAGE_PROFILE.md)
- [Contratto di migrazione](../architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Import PostgreSQL inattivo](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [ADR-021](../adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)
