# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 **Italiano** · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### Infrastruttura di memoria verificabile e local-first per sistemi di IA affidabili

`v0.3.0` · 🧪 **1853 test superati / 12 ignorati** · 🎯 **copertura 100%** · 🧬 **7/7 mutanti dichiarati eliminati** · ✅ **9 job CI** · 🐍 **runtime predefinito basato solo sulla libreria standard Python** · ⚖️ **AGPL-3.0**

> Crystal non è un altro chatbot. È un confine per memoria, evidenze e decisioni
> che registra che cosa rappresenta un’affermazione, da dove proviene, il suo
> stato epistemico, se può fondare una risposta e come una contraddizione è stata
> risolta esplicitamente.

**Checkpoint runtime verificato:** `f91299c44a1a1850fa516f3abb96c916326f7a8c` — PR #302 unita.  
**Evidenze esatte:** [TEST_REPORT.md](./TEST_REPORT.md) e il
[manifest di implementazione](./docs/status/implementation-manifest.json).

> Questa traduzione conserva gli stessi confini funzionali, di sicurezza e di
> stato del README inglese. Gli identificatori API stabili restano nella forma
> usata dal codice.

---

## 🎯 Perché esiste Crystal

Molti sistemi di IA mescolano documenti sorgente, affermazioni dell’utente,
output del modello, ipotesi, frammenti recuperati e memoria persistente nello
stesso contesto o archivio vettoriale. Un testo fluido può così acquisire
un’autorità non sostenuta dalle sue evidenze.

```text
Un’affermazione convincente non è automaticamente affidabile.
Un nodo del grafo non appartiene automaticamente al Canon rigoroso.
Un punteggio di retrieval non è un’evidenza.
L’output di un modello non è una fonte indipendente.
Una contraddizione non sceglie da sola un vincitore.
Un’etichetta tematica non è un verdetto di verità.
```

## 🧠 Capacità principali

- affermazioni tipizzate e ciclo di vita epistemico esplicito;
- metadati di fonte, evidence span e provenienza;
- confini di ammissione Guardian e TruthGate;
- grafo fisico L3 multi-stato separato dal Canon rigoroso;
- riconciliazione di lettura `TrustSnapshot` immutabile e deny-dominant;
- query pubbliche HTTP, CLI e MCP rigorosamente in sola lettura;
- TRACE e Receipt riproducibili con rilevamento delle alterazioni;
- restrizioni, cancellazione, audit e sessioni di importazione;
- code di revisione e sessioni riprendibili;
- report di contraddizione tipizzati e immutabili;
- decisioni esplicite `COEXIST`, `CONTEXTUALIZE` e `SUPERSEDE`;
- risoluzione dei conflitti tramite CLI e HTTP autenticato;
- ruoli di curatore limitati per scope e lease locali di decisione;
- facet tematiche consultive che non attribuiscono autorità;
- specifica ESM leggibile dalla macchina;
- valutazione deterministica, copertura 100% e mutation gate Ring Zero;
- storico versionato dei benchmark L3.

## 🏛️ Architettura in sintesi

Le tre mappe mostrano lo stesso sistema da prospettive complementari:
**scopo**, **flusso delle informazioni** e **relazioni tra i moduli**.

### 🧠 Mindmap — scopo e confini delle capacità

