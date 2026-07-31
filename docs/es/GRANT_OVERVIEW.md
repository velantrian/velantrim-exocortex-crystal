# 💶 Resumen de la subvención — Velantrim Crystal

> 🌐 🇬🇧 [English](../GRANT_NLNET_SCOPE.md) · 🇩🇪 [Deutsch](../de/GRANT_OVERVIEW.md) · 🇫🇷 [Français](../fr/GRANT_OVERVIEW.md) · 🇪🇸 **Español** · 🇮🇹 [Italiano](../it/GRANT_OVERVIEW.md) · 🇷🇺 [Русский](../ru/GRANT_OVERVIEW.md) · 🇨🇳 [简体中文](../zh-CN/GRANT_OVERVIEW.md) · 🇸🇦 [العربية](../ar/GRANT_OVERVIEW.md)
>
> Esta página es una ayuda de traducción y orientación. No sustituye la solicitud
> presentada ni los documentos ingleses de milestones, presupuesto y criterios de
> aceptación. En caso de discrepancia, prevalece la versión inglesa.

## 📌 Estado de la solicitud

Velantrim Crystal se presentó al **NLnet NGI0 Commons Fund** para evaluación. El
repositorio no afirma que la financiación haya sido concedida.

El núcleo público se presenta como infraestructura de memoria IA local,
verificable y de código abierto. Las prioridades son la procedencia auditable, la
admisión gobernada del conocimiento, la operación local y las pruebas de calidad
reproducibles.

## 🧭 Regla baseline / delta

```text
BASELINE ACTUAL
    +
DELTA FINANCIADO MEDIBLE
    =
ENTREGABLE VERIFICABLE DE FORMA INDEPENDIENTE
```

Esta regla evita volver a contabilizar como prestación financiada una función que
ya estaba fusionada.

Si `main` evoluciona antes de un acuerdo formal, debe actualizarse la matriz
baseline/delta. El delta financiado debe seguir siendo real, medible y verificable
por terceros.

## ✅ Baseline ya disponible

El núcleo público actual incluye, entre otros elementos:

- almacenamiento local L0/L1 y backends de grafo L3;
- fronteras de admisión Guardian y TruthGate;
- tipos de claims, estado de fuentes y metadatos de procedencia;
- TRACE y Receipts reproducibles;
- baseline de Evidence Spans;
- sesiones de importación, dry-run y revisión curatorial;
- mecanismos técnicos de borrado, restricción y auditoría;
- evaluación determinista con gates de CI;
- interfaces FastAPI y MCP opcionales;
- runtime local e independiente de proveedor por defecto.

La implementación exacta queda determinada únicamente por GitHub `main`,
[docs/STATUS.md](../STATUS.md) y [TEST_REPORT.md](../../TEST_REPORT.md).

## 🧱 Delta financiado previsto

La matriz inglesa describe nueve áreas de trabajo verificables:

| Milestone | Objetivo resumido |
|---|---|
| **M1** | baseline open source reproducible y desplegable localmente |
| **M2** | capa FastAPI opcional endurecida, roles claros y defaults seguros |
| **M3** | Evidence Spans y verificación de Receipts reforzados |
| **M4** | gates de evaluación más amplios, versionados y multilingües |
| **M5** | corpus de conocimiento curado con fuentes y licencias referenciadas |
| **M6** | adaptadores de conocimiento y formatos institucionales endurecidos |
| **M7** | accesibilidad multilingüe estructurada |
| **M8** | evaluación de independencia respecto a proveedores de modelos |
| **M9** | documentación, gobernanza y onboarding de reviewers |

Importes, prioridades y pruebas de aceptación exactas:

- [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
- [funding-use-plan.md](../grants/funding-use-plan.md)

## 🌍 Documentación española y M7

Este paquete español es una mejora docs-only de la baseline anterior a la fijación
formal de la subvención. No introduce ningún milestone ni partida presupuestaria
nuevos.

No debe presentarse retroactivamente como la entrega completa de M7. Un M7 futuro
financiado todavía tendría que aportar valor adicional medible, por ejemplo:

- estructura de localización mantenida;
- proceso definido de revisión de traducciones;
- otros idiomas europeos acordados;
- casos de evaluación e informes de calidad específicos por idioma;
- sincronización trazable con releases.

## 🧪 Evaluation replay y M4

Titan contiene una implementación de replay determinista revisada como trabajo
previo. Para Crystal:

```text
Trabajo previo documentado ≠ runtime Crystal implementado
```

Un M4 futuro puede incorporar digests estables, diffs baseline/candidate,
fixtures versionadas y gates estrictos de seguridad. No se incorporan
automáticamente al scope:

- captura live de trayectorias de consultas personales;
- optimización automática o automodificación;
- escritura directa o indirecta en el Canon;
- llamadas obligatorias a proveedores externos;
- promoción automática de candidatos.

## 🔒 Fuera de alcance y límites de comunicación

La fase actual no afirma ofrecer:

- un SaaS cerrado;
- conciencia, personalidad o cognición biológica;
- «cero alucinaciones»;
- autocanonización autónoma;
- hosting multi-tenant listo para producción sin arquitectura de seguridad dedicada;
- dependencia obligatoria de un proveedor LLM;
- certificación jurídica de RGPD o certificación de seguridad;
- Titan o el Personal ExoCortex completo como entregable.

## 🛡️ Formulación segura para reviewers

> Crystal ya proporciona un núcleo local y probado de confianza para memoria IA
> verificable. La financiación solicitada pretende cubrir un delta de ingeniería
> claramente delimitado y medible para hacer este núcleo más reproducible,
> desplegable, operable de forma segura, multilingüe y verificable de manera
> independiente.

## 📚 Fuentes normativas

1. [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)
2. [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
3. [funding-use-plan.md](../grants/funding-use-plan.md)
4. [reviewer-qa.md](../grants/reviewer-qa.md)
5. [STATUS.md](../STATUS.md)
6. [TEST_REPORT.md](../../TEST_REPORT.md)

---

> 🌐 🇬🇧 [English](../GRANT_NLNET_SCOPE.md) · 🇩🇪 [Deutsch](../de/GRANT_OVERVIEW.md) · 🇫🇷 [Français](../fr/GRANT_OVERVIEW.md) · 🇪🇸 **Español** · 🇮🇹 [Italiano](../it/GRANT_OVERVIEW.md) · 🇷🇺 [Русский](../ru/GRANT_OVERVIEW.md) · 🇨🇳 [简体中文](../zh-CN/GRANT_OVERVIEW.md) · 🇸🇦 [العربية](../ar/GRANT_OVERVIEW.md)