# Estado de checkpoints

| CP | Estado | Entregables | Commit |
|---|---|---|---|
| CP1 | Completo, análisis estático | inventario, VLAN, redes, 80 reglas ACL, 10 bindings, hashes, BASELINE | commit `research: capture advance 2 baseline` |
| CP2 | Completo, preparación | política propuesta, 14 casos, procedimientos, validadores, captura inmutable | commit `research: add policy test plan and reproducible PCO workflow` |
| CP3 | Completo con limitaciones T010 y procedencia de copia guardada | 14 casos, 16 ejecuciones, 13 casos válidos; observaciones, evidencia hashada, manifiestos y bitácora | commit `test: complete CP3 baseline evidence campaign` |
| CP4 | Completo con limitaciones documentadas | auditoría formal P–C–O, causalidad, procedencia, discrepancias documentales, alcance permitido y registro machine-readable | commit `analysis: close CP4 formal evidence audit` |
| CP5 | Pendiente | análisis académico basado en evidencia, relación riesgo–control, propuesta de solución y paquete del Capítulo IV | ninguno |

CP4 concluye que la campaña puede avanzar a análisis académico: 14/14 casos representados, 16 ejecuciones, 13 casos válidos, 9 casos con P=C=O y 13/13 casos válidos con P=O. T010 permanece indeterminado por falta de prerrequisito SSH verificable. T012 y T014 conservan causalidad `possible`; ningún caso se eleva a causalidad `confirmed`.

El `conformity_rate` de 69.23 % no es un porcentaje de seguridad. Cuatro allows válidos conservan C=unknown por diseño congelado. La copia runtime guardada difiere binariamente del PKT original y se mantiene como limitación de procedencia; no se modifica ni reinterpreta evidencia retroactivamente.

Ver `docs/advance2/CP4_AUDIT.md` y `research/advance2/results/cp4-audit.json`.

Los SHA exactos se obtienen con `git log --oneline research/advance2 docs/advance2`; los nombres de commit evitan una referencia circular al hash del propio archivo. Baseline original: 2873d7a0cfb71fd768775c32edc6d7b2f9b3ab46.
