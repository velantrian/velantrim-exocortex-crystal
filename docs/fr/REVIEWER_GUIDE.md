# 🔍 Guide reviewer — Velantrim Crystal

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 **Français** · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](../it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](../ru/REVIEWER_GUIDE.md) · 🇨🇳 [简体中文](../zh-CN/REVIEWER_GUIDE.md) · 🇸🇦 [العربية](../ar/REVIEWER_GUIDE.md)
>
> Cette page fournit un parcours de vérification francophone. Elle n’introduit
> aucun nouveau claim runtime, grant, conformité ou sécurité. En cas d’écart,
> GitHub `main`, [docs/STATUS.md](../STATUS.md) et
> [TEST_REPORT.md](../../TEST_REPORT.md) font autorité.

## 1. Ce qu’est Crystal

Crystal est le noyau public, minimal et vérifiable de mémoire Velantrim :

- local-first et sans dépendance cloud obligatoire ;
- claims sourcés avec état épistémique explicite ;
- Guardian + TruthGate comme frontière d’admission automatique vers L3 ;
- CanonicalView pour une lecture strictement fondée ;
- TRACE et Receipt comme couche de preuve vérifiable ;
- backends locaux SQLite/WAL et graphes embarqués ;
- mécanismes techniques d’effacement, restriction, audit et provenance ;
- tests reproductibles et gates d’évaluation déterministes.

## 2. Ce que Crystal n’est pas

Crystal ne prétend pas être :

- une AGI, une conscience, une personne ou l’équivalent biologique d’un cerveau ;
- une garantie de « zéro hallucination » ;
- le stack complet Titan ou Personal ExoCortex ;
- un système d’auto-modification ou d’auto-canonisation ;
- un produit dépendant d’un LLM, graphe ou cloud obligatoire ;
- une certification juridique RGPD ;
- une certification de sécurité ou un hébergement multi-tenant prêt production ;
- la réalisation runtime de chaque idée de recherche ou PR ouvert.

## 3. Sources faisant autorité

Vérifier dans cet ordre :

1. GitHub `main` — code effectivement fusionné ;
2. [TEST_REPORT.md](../../TEST_REPORT.md) — baseline tests et couverture ;
3. [docs/STATUS.md](../STATUS.md) — état actuel des claims et composants ;
4. [docs/IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md) — carte détaillée ;
5. [docs/ARCHITECTURE.md](../ARCHITECTURE.md) — frontières d’architecture ;
6. documents grant anglais — scope et critères d’acceptation.

Une note Notion, une roadmap, un RFC, un prototype ou un PR ouvert n’est pas une
capacité implémentée.

## 4. Reproduction propre

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

Attendus :

- tests et gate de couverture réussis ;
- aucune régression signalée par `eval_gate.py` ;
- les artefacts générés ne polluent pas l’arbre Git ;
- les chiffres sont comparés à [TEST_REPORT.md](../../TEST_REPORT.md).

## 5. Vérifier les contrats essentiels

### 🛡️ Admission

```text
nouveau claim
→ classification + preuves
→ Guardian
→ TruthGate
→ mémoire opérationnelle / Canon admis
```

Question de contrôle : un claim faible, non prouvé ou mal typé peut-il contourner
les gates prévus ?

### 🔎 Requête HTTP

```text
POST /ask ou GET /receipt
→ core.query_pipeline.query()
→ Canon déjà existant
→ CanonicalView
→ réponse ou refus borné
```

Question de contrôle : L0/L1, L3, ESM, outbox, liens épisodiques, empreinte
d’embedding et vérification adaptative restent-ils inchangés pendant les requêtes
HTTP migrées ?

La garantie est volontairement étroite :

- CLI `ask` et `receipt` ne sont pas encore migrés ;
- MCP peut initialiser une empreinte d’embedding absente.

### 🔗 TRACE et Receipt

```bash
velantrim receipt "your question" > receipt.json
velantrim verify-receipt receipt.json
velantrim verify-receipt receipt.json --strict-provenance
```

Question de contrôle : les faits et références de preuve soutenant une réponse
sont-ils visibles, et la dérive est-elle détectée ?

### 🧾 Audit et provenance

```bash
velantrim audit
velantrim audit-verify
velantrim history <fact_id>
```

`history` et la `ProvenanceChain` par fait sont deux vues différentes. La
documentation et les tests ne doivent pas les confondre.

## 6. Démarrer le service HTTP de façon prudente

```bash
pip install '.[api]'
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
docker compose up --build
curl http://127.0.0.1:8000/health
```

Points à vérifier :

- aucun token de secours ;
- publication loopback par défaut ;
- utilisateur de conteneur non privilégié ;
- dépendances API optionnelles ;
- contrats distincts pour `/ingest` et `/ask`.

## 7. Vérifier l’évaluation

Crystal mesure notamment :

- retrieval `hit@k` et MRR ;
- complétude TRACE et métadonnées ;
- couverture des Evidence Spans ;
- Receipt replay ;
- précision et rappel des contradictions ;
- refus corrects aux frontières de confiance.

Le replay Titan est une antériorité documentée, pas une capacité Crystal actuelle
ni un runtime auto-optimisant.

## 8. Vérifier le cadre de subvention

Le reviewer doit distinguer clairement la baseline existante du delta demandé :

```text
baseline existante et testée
+
travail financé concret et mesurable
=
livrable vérifiable indépendamment
```

Les fonctions déjà fusionnées ne doivent pas être recomptées comme travail payé.
La demande est en cours d’évaluation ; aucune attribution n’est revendiquée.

Résumé français : [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md)  
Source normative : [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)

## 9. Signaux d’alerte

🚩 Un document affirme davantage que `main` ou `STATUS.md`.  
🚩 Un module de recherche est présenté comme runtime Crystal.  
🚩 Une traduction élargit le scope, le budget ou les claims de conformité.  
🚩 Une requête modifie un état mémoire de manière inattendue.  
🚩 Une moyenne masque une régression de sécurité ou un cas individuel.  
🚩 Un fournisseur externe devient implicitement obligatoire.

## 10. Contrôle final

À la fin, un reviewer doit pouvoir répondre :

1. Quels claims peuvent entrer automatiquement dans le Canon ?
2. Quels chemins de requête sont réellement en lecture ?
3. Comment une réponse est-elle reliée aux faits et aux preuves ?
4. Quelles limites sont implémentées et lesquelles sont seulement planifiées ?
5. Quel delta grant reste après déduction de la baseline existante ?

---

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 **Français** · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](../it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](../ru/REVIEWER_GUIDE.md) · 🇨🇳 [简体中文](../zh-CN/REVIEWER_GUIDE.md) · 🇸🇦 [العربية](../ar/REVIEWER_GUIDE.md)