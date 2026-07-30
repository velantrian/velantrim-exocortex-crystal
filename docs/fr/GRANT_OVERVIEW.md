# 💶 Vue d’ensemble de la subvention — Velantrim Crystal

> 🌐 🇬🇧 [English](../GRANT_NLNET_SCOPE.md) · 🇩🇪 [Deutsch](../de/GRANT_OVERVIEW.md) · 🇫🇷 **Français** · 🇪🇸 [Español](../es/GRANT_OVERVIEW.md)
>
> Cette page est une aide de traduction et d’orientation. Elle ne remplace ni la
> demande soumise ni les documents anglais relatifs aux milestones, au budget et
> aux critères d’acceptation. En cas d’écart, la version anglaise prévaut.

## 📌 Statut de la demande

Velantrim Crystal a été soumis au **NLnet NGI0 Commons Fund** pour évaluation.
Le dépôt n’affirme pas qu’un financement a déjà été accordé.

Le noyau public est présenté comme une infrastructure de mémoire IA locale,
vérifiable et open source. Les priorités sont la provenance contrôlable,
l’admission gouvernée des connaissances, le fonctionnement local et les preuves
de qualité reproductibles.

## 🧭 Règle baseline / delta

```text
BASELINE ACTUELLE
    +
DELTA FINANCÉ MESURABLE
    =
LIVRABLE VÉRIFIABLE INDÉPENDAMMENT
```

Cette règle empêche de recompter comme prestation financée une fonctionnalité
déjà fusionnée.

Si `main` évolue avant un accord formel, la matrice baseline/delta doit être mise
à jour. Le delta financé doit rester réel, mesurable et vérifiable par un tiers.

## ✅ Baseline déjà disponible

Le noyau public comprend notamment :

- stockage local L0/L1 et backends de graphe L3 ;
- frontières d’admission Guardian et TruthGate ;
- types de claims, statut des sources et provenance ;
- TRACE et Receipts rejouables ;
- baseline d’Evidence Spans ;
- sessions d’import, dry-run et revue curatoriale ;
- mécanismes techniques d’effacement, restriction et audit ;
- évaluation déterministe avec gates CI ;
- interfaces FastAPI et MCP optionnelles ;
- runtime local et indépendant d’un fournisseur par défaut.

L’implémentation exacte est déterminée uniquement par GitHub `main`,
[docs/STATUS.md](../STATUS.md) et [TEST_REPORT.md](../../TEST_REPORT.md).

## 🧱 Delta financé prévu

La matrice anglaise décrit neuf domaines de travail vérifiables :

| Milestone | Objectif synthétique |
|---|---|
| **M1** | baseline open source reproductible et déployable localement |
| **M2** | couche FastAPI optionnelle durcie, rôles clairs et defaults sûrs |
| **M3** | Evidence Spans et vérification des Receipts renforcés |
| **M4** | gates d’évaluation plus larges, versionnés et multilingues |
| **M5** | corpus de connaissances curaté, avec sources et licences référencées |
| **M6** | adaptateurs de connaissances et formats institutionnels durcis |
| **M7** | accessibilité multilingue structurée |
| **M8** | évaluation de l’indépendance vis-à-vis des fournisseurs de modèles |
| **M9** | documentation, gouvernance et onboarding des reviewers |

Montants, priorités et preuves d’acceptation exactes :

- [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
- [funding-use-plan.md](../grants/funding-use-plan.md)

## 🌍 Documentation française et M7

Ce paquet français est une amélioration docs-only de la baseline avant une
fixation formelle de la subvention. Il n’introduit ni nouveau milestone ni nouveau
poste budgétaire.

Il ne doit pas être présenté rétroactivement comme la livraison complète de M7.
Un futur M7 financé devra encore fournir une valeur supplémentaire mesurable,
par exemple :

- structure de localisation maintenue ;
- processus de revue des traductions ;
- autres langues européennes convenues ;
- cas d’évaluation et rapports de qualité spécifiques aux langues ;
- synchronisation traçable avec les releases.

## 🧪 Evaluation replay et M4

Titan contient une implémentation de replay déterministe revue comme antériorité.
Pour Crystal :

```text
Antériorité documentée ≠ runtime Crystal implémenté
```

Un futur M4 peut reprendre des digests stables, des diffs baseline/candidate,
des fixtures versionnées et des gates de sécurité strictes. Ne sont pas intégrés
automatiquement au scope :

- capture live des trajectoires de requêtes personnelles ;
- optimisation automatique ou auto-modification ;
- écriture directe ou indirecte dans le Canon ;
- appels obligatoires à des fournisseurs externes ;
- promotion automatique de candidats.

## 🔒 Hors périmètre et limites de communication

La phase actuelle ne revendique pas :

- un SaaS fermé ;
- conscience, personnalité ou cognition biologique ;
- « zéro hallucination » ;
- auto-canonisation autonome ;
- hébergement multi-tenant prêt production sans architecture de sécurité dédiée ;
- dépendance obligatoire à un fournisseur LLM ;
- certification juridique RGPD ou certification de sécurité ;
- Titan ou le Personal ExoCortex complet comme livrable.

## 🛡️ Formulation reviewer-safe

> Crystal fournit déjà un noyau local et testé de confiance pour une mémoire IA
> vérifiable. Le financement demandé vise un delta d’ingénierie clairement borné
> et mesurable afin de rendre ce noyau plus reproductible, déployable, exploitable
> en sécurité, multilingue et vérifiable indépendamment.

## 📚 Sources normatives

1. [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)
2. [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
3. [funding-use-plan.md](../grants/funding-use-plan.md)
4. [reviewer-qa.md](../grants/reviewer-qa.md)
5. [STATUS.md](../STATUS.md)
6. [TEST_REPORT.md](../../TEST_REPORT.md)

---

> 🌐 🇬🇧 [English](../GRANT_NLNET_SCOPE.md) · 🇩🇪 [Deutsch](../de/GRANT_OVERVIEW.md) · 🇫🇷 **Français** · 🇪🇸 [Español](../es/GRANT_OVERVIEW.md)