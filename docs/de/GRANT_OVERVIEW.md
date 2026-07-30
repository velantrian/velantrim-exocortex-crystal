# 💶 Grant-Übersicht — Velantrim Crystal

> 🌐 [Deutsche Dokumentation](./README.md) ·
> [Verbindlicher englischer Grant-Scope](../GRANT_NLNET_SCOPE.md)
>
> Diese Seite ist eine Übersetzungs- und Orientierungshilfe. Sie ersetzt weder
> den eingereichten Antrag noch die englischen Milestone-, Budget- und
> Akzeptanzdokumente. Bei Abweichungen gilt die englische Fassung.

## 📌 Antragsstatus

Velantrim Crystal wurde beim **NLnet NGI0 Commons Fund** zur Prüfung eingereicht.
Das Repository behauptet nicht, dass eine Förderung bereits bewilligt wurde.

Der öffentliche Projektkern wird als lokale, nachweisbare und quelloffene
KI-Speicherinfrastruktur beschrieben. Im Mittelpunkt stehen überprüfbare
Provenienz, kontrollierte Wissenszulassung, lokale Betriebsfähigkeit und
reproduzierbare Qualitätsnachweise.

## 🧭 Baseline- und Delta-Regel

```text
HEUTIGE BASELINE
    +
MESSBARER FINANZIERTER DELTA
    =
UNABHÄNGIG PRÜFBARES DELIVERABLE
```

Diese Regel verhindert, dass bereits gemergte Funktionen später nochmals als
bezahlte Förderleistung gezählt werden.

Wenn sich `main` vor einer formalen Grant-Vereinbarung weiterentwickelt, muss die
Baseline-/Delta-Matrix angepasst werden. Der finanzierte Delta muss weiterhin
real, messbar und extern prüfbar bleiben.

## ✅ Bereits vorhandene Baseline

Der aktuelle öffentliche Kern umfasst unter anderem:

- lokale L0/L1-Speicherung und L3-Graph-Backends;
- Guardian- und TruthGate-Zulassungsgrenzen;
- Claim-Typen, Quellenstatus und Provenienzmetadaten;
- TRACE und reproduzierbare Receipts;
- Evidenzspannen-Baseline;
- Importsitzungen, Dry-run und Kurator-Review;
- technisch implementierte Lösch-, Einschränkungs- und Auditmechanismen;
- deterministische Evaluation mit CI-Gates;
- optionale FastAPI- und MCP-Schnittstellen;
- standardmäßig lokale, provider-unabhängige Runtime.

Die exakte aktuelle Implementierung wird ausschließlich durch GitHub `main`,
[docs/STATUS.md](../STATUS.md) und [TEST_REPORT.md](../../TEST_REPORT.md) bestimmt.

## 🧱 Geplanter Förder-Delta

Die englische Milestone-Matrix beschreibt neun prüfbare Arbeitsbereiche:

| Milestone | Förderziel in Kurzform |
|---|---|
| **M1** | reproduzierbare, lokal deploybare Open-Source-Baseline |
| **M2** | gehärtete optionale FastAPI-Schicht mit klaren Rollen und sicheren Defaults |
| **M3** | produktionsstärkere Evidenzspannen und Receipt-Prüfung |
| **M4** | größere, versionierte und mehrsprachige Evaluationsgates |
| **M5** | kuratierter, quell- und lizenzreferenzierter Wissenskorpus |
| **M6** | gehärtete Wissensadapter und institutionelle Formate |
| **M7** | strukturierte mehrsprachige Zugänglichkeit |
| **M8** | providerneutrale Modellunabhängigkeits-Evaluation |
| **M9** | Dokumentation, Governance und Reviewer-Onboarding |

Die exakten Beträge, Prioritäten und Akzeptanznachweise stehen in:

- [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
- [funding-use-plan.md](../grants/funding-use-plan.md)

## 🧪 Deutsche Dokumentation und M7

Dieses deutsche Dokumentationspaket ist eine docs-only Baseline-Verbesserung vor
einer formalen Grant-Fixierung. Es führt kein neues Milestone und keinen neuen
Budgetposten ein.

Es darf nicht rückwirkend als vollständig gelieferter M7-Delta dargestellt
werden. Ein später finanzierter M7 müsste weiterhin messbare zusätzliche Arbeit
liefern, zum Beispiel:

- gepflegte Lokalisierungsstruktur;
- definierter Übersetzungsreview;
- weitere vereinbarte europäische Sprachen;
- sprachspezifische Evaluationsfälle und Qualitätsberichte;
- nachvollziehbare Synchronisation mit Releases.

## 🧪 Evaluation-Replay und M4

Titan enthält eine deterministische Replay-Implementierung, die als technische
Vorarbeit geprüft wurde. Für Crystal gilt aktuell:

```text
Dokumentierte Vorarbeit ≠ implementierte Crystal-Runtime
```

Eine spätere M4-Umsetzung kann stabile Digests, Baseline-/Candidate-Diffs,
versionierte Fixtures und harte Safety-Gates übernehmen. Nicht automatisch in
den Grant-Scope übernommen werden:

- Live-Trajectory-Aufzeichnung persönlicher Anfragen;
- automatische Optimierung oder Selbstmodifikation;
- direkte oder indirekte Canon-Schreibpfade;
- verpflichtende externe Provider-Aufrufe;
- automatische Promotion von Kandidaten.

## 🔒 Nicht-Gegenstände und Claim-Grenzen

Die aktuelle Grant-Phase beansprucht nicht:

- geschlossenes SaaS-Produkt;
- Bewusstsein, Personsein oder biologische Kognition;
- „null Halluzinationen“;
- autonome Selbstkanonisierung;
- produktionsfertiges Multi-Tenant-Hosting ohne eigene Sicherheitsarchitektur;
- verpflichtende Abhängigkeit von einem bestimmten LLM-Anbieter;
- rechtliche GDPR- oder Sicherheitszertifizierung;
- den vollständigen persönlichen ExoCortex oder Titan als Deliverable.

## 🛡️ Reviewer-sichere Kurzform

> Crystal stellt bereits einen getesteten, lokalen Vertrauenskern für
> nachweisbare KI-Speicherung bereit. Die beantragte Förderung soll einen klar
> abgegrenzten, messbaren Engineering-Delta finanzieren, der diesen Kern besser
> reproduzierbar, deploybar, sicher betreibbar, mehrsprachig und unabhängig
> prüfbar macht.

## 📚 Verbindliche Quellen

1. [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)
2. [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
3. [funding-use-plan.md](../grants/funding-use-plan.md)
4. [reviewer-qa.md](../grants/reviewer-qa.md)
5. [STATUS.md](../STATUS.md)
6. [TEST_REPORT.md](../../TEST_REPORT.md)
