# 📖 Glossaire — Velantrim Crystal en français

> 🌐 🇬🇧 [English](../ARCHITECTURE.md) · 🇩🇪 [Deutsch](../de/GLOSSARY.md) · 🇫🇷 **Français** · 🇪🇸 [Español](../es/GLOSSARY.md)
>
> Ce glossaire harmonise la terminologie française. Il ne remplace aucun nom
> d’API, de schéma ou de code en anglais. Les identifiants dans les blocs de code
> et les interfaces restent inchangés.

## Règle générale

Les noms techniques `TruthGate`, `Guardian`, `CanonicalView`, `TRACE` et
`Receipt` restent visibles. Une explication française peut les accompagner lors
de la première occurrence ; le nom du contrat n’est pas traduit dans le code.

| Terme anglais | Forme française recommandée | Sens / limite |
|---|---|---|
| **admission** | admission / décision d’entrée | décision autorisant un claim à atteindre un état de mémoire plus fiable |
| **claim** | claim / assertion typée | affirmation structurée, pas automatiquement un fait vérifié |
| **Canon** | Canon | projection strictement admise, valide selon TRACE et conforme aux règles |
| **canonical graph** | graphe canonique | graphe L3 portant des objets admis et des statuts explicites |
| **Guardian** | Guardian / contrôle structurel et sécurité | contrôle préalable ; ne remplace pas TruthGate |
| **TruthGate** | TruthGate / frontière d’admission épistémique | contrôle l’admission automatique selon type, source, preuves et politique |
| **CanonicalView** | CanonicalView / vue canonique de lecture | projection fail-closed utilisée pour les réponses strictement fondées |
| **TRACE** | TRACE / chemin de justification | chaîne lisible par machine expliquant le fondement d’une réponse |
| **Receipt** | Receipt / preuve scellée | preuve rejouable et sensible aux altérations sur les faits et la provenance |
| **receipt replay** | replay de Receipt | revérification d’un Receipt contre l’état mémoire actuel |
| **trajectory replay** | replay de trajectoire | répétition d’un chemin d’exécution à des fins d’évaluation ; distinct du Receipt replay |
| **provenance** | provenance / traçabilité d’origine | source, processus de création et cycle de vie d’un claim |
| **evidence span** | Evidence Span / extrait probant | segment référencé d’une source soutenant un claim |
| **epistemic state** | état épistémique | statut exprimant la qualification d’un claim, pas une simple confiance numérique |
| **source status** | statut de source | catégorie d’origine : externe, utilisateur, sortie de modèle, etc. |
| **grounding** | fondement / ancrage par les preuves | rattachement d’une réponse aux claims admis et à leurs sources |
| **FactsPack** | FactsPack / paquet de faits contrôlé | contexte compact et traçable pour produire une réponse |
| **read-only query** | requête en lecture | contrat excluant explicitement les mutations mémoire et d’état listées |
| **fail-closed** | refus en cas d’incertitude | aucune admission silencieuse lorsque la confiance est ambiguë ou contradictoire |
| **baseline** | baseline / état de référence | travail déjà implémenté et vérifié avant le delta financé |
| **funded delta** | delta financé | travail supplémentaire mesurable devant être livré par le financement |
| **deliverable** | livrable vérifiable | artefact public avec preuve d’acceptation définie |
| **local-first** | local-first / local par défaut | données et exécution locales par défaut ; services externes optionnels |
| **stdlib-only runtime** | runtime par défaut sur bibliothèque standard | aucun runtime tiers obligatoire sur le chemin par défaut |
| **restriction** | restriction du traitement | limitation technique de l’utilisation d’un objet stocké |
| **erasure** | effacement | suppression via les couches prévues, avec règles d’audit ou tombstone |
| **review queue** | file de revue | zone des claims en attente ou bloqués avant décision curatoriale |
| **curator override** | exception curatoriale explicite | décision humaine attribuée et auditée, jamais bypass silencieux |
| **provider independence** | indépendance fournisseur | modèles externes interchangeables et optionnels, sans autorité de vérité |

## ⚠️ Termes à employer avec prudence

### « Vérifié »

Tout nœud du graphe n’est pas du Canon vérifié. Le terme ne doit être utilisé que
si le statut, les preuves, TRACE et les politiques le permettent réellement.

### « Conforme au RGPD »

Formulations préférées :

```text
contrôles techniques pertinents pour le RGPD
architecture orientée RGPD
```

À éviter sans fondement juridique :

```text
certifié RGPD
garantie de conformité juridique complète
```

### « Sécurisé » ou « durci »

« Durci » désigne des mesures techniques et des tests documentés. Ce n’est pas
une certification de sécurité ni la preuve de l’absence de vulnérabilité.

### « Vérité »

`TruthGate` n’est pas un détecteur universel de vérité. C’est une frontière
d’admission épistémique contrôlée dans un modèle de données et de politiques
défini.

### « Replay »

Toujours distinguer :

```text
Receipt replay    = revérifier une preuve existante
Trajectory replay = répéter un chemin d’exécution pour l’évaluation
```

### « Cognitif », « vivant », « conscience »

Ces termes ne décrivent pas les capacités runtime actuelles de Crystal. Les noms
bio-inspirés sont des métaphores d’ingénierie, pas des claims biologiques ou de
personnalité.

## Style recommandé pour les documents français

Préférer :

- phrases courtes et vérifiables ;
- identifiants de code inchangés entre backticks ;
- séparation claire entre « implémenté », « optionnel », « planifié » et « recherche » ;
- aucune traduction renforçant la source anglaise ;
- chiffres accompagnés d’un lien vers la source normative ;
- langage reviewer plutôt que marketing vague.

Éviter :

- promesses absolues de fiabilité ;
- formulations marketing sans preuve de test ;
- confusion entre Titan et Crystal ;
- assimilation automatique du contenu du graphe à une vérité vérifiée ;
- présentation d’un PR ouvert ou d’un RFC comme runtime.

---

> 🌐 🇬🇧 [English](../ARCHITECTURE.md) · 🇩🇪 [Deutsch](../de/GLOSSARY.md) · 🇫🇷 **Français** · 🇪🇸 [Español](../es/GLOSSARY.md)