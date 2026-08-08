# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 **Italiano** · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->
<!-- localization-status: IN_PROGRESS -->

### Infrastruttura local-first e verificabile di memoria, evidenza e decisione per sistemi di IA affidabili

`v0.3.0` · 🧪 **2078 superati / 13 ignorati / 0 falliti** · 🎯 **9756 istruzioni / 100,00% copertura delle linee** · 🧬 **7/7 mutanti Ring Zero eliminati** · ✅ **9 job CI permanenti** · 🐍 **runtime predefinito solo con la libreria standard Python** · ⚖️ **AGPL-3.0**

> Crystal non è un altro chatbot e non è un «oracolo della verità» autonomo. È un confine di memoria, evidenza e decisione che registra che cosa sia un’affermazione, da dove provenga, in quale stato epistemico si trovi, se possa fondare una risposta e come una contraddizione sia stata risolta mediante una decisione esplicita e verificabile.

**Checkpoint runtime verificato:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337 unita.  
**Head validato / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536` — 9/9 riusciti.  
**Integrazione PostgreSQL:** `31256316532` — PostgreSQL 16 e pgvector 0.8.2.  
**Evidenza primaria:** [TEST_REPORT.md](./TEST_REPORT.md), [STATUS.md](./docs/STATUS.md) e il [manifest leggibile dalla macchina](./docs/status/implementation-manifest.json).

> **Contratto di traduzione:** questo file è una presentazione italiana completa, visiva e semantica, non un riepilogo. L’inglese resta la fonte di lavoro primaria. Gli altri documenti vengono tradotti progressivamente; vedi [politica di localizzazione](./docs/LOCALIZATION_POLICY.md) e [stato delle traduzioni](./docs/TRANSLATION_STATUS.md).

---

## 🎯 Perché esiste Crystal

Molti sistemi di IA mescolano documenti sorgente, dichiarazioni dell’utente, output del modello, ipotesi, frammenti recuperati e memoria durevole nello stesso contesto o archivio vettoriale. Un testo convincente può così ricevere un’autorità che le sue prove non giustificano.

```text
Un’affermazione fluente non è automaticamente affidabile.
Un nodo del grafo fisico non è automaticamente Canon rigoroso.
Un punteggio di retrieval non è evidenza.
Un output del modello non è una fonte fattuale indipendente.
Una contraddizione non sceglie da sola il vincitore.
Un’etichetta tematica non è un verdetto di verità.
Un import riuscito non attiva il backend.
```

## 🧠 Che cosa offre Crystal

- affermazioni tipizzate e ciclo di vita epistemico esplicito;
- identità della fonte, span esatti di evidenza e provenienza;
- confini di ammissione Guardian e TruthGate;
- grafo fisico L3 multi-stato separato dal Canon rigoroso;
- `TrustSnapshot` immutabile e deny-dominant;
- superfici pubbliche HTTP, CLI e MCP in sola lettura;
- TRACE e Receipt riproducibili e anti-manomissione;
- restrizioni, cancellazione, audit e sessioni di importazione;
- code di revisione e sessioni riprendibili;
- report di contraddizione immutabili;
- decisioni `COEXIST`, `CONTEXTUALIZE`, `SUPERSEDE`;
- capacità scoped del curatore e lease locali al processo;
- TopicFacet consultivo senza autorità sulla verità;
- valutazione deterministica, copertura 100% e mutation gate Ring Zero;
- backup/restore SQLite e migrazione logica limitata verificati;
- import PostgreSQL/pgvector inattivo con equivalenza esatta indipendente.

## 🏛️ Architettura in tre viste

### 🧠 Mappa mentale

```text
🧠 Crystal
├── 🎯 Scopo
│   ├── memoria verificabile per l’IA
│   ├── infrastruttura di fiducia local-first
│   └── risposte e decisioni collegate alle prove
├── 🏛️ Memoria
│   ├── L0 — cache di lavoro veloce
│   ├── L1 — stato operativo e ciclo di vita
│   ├── L2 — confine di attesa/revisione
│   └── L3 — grafo fisico multi-stato
├── 🛡️ Fiducia
│   ├── Guardian
│   ├── TruthGate
│   ├── TrustSnapshot
│   └── CanonicalView
├── 📜 Evidenza
│   ├── fonte + span esatto
│   ├── provenienza
│   ├── TRACE
│   └── Receipt
├── ⚖️ Contraddizione
│   ├── coda/sessione di revisione
│   ├── ContradictionReport
│   └── COEXIST / CONTEXTUALIZE / SUPERSEDE
├── 🗄️ Archiviazione
│   ├── SQLite — profilo local-first ordinario
│   └── PostgreSQL/pgvector — destinazione inattiva
└── 📊 Verifica
    ├── Python 3.11 / 3.12
    ├── copertura 100%
    ├── mutazione / sicurezza / Docker
    └── evidenza CI esatta
