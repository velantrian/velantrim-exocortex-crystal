# 🔍 Reviewer-Leitfaden — Velantrim Crystal

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 **Deutsch** · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md)
>
> Diese Seite ist eine deutschsprachige Prüfroute. Sie führt keine neue
> Runtime-, Grant-, Compliance- oder Sicherheitsbehauptung ein. Bei Abweichungen
> gelten GitHub `main`, [docs/STATUS.md](../STATUS.md) und
> [TEST_REPORT.md](../../TEST_REPORT.md).

## 1. Was Crystal ist

Crystal ist der öffentliche, minimale und nachweisbare Speicherkern von
Velantrim:

- local-first und standardmäßig ohne Cloud-Abhängigkeit;
- source-grounded Claims mit explizitem epistemischem Zustand;
- Guardian + TruthGate als Zulassungsgrenze für automatische Aufnahme in L3;
- CanonicalView für streng begründete Lesesichten;
- TRACE und Receipt als prüfbare Nachweisschicht;
- lokale SQLite/WAL- und eingebettete Graph-Backends;
- technisch implementierte Lösch-, Einschränkungs-, Audit- und
  Provenienzmechanismen;
- reproduzierbare Tests und deterministische Evaluationsgates.

## 2. Was Crystal nicht ist

Crystal beansprucht nicht:

- AGI, Bewusstsein, Personsein oder biologische Gehirnäquivalenz;
- eine Garantie von „null Halluzinationen“;
- den vollständigen Titan- oder Personal-ExoCortex-Stack;
- autonome Selbstmodifikation oder automatische Selbstkanonisierung;
- verpflichtende Nutzung eines externen LLM-, Graph- oder Cloud-Anbieters;
- rechtliche GDPR-Zertifizierung;
- Sicherheitszertifizierung oder produktionsfertiges Multi-Tenant-Hosting;
- dass jede Forschungsidee oder jeder offene PR bereits Runtime ist.

## 3. Welche Quellen verbindlich sind

Prüfen Sie in dieser Reihenfolge:

1. GitHub `main` — tatsächlich gemergter Code;
2. [TEST_REPORT.md](../../TEST_REPORT.md) — Test- und Coverage-Baseline;
3. [docs/STATUS.md](../STATUS.md) — aktueller Claim- und Implementierungsstatus;
4. [docs/IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md) — Detailkarte;
5. [docs/ARCHITECTURE.md](../ARCHITECTURE.md) — Architekturgrenzen;
6. englische Grant-Dokumente — Umfang und Akzeptanzkriterien.

Ein Notion-Eintrag, eine Roadmap, ein RFC, ein Prototyp oder ein offener PR ist
keine implementierte Fähigkeit.

## 4. Saubere Reproduktion

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

Erwartung:

- Tests und Coverage-Gate bestehen;
- `eval_gate.py` meldet keinen Regressionsfehler;
- generierte Eval-Artefakte verschmutzen den Git-Arbeitsbaum nicht;
- die exakte Zahl wird mit [TEST_REPORT.md](../../TEST_REPORT.md) verglichen.

## 5. Kernverträge prüfen

### 🛡️ Zulassung

```text
neuer Claim
→ Klassifikation + Evidenz
→ Guardian
→ TruthGate
→ operative Speicherung / zugelassener Kanon
```

Prüffrage: Kann ein schwacher, nicht belegter oder falsch typisierter Claim die
vorgesehenen Gates umgehen?

### 🔎 HTTP-Abfrage

```text
POST /ask oder GET /receipt
→ core.query_pipeline.query()
→ bereits vorhandener Kanon
→ CanonicalView
→ Antwort oder begrenzte Ablehnung
```

Prüffrage: Bleiben L0/L1, L3, ESM, Outbox, Episodenlinks,
Embedding-Fingerprint und adaptive Verifikation während der migrierten
HTTP-Abfrage unverändert?

Die Garantie ist absichtlich eng:

- CLI `ask` und `receipt` sind noch nicht migriert;
- MCP kann einen fehlenden Embedding-Fingerprint initialisieren.

### 🔗 TRACE und Receipt

```bash
velantrim receipt "your question" > receipt.json
velantrim verify-receipt receipt.json
velantrim verify-receipt receipt.json --strict-provenance
```

Prüffrage: Ist nachvollziehbar, welche Fakten und Evidenzbezüge eine Antwort
getragen haben, und wird Drift erkannt?

### 🧾 Audit und Provenienz

```bash
velantrim audit
velantrim audit-verify
velantrim history <fact_id>
```

Beachten Sie: `history` und die per-Fakt-`ProvenanceChain` sind unterschiedliche
Sichten. Dokumentation und Tests müssen diese Begriffe nicht vermischen.

## 6. Optionalen HTTP-Dienst sicher starten

```bash
pip install '.[api]'
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
docker compose up --build
curl http://127.0.0.1:8000/health
```

Zu prüfen:

- kein Fallback-Token;
- Loopback-Publishing als sichere Voreinstellung;
- nicht privilegierter Container-Nutzer;
- optionale API-Abhängigkeiten statt verpflichtender Runtime-Abhängigkeiten;
- `/ingest` und `/ask` haben unterschiedliche Verträge.

## 7. Evaluation prüfen

Crystal misst nicht nur, ob Code läuft, sondern unter anderem:

- Retrieval `hit@k` und MRR;
- TRACE- und Metadatenvollständigkeit;
- Evidenzspannenabdeckung;
- Receipt-Replay;
- Widerspruchspräzision und -Recall;
- korrekte Ablehnungen an Vertrauensgrenzen.

Der Titan-Replay-Ansatz ist nur dokumentierte Vorarbeit. Er ist keine aktuell
implementierte Crystal-Fähigkeit und darf nicht als selbstoptimierende Runtime
beschrieben werden.

## 8. Grant-Prüfung

Reviewer sollten klar zwischen bestehender Baseline und beantragtem Delta
unterscheiden:

```text
bestehende, getestete Baseline
+
konkrete, messbare Förderarbeit
=
unabhängig prüfbares Deliverable
```

Bereits gemergte Funktionen dürfen nicht erneut als bezahlte Arbeit gezählt
werden. Der Antrag befindet sich in Prüfung; eine Bewilligung wird nicht
behauptet.

Deutsche Übersicht: [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md)  
Verbindliche Quelle: [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)

## 9. Warnzeichen bei der Prüfung

🚩 Ein Dokument behauptet mehr als `main` oder `STATUS.md`.  
🚩 Ein Forschungsmodul wird als aktuelle Crystal-Runtime dargestellt.  
🚩 Ein Übersetzungstext erweitert Scope, Budget oder Compliance-Claims.  
🚩 Eine Abfrage mutiert unerwartet Speicherzustand.  
🚩 Durchschnittsmetriken verdecken Safety- oder Einzelregressionen.  
🚩 Ein externer Anbieter wird stillschweigend verpflichtend.

## 10. Kompakter Abschluss

Ein Reviewer sollte nach der Prüfung beantworten können:

1. Welche Claims dürfen automatisch in den Kanon gelangen?
2. Welche Abfragepfade sind tatsächlich lesend?
3. Wie wird eine Antwort auf Fakten und Evidenz zurückgeführt?
4. Welche Grenzen sind implementiert und welche nur geplant?
5. Welcher Grant-Delta bleibt nach Abzug der bestehenden Baseline übrig?

---

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 **Deutsch** · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md)