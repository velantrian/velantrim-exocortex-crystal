# 🔱 Velantrim ExoCortex — Crystal

> 🌐 [English — maßgeblich](./README.md) · 🇩🇪 **Deutsche Übersicht**

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->

### Verifizierbare, lokal ausgerichtete Speicherinfrastruktur für vertrauenswürdige KI-Systeme

Diese Datei ist eine **kurze, nicht maßgebliche Orientierung**, keine vollständige Übersetzung.
Technische Entscheidungen, Architektur, Status, Sicherheit und Förderaussagen werden zuerst und
verbindlich auf Englisch gepflegt. Bei Abweichungen gelten [README.md](./README.md) und die
englischen Nachweise.

`v0.3.0` · 🧪 **2078 bestanden / 13 übersprungen** · 🎯 **100.00% Abdeckung** · ✅ **9 CI-Jobs**

**Verifizierter Runtime-Checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337.

Crystal trennt physische Speicherung, Evidenz, epistemische Zulassung und vertrauenswürdige
Leseansichten. Guardian und TruthGate können weder durch gespeicherte Daten noch durch Ranking
oder Migration umgangen werden.

## Verifizierter Funktionsumfang

- typisierte Behauptungen, Provenienz und genaue Quellspannen;
- Guardian- und TruthGate-Zulassungsgrenzen;
- unveränderliche `TrustSnapshot`- und `CanonicalView`-Leseansichten;
- schreibgeschützte öffentliche HTTP-, CLI- und MCP-Abfragen;
- TRACE, Receipts, Einschränkung, Löschung und explizite Widerspruchsentscheidungen;
- SQLite als normales lokales Profil;
- verifizierte Sicherung/Wiederherstellung und begrenzter logischer Export;
- optionaler PostgreSQL/pgvector-Import in ein inaktives Zielschema mit unabhängiger
  exakter Zustandsprüfung.

## Speichergrenze

```text
SQLite = aktuelles gewöhnliches local-first Profil
PostgreSQL + pgvector = optionales Migrationsziel
active=false
keine normalen Runtime-Reads/Writes
kein automatischer Wechsel, Cutover, Rollback oder Dual-Write
```

Der PostgreSQL-Treiber wird nur über `[postgresql]` installiert und nur durch explizite
Operatorbefehle geladen. Ein erfolgreicher Import ist Betriebsnachweis, aber weder Aktivierung
noch Aufnahme in den strikten Canon.

## Unveränderliche Bedeutungsgrenzen

```text
physical L3          != strict Canon
retrieval score      != evidence
migration receipt    != claim evidence
successful import    != activation
backend availability != backend selection
```

Crystal beansprucht keine universelle Wahrheit, null Halluzinationen, aktives PostgreSQL-Runtime,
Produktions-Mandantenfähigkeit, distributed exactly-once, rechtliche/GDPR/Sicherheitszertifizierung,
Titan-Integration oder künstliches Bewusstsein.

## Schnellstart

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## Aktuelle englische Nachweise

- [Authoritative README](./README.md)
- [Verification report](./TEST_REPORT.md)
- [Current status](./docs/STATUS.md)
- [Implementation matrix](./docs/IMPLEMENTATION_STATUS.md)
- [Security policy](./SECURITY.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [Deutscher Dokumentationsweg](./docs/de/README.md)

Der NLnet-Antrag ist eingereicht und wird geprüft; eine Förderung oder Budgetänderung wird nicht behauptet.
