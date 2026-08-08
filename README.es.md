# 🔱 Velantrim ExoCortex — Crystal

> 🌐 [English — fuente normativa](./README.md) · 🇪🇸 **Resumen en español**

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->

### Infraestructura de memoria verificable y local para sistemas de IA confiables

Este archivo es un **resumen de orientación no normativo**, no una traducción completa. Las
decisiones técnicas, la arquitectura, el estado, la seguridad y las afirmaciones sobre la
subvención se mantienen en inglés. Si hay diferencias, prevalecen [README.md](./README.md) y la
evidencia inglesa.

`v0.3.0` · 🧪 **2078 aprobadas / 13 omitidas** · 🎯 **100.00% de cobertura** · ✅ **9 tareas CI**

**Checkpoint runtime verificado:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337.

Crystal separa almacenamiento físico, evidencia, admisión epistémica y lecturas confiables. La
presencia de datos, su clasificación o una migración no pueden eludir Guardian, TruthGate ni la
reconciliación del Canon estricto.

## Alcance verificado

- afirmaciones tipadas, procedencia y fragmentos exactos de fuente;
- límites de admisión Guardian y TruthGate;
- lecturas inmutables `TrustSnapshot` y `CanonicalView`;
- consultas públicas HTTP, CLI y MCP de solo lectura;
- TRACE, recibos, restricciones, borrado y decisiones explícitas de contradicción;
- SQLite como perfil local ordinario;
- copia/restauración verificadas y exportación lógica con recursos acotados;
- importación PostgreSQL/pgvector opcional a un esquema objetivo inactivo con comprobación
  independiente del estado exacto.

## Límite de almacenamiento

```text
SQLite = perfil local-first ordinario actual
PostgreSQL + pgvector = objetivo de migración opcional
active=false
sin lecturas/escrituras runtime ordinarias
sin cambio automático, cutover, rollback ni dual-write
```

El controlador PostgreSQL solo se instala mediante `[postgresql]` y solo se carga por una orden
explícita del operador. Una importación correcta es evidencia operativa, no activación ni ingreso
al Canon estricto.

## Límites de significado invariantes

```text
physical L3          != strict Canon
retrieval score      != evidence
migration receipt    != claim evidence
successful import    != activation
backend availability != backend selection
```

Crystal no afirma verdad universal, cero alucinaciones, un runtime PostgreSQL activo,
multi-tenancy de producción, distributed exactly-once, certificación legal/RGPD/seguridad,
integración Titan ni conciencia artificial.

## Inicio rápido

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## Evidencia inglesa actual

- [README normativo](./README.md)
- [Informe de verificación](./TEST_REPORT.md)
- [Estado actual](./docs/STATUS.md)
- [Matriz de implementación](./docs/IMPLEMENTATION_STATUS.md)
- [Política de seguridad](./SECURITY.md)
- [Política de localización](./docs/LOCALIZATION_POLICY.md)
- [Ruta documental en español](./docs/es/README.md)

La solicitud NLnet está presentada y en revisión; no se afirma concesión ni cambio presupuestario.
