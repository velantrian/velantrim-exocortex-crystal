# 📌 Velantrim Crystal — État actuel

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 **Français** · 🇪🇸 [Español](../es/STATUS.md) · 🇮🇹 [Italiano](../it/STATUS.md) · 🇷🇺 [Русский](../ru/STATUS.md) · 🇨🇳 [简体中文](../zh-CN/STATUS.md) · 🇸🇦 [العربية](../ar/STATUS.md) · 🇯🇵 [日本語](../ja/STATUS.md)

**Date de statut :** 31 juillet 2026  
**État du dépôt utilisé pour cette traduction :** `main@14bc0659`  
**Dernier checkpoint modifiant le runtime :** PR #265 / `cd6fd44`  
**Baseline de tests normative :** [TEST_REPORT.md](../../TEST_REPORT.md)

> Cette page est une traduction de statut. En cas d’écart, GitHub `main`, le
> [STATUS anglais](../STATUS.md) et [TEST_REPORT.md](../../TEST_REPORT.md) font
> autorité.

---

## 🧭 Règle de lecture

```text
GitHub Crystal main = vérité d’implémentation publique
Notion Crystal       = carte grant et stratégie synchronisée
Titan / Full         = laboratoire de recherche séparé
```

Un document, une note Notion, une branche prototype ou un module Titan n’est pas
une capacité Crystal actuelle tant qu’il n’est pas implémenté, testé et fusionné
dans Crystal `main`.

## ✅ Checkpoint vérifié

Le PR #265 a introduit la frontière de requête HTTP strictement en lecture :

```text
POST /ingest   → admission via Guardian + TruthGate
POST /ask      → requête canonique strictement en lecture
GET  /receipt  → lecture stricte avec Receipt
```

Les endpoints HTTP `/ask` et `/receipt` n’écrivent ni L0/L1 ni L3, ne font pas
évoluer ESM, n’opèrent pas l’outbox, n’enregistrent pas de lien épisodique,
n’initialisent pas d’empreinte d’embedding et ne modifient pas la vérification
adaptative.

### Limites résiduelles explicites

- CLI `ask` et `receipt` restent sur `core.pipeline.run()` ;
- `core.pipeline.run()` reste un chemin de compatibilité capable d’admission ;
- MCP ne possède aucun outil d’écriture canonique explicite, mais une recherche
  peut initialiser une empreinte d’embedding absente.

Ces éléments sont des follow-ups connus, pas des capacités dissimulées.

## 🧪 Baseline de vérification

```text
1713 passed
12 skipped
0 failed
6389 measured statements
100.00% coverage
```

Le run CI `30284938992` a terminé avec succès les sept jobs permanents avant
fusion : Python 3.11/3.12, Ruff, sécurité, Docker build, evaluation gate et
intégrité JSONL.

## 🛡️ Frontière des claims publics

Crystal peut être décrit comme :

- une infrastructure de mémoire IA locale et vérifiable ;
- un noyau orienté sources et provenance ;
- un système avec contrôles d’admission Guardian et TruthGate là où ils sont câblés ;
- un système avec CanonicalView, TRACE et Receipts rejouables là où ils sont câblés ;
- un runtime par défaut fondé sur la bibliothèque standard avec adaptateurs optionnels ;
- un projet avec mécanismes techniques d’effacement et de restriction liés au RGPD ;
- une baseline open source de niveau recherche, testable indépendamment.

Crystal ne doit pas être décrit comme :

- Titan ou le Personal ExoCortex complet ;
- un système d’exploitation cognitif autonome ;
- conscient, vivant ou biologiquement équivalent à un cerveau ;
- universellement vrai ou sans hallucinations ;
- juridiquement certifié RGPD ;
- certifié sécurité ou prêt pour un hébergement multi-tenant de production ;
- dépendant d’un LLM externe ou d’un fournisseur cloud obligatoire.

## 💶 Statut de la subvention

La proposition au **NLnet NGI0 Commons Fund** a été soumise et se trouve en cours
d’évaluation. Le dépôt n’affirme pas que le financement a été accordé.

```text
BASELINE ACTUELLE
    +
DELTA FINANCÉ MESURABLE
    =
LIVRABLE VÉRIFIABLE INDÉPENDAMMENT
```

Le travail déjà fusionné reste la baseline et n’est pas recompté comme milestone
payé. Les règles normatives sont maintenues dans :

- [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)
- [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
- [funding-use-plan.md](../grants/funding-use-plan.md)

Une synthèse française se trouve dans [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md).

## 🧪 Décision sur l’evaluation replay

L’implémentation de replay déterministe de Titan a été examinée comme antériorité.
Elle n’a pas été copiée dans le runtime Crystal.

```text
REVIEWED_PRIOR_ART
DOCUMENTED_ONLY
M4_CANDIDATE
NO_RUNTIME_CHANGE
NO_CANON_WRITE
NO_BUDGET_CHANGE
BASELINE_NOT_MOVED
```

Une future implémentation doit étendre le stack d’évaluation Crystal existant,
passer par un RFC/issue/PR séparé, rester hors ligne et non autoritative, et
préserver TruthGate ainsi que les frontières de requête.

## 🔬 Règle pour la recherche et les PR draft

Les PR de recherche ou de branding ouverts ne sont pas la vérité
d’implémentation. Avant fusion, ils doivent être rebasés sur le `main` actuel,
réaudités pour le langage grant et vérifiés contre ce statut normatif.

## 📚 Parcours reviewer

1. [REVIEWER_GUIDE.md](./REVIEWER_GUIDE.md)
2. [QUICKSTART.md](./QUICKSTART.md)
3. [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md)
4. [GLOSSARY.md](./GLOSSARY.md)
5. [Statut anglais normatif](../STATUS.md)
6. [TEST_REPORT.md](../../TEST_REPORT.md)

---

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 **Français** · 🇪🇸 [Español](../es/STATUS.md) · 🇮🇹 [Italiano](../it/STATUS.md) · 🇷🇺 [Русский](../ru/STATUS.md) · 🇨🇳 [简体中文](../zh-CN/STATUS.md) · 🇸🇦 [العربية](../ar/STATUS.md) · 🇯🇵 [日本語](../ja/STATUS.md)