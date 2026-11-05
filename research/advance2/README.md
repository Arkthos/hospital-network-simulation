# Segundo avance — experimento reproducible P–C–O

Caso hipotético: Centro Médico Horizonte CR. Se comparan riesgos y controles de Wi-Fi público/privado mediante revisión documental y pruebas de segmentación. **Este paquete no es el Capítulo IV ni contiene resultados inventados.**

## Estado y checkpoints

- CP1: inventario, VLAN, redes, reglas/aplicaciones ACL y hashes completados.
- CP2: política propuesta y 14 casos generados; mecanismo de evidencia, comparación y validación preparado.
- CP3: en curso. T001-R1, T002-R1 y T013-R1 registrados con evidencia real; 11 casos pendientes. Ver docs/advance2/CP3_EXECUTION_LOG.md.
- CP4: herramientas verificadas; cierre experimental pendiente de CP3. CSV vacíos y métricas null no significan controles conformes.
- CP5: esquemas de análisis y trazabilidad; sin hallazgos experimentales ni recomendaciones finales.

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

Los `manifest.template.json` son plantillas sin observación y nunca se cuentan como evidencia. El CSV observations empieza solo con encabezado. El resumen usa la primera ejecución registrada por caso; las repeticiones se conservan en results.csv sin elegir el resultado más conveniente.

Para cerrar CP3/CP4:

```powershell
python research/advance2/scripts/validate_results.py --require-complete
```

En CP2 este comando debe fallar porque aún faltan ejecuciones. Un caso puede cerrarse como indeterminate con evidencia real de la limitación; no se convierte en bloqueo de seguridad.

## Métricas y causalidad

`conformity_rate = conforming_valid_tests / valid_tests * 100`, usando CONFORMING=P=C=O. C desconocida impide esa clasificación. También se calcula `policy_agreement_rate` para P=O, evitando atribuir al primer indicador un significado distinto. Sin pruebas válidas ambos son null. Ninguno representa porcentaje de seguridad de la red.

Un deny puede ser falta de respuesta, routing, servicio ausente o ACL. Registrar causalidad `confirmed`, `strongly_supported`, `possible`, `unknown` y su evidencia. No se asigna severidad arbitraria: `not_assessed` hasta disponer de criterios/contexto. Un control positivo no prueba por sí solo que todos los destinos están activos.

## Límites

Packet Tracer representa protocolos y equipos simplificados. No prueba RF, Evil Twin real, WPA3/Dragonblood, OWE, TLS/certificados reales ni clientes modernos. Los servicios ausentes no se habilitan para forzar éxito. La administración SSH de RADIUS puede no estar implementada; T010 será indeterminate si no existe. La red externa debe ser un host fuera del ASA; DMZ/hairpin no prueba Internet.

`analysis/` contiene plantillas y revisión preliminar de configuración; no conclusiones experimentales ni controles finales. No iniciar remediación antes del cierre del baseline. No hacer merge automático.
