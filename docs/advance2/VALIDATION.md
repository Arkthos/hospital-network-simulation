# Validación de preparación y cierre CP3

Fecha: 2026-11-05. Python 3.12 local; sin dependencias externas.

- Inventario: 57 fuentes originales; 42 TXT, 11 DOCX, 2 PKT, README y LICENSE. SHA-256 verificados contra baseline.
- Parser: 80 reglas ACL explícitas, 10 aplicaciones a interfaces, cero reglas ACL sin reconocer. No se afirma cobertura de IOS completo.
- Plan: 14 IDs únicos, política y objetivo por caso. Categorías primarias: external-connectivity 2, guest-isolation 2, management 3, radius 3, internal-access 1, wlc 2, negative-control 1; segmentation como categoría secundaria.
- C: 9 deny previstos por reglas conocidas, 5 unknown por información incompleta. No se sustituye permiso ACL por conectividad end-to-end.
- Pruebas del software: 6 pruebas unittest con aserciones sobre corpus real, primera coincidencia/puertos CAPWAP-DHCP, restricciones de Management/RADIUS, sintaxis no soportada, clasificación P–C–O, rutas fuera del proyecto, registro/repetición inmutable, rechazo de sobrescritura y alteración posterior de artefactos. Fixtures sintéticos exclusivamente temporales, fuera de evidencia experimental.
- validate_evidence.py y validate_results.py: sin inconsistencias críticas en preparación.
- validate_results.py --require-complete: debe retornar !=0 por 14 casos sin ejecución. No es un fallo de los controles de red.
- observations/results/discrepancies: encabezados sin filas de ejecución. Summary: executed=0, valid=0, conformity_rate=null.
- Git diff de rutas originales contra commit base: sin cambios de contenido. No se modifican PKT, configuración ni main.

No se afirma validación de accesibilidad de todas las ventanas de equipos ni ejecución headless. Sí se inspeccionó la ventana principal y Workspace List de la GUI real. No se redactó Capítulo IV ni recomendaciones finales.

## Cierre CP3

- 14 IDs cubiertos por 16 ejecuciones; 13 casos válidos y T010 indeterminado por prerrequisito no verificado. Se retienen R1/R2 y se usa la primera ejecución por caso para el resumen.
- validate_evidence.py: cero errores, incluyendo hashes del preflight CP3-01, cada artefacto de ejecución, correspondencia observación/manifiesto, controles y hashes de P/C congelados.
- validate_results.py --require-complete: cero errores. Esta cobertura admite una limitación documentada; no afirma que T010 haya ejecutado SSH.
- 7 pruebas unittest pasan; se añadió detección de alteración y escape de directorio del preflight con fixtures temporales.
- Los 57 archivos originales conservan hashes de baseline. La copia de ejecución fue guardada por el usuario sin cambios de configuración según su declaración y tiene otro hash; véase CP3-02. No se afirma equivalencia binaria ni se atribuye una causa técnica específica al cambio.
- Automatización GUI observada: accesibilidad a veces ausente/atrasada; capturas visuales reales conservadas como evidencia. No hubo PDU fiable ni atribución confirmada a una regla específica.

Los bullets de preparación anteriores describen el estado histórico CP2; no sustituyen este cierre. La revisión formal CP4 y el análisis CP5 permanecen pendientes.

## Procedencia de la copia guardada

La revisión final encontró la copia runtime de 254166 bytes con última escritura 2026-11-05 23:38:40 UTC (17:38:40 Costa Rica), antes de las pruebas de la sesión actual. Los dos originales tienen 258544 bytes y conservan sus hashes. Al consultar, el usuario respondió: «Sí, lo guardé sin cambiar configuración».

Se preservó la copia guardada y un registro de hashes, fechas y ejecuciones posteriores en `research/advance2/evidence/preflight/CP3-02/` (ruta desde la raíz del repositorio). Los manifiestos originales de las pruebas no se reescribieron. El commit baseline identifica la fuente original, sin certificar igualdad binaria de la copia guardada. La ausencia de cambios de configuración en ese guardado está sustentada por la declaración del usuario; no se afirma haber comparado todos los estados internos de ambos PKT. Esta limitación debe acompañar el uso académico de los resultados. Para exigir equivalencia binaria estricta, sería necesaria otra campaña desde una copia nueva y verificada; no se sustituye ni borra esta campaña.
