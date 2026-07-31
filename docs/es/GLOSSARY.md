# 📖 Glosario — Velantrim Crystal en español

> 🌐 🇬🇧 [English](../ARCHITECTURE.md) · 🇩🇪 [Deutsch](../de/GLOSSARY.md) · 🇫🇷 [Français](../fr/GLOSSARY.md) · 🇪🇸 **Español** · 🇮🇹 [Italiano](../it/GLOSSARY.md) · 🇷🇺 [Русский](../ru/GLOSSARY.md) · 🇨🇳 [简体中文](../zh-CN/GLOSSARY.md) · 🇸🇦 [العربية](../ar/GLOSSARY.md) · 🇯🇵 [日本語](../ja/GLOSSARY.md) · 🇮🇳 [हिन्दी](../hi/GLOSSARY.md)
>
> Este glosario armoniza la terminología española. No sustituye ningún nombre de
> API, esquema o código en inglés. Los identificadores en bloques de código e
> interfaces permanecen sin cambios.

## Regla general

Los nombres técnicos `TruthGate`, `Guardian`, `CanonicalView`, `TRACE` y
`Receipt` se mantienen visibles. Puede añadirse una explicación en español en la
primera aparición; el nombre del contrato no se traduce en el código.

| Término inglés | Forma española recomendada | Significado / límite |
|---|---|---|
| **admission** | admisión / decisión de entrada | decisión que permite a un claim alcanzar un estado de memoria más fiable |
| **claim** | claim / afirmación tipada | afirmación estructurada; no es automáticamente un hecho verificado |
| **Canon** | Canon | proyección estrictamente admitida, válida según TRACE y conforme a la política |
| **canonical graph** | grafo canónico | grafo L3 que contiene objetos admitidos y estados explícitos |
| **Guardian** | Guardian / control estructural y de seguridad | control previo; no sustituye a TruthGate |
| **TruthGate** | TruthGate / frontera de admisión epistémica | controla la admisión automática según tipo, fuente, evidencia y política |
| **CanonicalView** | CanonicalView / vista canónica de lectura | proyección fail-closed para respuestas estrictamente fundamentadas |
| **TRACE** | TRACE / ruta de justificación | cadena legible por máquina que explica la fundamentación de una respuesta |
| **Receipt** | Receipt / prueba sellada | prueba reproducible y sensible a alteraciones sobre hechos y procedencia |
| **receipt replay** | replay de Receipt | nueva verificación de un Receipt frente al estado actual de la memoria |
| **trajectory replay** | replay de trayectoria | repetición de una ruta de ejecución con fines de evaluación; distinto del Receipt replay |
| **provenance** | procedencia / trazabilidad de origen | fuente, proceso de creación y ciclo de vida de un claim |
| **evidence span** | Evidence Span / fragmento probatorio | segmento referenciado de una fuente que respalda un claim |
| **epistemic state** | estado epistémico | estado que expresa cómo se califica un claim; no es una simple confianza numérica |
| **source status** | estado de la fuente | categoría de origen: externo, usuario, salida de modelo, etc. |
| **grounding** | fundamentación / anclaje en evidencia | vínculo de una respuesta con claims admitidos y sus fuentes |
| **FactsPack** | FactsPack / paquete controlado de hechos | contexto compacto y trazable para producir una respuesta |
| **read-only query** | consulta de solo lectura | contrato que excluye explícitamente las mutaciones de memoria y estado enumeradas |
| **fail-closed** | rechazo ante la incertidumbre | no hay admisión silenciosa cuando la confianza es ambigua o contradictoria |
| **baseline** | baseline / estado de referencia | trabajo ya implementado y verificado antes del delta financiado |
| **funded delta** | delta financiado | trabajo adicional medible que debe entregarse con la financiación |
| **deliverable** | entregable verificable | artefacto público con prueba de aceptación definida |
| **local-first** | local-first / local por defecto | datos y ejecución locales por defecto; servicios externos opcionales |
| **stdlib-only runtime** | runtime predeterminado sobre biblioteca estándar | ningún runtime de terceros obligatorio en la ruta predeterminada |
| **restriction** | restricción del tratamiento | limitación técnica del uso de un objeto almacenado |
| **erasure** | borrado | eliminación mediante las capas previstas, con reglas de auditoría o tombstone |
| **review queue** | cola de revisión | zona para claims pendientes o bloqueados antes de una decisión curatorial |
| **curator override** | excepción curatorial explícita | decisión humana atribuida y auditada; nunca un bypass silencioso |
| **provider independence** | independencia de proveedor | modelos externos intercambiables y opcionales, sin autoridad de verdad |

## ⚠️ Términos que requieren prudencia

### «Verificado»

No todo nodo del grafo forma parte del Canon verificado. El término solo debe
usarse cuando el estado, la evidencia, TRACE y las políticas lo permiten realmente.

### «Conforme al RGPD»

Formulaciones preferidas:

```text
controles técnicos relevantes para el RGPD
arquitectura orientada al RGPD
```

Evitar sin fundamento jurídico:

```text
certificado conforme al RGPD
garantía de cumplimiento jurídico completo
```

### «Seguro» o «endurecido»

«Endurecido» describe medidas técnicas y tests documentados. No es una
certificación de seguridad ni demuestra la ausencia de vulnerabilidades.

### «Verdad»

`TruthGate` no es un detector universal de verdad. Es una frontera controlada de
admisión epistémica dentro de un modelo definido de datos y políticas.

### «Replay»

Distinguir siempre:

```text
Receipt replay    = volver a verificar una prueba existente
Trajectory replay = repetir una ruta de ejecución para evaluación
```

### «Cognitivo», «vivo», «conciencia»

Estos términos no describen las capacidades actuales del runtime de Crystal. Los
nombres bioinspirados son metáforas de ingeniería, no claims biológicos o de
personalidad.

## Estilo recomendado para documentos en español

Preferir:

- frases breves y verificables;
- identificadores de código sin traducir y entre backticks;
- separación clara entre «implementado», «opcional», «planificado» e «investigación»;
- ninguna traducción que refuerce la fuente inglesa;
- cifras acompañadas de un enlace a la fuente normativa;
- lenguaje para reviewers en lugar de marketing impreciso.

Evitar:

- promesas absolutas de fiabilidad;
- formulaciones de marketing sin prueba de tests;
- confusión entre Titan y Crystal;
- equiparar automáticamente el contenido del grafo con verdad verificada;
- presentar un PR abierto o un RFC como runtime.

---

> 🌐 🇬🇧 [English](../ARCHITECTURE.md) · 🇩🇪 [Deutsch](../de/GLOSSARY.md) · 🇫🇷 [Français](../fr/GLOSSARY.md) · 🇪🇸 **Español** · 🇮🇹 [Italiano](../it/GLOSSARY.md) · 🇷🇺 [Русский](../ru/GLOSSARY.md) · 🇨🇳 [简体中文](../zh-CN/GLOSSARY.md) · 🇸🇦 [العربية](../ar/GLOSSARY.md) · 🇯🇵 [日本語](../ja/GLOSSARY.md) · 🇮🇳 [हिन्दी](../hi/GLOSSARY.md)