```

### 🏗️ Flusso delle informazioni

```text
📥 ingest esplicito
        ↓
🧾 tipo di claim + fonte + span esatto di evidenza
        ↓
🧠 stato osservato in L0/L1
        ↓
🛡️ Guardian → ⚖️ TruthGate → 🚧 restrizioni
        ↓                         ↓
⏳ revisione L2             🏛️ grafo fisico L3
        └──────────────┬──────────┘
                       ↓
             📐 TrustSnapshot immutabile
                       ↓
          🛡️ Guardian + CanonicalView STRICT
                  ↓                 ↓
          💬 risposta fondata      🚫 rifiuto motivato
                  ↓
             🧾 Receipt riproducibile
```

### 🌳 Albero dei moduli

```text
🌳 Crystal
├── 🧠 Memory: L0 / L1 / L2 / L3
├── 🛡️ Trust: Guardian / TruthGate / TrustSnapshot / CanonicalView
├── 📜 Evidence: Source / Span / Provenance / TRACE / Receipt
├── ⚖️ Review: Queue / Session / ContradictionReport / Disposition
├── 🔎 Query: HTTP / CLI / MCP
├── 🗄️ Portability: SQLite lifecycle / bundle logico / import PostgreSQL inattivo
└── 📊 Verification: test / copertura / mutazione / sicurezza / Docker / docs-status
```

## 🧭 Distinzioni centrali

```text
grafo fisico L3      != Canon rigoroso
query                != ingest
confidence           != evidenza indipendente
output LLM           != fonte fattuale indipendente
rilevare conflitto   != vincitore automatico
rilevanza TopicFacet != verità
Receipt di migrazione != evidenza di claim
import riuscito      != attivazione backend
lease locale         != coordinamento distribuito
```

TruthGate è un gate di politica di ammissione, non un oracolo. Il Canon rigoroso è una proiezione di lettura consentita dalla policy su evidenza, stato, ESM, forma della confidence e restrizioni di trattamento.

## 🧱 Superfici di memoria ed evidenza

| Superficie | Ruolo | Confine critico |
|---|---|---|
| L0 | cache di lavoro nel processo | veloce e ricostruibile |
| L1 | memoria operativa SQLite/WAL | ciclo di vita e restrizioni |
| L2 | confine logico di revisione | non automaticamente Canon |
| L3 | memoria fisica multi-stato | presenza ≠ fiducia |
| TrustSnapshot | riconciliazione immutabile | risoluzione deny-dominant |
| CanonicalView | proiezione rigorosa | solo letture consentite |
| TRACE / Receipt | prova e replay | grounding, deriva, manomissione |
| ContradictionReport | conflitto immutabile | confidence non decide |
| TopicFacet | navigazione | non cambia verità o Canon |

## 🗄️ SQLite e PostgreSQL/pgvector

```text
SQLite
└── runtime local-first ordinario
    ├── letture/scritture
    ├── backup/restore
    ├── recupero dei lock
    └── export logico canonico limitato

