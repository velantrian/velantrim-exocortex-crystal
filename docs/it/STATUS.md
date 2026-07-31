# 📌 Velantrim Crystal — Stato attuale

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 [Español](../es/STATUS.md) · 🇮🇹 **Italiano** · 🇷🇺 [Русский](../ru/STATUS.md)

**Data dello stato:** 30 luglio 2026  
**Stato del repository usato per questa traduzione:** `main@dee0b9a0`  
**Ultimo checkpoint che modifica il runtime:** PR #265 / `cd6fd44`  
**Baseline di test normativa:** [TEST_REPORT.md](../../TEST_REPORT.md)

> Questa pagina è una traduzione dello stato. In caso di divergenza, GitHub
> `main`, lo [STATUS inglese](../STATUS.md) e
> [TEST_REPORT.md](../../TEST_REPORT.md) fanno autorità.

---

## 🧭 Regola di lettura

```text
GitHub Crystal main = verità pubblica dell’implementazione
Notion Crystal       = mappa grant e strategica sincronizzata
Titan / Full         = laboratorio di ricerca separato
```

Un documento, una nota Notion, un branch prototipo o un modulo Titan non è una
capacità Crystal attuale finché non viene implementato, testato e fuso in
Crystal `main`.

## ✅ Checkpoint verificato

Il PR #265 ha introdotto il confine di query HTTP strettamente in lettura:

```text
POST /ingest   → ammissione tramite Guardian + TruthGate
POST /ask      → query canonica strettamente in lettura
GET  /receipt  → lettura stretta con Receipt
```

Gli endpoint HTTP `/ask` e `/receipt` non scrivono in L0/L1 o L3, non modificano
ESM, non operano l’outbox, non registrano collegamenti episodici, non
inizializzano un embedding fingerprint e non cambiano la verifica adattiva.

### Limiti residui espliciti

- CLI `ask` e `receipt` restano su `core.pipeline.run()`;
- `core.pipeline.run()` resta un percorso di compatibilità capace di ammissione;
- MCP non possiede strumenti espliciti di scrittura canonica, ma una ricerca può
  inizializzare un embedding fingerprint assente.

Questi elementi sono follow-up noti, non capacità nascoste.

## 🧪 Baseline di verifica

```text
1713 passed
12 skipped
0 failed
6389 measured statements
100.00% coverage
```

Il run CI `30284938992` ha completato con successo i sette job permanenti prima
del merge: Python 3.11/3.12, Ruff, security, Docker build, evaluation gate e
integrità JSONL.

## 🛡️ Confine dei claim pubblici

Crystal può essere descritto come:

- infrastruttura di memoria IA locale e verificabile;
- nucleo orientato a fonti e provenienza;
- sistema con controlli Guardian e TruthGate dove collegati;
- sistema con CanonicalView, TRACE e Receipt riproducibili dove collegati;
- runtime predefinito basato sulla libreria standard con adapter opzionali;
- progetto con meccanismi tecnici di cancellazione e restrizione rilevanti per il GDPR;
- baseline open source di livello ricerca, verificabile indipendentemente.

Crystal non deve essere descritto come:

- Titan o il Personal ExoCortex completo;
- sistema operativo cognitivo autonomo;
- cosciente, vivo o biologicamente equivalente a un cervello;
- universalmente vero o privo di allucinazioni;
- legalmente certificato GDPR;
- certificato per la sicurezza o pronto per hosting multi-tenant in produzione;
- dipendente da un LLM esterno o provider cloud obbligatorio.

## 💶 Stato della sovvenzione

La proposta al **NLnet NGI0 Commons Fund** è stata presentata ed è in fase di
valutazione. Il repository non afferma che il finanziamento sia stato assegnato.

```text
BASELINE ATTUALE
    +
DELTA FINANZIATO MISURABILE
    =
DELIVERABLE VERIFICABILE INDIPENDENTEMENTE
```

Il lavoro già fuso resta baseline e non viene ricontato come milestone pagata.
Le regole normative sono mantenute in:

- [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)
- [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
- [funding-use-plan.md](../grants/funding-use-plan.md)

Una sintesi italiana si trova in [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md).

## 🧪 Decisione sull’evaluation replay

L’implementazione di replay deterministico di Titan è stata riesaminata come
lavoro precedente. Non è stata copiata nel runtime Crystal.

```text
REVIEWED_PRIOR_ART
DOCUMENTED_ONLY
M4_CANDIDATE
NO_RUNTIME_CHANGE
NO_CANON_WRITE
NO_BUDGET_CHANGE
BASELINE_NOT_MOVED
```

Una futura implementazione deve estendere lo stack di valutazione Crystal
esistente, passare attraverso RFC/issue/PR separati, restare offline e non
autoritativa e preservare TruthGate e i confini di query.

## 🔬 Regola per ricerca e PR draft

PR aperti di ricerca o branding non sono verità dell’implementazione. Prima del
merge devono essere ribasati sull’attuale `main`, riesaminati per il linguaggio
grant e verificati rispetto allo stato normativo.

## 📚 Percorso reviewer

1. [REVIEWER_GUIDE.md](./REVIEWER_GUIDE.md)
2. [QUICKSTART.md](./QUICKSTART.md)
3. [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md)
4. [GLOSSARY.md](./GLOSSARY.md)
5. [Stato inglese normativo](../STATUS.md)
6. [TEST_REPORT.md](../../TEST_REPORT.md)

---

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 [Español](../es/STATUS.md) · 🇮🇹 **Italiano** · 🇷🇺 [Русский](../ru/STATUS.md)