# 🔍 Guía para reviewers — Velantrim Crystal

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 **Español** · 🇮🇹 [Italiano](../it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](../ru/REVIEWER_GUIDE.md)
>
> Esta página proporciona una ruta de verificación en español. No introduce
> ningún claim nuevo de runtime, subvención, cumplimiento o seguridad. En caso de
> discrepancia, GitHub `main`, [docs/STATUS.md](../STATUS.md) y
> [TEST_REPORT.md](../../TEST_REPORT.md) son autoritativos.

## 1. Qué es Crystal

Crystal es el núcleo público, mínimo y verificable de memoria de Velantrim:

- local-first y sin dependencia cloud obligatoria;
- claims fundamentados en fuentes con estado epistémico explícito;
- Guardian + TruthGate como frontera de admisión automática hacia L3;
- CanonicalView para lecturas estrictamente fundamentadas;
- TRACE y Receipt como capa de prueba verificable;
- backends locales SQLite/WAL y grafos embebidos;
- mecanismos técnicos de borrado, restricción, auditoría y procedencia;
- tests reproducibles y gates de evaluación deterministas.

## 2. Qué no es Crystal

Crystal no afirma ser:

- una AGI, una conciencia, una persona o el equivalente biológico de un cerebro;
- una garantía de «cero alucinaciones»;
- el stack completo de Titan o Personal ExoCortex;
- un sistema de automodificación o autocanonización;
- un producto dependiente de un LLM, grafo o cloud obligatorio;
- una certificación jurídica de conformidad con el RGPD;
- una certificación de seguridad o hosting multi-tenant listo para producción;
- la implementación runtime de cada idea de investigación o PR abierto.

## 3. Fuentes autoritativas

Comprobar en este orden:

1. GitHub `main` — código realmente fusionado;
2. [TEST_REPORT.md](../../TEST_REPORT.md) — baseline de tests y cobertura;
3. [docs/STATUS.md](../STATUS.md) — estado actual de claims y componentes;
4. [docs/IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md) — mapa detallado;
5. [docs/ARCHITECTURE.md](../ARCHITECTURE.md) — fronteras de arquitectura;
6. documentos de subvención en inglés — scope y criterios de aceptación.

Una nota de Notion, una roadmap, un RFC, un prototipo o un PR abierto no es una
capacidad implementada.

## 4. Reproducción limpia

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

Resultados esperados:

- tests y gate de cobertura superados;
- ninguna regresión comunicada por `eval_gate.py`;
- los artefactos generados no ensucian el árbol Git;
- las cifras se comparan con [TEST_REPORT.md](../../TEST_REPORT.md).

## 5. Verificar los contratos esenciales

### 🛡️ Admisión

```text
nuevo claim
→ clasificación + evidencia
→ Guardian
→ TruthGate
→ memoria operativa / Canon admitido
```

Pregunta de control: ¿puede un claim débil, sin evidencia o mal tipado evitar los
gates previstos?

### 🔎 Consulta HTTP

```text
POST /ask o GET /receipt
→ core.query_pipeline.query()
→ Canon ya existente
→ CanonicalView
→ respuesta o rechazo acotado
```

Pregunta de control: ¿L0/L1, L3, ESM, outbox, enlaces episódicos, huella de
embedding y verificación adaptativa permanecen sin cambios durante las consultas
HTTP migradas?

La garantía es deliberadamente estrecha:

- CLI `ask` y `receipt` aún no están migrados;
- MCP puede inicializar una huella de embedding ausente.

### 🔗 TRACE y Receipt

```bash
velantrim receipt "your question" > receipt.json
velantrim verify-receipt receipt.json
velantrim verify-receipt receipt.json --strict-provenance
```

Pregunta de control: ¿se pueden identificar los hechos y referencias de evidencia
que sostuvieron una respuesta, y se detecta la deriva?

### 🧾 Auditoría y procedencia

```bash
velantrim audit
velantrim audit-verify
velantrim history <fact_id>
```

`history` y la `ProvenanceChain` por hecho son vistas diferentes. La documentación
y los tests no deben confundirlas.

## 6. Iniciar el servicio HTTP de forma prudente

```bash
pip install '.[api]'
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
docker compose up --build
curl http://127.0.0.1:8000/health
```

Puntos que deben comprobarse:

- no existe token fallback;
- publicación loopback por defecto;
- usuario del contenedor no privilegiado;
- dependencias de API opcionales;
- contratos distintos para `/ingest` y `/ask`.

## 7. Verificar la evaluación

Crystal mide, entre otros elementos:

- retrieval `hit@k` y MRR;
- completitud de TRACE y metadatos;
- cobertura de Evidence Spans;
- Receipt replay;
- precisión y recall de contradicciones;
- rechazos correctos en las fronteras de confianza.

El replay de Titan es trabajo previo documentado, no una capacidad actual de
Crystal ni un runtime que se autooptimiza.

## 8. Verificar el marco de subvención

El reviewer debe separar claramente la baseline existente del delta solicitado:

```text
baseline existente y probada
+
trabajo financiado concreto y medible
=
entregable verificable de forma independiente
```

Las funciones ya fusionadas no deben volver a contabilizarse como trabajo pagado.
La solicitud está en evaluación; no se afirma que haya sido concedida.

Resumen español: [GRANT_OVERVIEW.md](./GRANT_OVERVIEW.md)  
Fuente normativa: [GRANT_NLNET_SCOPE.md](../GRANT_NLNET_SCOPE.md)

## 9. Señales de alerta

🚩 Un documento afirma más que `main` o `STATUS.md`.  
🚩 Un módulo de investigación se presenta como runtime de Crystal.  
🚩 Una traducción amplía scope, presupuesto o claims de cumplimiento.  
🚩 Una consulta modifica inesperadamente un estado de memoria.  
🚩 Una métrica media oculta una regresión de seguridad o un caso individual.  
🚩 Un proveedor externo se convierte implícitamente en obligatorio.

## 10. Comprobación final

Al terminar, un reviewer debe poder responder:

1. ¿Qué claims pueden entrar automáticamente en el Canon?
2. ¿Qué rutas de consulta son realmente de solo lectura?
3. ¿Cómo se vincula una respuesta con hechos y evidencia?
4. ¿Qué límites están implementados y cuáles solo planificados?
5. ¿Qué delta de subvención queda tras descontar la baseline existente?

---

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 **Español** · 🇮🇹 [Italiano](../it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](../ru/REVIEWER_GUIDE.md)