PostgreSQL 16 + pgvector
└── profilo opzionale di migrazione/equivalenza
    ├── extra opzionale [postgresql]
    ├── caricamento lazy del driver
    ├── nuovo schema destinazione
    ├── active=false
    ├── import SERIALIZABLE
    └── equivalenza indipendente count/byte/SHA-256
```

La destinazione PostgreSQL è assente dalla composizione runtime ordinaria e non serve letture o scritture normali. L’import riuscito non stabilisce attivazione, selezione automatica, cutover, rollback, dual-write, ammissione TruthGate, appartenenza al Canon, accettazione ANN o multi-tenancy di produzione.

## 🔎 Crystal rispetto al RAG classico

| Domanda | RAG classico | Crystal |
|---|---|---|
| Trovare materiale rilevante | forza principale | adapter di retrieval |
| Separare dichiarazione utente e fatto verificato | logica applicativa | confine tipizzato esplicito |
| Tracciare ciclo di vita e contraddizioni | spesso esterno | stati e report first-class |
| Impedire al testo generato di diventare la propria fonte | non intrinseco | invariante Ring Zero |
| Riprodurre le prove di una risposta | opzionale | TRACE e Receipt |
| Risolvere contraddizioni responsabilmente | specifico dell’app | disposizioni autorizzate |
| Funzionare senza provider cloud/modello obbligatorio | variabile | base local-first pure-stdlib |

## 🛡️ Confine pubblico in sola lettura

`HTTP /ask`, `HTTP /receipt`, `CLI ask`, `CLI receipt` e `MCP search` condividono `core.query_pipeline`. Non creano fatti, non cambiano lo stato ESM, non scrivono in L3 e non modificano il Canon.

## ⚖️ Decisione esplicita sulle contraddizioni

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "le affermazioni descrivono contesti diversi" \
  --expected-report-id REPORT_ID
```

`CuratorLeaseRegistry` coordina solo all’interno di un processo. Un deployment distribuito richiede un adapter di lease esterno.

## 🚀 Avvio rapido

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Tooling PostgreSQL inattivo opzionale: `pip install -e '.[postgresql]'`.

## 📚 Navigazione

- [Indice italiano](./docs/it/README.md)
- [Mappa inglese](./docs/DOCUMENTATION_MAP.md)
- [Report test](./TEST_REPORT.md)
- [Stato](./docs/STATUS.md)
- [Stato implementazione](./docs/IMPLEMENTATION_STATUS.md)
- [Architettura](./docs/ARCHITECTURE.md)
- [Sicurezza](./SECURITY.md)
- [Ambito NLnet](./docs/GRANT_NLNET_SCOPE.md)
- [Politica di localizzazione](./docs/LOCALIZATION_POLICY.md)
- [Stato traduzioni](./docs/TRANSLATION_STATUS.md)

## ✅ Baseline verificata

```text
Runtime merge: bbd816c09dd39a02e6de6c1014438490572f40f6 (PR #337)
Python 3.11: 2078 passed / 13 skipped / 0 failed
Python 3.12: 2078 passed / 13 skipped / 0 failed
Statements: 9756
Coverage: 100.00%
Mutation: 7/7
CI: 9/9
PostgreSQL integration: PostgreSQL 16 + pgvector 0.8.2 riuscita
```

## 🚧 Limite delle affermazioni

Crystal non dichiara rilevamento universale della verità, zero allucinazioni, certificazione legale GDPR/sicurezza, multi-tenancy pronta per la produzione, locking distribuito, AGI o coscienza, runtime PostgreSQL attivo, switching automatico, cutover/rollback o un Reader Core dedicato completato. La proposta NLnet resta **submitted / under review / not awarded**.

## 🤝 Contributi e licenza

Vedi [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md), [GOVERNANCE.md](./GOVERNANCE.md) e [AGPL-3.0](./LICENSE).
