# Estado de checkpoints

| CP | Estado | Entregables | Commit |
|---|---|---|---|
| CP1 | Completo, análisis estático | inventario, VLAN, redes, 80 reglas ACL, 10 bindings, hashes, BASELINE | commit `research: capture advance 2 baseline` |
| CP2 | Completo, preparación | política propuesta, 14 casos, procedimientos, validadores, captura inmutable | commit `research: add policy test plan and reproducible PCO workflow` |
| CP3 | Pendiente | ejecución real, endpoints, artefactos, manifiestos, observations | ninguno |
| CP4 | Pendiente experimental; herramientas listas | validación completa y clasificación de observaciones reales | ninguno |
| CP5 | Pendiente | análisis basado en evidencia y paquete del Capítulo IV | ninguno |

Los SHA exactos se obtienen con `git log --oneline research/advance2 docs/advance2`; los nombres de commit evitan una referencia circular al hash del propio archivo. Baseline original: 2873d7a0cfb71fd768775c32edc6d7b2f9b3ab46.
