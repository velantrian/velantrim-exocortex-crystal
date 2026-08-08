<!-- translation-source: docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: it -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# Confini di sicurezza, privacy e fallimento

**Fonte:** `docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`

Questa panoramica non sostituisce test, security review o consulenza legale.

## Sicurezza epistemica

```text
physical L3 != strict Canon
retrieval score != evidence
model output != verified fact
migration bundle != claim evidence
successful import != activation
```

Guardian e TruthGate restano confini di ammissione. Le query pubbliche sono read-only;
l’ingest esplicito è il percorso di scrittura separato. Crystal non garantisce verità o zero
allucinazioni: il materiale non supportato deve essere bloccato, etichettato, rifiutato o
auditabile.

## Confine locale

L’installazione default non richiede cloud, LLM, telemetry o analytics. SQLite è il profilo
attivo ordinario. `auto` durable può scegliere LadybugDB opzionale o SQLite e blocca la
scelta; Mock resta stato dev/test esplicito. PostgreSQL/pgvector è solo target operatore
inattivo con `active=false`.

## Dati ed espansione opzionale

Possono essere memorizzati claims, metadata, provenance, stato epistemico, grafo,
restrictions, registri erasure/audit, Receipts, outbox, bundles, backups ed exports. I dati
escono dal confine locale solo con Anthropic, Neo4j remoto, Wikidata, Redis, migrazione
PostgreSQL, API ampia o copie esterne attivate esplicitamente.

## Encryption e secrets

`VELANTRIM_ENCRYPTION_KEY` protegge campi L1 selezionati, non automaticamente L3, backups,
exports, Receipts, logs o temporanei. Servono cifratura host e gestione chiavi. Credentials
non devono entrare in profiles, bundles, receipts, logs, issues o Notion.

## API, privacy ed erasure

Il baseline API usa authentication e loopback. L’esposizione esterna richiede TLS,
autenticazione revisionata, least privilege, limiti, monitoring e incident handling. Access,
rectification, restriction, erasure e processing record sono controlli tecnici, non
certificazione GDPR. Cancellare lo store attivo non cancella globalmente le copie.

## Reazioni sicure ai fallimenti

| Classe | Comportamento atteso |
|---|---|
| Claim non supportato | block, label o bounded refusal |
| Mutazione read-only | reject / nessun cambio |
| Conflitto profile | errore prima della cache backend |
| Dependency assente | errore esplicito, senza Mock nascosto |
| Import fallisce | rollback, `active=false` |
| Evidence mismatch | verification failure |
| Manomissione Receipt/audit | errore digest/hash |
| Migrazione troppo grande | fail closed ai limiti |
| Esposizione rete | solo esplicita e autenticata |
| Copia dopo erasure | inventario e cancellazione separati |

## Non-dichiarazioni

Crystal non è certificazione security/legal/GDPR, prova di scala arbitraria, runtime
PostgreSQL attivo, sistema di migrazione automatica, garanzia di verità perfetta,
AGI/coscienza o prova di grant NLnet assegnato.

Dettagli: [Security](../../SECURITY.md), [Privacy](../../PRIVACY.md), [GDPR](../../GDPR.md),
[Failure Modes](../FAILURE_MODES.md) e [riepilogo inglese](../SAFETY_PRIVACY_AND_FAILURES.md).
