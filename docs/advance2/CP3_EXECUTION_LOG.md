# Bitácora CP3

Baseline original: 2873d7a0cfb71fd768775c32edc6d7b2f9b3ab46. PKT de ejecución: copia inicial del original en runtime/, posteriormente guardada por el usuario sin cambios de configuración según su declaración; ver revisión de procedencia al final. Los originales no se sobrescribieron. Packet Tracer 9.0.1.0858. P y C de CP2 permanecen congeladas; no se ajustan retrospectivamente a O.

## Preflight y sesiones

- Primera copia de ejecución: consultas show run/show ip route en MLS0. Fallo inesperado del simulador al cerrar la ventana de equipo. Se conserva el aviso real en evidence/preflight/CP3-01; no se ejecutaron casos de tráfico en esa sesión fallida.
- Sesión recuperada: show run de MLS1; verificación de Smartphone0 en guestwifi, WPA2-PSK/AES, IP 192.168.50.25/24, gateway .50.1. PC2 externo 172.16.10.30/24, gateway 172.16.10.1. PC1(1) cableado VLAN30: 192.168.30.22/24, gateway .30.1. Los respectivos artefactos se conservan en los manifiestos de ejecución.
- Diferencias reales respecto a TXT: ambos MLS incluyen en radius permisos UDP1812/1813 y permiso IP del bastión .60.8; wifi/guestwifi incluyen respuesta DHCP. MLS1 termina wifi con permit del subnet40 hacia any, mientras MLS0 usa any any. Estas son observaciones de configuración, no resultados de tráfico ni remediación.
- Al retomar la tarea, el inventario de ventanas/procesos no encontró Packet Tracer. Se conserva lo ejecutado, se inicia una copia limpia y se requieren controles positivos renovados para nuevos casos. No se atribuye la causa del cierre ni se declara completada la repetición incompleta.

## Casos registrados

| Ejecución | O | Evidencia y límites |
|---|---|---|
| T001-R1 | allow, válido | Smartphone0→PC2 externo. Serie1 2/4 respuestas; serie2 4/4. Pérdidas iniciales conservadas, causa desconocida. C unknown heredada; clasificación PCO INDETERMINATE no invalida la conectividad observada. |
| T013-R1 | allow, válido | PC1(1) VLAN30→192.168.10.5. Dos series 4/4 respuestas. Control de origen y destino interno. C unknown heredada. |
| T002-R1 | deny, válido | Smartphone0→192.168.10.5. Serie completa: cuatro Destination host unreachable desde 192.168.50.2. T001/T013 verifican origen y destino. ACL aplicadas y ruta sustentan causa strongly_supported, sin confirmación por PDU o delta de contadores. Segunda serie solo capturada parcialmente: no se afirma conteo completo. |

Cada manifiesto contiene timestamp real de captura, hashes y archivos primarios. No confundir IP del gateway que devuelve unreachable con respuesta del servidor destino. El agente no guardó la simulación para forzar persistencia de cachés ni cambió configuración. El usuario confirmó un guardado de la copia sin cambios de configuración; véase revisión de procedencia.

## Continuación de la campaña

