<!-- translation-source: docs/QUICKSTART.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: it -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🚀 Avvio rapido di Crystal

Questa guida esegue la base locale senza dipendenze obbligatorie, ingerisce
un’affermazione esplicita, la interroga tramite il confine di sola lettura e verifica
un Receipt.

## Requisiti

- Python 3.11 o 3.12;
- Git;
- uno spazio locale per repository e dati SQLite.

Il runtime predefinito non richiede LLM, provider di embedding o cloud. Gli extra di
sviluppo e test installano i pacchetti opzionali della suite completa.

## 1. Installazione

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

In Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 2. Verifica del repository

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

Checkpoint e metriche esatte sono mantenuti in
[TEST_REPORT.md](../../TEST_REPORT.md), non duplicati qui come requisiti mutevoli.

## 3. Selezionare lo storage locale persistente

```bash
export VELANTRIM_L3_BACKEND=sqlite
export VELANTRIM_L3_PATH=./data/canon.db
```

PowerShell:

```powershell
$env:VELANTRIM_L3_BACKEND = "sqlite"
$env:VELANTRIM_L3_PATH = ".\data\canon.db"
```

SQLite resta il profilo local-first attivo ordinario. PostgreSQL/pgvector è solo un
percorso opzionale di importazione ed equivalenza inattiva; il target rimane
`active=false`.

## 4. Ingerire esplicitamente un’affermazione

```bash
velantrim ingest "Water boils at 100C at sea level"
```

`ingest` scrive. L’affermazione entra nello stato operativo e passa dal percorso di
ammissione Guardian/TruthGate configurato. Il comando non significa che Crystal provi
autonomamente la verità oggettiva: l’ammissione dipende da evidenza e policy.

## 5. Interrogare tramite il confine di sola lettura

```bash
velantrim ask "how does water behave"
```

Il `ask` pubblico usa `core.query_pipeline.query()` e non deve creare o modificare fatti
L0/L1, cambiare ESM, scrivere L3, operare l’outbox, registrare collegamenti di episodi,
inizializzare un fingerprint embedding non impostato o persistere candidati sconosciuti.

Quando manca grounding canonico rigoroso, è previsto un rifiuto limitato. È un risultato
valido del confine di fiducia, non necessariamente un errore runtime.

## 6. Creare e verificare un Receipt

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

Un Receipt sigilla query, risposta e ID citati sotto un digest e può rigiocare le citazioni
contro lo stato corrente. Rende evidenti le manomissioni; la firma HMAC opzionale richiede
una chiave locale di provenienza.

## 7. Eseguire l’API opzionale

```bash
pip install '.[api]'
velantrim-api
```

| Metodo | Route | Confine |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | ammissione/scrittura esplicita |
| `POST` | `/ask` | query rigorosamente read-only |
| `GET` | `/receipt?q=...` | query più Receipt |
| `POST` | `/verify-receipt` | replay del Receipt |
| `GET` | `/evidence/{fact_id}` | vista evidenza policy-aware |

L’API usa una base bearer-token. Non è un modello completo di autorizzazione
multi-tenant di produzione.

## 8. Eseguire la superficie MCP di ispezione

```bash
python -m core.mcp_server
```

MCP offre ricerca read-only, report memoria, storia dei fatti, conflitti e verifica
Receipt. Non espone strumenti di scrittura canonica.

## Errori comuni di confine

```text
ask / receipt / MCP search → read-only
explicit ingest            → admission-capable write path
```

- L3 fisico non è Canon rigoroso.
- Confidence, duplicazione o similarità retrieval non sono evidenza indipendente.
- Importazione o equivalenza riuscita non è attivazione, cutover o selezione backend.

## Documenti successivi

- [README](../../README.md)
- [Mappa della documentazione](../DOCUMENTATION_MAP.md)
- [Architettura](../ARCHITECTURE.md)
- [Stato dell’implementazione](../IMPLEMENTATION_STATUS.md)
- [Rapporto di test](../../TEST_REPORT.md)
- [Politica di sicurezza](../../SECURITY.md)