```text
🧠 Velantrim ExoCortex — Crystal
│
├── 🎯 Scopo
│   ├── Memoria verificabile per l’IA
│   ├── Infrastruttura di fiducia local-first
│   └── Risposte e decisioni fondate su evidenze
│
├── 🏛️ Modello di memoria
│   ├── L0 — cache di lavoro interna al processo
│   ├── L1 — memoria operativa del ciclo di vita
│   ├── L2 — confine di attesa e revisione
│   └── L3 — memoria multi-stato basata su grafo
│
├── 🛡️ Confine di fiducia
│   ├── Guardian — controlli strutturali e di policy
│   ├── TruthGate — confine della policy di ammissione
│   ├── TrustSnapshot — riconciliazione immutabile in lettura
│   └── CanonicalView — proiezione rigorosa e fidata
│
├── 📜 Evidenze e auditabilità
│   ├── Provenienza ed evidence span
│   ├── TRACE — linea di fondazione
│   └── Receipt — replay e prova di alterazione
│
├── ⚖️ Revisione e contraddizioni
│   ├── Code e sessioni di revisione riprendibili
│   ├── ContradictionReport immutabile
│   ├── COEXIST
│   ├── CONTEXTUALIZE
│   └── SUPERSEDE
│
├── 🏷️ Navigazione consultiva
│   └── TopicFacet — metadato multi-etichetta non autoritativo
│
├── 🔐 Governance e coordinamento
│   ├── Ruoli e capacità del curatore limitati per scope
│   ├── Associazione con actor autenticato
│   └── Lease decisionali locali al processo
│
└── 📊 Verifica
    ├── Test e valutazione deterministici
    ├── Copertura delle linee al 100%
    ├── Mutation gate Ring Zero
    └── Storico versionato dei benchmark
```

### 🏗️ Architettura ASCII — come fluiscono le informazioni

```text
┌─────────────────────────────────────────────────────────────────────┐
│              🔱 Velantrim ExoCortex — Crystal                      │
│      Infrastruttura local-first di memoria verificabile per IA     │
└─────────────────────────────────────────────────────────────────────┘

                          📥 Ingest esplicito
                                  │
                                  ▼
             🧾 Tipo di affermazione + fonte + evidence span
                                  │
                                  ▼
                       🧠 Stato Observed L0 / L1
                                  │
                                  ▼
            🛡️ Guardian ──► ⚖️ TruthGate ──► 🚧 restrizioni
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
          ⏳ L2 in attesa / revisione   🏛️ Grafo fisico L3
                    │                           │
                    │                           ▼
                    │                 📜 provenienza / TRACE
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                      📐 TrustSnapshot immutabile
                                  │
                                  ▼
                    🛡️ Guardian + CanonicalView STRICT
                                  │
                     ┌────────────┴────────────┐
                     │                         │
                     ▼                         ▼
           💬 Risposta fondata        🚫 Rifiuto circoscritto
                     │
                     ▼
              🧾 Receipt riproducibile

⚖️ Contraddizione irrisolta
        │
        ▼
📋 ContradictionReport immutabile
        │
        ▼
🔐 principal con scope + capacità + decision lease
        │
        ▼
🧑‍⚖️ COEXIST / CONTEXTUALIZE / SUPERSEDE esplicito
        │
        ▼
📜 percorso di scrittura canonico auditabile

🏷️ Metadati TopicFacet ──► navigazione / filtro / raggruppamento
                          └─► mai autorità su verità, ESM, evidenza o Canon
```

### 🌳 Albero delle relazioni — come si collegano i moduli

```text
🌳 Relazioni del sistema Crystal
│
├── 🧠 Livello di memoria
│   ├── L0 ──► cache di lavoro veloce e ricostruibile
│   ├── L1 ──► ciclo di vita, restrizioni e lavoro in sospeso
│   ├── L2 ──► confine logico di revisione
│   └── L3 ──► archivio multi-stato basato su grafo
│
├── 🛡️ Livello di fiducia
│   ├── Guardian ──► validazione strutturale e di policy
│   ├── TruthGate ──► decisione di ammissione
│   ├── TrustSnapshot ──► riconciliazione L1/L3 deny-dominant
│   └── CanonicalView ──► proiezione rigorosa di fondazione
│
├── 📜 Livello delle evidenze
│   ├── Metadati della fonte
│   ├── Evidence span
│   ├── Provenienza
│   ├── TRACE
│   └── Receipt
│
├── ⚖️ Livello di revisione
│   ├── Coda di revisione
│   ├── Sessione di revisione riprendibile
│   ├── ContradictionReport
│   └── Disposizione esplicita
│       ├── COEXIST
│       ├── CONTEXTUALIZE
│       └── SUPERSEDE
│
├── 🔐 Livello di autorizzazione
│   ├── CuratorPrincipal
│   ├── Ruolo e capacità limitati per scope
│   ├── Corrispondenza con actor autenticato
│   └── Decision lease locale al processo
│
├── 🏷️ Livello consultivo
│   └── TopicFacet
│       ├── multi-etichetta
│       ├── punteggio di sola rilevanza
│       └── nessuna autorità su verità o ammissione
│
├── 🔎 Livello pubblico di query
│   ├── HTTP /ask e /receipt
│   ├── CLI ask e receipt
│   └── MCP search
│       └── pipeline condivisa in sola lettura
│
└── 📊 Livello di verifica
    ├── Test Python 3.11 / 3.12
    ├── Gate di copertura
    ├── Mutation gate Ring Zero
    ├── Controlli di sicurezza e container
    └── Storico dei benchmark
```

