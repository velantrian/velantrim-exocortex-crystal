# 🇫🇷 Documentation française — Velantrim Crystal

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/README.md) · 🇫🇷 **Français** · 🇪🇸 [Español](../es/README.md) · 🇮🇹 [Italiano](../it/README.md) · 🇷🇺 [Русский](../ru/README.md)

## 🔒 Règle de traduction et d’autorité

Ces pages constituent une orientation française maintenue pour les reviewers,
institutions et contributeurs. Elles ne modifient ni le runtime ni le périmètre
de la subvention.

```text
GitHub main + documents anglais normatifs = source faisant autorité
Documents français, allemands, espagnols, italiens et russes = traductions et aides de lecture
```

En cas d’écart, appliquer dans cet ordre :

1. le code réellement fusionné sur GitHub `main` ;
2. [TEST_REPORT.md](../../TEST_REPORT.md) pour les chiffres de tests et de couverture ;
3. [docs/STATUS.md](../STATUS.md) pour l’état d’implémentation ;
4. les documents anglais de subvention pour le scope, le budget et les livrables.

Une traduction ne doit jamais renforcer une capacité par rapport à la source
anglaise. Les termes « orienté RGPD », « durci », « vérifiable » ou « local »
sont des descriptions techniques, pas des certifications juridiques ou de
sécurité.

---

## 🧭 Parcours recommandé

| Ordre | Document | Objectif |
|---:|---|---|
| 1 | [README français](../../README.fr.md) | projet, frontières et architecture en résumé |
| 2 | [Guide reviewer](./REVIEWER_GUIDE.md) | contrôles attendus d’un reviewer externe |
| 3 | [Démarrage rapide](./QUICKSTART.md) | installation, tests, CLI et API optionnelle |
| 4 | [État actuel](./STATUS.md) | limites d’implémentation et de communication |
| 5 | [Vue subvention](./GRANT_OVERVIEW.md) | résumé grant-safe en français |
| 6 | [Glossaire](./GLOSSARY.md) | terminologie technique cohérente |

---

## 📚 Sources anglaises normatives

| Document | Contenu faisant autorité |
|---|---|
| [README.md](../../README.md) | entrée publique et claims actuels |
| [TEST_REPORT.md](../../TEST_REPORT.md) | baseline reproductible tests/couverture |
| [docs/STATUS.md](../STATUS.md) | statut d’implémentation actuel |
| [docs/REVIEWER_GUIDE.md](../REVIEWER_GUIDE.md) | parcours reviewer anglais |
| [docs/ARCHITECTURE.md](../ARCHITECTURE.md) | frontières architecture et stockage |
| [docs/EVAL.md](../EVAL.md) | méthode d’évaluation |
| [docs/GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md) | périmètre de subvention soumis |
| [Matrice baseline/delta](../grants/baseline-funded-delta-matrix.md) | milestones et preuves d’acceptation |
| [Funding Use Plan](../grants/funding-use-plan.md) | budget et priorisation |

---

## 🛠️ Convention de maintenance

```text
1. mettre à jour et fusionner la source anglaise
2. vérifier le nouveau main
3. synchroniser les traductions dans un PR docs-only séparé
4. ne jamais introduire uniquement dans une traduction un chiffre ou un claim
```

Ce paquet français a été resynchronisé sur la base de Crystal `main@dee0b9a0`.
Le dernier checkpoint modifiant le runtime reste PR #265 / `cd6fd44`.

---

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/README.md) · 🇫🇷 **Français** · 🇪🇸 [Español](../es/README.md) · 🇮🇹 [Italiano](../it/README.md) · 🇷🇺 [Русский](../ru/README.md)