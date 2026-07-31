# 🚀 Avvio rapido — Velantrim Crystal

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 [Español](../es/QUICKSTART.md) · 🇮🇹 **Italiano** · 🇷🇺 [Русский](../ru/QUICKSTART.md) · 🇨🇳 [简体中文](../zh-CN/QUICKSTART.md) · 🇸🇦 [العربية](../ar/QUICKSTART.md) · 🇯🇵 [日本語](../ja/QUICKSTART.md)
>
> **Nota:** comandi, nomi dei pacchetti, variabili d’ambiente e percorsi API non
> vengono tradotti. In caso di divergenza valgono GitHub `main` e i documenti
> inglesi.

## 1. Clonare il repository

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
```

## 2. Creare un ambiente virtuale

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Installare l’ambiente di sviluppo

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

Il runtime predefinito di Crystal usa la libreria standard Python. Le dipendenze
di sviluppo, API e adapter sono extra opzionali.

## 4. Eseguire la verifica completa

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

La baseline normativa si trova in [TEST_REPORT.md](../../TEST_REPORT.md). Il
checkpoint documentato è:

```text
1713 passed
12 skipped
0 failed
6389 measured statements
100.00% coverage
```

Questi numeri non sostituiscono un’esecuzione indipendente su un clone pulito.

## 5. Usare la CLI

### Inserire un claim

```bash
velantrim ingest "Water boils at 100C at sea level"
```

L’ingestione è un’operazione di ammissione. I nuovi claim attraversano i confini
di classificazione, Guardian e TruthGate previsti.

### Porre una domanda

```bash
velantrim ask "how does water behave"
```

⚠️ I comandi CLI `ask` e `receipt` usano ancora il percorso storico
`core.pipeline.run()`, capace di ammissione. La garanzia stretta di zero scritture
si applica attualmente agli endpoint HTTP migrati `/ask` e `/receipt`, non a ogni
caller.

### Generare e verificare un Receipt

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
velantrim verify-receipt receipt.json --strict-provenance
```

Un Receipt è una prova sigillata dei fatti e dei riferimenti di provenienza usati.
Il replay verifica la prova rispetto allo stato corrente e può evidenziare deriva
o alterazioni.

## 6. Attivare un backend L3 locale persistente

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

Il percorso SQLite resta locale. Crystal non invia automaticamente dati a un
provider cloud o di modelli.

## 7. Avviare l’interfaccia FastAPI opzionale

```bash
pip install '.[api]'
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
velantrim-api
```

Indirizzo predefinito:

```text
http://127.0.0.1:8000
```

Esempio:

```bash
curl http://127.0.0.1:8000/health
```

| Metodo | Percorso | Comportamento |
|---|---|---|
| `POST` | `/ingest` | ammissione tramite Guardian + TruthGate |
| `POST` | `/ask` | lettura stretta del Canon esistente |
| `GET` | `/receipt?q=...` | lettura con Receipt |
| `POST` | `/verify-receipt` | replay del Receipt |

## 8. Avviare il server MCP opzionale

```bash
python -m core.mcp_server
```

MCP non espone strumenti espliciti di scrittura canonica. Una ricerca può però
inizializzare un embedding fingerprint assente; MCP non viene quindi descritto
come percorso completamente privo di mutazioni.

## 9. Documenti successivi

- [Guida per reviewer](./REVIEWER_GUIDE.md)
- [Stato attuale](./STATUS.md)
- [Panoramica della sovvenzione](./GRANT_OVERVIEW.md)
- [Glossario](./GLOSSARY.md)
- [Architettura normativa](../ARCHITECTURE.md)
- [Valutazione normativa](../EVAL.md)

---

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 [Español](../es/QUICKSTART.md) · 🇮🇹 **Italiano** · 🇷🇺 [Русский](../ru/QUICKSTART.md) · 🇨🇳 [简体中文](../zh-CN/QUICKSTART.md) · 🇸🇦 [العربية](../ar/QUICKSTART.md) · 🇯🇵 [日本語](../ja/QUICKSTART.md)