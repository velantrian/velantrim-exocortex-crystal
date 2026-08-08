<!-- translation-source: docs/REVIEWER_GUIDE.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: de -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# Leitfaden für Reviewer — Velantrim Exo-Cortex Crystal

**Englischer Quell-Checkpoint:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`  
Dieser Leitfaden ist eine gepflegte Orientierung. Implementierungsnachweise bleiben der
Code in `main`, ausführbare Tests, exaktes CI, [TEST_REPORT.md](../../TEST_REPORT.md) und
das [Manifest](../status/implementation-manifest.json).

## 1. Gegenstand der Prüfung

Crystal ist öffentliche, lokale, quellengebundene und auditierbare Speicherinfrastruktur
für KI-Systeme. Die verifizierte Basis umfasst typisierte Claims, Guardian/TruthGate,
eine strikte Canon-Leseprojektion über multi-status L3, schreibgeschützte öffentliche
Abfragen, einen getrennten expliziten Ingest-Pfad, Receipts und Audit-Provenienz.

Nicht behauptet werden AGI, Bewusstsein, universelle Wahrheit, null Halluzinationen,
aktives PostgreSQL-Runtime, automatisches Backend-Switching, produktive Multi-Tenancy,
Sicherheits-/DSGVO-Zertifizierung oder ein bewilligter NLnet-Grant.

## 2. Reproduzieren

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

Aktuelle Test- und Coverage-Zahlen stehen ausschließlich im englischen Testbericht.

## 3. Lese-/Schreibgrenze

```text
ask / receipt / MCP inspection → read-only
explicit ingest                → admission-capable write path
curator override               → explizit, attribuiert und auditiert
```

Das öffentliche `ask` nutzt `core.query_pipeline.query()` und darf Facts, ESM, L3,
Outbox, Episode-Links, Embedding-Identität oder unbekannte Kandidaten nicht verändern.
Ein begrenzter Refusal bei unzureichendem strikten Grounding ist erwartetes Verhalten.

`ingest` schreibt, aber Admission hängt weiterhin von Evidence, Claim-Typ, Policy und
TruthGate ab. Modellausgabe kann sich nicht selbst als verifizierte Welt-Tatsache bestätigen.

## 4. Storage und Migration

SQLite ist das gewöhnliche aktive Local-first-Profil. Ein erster dauerhafter `auto`-Start
kann optional LadybugDB wählen, falls installiert, sonst SQLite; Auswahl und nicht-geheimer
Locator werden gesperrt. Ein stiller Fallback auf ephemeres Mock ist verboten.

PostgreSQL/pgvector ist ein separater Operatorpfad: geprüftes Bundle → Version/TLS-Preflight
→ neues inaktives Schema → serialisierbarer Import → unabhängiger Read-only-Rehash → exakte
Äquivalenz; der Zielzustand bleibt `active=false`.

Import oder Äquivalenz ist keine Aktivierung, Auswahl, TruthGate-Zulassung, Canon-Mitgliedschaft,
Cutover, Rollback, Dual-Write oder Produktionsreife.

## 5. Security und Privacy

Defaultbetrieb benötigt weder Cloud, LLM, Telemetrie noch Analytics. Remote Neo4j,
Anthropic, Wikidata, Redis, PostgreSQL-Migration, breite API-Bindings und kopierte
Backups/Exports erweitern die Vertrauensgrenze nur durch Operatorentscheidung.

`VELANTRIM_ENCRYPTION_KEY` schützt ausgewählte L1-Felder, aber nicht automatisch jedes L3,
Backup, Bundle, Receipt, Log oder temporäre File. Secrets und credential-bearing DSNs dürfen
nicht in Profiles, Bundles, Receipts, Logs, Issues oder Notion gelangen.

Löschung im aktiven lokalen Store entfernt nicht automatisch Backups, Exporte,
Operator-Kopien, Remote-Systeme oder Drittanbieter-Daten.

## 6. Fail-closed-Prüfung

- Unsupported Claims werden blockiert, markiert oder begrenzt abgelehnt.
- Profile-/Locator-Konflikte scheitern vor Backend-Caching.
- Importfehler rollen zurück und lassen das Target `active=false`.
- Evidence-Mismatch und Receipt-/Audit-Manipulation werden erkannt.
- Oversized Input scheitert an festen Limits.
- Fehlende optionale Dependencies führen nicht zu einem versteckten dauerhaften Switch.
- Externe API-Exposition verlangt TLS, Authentifizierung, Least Privilege und Monitoring.

## 7. Checkliste

- [ ] Aktuelles `main` und exaktes CI identifiziert.
- [ ] Read-only Query von explizitem Ingest getrennt.
- [ ] Physisches L3 von strict Canon getrennt.
- [ ] Inaktiver PostgreSQL-Import von Activation getrennt.
- [ ] Netzwerkadapter, Secrets, Encryption- und Erasure-Grenzen geprüft.
- [ ] Keine Zertifizierung, Production Readiness oder Grant-Bewilligung abgeleitet.

Englische Details: [Reviewer Guide](../REVIEWER_GUIDE.md), [Security](../../SECURITY.md),
[Privacy](../../PRIVACY.md), [Failure Modes](../FAILURE_MODES.md) und
[Safety Summary](../SAFETY_PRIVACY_AND_FAILURES.md).
