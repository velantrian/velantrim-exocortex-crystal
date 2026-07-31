# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 **Italiano** · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md)   · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)
> 📚 [Documentazione tedesca](./docs/de/README.md) · [Documentazione francese](./docs/fr/README.md) · [Documentazione spagnola](./docs/es/README.md) · [Documentazione italiana](./docs/it/README.md) · [Документация на русском](./docs/ru/README.md) · [简体中文文档](./docs/zh-CN/README.md) · [التوثيق العربي](./docs/ar/README.md) · [日本語ドキュメント](./docs/ja/README.md) · [हिन्दी दस्तावेज़](./docs/hi/README.md)

### *Infrastruttura di memoria verificabile, local-first e open source per un’IA affidabile*

`v0.3.0` · 🧪 **1713 test superati / 12 ignorati** · 🎯 **copertura 100%** · 🐍 **runtime predefinito basato sulla sola libreria standard** · ⚖️ **AGPL-3.0** · 🔒 **local-first**

> Crystal è uno strato di memoria verificabile, non un altro chatbot. Ogni claim
> conserva fonte, stato epistemico e metadati di provenienza. L’ammissione
> automatica nel grafo canonico resta governata da **Guardian + TruthGate**.

> **Fonte normativa:** il codice fuso su GitHub `main` e i documenti inglesi
> determinano lo stato dell’implementazione e il perimetro della sovvenzione.
> Questa versione italiana è una traduzione mantenuta per reviewer, istituzioni e
> contributor italofoni. In caso di divergenza valgono [README.md](./README.md),
> [docs/STATUS.md](./docs/STATUS.md) e [TEST_REPORT.md](./TEST_REPORT.md).

---

## 🧭 Crystal in un minuto

Crystal è il nucleo pubblico di Velantrim orientato alla sovvenzione:

- memoria operativa locale L0/L1;
- backend locali per il grafo canonico L3;
- controlli di ammissione Guardian e TruthGate;
- `CanonicalView` per risposte strettamente fondate;
- TRACE, provenienza e Receipt riproducibili;
- Evidence Span, code di revisione e sessioni di importazione;
- meccanismi tecnici di cancellazione e limitazione del trattamento rilevanti per il GDPR;
- valutazione deterministica e quality gate CI;
- interfacce FastAPI e MCP opzionali.

Crystal **non è** Titan, il Personal ExoCortex completo, un sistema operativo
cognitivo autonomo, un progetto di coscienza o un agente auto-modificante. Le
idee di ricerca possono alimentare futuri RFC, ma non costituiscono capacità
runtime attuali.

```text
GitHub Crystal main = verità pubblica dell’implementazione
Notion Crystal       = mappa strategica e grant sincronizzata
Titan / Full         = linea di ricerca separata
```

---

## 🛡️ Confine di fiducia attuale

### Percorso di ammissione

```text
input / documento / evento agente
→ classificazione ed evidenza
→ Guardian + TruthGate
→ memoria operativa L0/L1
→ grafo canonico L3 ammesso
```

### Percorso di query HTTP

Il PR #265 ha introdotto un contratto HTTP di sola lettura separato:

```text
POST /ask, GET /receipt
→ core.aio.arun()
→ core.query_pipeline.query()
→ solo Canon già esistente
→ CanonicalView
→ risposta o rifiuto limitato
```

Per queste superfici HTTP, porre una domanda non inserisce dati in L0/L1, non
modifica ESM, non scrive fatti o archi L3, non svuota l’outbox, non registra
collegamenti episodici, non inizializza un embedding fingerprint e non modifica
lo stato di verifica adattiva.

### Ambito residuo dichiarato esplicitamente

- i comandi CLI `ask` e `receipt` usano ancora il percorso storico
  `core.pipeline.run()`, capace di ammissione;
- `core.pipeline.run()` resta disponibile;
- MCP non espone strumenti espliciti di scrittura canonica, ma una ricerca può
  inizializzare un embedding fingerprint non ancora impostato.

La garanzia di sola lettura è quindi intenzionalmente precisa, non generalizzata.
Vedere [read-only-query-boundary.md](./docs/architecture/read-only-query-boundary.md).

---

## 🧠 Modello di memoria

| Livello | Ruolo | Confine |
|---|---|---|
| **L0** | cache di lavoro in-process | veloce, ricostruibile |
| **L1** | memoria operativa SQLite/WAL | stati, restrizioni, aggiornamenti |
| **L2** | claim in attesa e revisione curatoriale | non automaticamente canonico |
| **L3** | grafo canonico | ammissione automatica solo tramite TruthGate |
| **TRACE / Receipt** | livello di prova | spiega il grounding e rileva deriva |

Il grafo fisico può contenere stati di verità differenti. In senso rigoroso,
**Canon** indica soltanto la proiezione verificata, valida secondo TRACE e
consentita dalle policy — non ogni nodo presente in un backend a grafo.

---

## 🚀 Avvio rapido

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

