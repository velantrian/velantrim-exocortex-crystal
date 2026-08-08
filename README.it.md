# 🔱 Velantrim ExoCortex — Crystal

> 🌐 [English — fonte normativa](./README.md) · 🇮🇹 **Panoramica italiana**

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->

### Infrastruttura di memoria verificabile e local-first per sistemi di IA affidabili

Questo file è un **riepilogo orientativo non normativo**, non una traduzione completa. Decisioni
tecniche, architettura, stato, sicurezza e dichiarazioni sul finanziamento sono mantenuti in
inglese. In caso di differenze prevalgono [README.md](./README.md) e le prove inglesi.

`v0.3.0` · 🧪 **2078 superati / 13 ignorati** · 🎯 **100.00% di copertura** · ✅ **9 job CI**

**Checkpoint runtime verificato:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337.

Crystal separa memoria fisica, evidenza, ammissione epistemica e letture affidabili. Presenza dei
dati, ranking o migrazione non possono aggirare Guardian, TruthGate o la riconciliazione del Canon
rigoroso.

## Ambito verificato

- affermazioni tipizzate, provenienza e intervalli precisi della fonte;
- confini di ammissione Guardian e TruthGate;
- letture immutabili `TrustSnapshot` e `CanonicalView`;
- query pubbliche HTTP, CLI e MCP in sola lettura;
- TRACE, ricevute, restrizioni, cancellazione e decisioni esplicite sulle contraddizioni;
- SQLite come profilo locale ordinario;
- backup/ripristino verificati ed esportazione logica a risorse limitate;
- importazione PostgreSQL/pgvector opzionale in uno schema target inattivo con verifica
  indipendente dello stato esatto.

## Confine dello storage

```text
SQLite = profilo local-first ordinario attuale
PostgreSQL + pgvector = target di migrazione opzionale
active=false
nessuna normale lettura/scrittura runtime
nessun cambio automatico, cutover, rollback o dual-write
```

Il driver PostgreSQL viene installato solo tramite `[postgresql]` e caricato solo da un comando
esplicito dell’operatore. Un’importazione riuscita è evidenza operativa, non attivazione né
ammissione nel Canon rigoroso.

## Limiti di significato invarianti

```text
physical L3          != strict Canon
retrieval score      != evidence
migration receipt    != claim evidence
successful import    != activation
backend availability != backend selection
```

Crystal non dichiara verità universale, zero allucinazioni, runtime PostgreSQL attivo,
multi-tenancy di produzione, distributed exactly-once, certificazione legale/GDPR/sicurezza,
integrazione Titan o coscienza artificiale.

## Avvio rapido

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## Prove inglesi correnti

- [README normativo](./README.md)
- [Rapporto di verifica](./TEST_REPORT.md)
- [Stato corrente](./docs/STATUS.md)
- [Matrice di implementazione](./docs/IMPLEMENTATION_STATUS.md)
- [Politica di sicurezza](./SECURITY.md)
- [Politica di localizzazione](./docs/LOCALIZATION_POLICY.md)
- [Percorso italiano](./docs/it/README.md)

La domanda NLnet è stata presentata ed è in revisione; non si dichiara alcuna assegnazione o modifica di budget.
