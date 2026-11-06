# Índice de anexos y trazabilidad del Avance 2

El propósito de los anexos es mantener la data dura disponible sin convertir el cuerpo IEEE en un volcado de logs. Los anexos no sustituyen la interpretación; permiten verificarla.

## Anexo A — Matriz completa de pruebas y resultados

Fuentes canónicas:
- 'research/advance2/analysis/case-analysis.csv' — versión interpretada y compacta para navegación.
- 'research/advance2/tests/test-plan.csv' — P y C congelados antes de ejecutar.
- 'research/advance2/results/observations.csv' — runs observados.
- 'research/advance2/results/results.csv' — clasificación P–C–O.
- 'research/advance2/results/summary.json' — métricas derivadas.
- 'research/advance2/results/cp4-audit.json' — audit formal.

Uso académico sugerido: Tabla A-I con T001–T014; el cuerpo del artículo utiliza solo tablas resumidas.

## Anexo B — Evidencia primaria por caso

| Caso | Manifest principal | Captura/salida recomendada | Función |
|---|---|---|---|
| T001 | research/advance2/evidence/raw/T001-R1/manifest.json | T001-R2/03-T001-R2-series2-complete-0.jpg | Control Guest→External |
| T002 | research/advance2/evidence/raw/T002-R1/manifest.json | T002-R1/01-T002-series1-0.jpg | Guest→Internal deny |
| T003 | research/advance2/evidence/raw/T003-R1/manifest.json | T003-R1/14-T003-series2-complete-0.jpg | Guest→Management deny |
| T004 | research/advance2/evidence/raw/T004-R1/manifest.json | T004-R1/11-T004-series2-observed-0.jpg | Guest→RADIUS deny |
| T005 | research/advance2/evidence/raw/T005-R1/manifest.json | T005-R1/12-T005-series2-observed-0.jpg | Guest→Corp Wi-Fi deny |
| T006 | research/advance2/evidence/raw/T006-R1/manifest.json | T006-R1/04-T006-series2-complete-0.jpg | Corp Wi-Fi→External |
| T007 | research/advance2/evidence/raw/T007-R1/manifest.json | T007-R1/01-T007-series1-complete-0.jpg | Corp Wi-Fi→Internal deny |
| T008 | research/advance2/evidence/raw/T008-R1/manifest.json | T008-R1/03-T008-series2-complete-0.jpg | Corp Wi-Fi→Management deny |
| T009 | research/advance2/evidence/raw/T009-R1/manifest.json | T009-R1/01-T009-request1-0.jpg | Management→WLC HTTPS |
| T010 | research/advance2/evidence/raw/T010-R1/manifest.json | T010-R1/01-T010-SSH-precondition-0.jpg | Prerrequisito SSH ausente |
| T011 | research/advance2/evidence/raw/T011-R1/manifest.json | T011-R1/04-T011-series2-complete-0.jpg | Staff→RADIUS deny |
| T012 | research/advance2/evidence/raw/T012-R1/manifest.json | T012-R1/09-T012-series2-final-0.jpg | Staff→Management sin intercambio |
| T013 | research/advance2/evidence/raw/T013-R1/manifest.json | T013-R2/07-T013-R2-series2-complete-0.jpg | Staff→Internal allow |
| T014 | research/advance2/evidence/raw/T014-R1/manifest.json | T014-R1/13-T014-request1-observed-0.jpg | Guest→WLC HTTPS timeout |

Cada manifest contiene SHA-256 de sus artefactos. 'research/advance2/evidence/SHA256SUMS.txt' agrega el índice global.

## Anexo C — Configuración y causalidad

Fuentes:
- 'research/advance2/baseline/acl_rules.csv'
- 'research/advance2/baseline/acl_bindings.csv'
- running-config observado preservado dentro de T002/T003/T004/T005/T007/T008/T011/T012/T014.
- 'docs/advance2/CP3_EXECUTION_LOG.md'
- 'docs/advance2/CP4_AUDIT.md'

Usos:
1. justificar C=deny;
2. distinguir strongly_supported de confirmed;
3. documentar diferencias entre fragmentos históricos y estado vivo.

## Anexo D — Procedencia e integridad

- Baseline commit: 2873d7a0cfb71fd768775c32edc6d7b2f9b3ab46.
- PKT original SHA-256: 1be4c1d7c247c542ceaae24e58f43a782dfe4fcbdd524e7139f6f535b88a50fe.
- Runtime guardado SHA-256: 990d282545cc37295af7236228a8acf30981dd4ad835ffc71307b740f9db2812.
- 'research/advance2/evidence/preflight/CP3-02/provenance.json'
- 'research/advance2/baseline/hashes.json'
- 'docs/advance2/VALIDATION.md'

Este anexo debe acompañar cualquier afirmación de reproducibilidad.

## Anexo E — Cadena metodológica

- 'docs/advance2/METHODOLOGY_MAPPING.md'
- 'research/advance2/analysis/traceability.json'
- 'research/advance2/analysis/findings.md'
- 'research/advance2/analysis/proposed-controls.md'
- 'research/advance2/analysis/control-gaps.md'

Cadena:
Pregunta → objetivo → variable → caso → manifest/hash → P–C–O → hallazgo → control → verificación.

## Anexo F — Visualizaciones derivadas

- fig4_pco_status.svg
- fig5_zone_evidence.svg
- fig6_access_matrix.svg
- fig7_causal_confidence.svg
- fig8_traceability.svg

Las figuras son visualizaciones derivadas de los CSV/JSON; no sustituyen la evidencia primaria ni se presentan como screenshots de Packet Tracer.
