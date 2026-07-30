# 🔍 Guida per reviewer — Velantrim Crystal

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md) · 🇮🇹 **Italiano**
>
> Questa pagina fornisce un percorso di verifica in italiano. Non introduce nuovi
> claim su runtime, sovvenzione, conformità o sicurezza. In caso di divergenza,
> fanno autorità GitHub `main`, [docs/STATUS.md](../STATUS.md) e
> [TEST_REPORT.md](../../TEST_REPORT.md).

## 1. Che cos’è Crystal

Crystal è il nucleo pubblico, minimo e verificabile della memoria Velantrim:

- local-first e senza dipendenza cloud obbligatoria;
- claim con fonti e stato epistemico esplicito;
- Guardian + TruthGate come confine di ammissione automatica verso L3;
- CanonicalView per letture strettamente fondate;
- TRACE e Receipt come livello di prova verificabile;
- backend locali SQLite/WAL e grafi embedded;
- meccanismi tecnici di cancellazione, restrizione, audit e provenienza;
- test riproducibili e gate di valutazione deterministici.

## 2. Che cosa non è Crystal

Crystal non pretende di essere:

- AGI, coscienza, persona o equivalente biologico di un cervello;
- garanzia di «zero allucinazioni»;
- stack completo Titan o Personal ExoCortex;
- sistema di auto-modifica o auto-canonizzazione;
- prodotto dipendente da un LLM, grafo o cloud obbligatorio;
- certificazione legale GDPR;
- certificazione di sicurezza o hosting multi-tenant pronto per la produzione;
- realizzazione runtime di ogni idea di ricerca o PR aperto.

## 3. Fonti autorevoli

Verificare in questo ordine:

1. GitHub `main` — codice effettivamente fuso;
2. [TEST_REPORT.md](../../TEST_REPORT.md) — baseline di test e copertura;
3. [docs/STATUS.md](../STATUS.md) — stato corrente dei claim e componenti;
4. [docs/IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md) — mappa dettagliata;
5. [docs/ARCHITECTURE.md](../ARCHITECTURE.md) — confini architetturali;
6. documenti grant inglesi — scope e criteri di accettazione.

Una nota Notion, roadmap, RFC, prototipo o PR aperto non è una capacità
implementata.

## 4. Riproduzione pulita

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
git status --short
```

Atteso:

- test e gate di copertura superati;
- nessuna regressione segnalata da `eval_gate.py`;
- gli artefatti generati non sporcano l’albero Git;
- i numeri vengono confrontati con [TEST_REPORT.md](../../TEST_REPORT.md).

## 5. Verificare i contratti essenziali

### 🛡️ Ammissione

```text
nuovo claim
→ classificazione + evidenza
→ Guardian
→ TruthGate
→ memoria operativa / Canon ammesso
```

Domanda di controllo: un claim debole, non provato o tipizzato in modo errato può
aggirare i gate previsti?

### 🔎 Query HTTP

```text
POST /ask o GET /receipt
→ core.query_pipeline.query()
→ Canon già esistente
→ CanonicalView
→ risposta o rifiuto limitato
```

Domanda di controllo: L0/L1, L3, ESM, outbox, collegamenti episodici, embedding
fingerprint e verifica adattiva restano invariati durante le query HTTP migrate?

La garanzia è volutamente stretta:

- CLI `ask` e `receipt` non sono ancora migrati;
- MCP può inizializzare un embedding fingerprint assente.

### 🔗 TRACE e Receipt

```bash
velantrim receipt "your question" > receipt.json
velantrim verify-receipt receipt.json
velantrim verify-receipt receipt.json --strict-provenance
```

Domanda di controllo: sono visibili fatti e riferimenti di evidenza che sostengono
una risposta, e viene rilevata la deriva?

### 🧾 Audit e provenienza

```bash
velantrim audit
velantrim audit-verify
velantrim history <fact_id>
```

`history` e la `ProvenanceChain` per fatto sono due viste differenti. Documenti e
test non devono confonderle.

## 6. Avviare con prudenza il servizio HTTP opzionale

```bash
pip install '.[api]'
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
docker compose up --build
curl http://127.0.0.1:8000/health
```

Punti da verificare:

- nessun token di fallback;
- pubblicazione loopback come default;
- utente container non privilegiato;
- dipendenze API opzionali;
- contratti distinti per `/ingest` e `/ask`.

## 7. Verificare la valutazione

Crystal misura tra l’altro:

- retrieval `hit@k` e MRR;
- completezza TRACE e metadati;
- copertura degli Evidence Span;
- replay dei Receipt;
- precisione e recall delle contraddizioni;
- rifiuti corretti ai confini di fiducia.

Il replay Titan è lavoro precedente documentato, non una capacità Crystal attuale
né un runtime auto-ottimizzante.

## 8. Verificare il quadro della sovvenzione

Il reviewer deve distinguere chiaramente la baseline esistente dal delta richiesto:

```text
baseline esistente e testata
+
lavoro finanziato concreto e misurabile
=
deliverable verificabile indipendentemente
```

Le funzioni già fuse non devono essere ricontate come lavoro pagato. La richiesta
è in valutazione; non viene rivendicata alcuna assegnazione.

Sintesi italiana: [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md)  
Fonte normativa: [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)

## 9. Segnali d’allarme

🚩 Un documento afferma più di `main` o `STATUS.md`.  
🚩 Un modulo di ricerca viene presentato come runtime Crystal.  
🚩 Una traduzione amplia scope, budget o claim di conformità.  
🚩 Una query modifica inaspettatamente lo stato della memoria.  
🚩 Una media nasconde una regressione di sicurezza o un singolo caso.  
🚩 Un provider esterno diventa implicitamente obbligatorio.

## 10. Controllo finale

Al termine, un reviewer deve poter rispondere:

1. Quali claim possono entrare automaticamente nel Canon?
2. Quali percorsi di query sono realmente in lettura?
3. Come viene collegata una risposta a fatti ed evidenza?
4. Quali limiti sono implementati e quali soltanto pianificati?
5. Quale delta grant resta dopo aver sottratto la baseline esistente?

---

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md) · 🇮🇹 **Italiano**