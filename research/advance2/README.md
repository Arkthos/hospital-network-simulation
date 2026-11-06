# Segundo avance — experimento reproducible P–C–O

Caso hipotético: Centro Médico Horizonte CR. Se comparan riesgos y controles de Wi-Fi público/privado mediante revisión documental y pruebas de segmentación. **Este paquete no es el Capítulo IV ni contiene resultados inventados.**

## Estado y checkpoints

- CP1: inventario, VLAN, redes, reglas/aplicaciones ACL y hashes completados.
- CP2: política propuesta y 14 casos generados; mecanismo de evidencia, comparación y validación preparado.
- CP3: completo. 14 casos representados en 16 ejecuciones, 13 casos válidos; T010 indeterminado por prerrequisito SSH no verificado. Evidencia/manifiestos inmutables. Ver [bitácora](../../docs/advance2/CP3_EXECUTION_LOG.md) y [reporte CP3](../../docs/advance2/CP3_REPORT.md).
- CP4: revisión formal pendiente. Comparación y resumen regenerados; validación de evidencia y cobertura completa pasan sin errores críticos.
- CP5: análisis académico y recomendaciones finales pendientes. Nueve casos P=C=O; cuatro allow válidos conservan C unknown y T010 tiene O indeterminada. No es una evaluación general de seguridad.

La tabla de commits/checkpoints está en `docs/advance2/CHECKPOINTS.md`. Baseline y alcance: `docs/advance2/BASELINE.md`.

## Metodología

P es política propuesta del caso, C es previsión conservadora del comportamiento según fuentes, O es observación nueva. Un permiso ACL no basta para C=allow sin ruta/servicio/retorno verificados. `acl_exchange_expected` muestra la decisión de las ACL conocidas por separado; `config_basis` conserva las reglas y líneas. C=unknown es explícito y evita fingir certeza.

VLAN40 es movilidad corporativa restringida, no una WLAN clínica con acceso implícito. La política se define antes de ejecutar, con justificación separada. OE1 y OE3 requieren revisión/análisis además de las pruebas OE2; el mapeo explica esa limitación.

## Reproducción

Requisito: Python 3.10+ (validado aquí con 3.12), Git y Packet Tracer para CP3. No hay dependencias Python externas. Los `.yaml` usan sintaxis JSON válida en YAML 1.2; editarlos como JSON permite analizarlos con la biblioteca estándar. Ejecutar desde la raíz del repositorio:

```powershell
python research/advance2/scripts/inventory.py
python research/advance2/scripts/generate_tests.py
python research/advance2/scripts/compare_pco.py
python research/advance2/scripts/generate_summary.py
python research/advance2/scripts/validate_evidence.py
python research/advance2/scripts/validate_results.py
python -m unittest discover -s research/advance2/scripts -p "test_*.py"
```

`generate_tests.py` debe ejecutarse solo durante preparación; después de iniciar CP3 los hashes del plan/política en cada manifiesto detectan cambios. Si se cambia P o el plan, abrir otra campaña y conservar todos los artefactos anteriores.

## Ejecución y registro

1. Seguir `docs/advance2/PACKET_TRACER_EXECUTION.md`; resolver endpoints en una ficha de preflight, sin cambiar IP/SSID/ACL ni servicios.
2. Ejecutar controles positivos T001, T006 y T013 antes de negativos dependientes. Verificar también el destino de cada bloqueo desde una fuente permitida o mediante inspección del servicio.
3. Capturar salida real y capturas reales en archivos temporales fuera de `evidence/raw`. Una imagen de documentación histórica no sustituye esta ejecución.
4. Crear un JSON de metadatos con la estructura de `evidence/README.md`; ejecutar:

```powershell
python research/advance2/scripts/collect_evidence.py C:/ruta/real/T001-R1-input.json
python research/advance2/scripts/compare_pco.py
python research/advance2/scripts/generate_summary.py
python research/advance2/scripts/validate_evidence.py
python research/advance2/scripts/validate_results.py
```

Cada ejecución se guarda como T001-R1, T001-R2, etc. El registrador rechaza rutas existentes, valida en copia temporal antes de publicar y agrega observaciones; no sobrescribe evidencia previa. No ejecutar colectores concurrentemente. Una interrupción entre publicar y agregar CSV deja un manifiesto huérfano que el validador detecta: conservarlo y reconciliar con auditoría, nunca borrarlo.

Los `manifest.template.json` son plantillas sin observación y nunca se cuentan como evidencia. El CSV observations empezó solo con encabezado; ahora conserva todas las ejecuciones reales. El resumen usa la primera ejecución registrada por caso; las repeticiones se conservan en results.csv sin elegir el resultado más conveniente.

Para cerrar CP3/CP4:

```powershell
python research/advance2/scripts/validate_results.py --require-complete
```

En el checkpoint CP2 este comando fallaba por falta de ejecuciones; al cerrar CP3 pasa con los 14 casos representados. Un caso puede cerrarse como indeterminate con evidencia real de la limitación; no se convierte en bloqueo de seguridad.

## Métricas y causalidad

`conformity_rate = conforming_valid_tests / valid_tests * 100`, usando CONFORMING=P=C=O. C desconocida impide esa clasificación. También se calcula `policy_agreement_rate` para P=O, evitando atribuir al primer indicador un significado distinto. Sin pruebas válidas ambos son null. Ninguno representa porcentaje de seguridad de la red.

Un deny puede ser falta de respuesta, routing, servicio ausente o ACL. Registrar causalidad `confirmed`, `strongly_supported`, `possible`, `unknown` y su evidencia. No se asigna severidad arbitraria: `not_assessed` hasta disponer de criterios/contexto. Un control positivo no prueba por sí solo que todos los destinos están activos.

## Límites

Packet Tracer representa protocolos y equipos simplificados. No prueba RF, Evil Twin real, WPA3/Dragonblood, OWE, TLS/certificados reales ni clientes modernos. Los servicios ausentes no se habilitan para forzar éxito. La administración SSH de RADIUS puede no estar implementada; T010 será indeterminate si no existe. La red externa debe ser un host fuera del ASA; DMZ/hairpin no prueba Internet.

`analysis/` contiene plantillas y revisión preliminar de configuración; las observaciones CP3 están en results/ y en el reporte CP3. No hay controles finales ni Capítulo IV. No iniciar remediación antes del cierre del baseline. No hacer merge automático.

## Procedencia de la copia guardada

La revisión final encontró la copia runtime de 254166 bytes con última escritura 2026-11-05 23:38:40 UTC (17:38:40 Costa Rica), antes de las pruebas de la sesión actual. Los dos originales tienen 258544 bytes y conservan sus hashes. Al consultar, el usuario respondió: «Sí, lo guardé sin cambiar configuración».

Se preservó la copia guardada y un registro de hashes, fechas y ejecuciones posteriores en `research/advance2/evidence/preflight/CP3-02/` (ruta desde la raíz del repositorio). Los manifiestos originales de las pruebas no se reescribieron. El commit baseline identifica la fuente original, sin certificar igualdad binaria de la copia guardada. La ausencia de cambios de configuración en ese guardado está sustentada por la declaración del usuario; no se afirma haber comparado todos los estados internos de ambos PKT. Esta limitación debe acompañar el uso académico de los resultados. Para exigir equivalencia binaria estricta, sería necesaria otra campaña desde una copia nueva y verificada; no se sustituye ni borra esta campaña.
