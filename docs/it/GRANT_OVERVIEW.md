# 💶 Panoramica della sovvenzione — Velantrim Crystal

> 🌐 🇬🇧 [English](../GRANT_NLNET_SCOPE.md) · 🇩🇪 [Deutsch](../de/GRANT_OVERVIEW.md) · 🇫🇷 [Français](../fr/GRANT_OVERVIEW.md) · 🇪🇸 [Español](../es/GRANT_OVERVIEW.md) · 🇮🇹 **Italiano** · 🇷🇺 [Русский](../ru/GRANT_OVERVIEW.md) · 🇨🇳 [简体中文](../zh-CN/GRANT_OVERVIEW.md)
>
> Questa pagina è un supporto di traduzione e orientamento. Non sostituisce la
> proposta presentata né i documenti inglesi su milestone, budget e criteri di
> accettazione. In caso di divergenza prevale la versione inglese.

## 📌 Stato della domanda

Velantrim Crystal è stato presentato al **NLnet NGI0 Commons Fund** per la
valutazione. Il repository non afferma che un finanziamento sia già stato
assegnato.

Il nucleo pubblico è descritto come infrastruttura di memoria IA locale,
verificabile e open source. Le priorità sono provenienza controllabile,
ammissione governata della conoscenza, funzionamento locale e prove di qualità
riproducibili.

## 🧭 Regola baseline / delta

```text
BASELINE ATTUALE
    +
DELTA FINANZIATO MISURABILE
    =
DELIVERABLE VERIFICABILE INDIPENDENTEMENTE
```

Questa regola impedisce di ricontare come prestazione finanziata una funzione già
fusa.

Se `main` evolve prima di un accordo formale, la matrice baseline/delta deve essere
aggiornata. Il delta finanziato deve restare reale, misurabile e verificabile da
terzi.

## ✅ Baseline già disponibile

Il nucleo pubblico comprende tra l’altro:

- memoria locale L0/L1 e backend a grafo L3;
- confini di ammissione Guardian e TruthGate;
- tipi di claim, stato delle fonti e provenienza;
- TRACE e Receipt riproducibili;
- baseline di Evidence Span;
- sessioni di importazione, dry-run e revisione curatoriale;
- meccanismi tecnici di cancellazione, restrizione e audit;
- valutazione deterministica con gate CI;
- interfacce FastAPI e MCP opzionali;
- runtime locale e indipendente dal provider per default.

L’implementazione esatta è determinata soltanto da GitHub `main`,
[docs/STATUS.md](../STATUS.md) e [TEST_REPORT.md](../../TEST_REPORT.md).

## 🧱 Delta finanziato previsto

La matrice inglese descrive nove aree di lavoro verificabili:

| Milestone | Obiettivo sintetico |
|---|---|
| **M1** | baseline open source riproducibile e distribuibile localmente |
| **M2** | livello FastAPI opzionale hardenizzato, ruoli chiari e default sicuri |
| **M3** | Evidence Span e verifica dei Receipt rafforzati |
| **M4** | gate di valutazione più ampi, versionati e multilingue |
| **M5** | corpus di conoscenza curato con fonti e licenze referenziate |
| **M6** | adapter di conoscenza e formati istituzionali hardenizzati |
| **M7** | accessibilità multilingue strutturata |
| **M8** | valutazione dell’indipendenza dai provider di modelli |
| **M9** | documentazione, governance e onboarding dei reviewer |

Importi, priorità e prove di accettazione esatte:

- [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
- [funding-use-plan.md](../grants/funding-use-plan.md)

## 🌍 Documentazione italiana e M7

Questo pacchetto italiano è un miglioramento docs-only della baseline prima della
formalizzazione della sovvenzione. Non introduce nuovi milestone né nuove voci di
budget.

Non deve essere presentato retroattivamente come consegna completa di M7. Un
futuro M7 finanziato dovrà ancora fornire valore aggiuntivo misurabile, ad esempio:

- struttura di localizzazione mantenuta;
- processo definito di revisione delle traduzioni;
- ulteriori lingue europee concordate;
- casi di valutazione e report di qualità specifici per lingua;
- sincronizzazione tracciabile con le release.

## 🧪 Evaluation replay e M4

Titan contiene un’implementazione di replay deterministico riesaminata come lavoro
precedente. Per Crystal:

```text
Lavoro precedente documentato ≠ runtime Crystal implementato
```

Un futuro M4 può adottare digest stabili, diff baseline/candidate, fixture
versionate e gate di sicurezza rigidi. Non entrano automaticamente nello scope:

- acquisizione live delle traiettorie di query personali;
- ottimizzazione automatica o auto-modifica;
- scrittura diretta o indiretta nel Canon;
- chiamate obbligatorie a provider esterni;
- promozione automatica dei candidati.

## 🔒 Fuori perimetro e limiti dei claim

La fase attuale non rivendica:

- SaaS chiuso;
- coscienza, personalità o cognizione biologica;
- «zero allucinazioni»;
- auto-canonizzazione autonoma;
- hosting multi-tenant pronto per la produzione senza architettura di sicurezza dedicata;
- dipendenza obbligatoria da un provider LLM;
- certificazione legale GDPR o di sicurezza;
- Titan o il Personal ExoCortex completo come deliverable.

## 🛡️ Formulazione sicura per reviewer

> Crystal offre già un nucleo locale e testato di fiducia per una memoria IA
> verificabile. Il finanziamento richiesto mira a un delta ingegneristico
> chiaramente delimitato e misurabile, per rendere questo nucleo più riproducibile,
> distribuibile, gestibile in sicurezza, multilingue e verificabile
> indipendentemente.

## 📚 Fonti normative

1. [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)
2. [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
3. [funding-use-plan.md](../grants/funding-use-plan.md)
4. [reviewer-qa.md](../grants/reviewer-qa.md)
5. [STATUS.md](../STATUS.md)
6. [TEST_REPORT.md](../../TEST_REPORT.md)

---

> 🌐 🇬🇧 [English](../GRANT_NLNET_SCOPE.md) · 🇩🇪 [Deutsch](../de/GRANT_OVERVIEW.md) · 🇫🇷 [Français](../fr/GRANT_OVERVIEW.md) · 🇪🇸 [Español](../es/GRANT_OVERVIEW.md) · 🇮🇹 **Italiano** · 🇷🇺 [Русский](../ru/GRANT_OVERVIEW.md) · 🇨🇳 [简体中文](../zh-CN/GRANT_OVERVIEW.md)