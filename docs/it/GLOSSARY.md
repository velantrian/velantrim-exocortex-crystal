# 📖 Glossario — Velantrim Crystal in italiano

> 🌐 🇬🇧 [English](../ARCHITECTURE.md) · 🇩🇪 [Deutsch](../de/GLOSSARY.md) · 🇫🇷 [Français](../fr/GLOSSARY.md) · 🇪🇸 [Español](../es/GLOSSARY.md) · 🇮🇹 **Italiano** · 🇷🇺 [Русский](../ru/GLOSSARY.md) · 🇨🇳 [简体中文](../zh-CN/GLOSSARY.md) · 🇸🇦 [العربية](../ar/GLOSSARY.md)
>
> Questo glossario armonizza la terminologia italiana. Non sostituisce nomi API,
> schema o codice in inglese. Gli identificatori nei blocchi di codice e nelle
> interfacce restano invariati.

## Regola generale

I nomi tecnici `TruthGate`, `Guardian`, `CanonicalView`, `TRACE` e `Receipt`
restano visibili. Alla prima occorrenza può essere aggiunta una spiegazione
italiana; il nome del contratto non viene tradotto nel codice.

| Termine inglese | Forma italiana consigliata | Significato / limite |
|---|---|---|
| **admission** | ammissione / decisione di ingresso | decisione che consente a un claim di raggiungere uno stato di memoria più affidabile |
| **claim** | claim / asserzione tipizzata | affermazione strutturata, non automaticamente un fatto verificato |
| **Canon** | Canon | proiezione strettamente ammessa, valida secondo TRACE e conforme alle policy |
| **canonical graph** | grafo canonico | grafo L3 che contiene oggetti ammessi e stati espliciti |
| **Guardian** | Guardian / controllo strutturale e di sicurezza | controllo preliminare; non sostituisce TruthGate |
| **TruthGate** | TruthGate / confine epistemico di ammissione | controlla l’ammissione automatica secondo tipo, fonte, evidenza e policy |
| **CanonicalView** | CanonicalView / vista canonica di lettura | proiezione fail-closed usata per risposte strettamente fondate |
| **TRACE** | TRACE / percorso di giustificazione | catena leggibile dalla macchina che spiega il fondamento di una risposta |
| **Receipt** | Receipt / prova sigillata | prova riproducibile e sensibile alle alterazioni su fatti e provenienza |
| **receipt replay** | replay del Receipt | nuova verifica di un Receipt rispetto allo stato corrente della memoria |
| **trajectory replay** | replay della traiettoria | ripetizione di un percorso di esecuzione per valutazione; distinto dal Receipt replay |
| **provenance** | provenienza / tracciabilità dell’origine | fonte, processo di creazione e ciclo di vita di un claim |
| **evidence span** | Evidence Span / estratto probatorio | segmento referenziato di una fonte che sostiene un claim |
| **epistemic state** | stato epistemico | stato che esprime la qualificazione di un claim, non una semplice confidenza numerica |
| **source status** | stato della fonte | categoria di origine: esterna, utente, output di modello e così via |
| **grounding** | fondamento / ancoraggio nell’evidenza | collegamento di una risposta ai claim ammessi e alle loro fonti |
| **FactsPack** | FactsPack / pacchetto controllato di fatti | contesto compatto e tracciabile per produrre una risposta |
| **read-only query** | query in sola lettura | contratto che esclude esplicitamente le mutazioni di memoria e stato elencate |
| **fail-closed** | rifiuto in caso di incertezza | nessuna ammissione silenziosa quando la fiducia è ambigua o contraddittoria |
| **baseline** | baseline / stato di riferimento | lavoro già implementato e verificato prima del delta finanziato |
| **funded delta** | delta finanziato | lavoro aggiuntivo misurabile da consegnare tramite il finanziamento |
| **deliverable** | deliverable verificabile | artefatto pubblico con prova di accettazione definita |
| **local-first** | local-first / locale per default | dati ed esecuzione locali per default; servizi esterni opzionali |
| **stdlib-only runtime** | runtime predefinito sulla libreria standard | nessun runtime terzo obbligatorio sul percorso predefinito |
| **restriction** | limitazione del trattamento | restrizione tecnica dell’uso di un oggetto memorizzato |
| **erasure** | cancellazione | rimozione tramite i livelli previsti, con regole di audit o tombstone |
| **review queue** | coda di revisione | area per claim in attesa o bloccati prima di una decisione curatoriale |
| **curator override** | eccezione curatoriale esplicita | decisione umana attribuita e auditata, mai bypass silenzioso |
| **provider independence** | indipendenza dal provider | modelli esterni intercambiabili e opzionali, senza autorità di verità |

## ⚠️ Termini da usare con cautela

### «Verificato»

Non ogni nodo del grafo è Canon verificato. Il termine deve essere usato solo
quando stato, evidenza, TRACE e policy lo sostengono realmente.

### «Conforme al GDPR»

Formulazioni preferite:

```text
controlli tecnici rilevanti per il GDPR
architettura orientata al GDPR
```

Da evitare senza fondamento legale:

```text
certificato GDPR
garanzia di piena conformità legale
```

### «Sicuro» o «hardened»

«Hardened» indica misure tecniche e test documentati. Non è una certificazione di
sicurezza né prova dell’assenza di vulnerabilità.

### «Verità»

`TruthGate` non è un rilevatore universale di verità. È un confine epistemico di
ammissione controllato entro un modello definito di dati e policy.

### «Replay»

Distinguere sempre:

```text
Receipt replay    = verificare di nuovo una prova esistente
Trajectory replay = ripetere un percorso di esecuzione per la valutazione
```

### «Cognitivo», «vivo», «coscienza»

Questi termini non descrivono le capacità runtime attuali di Crystal. I nomi
bio-ispirati sono metafore ingegneristiche, non claim biologici o personali.

## Stile consigliato per i documenti italiani

Preferire:

- frasi brevi e verificabili;
- identificatori di codice invariati tra backtick;
- separazione chiara tra «implementato», «opzionale», «pianificato» e «ricerca»;
- nessuna traduzione che rafforzi la fonte inglese;
- numeri accompagnati da un collegamento alla fonte normativa;
- linguaggio da reviewer invece di marketing vago.

Evitare:

- promesse assolute di affidabilità;
- formulazioni di marketing senza prova di test;
- confusione tra Titan e Crystal;
- equiparazione automatica del contenuto del grafo a verità verificata;
- presentazione di un PR aperto o RFC come runtime.

---

> 🌐 🇬🇧 [English](../ARCHITECTURE.md) · 🇩🇪 [Deutsch](../de/GLOSSARY.md) · 🇫🇷 [Français](../fr/GLOSSARY.md) · 🇪🇸 [Español](../es/GLOSSARY.md) · 🇮🇹 **Italiano** · 🇷🇺 [Русский](../ru/GLOSSARY.md) · 🇨🇳 [简体中文](../zh-CN/GLOSSARY.md) · 🇸🇦 [العربية](../ar/GLOSSARY.md)