# 🔱 Velantrim ExoCortex — Crystal

> 🌐 [English — source normative](./README.md) · 🇫🇷 **Aperçu français**

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->

### Infrastructure de mémoire vérifiable et locale pour des systèmes d’IA dignes de confiance

Ce fichier est un **résumé d’orientation non normatif**, pas une traduction complète. Les
décisions techniques, l’architecture, le statut, la sécurité et les déclarations de financement
sont maintenus en anglais. En cas d’écart, [README.md](./README.md) et les preuves anglaises
prévalent.

`v0.3.0` · 🧪 **2078 réussis / 13 ignorés** · 🎯 **100.00% de couverture** · ✅ **9 tâches CI**

**Checkpoint runtime vérifié :** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337.

Crystal sépare le stockage physique, les preuves, l’admission épistémique et les lectures de
confiance. La présence d’une donnée, son classement ou une migration ne peuvent pas contourner
Guardian, TruthGate ou la réconciliation du Canon strict.

## Périmètre vérifié

- affirmations typées, provenance et segments de source précis ;
- frontières d’admission Guardian et TruthGate ;
- lectures immuables `TrustSnapshot` et `CanonicalView` ;
- requêtes publiques HTTP, CLI et MCP en lecture seule ;
- TRACE, reçus, restrictions, effacement et décisions explicites sur les contradictions ;
- SQLite comme profil local ordinaire ;
- sauvegarde/restauration vérifiées et export logique à ressources bornées ;
- import PostgreSQL/pgvector facultatif vers un schéma cible inactif avec vérification
  indépendante de l’état exact.

## Limite de stockage

```text
SQLite = profil local-first ordinaire actuel
PostgreSQL + pgvector = cible de migration facultative
active=false
aucune lecture/écriture runtime ordinaire
aucun basculement automatique, cutover, rollback ou dual-write
```

Le pilote PostgreSQL n’est installé qu’avec `[postgresql]` et chargé uniquement par une commande
explicite d’opérateur. Un import réussi est une preuve opérationnelle, pas une activation ni une
admission dans le Canon strict.

## Limites de sens invariantes

```text
physical L3          != strict Canon
retrieval score      != evidence
migration receipt    != claim evidence
successful import    != activation
backend availability != backend selection
```

Crystal ne revendique ni vérité universelle, ni zéro hallucination, ni runtime PostgreSQL actif,
ni multi-tenant de production, ni distributed exactly-once, ni certification juridique/RGPD/
sécurité, ni intégration Titan, ni conscience artificielle.

## Démarrage rapide

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## Preuves anglaises actuelles

- [README normatif](./README.md)
- [Rapport de vérification](./TEST_REPORT.md)
- [Statut actuel](./docs/STATUS.md)
- [Matrice d’implémentation](./docs/IMPLEMENTATION_STATUS.md)
- [Politique de sécurité](./SECURITY.md)
- [Politique de localisation](./docs/LOCALIZATION_POLICY.md)
- [Parcours français](./docs/fr/README.md)

La demande NLnet est soumise et en cours d’examen ; aucune attribution ni modification budgétaire n’est revendiquée.
