# Propuesta de solución basada en CP5

La propuesta separa controles preservados, mejoras sustentadas por la campaña y controles recomendados por literatura pero no demostrados en Packet Tracer.

| ID | Base | Hallazgo/brecha | Control propuesto | Razón | Verificación |
|---|---|---|---|---|---|
| C01 | Experimental | F01 | Mantener Guest Wi-Fi como zona dedicada con salida externa y denegación explícita hacia redes internas y de administración. | El baseline ya demuestra servicio útil sin acceso a los destinos internos seleccionados. | Repetir T001–T005 y T014 tras cambios de red. |
| C02 | Experimental | F02 | Formalizar VLAN40/SSID wifi como **movilidad corporativa restringida**. Si se requiere WLAN clínica, crear un SSID/VLAN separado con privilegios mínimos en vez de relajar ampliamente VLAN40. | El baseline muestra Internet funcional pero no acceso a Internal Server/Management. Separar roles evita que privada se convierta en sinónimo de confianza total. | T006–T008 como regresión; nuevos tests específicos para una futura WLAN clínica. |
| C03 | Experimental + literatura | F02 | Evaluar migración de la WLAN corporativa desde WPA2-PSK compartido hacia autenticación individual 802.1X/EAP con RADIUS y validación correcta del servidor; usar WPA3 donde el entorno real lo soporte. | El preflight observa WPA2-PSK/AES. Credenciales individualizadas reducen dependencia de secretos compartidos y permiten revocación por usuario. NIST recomienda configuraciones WLAN estandarizadas y administradas [3]; la validación de infraestructura sigue siendo necesaria [7]. | No considerarlo verificado por Packet Tracer. Validar en entorno real o laboratorio específico de autenticación. |
| C04 | Experimental | F03, G02 | Definir una matriz explícita de servicios de administración: origen autorizado, destino, protocolo y puerto. Mantener WLC restringido a Management y documentar cuál es el protocolo administrativo real de RADIUS antes de probarlo. | T009/T014 muestran selectividad para WLC; T010 demuestra que probar un servicio inexistente produce falsa ambigüedad. | Repetir T009/T014 y crear un reemplazo versionado de T010 solo cuando exista servicio real. |
| C05 | Experimental + gobernanza | F06, G01 | Capturar running-config como fuente de verdad operativa, versionarlo y ejecutar diff automático contra la documentación del repositorio antes de cada campaña. | Se observaron diferencias reales entre TXT y estado vivo. NIST recomienda estandarizar, automatizar y centralizar la gestión de configuración WLAN [3]. | Pipeline debe fallar ante drift no explicado; conservar diff como evidencia. |
| C06 | Experimental | F05 | Mantener la matriz P–C–O y los 14 casos como suite de regresión después de cambios de ACL, routing, WLC o servicios. | Cuatro allows válidos no podían predecirse legítimamente solo con configuración estática. | Ejecutar suite baseline/post-change y comparar before/after sin sobrescribir evidencia anterior. |
| C07 | Literatura / fuera del simulador | G06 | Complementar segmentación con controles de endpoint y capa de aplicación: validación de certificados, evitar auto-asociación innecesaria, actualización de clientes, TLS/HTTPS y monitoreo de WLAN/rogue AP. | Packet Tracer no cubre estas amenazas. La literatura muestra que asociación, comportamiento del usuario y aplicación siguen siendo capas independientes [1], [7], [9], [12]. | Auditoría/laboratorio separado; no usar CP3 como prueba de efectividad. |

## Orden de implementación recomendado

1. **Preservar controles efectivos**: C01 y C02.
2. **Corregir gobernanza y trazabilidad**: C05 y C06.
3. **Cerrar el plano administrativo**: C04.
4. **Fortalecer autenticación corporativa**: C03.
5. **Completar capas fuera del alcance del simulador**: C07.

Este orden no es una severidad CVSS. Prioriza primero no romper controles ya observados, luego asegurar que el estado real sea trazable y finalmente ampliar la postura de seguridad.