Uso CLI di base:

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask "how does water behave"
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

Backend L3 SQLite persistente e locale:

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

Guida dettagliata: [docs/it/QUICKSTART.md](./docs/it/QUICKSTART.md).

---

## 🔌 Interfacce opzionali

### FastAPI

```bash
pip install '.[api]'
velantrim-api
```

| Metodo | Percorso | Contratto |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | ammissione tramite Guardian + TruthGate |
| `POST` | `/ask` | query canonica strettamente in lettura |
| `GET` | `/receipt?q=...` | lettura con Receipt |
| `POST` | `/verify-receipt` | replay del Receipt sullo stato corrente |
| `GET` | `/evidence/{fact_id}` | vista pubblica dell’evidenza secondo policy |

FastAPI e Uvicorn sono extra opzionali. Il runtime predefinito non richiede un
servizio cloud né un provider di modelli terzo.

### MCP

```bash
python -m core.mcp_server
```

MCP offre strumenti orientati all’ispezione per ricerca, report di memoria,
storia dei fatti, conflitti e verifica dei Receipt. Resta applicabile il limite
residuo legato all’embedding fingerprint.

---

## 🧪 Valutazione

Crystal include già una baseline deterministica:

- retrieval `hit@k` e MRR;
- completezza TRACE e metadati;
- copertura degli Evidence Span;
- sopravvivenza al replay dei Receipt;
- precisione e recall nel rilevamento delle contraddizioni;
- test di rifiuto ai confini di fiducia;
- soglie e limiti di regressione CI.

L’implementazione di replay deterministico di Titan è precedente lavoro tecnico
riesaminato, non runtime Crystal copiato. Qualsiasi futura implementazione deve
estendere lo stack di valutazione esistente, rimanere offline e non autoritativa,
e preservare TruthGate e i confini di query.

---

## 💶 Confine della sovvenzione

Il progetto è stato presentato al **NLnet NGI0 Commons Fund** ed è in fase di
valutazione. Il repository non afferma che il finanziamento sia già stato
assegnato.

```text
BASELINE ATTUALE
    +
DELTA FINANZIATO MISURABILE
    =
DELIVERABLE VERIFICABILE INDIPENDENTEMENTE
```

Il lavoro già fuso resta baseline e non viene ricontato come consegna pagata.
Meccanismi cognitivi, neuromorfici o Titan non vengono aggiunti silenziosamente
al perimetro Crystal.

Sintesi italiana: [docs/it/GRANT_OVERVIEW.md](./docs/it/GRANT_OVERVIEW.md)  
Fonti normative:

- [docs/GRANT_NLNET_SCOPE.md](./docs/GRANT_NLNET_SCOPE.md)
- [docs/grants/baseline-funded-delta-matrix.md](./docs/grants/baseline-funded-delta-matrix.md)
- [docs/grants/funding-use-plan.md](./docs/grants/funding-use-plan.md)
- [docs/grants/evaluation-replay-adoption.md](./docs/grants/evaluation-replay-adoption.md)

---

## ✅ Gate di verifica

| Gate | Funzione |
|---|---|
| pytest + coverage | suite completa con soglia obbligatoria del 100% |
| Ruff | lint del codice e degli strumenti del repository |
| Gitleaks | rilevamento di secret versionati |
| Bandit | analisi statica di sicurezza Python |
| pip-audit | audit delle vulnerabilità delle dipendenze |
| Docker build | build riproducibile dell’immagine hardenizzata |
| eval-gate | controllo regressioni di retrieval, grounding e contraddizioni |
| JSONL integrity | struttura del corpus e identificativi duplicati |

Questi controlli riducono il rischio; non provano l’assenza di ogni difetto e non
costituiscono certificazione legale o di sicurezza.

---

## 📚 Percorso reviewer in italiano

1. [docs/it/REVIEWER_GUIDE.md](./docs/it/REVIEWER_GUIDE.md)
2. [docs/it/QUICKSTART.md](./docs/it/QUICKSTART.md)
3. [docs/it/STATUS.md](./docs/it/STATUS.md)
4. [docs/it/GRANT_OVERVIEW.md](./docs/it/GRANT_OVERVIEW.md)
5. [docs/it/GLOSSARY.md](./docs/it/GLOSSARY.md)
6. [TEST_REPORT.md](./TEST_REPORT.md) — risultati normativi
7. [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) — architettura normativa

---

## ⚖️ Licenza e contributi

Crystal è distribuito con licenza **AGPL-3.0**. Vedere [LICENSE](./LICENSE),
[CONTRIBUTING.md](./CONTRIBUTING.md), [GOVERNANCE.md](./GOVERNANCE.md),
[SECURITY.md](./SECURITY.md) e [PRIVACY.md](./PRIVACY.md).

> **📊 Canon = verità ammessa** · **🔗 Provenienza = fiducia** · **🏠 Local-first = controllo**

---

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 **Italiano** · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)