- En la sesión actual, Laptop0 está asociado a wifi con 192.168.40.25/24; Management PC3(1)(1) conserva 192.168.60.8/24; Server4 conserva 192.168.80.5/24. Smartphone0 recibió 192.168.50.24/24, diferente del lease .25 de la sesión previa. T001-R2 renueva su control positivo antes de T003–T005/T014.
- T006-R1: Wifi→172.16.10.30, primera serie 3/4 y segunda 4/4 respuestas. T013-R2: VLAN30→192.168.10.5, ambas series 4/4. Se conservan los controles originales y las repeticiones.
- T009-R1: Management .60.8→WLC .70.5 por HTTPS devuelve la página de bienvenida/login de Cisco WLC. No se inició sesión. Esto comprueba respuesta del servicio simulado, no autenticación ni seguridad TLS real.
- T010-R1: inspección real de Server4 sin servicio SSH expuesto/verificado ni cuenta SSH verificada. O=indeterminate, valid=false; no hubo transacción SSH y no se inventaron credenciales ni un bloqueo.
- T007-R1 y T008-R1: Wifi→Internal y Wifi→Management; dos series por caso, cuatro mensajes Destination host unreachable desde .40.3 en cada serie. Controles y destinos verificados según sus manifiestos.
- T011-R1: VLAN30→RADIUS; dos series con cuatro Destination host unreachable desde .30.2 cada una. Destino inspeccionado, sin afirmar control ICMP remoto positivo a RADIUS.
- T012-R1: VLAN30→Management; dos series de cuatro Request timed out. Causalidad possible. [Inference] La ACL in de VLAN60 puede filtrar la respuesta; el resultado no demuestra que la solicitud no llegara al destino. No se obtuvo traza PDU fiable.
- El intento de inspeccionar filtros de Simulation produjo una falta temporal de respuesta, documentada en incident-02 dentro de T012-R1. El proceso se recuperó antes de cumplir la condición de la guarda de terminación; no se terminó ni reinició. Se cerró el diálogo y se verificó Realtime antes de los siguientes casos.
- T003-R1, T004-R1 y T005-R1: Guest→Management, RADIUS y Wifi, respectivamente. Dos series completas por caso, cuatro Destination host unreachable desde .50.2 por serie. T001-R2 verifica el origen; los destinos tienen inspección/controles descritos en cada manifiesto. Atribución ACL strongly_supported, sin PDU o delta de contadores que confirme una regla exacta.
- La accesibilidad de la GUI puede faltar o quedar atrasada al cambiar de applet. Las capturas de pantalla son la referencia visual; no se interpreta texto de accesibilidad antiguo como una nueva respuesta de servicio. Se preservan también capturas parciales, sin presentarlas como series completas.

- T014-R1: Guest→WLC .70.5 HTTPS. Se envió la URL con Return y luego Go mientras la página seguía en blanco; la captura final muestra Request Timeout. T001-R2 y T009-R1 son controles positivos. O=deny describe ausencia de intercambio exitoso; causalidad possible, sin identificar una regla de descarte mediante PDU/contadores.

## Estado

CP3 cerrado: 14/14 casos representados, 16 ejecuciones registradas, 13 casos con O válida y T010 indeterminado por prerrequisito SSH no verificado. Los 5 INDETERMINATE de P–C–O incluyen T010 y cuatro observaciones allow válidas con C=unknown congelada: T001, T006, T009 y T013. No confundir clasificación indeterminada con una ejecución inválida en esos cuatro casos.

Las validaciones de evidencia y cobertura completa pasan sin errores críticos; 7 pruebas de software pasan. Nueve casos tienen P=C=O; ningún caso válido discrepa de P en esta matriz limitada. No se infiere seguridad general, resistencia criptográfica ni aislamiento unidireccional a partir de estas cifras. CP4 mantiene pendiente la revisión formal de discrepancias documentales/configuración y CP5 el análisis académico; no se realizó remediación ni Capítulo IV.

## Procedencia de la copia guardada

La revisión final encontró la copia runtime de 254166 bytes con última escritura 2026-11-05 23:38:40 UTC (17:38:40 Costa Rica), antes de las pruebas de la sesión actual. Los dos originales tienen 258544 bytes y conservan sus hashes. Al consultar, el usuario respondió: «Sí, lo guardé sin cambiar configuración».

Se preservó la copia guardada y un registro de hashes, fechas y ejecuciones posteriores en `research/advance2/evidence/preflight/CP3-02/` (ruta desde la raíz del repositorio). Los manifiestos originales de las pruebas no se reescribieron. El commit baseline identifica la fuente original, sin certificar igualdad binaria de la copia guardada. La ausencia de cambios de configuración en ese guardado está sustentada por la declaración del usuario; no se afirma haber comparado todos los estados internos de ambos PKT. Esta limitación debe acompañar el uso académico de los resultados. Para exigir equivalencia binaria estricta, sería necesaria otra campaña desde una copia nueva y verificada; no se sustituye ni borra esta campaña.
