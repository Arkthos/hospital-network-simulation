# Cierre de ejecución CP3

Baseline: `2873d7a0cfb71fd768775c32edc6d7b2f9b3ab46`. Packet Tracer 9.0.1.0858. Sin cambios de configuración, servicios, credenciales o archivos originales. P y C conservan los hashes del plan CP2.

14 casos representados, 16 registros incluyendo dos repeticiones formales; 13 casos con observación válida. T010 tiene una limitación real documentada y no constituye un resultado SSH.

| Caso | Origen → destino | P | C | O | Válido | Evidencia primaria |
|---|---|---|---|---|---|---|
| T001 | 192.168.50.25 → 172.16.10.30 | allow | unknown | allow | true | [T001-R1](../../research/advance2/evidence/raw/T001-R1/manifest.json) |
| T002 | 192.168.50.25 → 192.168.10.5 | deny | deny | deny | true | [T002-R1](../../research/advance2/evidence/raw/T002-R1/manifest.json) |
| T003 | 192.168.50.24 → 192.168.60.8 | deny | deny | deny | true | [T003-R1](../../research/advance2/evidence/raw/T003-R1/manifest.json) |
| T004 | 192.168.50.24 → 192.168.80.5 | deny | deny | deny | true | [T004-R1](../../research/advance2/evidence/raw/T004-R1/manifest.json) |
| T005 | 192.168.50.24 → 192.168.40.25 | deny | deny | deny | true | [T005-R1](../../research/advance2/evidence/raw/T005-R1/manifest.json) |
| T006 | 192.168.40.25 → 172.16.10.30 | allow | unknown | allow | true | [T006-R1](../../research/advance2/evidence/raw/T006-R1/manifest.json) |
| T007 | 192.168.40.25 → 192.168.10.5 | deny | deny | deny | true | [T007-R1](../../research/advance2/evidence/raw/T007-R1/manifest.json) |
| T008 | 192.168.40.25 → 192.168.60.8 | deny | deny | deny | true | [T008-R1](../../research/advance2/evidence/raw/T008-R1/manifest.json) |
| T009 | 192.168.60.8 → 192.168.70.5 | allow | unknown | allow | true | [T009-R1](../../research/advance2/evidence/raw/T009-R1/manifest.json) |
| T010 | 192.168.60.8 → 192.168.80.5 | allow | unknown | indeterminate | false | [T010-R1](../../research/advance2/evidence/raw/T010-R1/manifest.json) |
| T011 | 192.168.30.22 → 192.168.80.5 | deny | deny | deny | true | [T011-R1](../../research/advance2/evidence/raw/T011-R1/manifest.json) |
| T012 | 192.168.30.22 → 192.168.60.8 | deny | deny | deny | true | [T012-R1](../../research/advance2/evidence/raw/T012-R1/manifest.json) |
| T013 | 192.168.30.22 → 192.168.10.5 | allow | unknown | allow | true | [T013-R1](../../research/advance2/evidence/raw/T013-R1/manifest.json) |
| T014 | 192.168.50.24 → 192.168.70.5 | deny | deny | deny | true | [T014-R1](../../research/advance2/evidence/raw/T014-R1/manifest.json) |

## Interpretación y límites

- Cuatro casos allow válidos: T001, T006, T009 y T013. Conservan C=unknown porque así se congeló la previsión antes de ejecutar. Su clasificación P–C–O sigue siendo INDETERMINATE.
- Nueve casos deny válidos coinciden con P y C. El resumen obtiene 9/13 = 69,23 % de conformidad estricta y 13/13 = 100 % de coincidencia P=O. Ninguno es un porcentaje de seguridad de la red.
- T010: no se verificó servidor/cuenta SSH en Server4; se inspeccionó el prerrequisito y se conservó evidencia. No hubo intento SSH ni se fabricaron credenciales o bloqueo.
- T012: dos series sin respuesta. [Inference] Una ACL de retorno en VLAN60 puede explicar el resultado. No demuestra que una solicitud de otra VLAN no llegue a Management. Causalidad possible.
- T014: Request Timeout explícito desde Guest, con WLC disponible desde Management y Guest con conectividad externa. Describe ausencia de intercambio HTTPS exitoso; causalidad possible, sin traza PDU/contadores que identifique el punto de descarte.
- En los demás negativos, los mensajes de inaccesibilidad, controles, rutas y ACL respaldan causalidad strongly_supported; no se eleva a confirmed. Para RADIUS se documenta inspección local del destino, no un control ICMP remoto inexistente.
- La página WLC de T009 solo verifica respuesta del servicio simulado. No se inició sesión; no demuestra seguridad de autenticación, certificados ni TLS real.
- Los dos PKT originales conservan SHA-256 `1be4c1d7c247c542ceaae24e58f43a782dfe4fcbdd524e7139f6f535b88a50fe`. La copia guardada por el usuario tiene SHA-256 `990d282545cc37295af7236228a8acf30981dd4ad835ffc71307b740f9db2812`; no es idéntica byte a byte al original.
- Diferencias entre TXT y running-config y limitaciones de GUI/incidentes están en la [bitácora](CP3_EXECUTION_LOG.md). No se alteró C retrospectivamente.

## Validación y continuidad

validate_evidence.py y validate_results.py --require-complete pasan sin errores críticos. Siete pruebas de software pasan. Los datos derivados están en [summary.md](../../research/advance2/results/summary.md); el CSV de discrepancias no contiene filas porque ninguna observación con P/C conocidas contradice esas expectativas en esta matriz. Eso no descarta brechas fuera del alcance o discrepancias documentales.

CP4 requiere revisión formal de la trazabilidad e interpretación; CP5, análisis y paquete académico. No se redactó Capítulo IV ni se inició remediación.

## Procedencia de la copia guardada

La revisión final encontró la copia runtime de 254166 bytes con última escritura 2026-11-05 23:38:40 UTC (17:38:40 Costa Rica), antes de las pruebas de la sesión actual. Los dos originales tienen 258544 bytes y conservan sus hashes. Al consultar, el usuario respondió: «Sí, lo guardé sin cambiar configuración».

Se preservó la copia guardada y un registro de hashes, fechas y ejecuciones posteriores en `research/advance2/evidence/preflight/CP3-02/` (ruta desde la raíz del repositorio). Los manifiestos originales de las pruebas no se reescribieron. El commit baseline identifica la fuente original, sin certificar igualdad binaria de la copia guardada. La ausencia de cambios de configuración en ese guardado está sustentada por la declaración del usuario; no se afirma haber comparado todos los estados internos de ambos PKT. Esta limitación debe acompañar el uso académico de los resultados. Para exigir equivalencia binaria estricta, sería necesaria otra campaña desde una copia nueva y verificada; no se sustituye ni borra esta campaña.