### Distinzioni centrali

```text
Grafo fisico L3 ≠ Canon rigoroso
query ≠ ingest
confidence ≠ evidenza indipendente
output LLM ≠ fonte fattuale indipendente
contraddizione ≠ vincitore automatico
rilevanza tematica ≠ verità o qualità dell’evidenza
lease locale ≠ coordinamento distribuito garantito
```

TruthGate è una porta di policy per l’ammissione, non un oracolo della verità
oggettiva. Il Canon rigoroso è una proiezione di lettura consentita dalla policy
su evidenza, stato, ESM e restrizioni di trattamento.

## 🛡️ Confine pubblico di sola lettura

`HTTP /ask`, `HTTP /receipt`, `CLI ask`, `CLI receipt` e `MCP search` condividono
`core.query_pipeline`. Non creano fatti, non cambiano ESM, non scrivono in L3,
non elaborano l’outbox e non inizializzano un embedding fingerprint.

Vedere [Read-Only Query Boundary](./docs/architecture/read-only-query-boundary.md).

## ⚖️ Risoluzione esplicita delle contraddizioni

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "le affermazioni descrivono contesti diversi" \
  --expected-report-id REPORT_ID
```

In FastAPI, `POST /review/resolve-conflict` deve essere registrato con
autenticazione dell’applicazione host. `core.curator_auth` verifica actor,
capacità e scope. `CuratorLeaseRegistry` protegge un solo processo; un deployment
distribuito richiede un adattatore di lease esterno.

Vedere [le superfici di risoluzione](./docs/CONFLICT_RESOLUTION_SURFACES.md) e
[topic facets e curator IAM](./docs/TOPIC_FACETS_AND_CURATOR_IAM.md).

## 🏷️ Facet tematiche consultive

`core.topic_facets` fornisce etichette normalizzate per navigazione, filtro e
raggruppamento. Il punteggio esprime soltanto rilevanza tematica; non modifica
truth status, evidenze, ESM o appartenenza al Canon rigoroso.

## 🚀 Avvio rapido

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## 📚 Documentazione

- [Mappa della documentazione](./docs/DOCUMENTATION_MAP.md)
- [Stato attuale](./docs/STATUS.md)
- [Architettura](./docs/ARCHITECTURE.md)
- [Rapporto dei test](./TEST_REPORT.md)
- [Valutazione](./docs/EVAL.md)
- [Ambito NLnet](./docs/GRANT_NLNET_SCOPE.md)

## ✅ Baseline verificata

```text
Python 3.11: 1853 passed / 12 skipped
Python 3.12: 1853 passed / 12 skipped
Statements:  7236
Coverage:    100.00%
Mutation:    7/7 declared Ring Zero mutants killed
CI jobs:     9
```

## 🚧 Limite delle affermazioni

Crystal non dichiara rilevamento universale della verità, assenza totale di
allucinazioni, certificazione GDPR o di sicurezza, prontezza multi-tenant di
produzione, coscienza artificiale o funzionalità Titan/Full ExoCortex. I lease
attuali sono locali al processo; coordinamento distribuito e integrazione con un
identity provider restano lavori indipendenti.

## 🤝 Contributi e licenza

Vedere [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md),
[GOVERNANCE.md](./GOVERNANCE.md) e [AGPL-3.0](./LICENSE).
