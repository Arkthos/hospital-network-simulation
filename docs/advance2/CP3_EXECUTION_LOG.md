# Bitácora CP3

Baseline original: 2873d7a0cfb71fd768775c32edc6d7b2f9b3ab46. PKT de ejecución: copia byte a byte en runtime/, no guardada encima del original. Packet Tracer 9.0.1.0858. P y C de CP2 permanecen congeladas; no se ajustan retrospectivamente a O.

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

Cada manifiesto contiene timestamp real de captura, hashes y archivos primarios. No confundir IP del gateway que devuelve unreachable con respuesta del servidor destino. No se guarda la simulación para forzar persistencia de cachés ni se cambia configuración.

## Estado

CP3 en curso; no cerrado. Ningún caso pendiente se rellena con indeterminate ficticio. Las observaciones existentes pasan validación de integridad, pero el cierre --require-complete debe seguir fallando hasta cubrir el plan.
