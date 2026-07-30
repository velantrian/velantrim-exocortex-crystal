# 📌 Velantrim Crystal — Estado actual

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 **Español** · 🇮🇹 [Italiano](../it/STATUS.md)

**Fecha del estado:** 30 de julio de 2026  
**Estado del repositorio utilizado para esta traducción:** `main@30e87df4`  
**Último checkpoint con cambios de runtime:** PR #265 / `cd6fd44`  
**Baseline normativa de tests:** [TEST_REPORT.md](../../TEST_REPORT.md)

> Esta página es una traducción del estado. En caso de discrepancia, GitHub
> `main`, el [STATUS en inglés](../STATUS.md) y
> [TEST_REPORT.md](../../TEST_REPORT.md) son autoritativos.

---

## 🧭 Regla de lectura

```text
GitHub Crystal main = verdad pública de implementación
Notion Crystal       = mapa sincronizado de subvención y estrategia
Titan / Full         = laboratorio de investigación separado
```

Un documento, una nota de Notion, una rama prototipo o un módulo de Titan no es
una capacidad actual de Crystal hasta que se implemente, se pruebe y se fusione
en Crystal `main`.

## ✅ Checkpoint verificado

El PR #265 introdujo la frontera HTTP estrictamente de solo lectura:

```text
POST /ingest   → admisión mediante Guardian + TruthGate
POST /ask      → consulta canónica estrictamente de solo lectura
GET  /receipt  → lectura estricta con Receipt
```

Los endpoints HTTP `/ask` y `/receipt` no escriben en L0/L1 ni L3, no transicionan
ESM, no operan la outbox, no registran enlaces episódicos, no inicializan una
huella de embedding y no modifican la verificación adaptativa.

### Límites residuales explícitos

- CLI `ask` y `receipt` permanecen sobre `core.pipeline.run()`;
- `core.pipeline.run()` sigue siendo una ruta de compatibilidad capaz de admisión;
- MCP no tiene herramientas explícitas de escritura canónica, pero una búsqueda
  puede inicializar una huella de embedding ausente.

Estos puntos son follow-ups conocidos, no capacidades ocultas.

## 🧪 Baseline de verificación

```text
1713 passed
12 skipped
0 failed
6389 measured statements
100.00% coverage
```

El run CI `30284938992` completó correctamente los siete jobs permanentes antes
del merge: Python 3.11/3.12, Ruff, seguridad, Docker build, evaluation gate e
integridad JSONL.

## 🛡️ Frontera de claims públicos

Crystal puede describirse como:

- infraestructura de memoria IA local-first y verificable;
- núcleo de memoria orientado a fuentes y procedencia;
- sistema con controles de admisión Guardian y TruthGate donde están conectados;
- sistema con CanonicalView, TRACE y Receipts reproducibles donde están conectados;
- runtime predeterminado basado en la biblioteca estándar con adaptadores opcionales;
- proyecto con mecanismos técnicos de borrado y restricción relacionados con el RGPD;
- baseline open source de nivel investigación verificable de forma independiente.

Crystal no debe describirse como:

- Titan o el Personal ExoCortex completo;
- un sistema operativo cognitivo autónomo;
- consciente, vivo o biológicamente equivalente a un cerebro;
- universalmente verdadero o libre de alucinaciones;
- jurídicamente certificado conforme al RGPD;
- certificado en seguridad o listo para producción multi-tenant;
- dependiente de un LLM externo o proveedor cloud obligatorio.

## 💶 Estado de la subvención

La propuesta al **NLnet NGI0 Commons Fund** fue presentada y está en evaluación.
El repositorio no afirma que la financiación haya sido concedida.

```text
BASELINE ACTUAL
    +
DELTA FINANCIADO MEDIBLE
    =
ENTREGABLE VERIFICABLE DE FORMA INDEPENDIENTE
```

El trabajo ya fusionado permanece en la baseline y no se vuelve a contar como
milestone pagado. Las reglas normativas se mantienen en:

- [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)
- [baseline-funded-delta-matrix.md](../grants/baseline-funded-delta-matrix.md)
- [funding-use-plan.md](../grants/funding-use-plan.md)

La síntesis española se encuentra en [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md).

## 🧪 Decisión sobre evaluation replay

La implementación de replay determinista de Titan se examinó como trabajo previo.
No se copió al runtime de Crystal.

```text
REVIEWED_PRIOR_ART
DOCUMENTED_ONLY
M4_CANDIDATE
NO_RUNTIME_CHANGE
NO_CANON_WRITE
NO_BUDGET_CHANGE
BASELINE_NOT_MOVED
```

Una implementación futura debe ampliar el stack de evaluación existente de
Crystal, pasar por un RFC/issue/PR separado, permanecer offline y no autoritativa,
y preservar TruthGate y las fronteras de consulta.

## 🔬 Regla para investigación y PR draft

Los PR abiertos de investigación o branding no son verdad de implementación.
Antes del merge deben rebasarse sobre el `main` actual, volver a auditarse para el
lenguaje de subvención y comprobarse frente al estado normativo.

## 📚 Ruta para reviewers

1. [REVIEWER_GUIDE.md](./REVIEWER_GUIDE.md)
2. [QUICKSTART.md](./QUICKSTART.md)
3. [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md)
4. [GLOSSARY.md](./GLOSSARY.md)
5. [Estado normativo en inglés](../STATUS.md)
6. [TEST_REPORT.md](../../TEST_REPORT.md)

---

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 **Español** · 🇮🇹 [Italiano](../it/STATUS.md)