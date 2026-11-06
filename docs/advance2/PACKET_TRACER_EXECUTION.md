# Ejecución reproducible en Packet Tracer

## Capacidades investigadas localmente

Instalación: `C:/Program Files/Cisco Packet Tracer 9.0.1`, ejecutable ProductVersion/FileVersion 9.0.1.0858. La documentación local es fuente primaria de la versión instalada:

| Función | Fuente local relativa a help/default | Alcance comprobado |
|---|---|---|
| CLI IOS/ASA | CLI_routerIOS.htm, CLI_asa.htm | CLI simulada dentro de ventanas de equipos; no equivale a CLI headless del programa |
| IPC/ExApps | ipc.htm, IpcAPI/ | Extensiones externas, archivos .pta, PTMP; puerto de escucha predeterminado documentado 39000; no se sondeó ni habilitó |
| Script Modules | scriptModules.htm, scriptModules_scriptingInterface.htm | módulos PT .pts y módulo embebido en .pkt/.pka; editor integrado y acceso IPC |
| Activity Wizard | activityWizard_scoringModelAndScripting.htm | evaluación/scoring por actividad; no se convierte baseline a actividad |
| Network Controller API | NetconRestAPI/index.html | API northbound del dispositivo Network Controller simulado; no es API general del host Packet Tracer ni garantiza control de esta topología |
| Accesibilidad | AccessibilityBasics.htm | Workspace List Shift+W, tabla de dispositivos/enlaces y apertura con Enter; tabla de eventos PDU accesible |

La existencia de IPC y scripting está documentada; sería incorrecto afirmar que Packet Tracer no tiene API. No se encontró en la revisión local un flujo headless soportado, configurado y validado para abrir este PKT, ejecutar estos casos y exportar evidencia con garantías. La carpeta extensions contiene archivos de la instalación, pero no se identificó un ejecutor listo para esta campaña. No se descargaron SDK ni herramientas de terceros ni se habilitaron puertos.

Decisión conservadora: Python automatiza preparación y procesamiento; GUI accesible para inspección y tráfico. No insertar un File Script Module: modificaría el PKT. Un futuro módulo PT independiente exigiría revisión y validación en copia, fuera del baseline y antes de confiar en sus resultados. No se escribe un protocolo IPC por ingeniería inversa.

## Estado local de acceso GUI

La aplicación inicialmente se inició sin ventana targetable. Después de intervención del usuario, Computer Use obtuvo una ventana y un árbol de accesibilidad con menús, Workspace List y controles. Por tanto, la GUI sí puede inspeccionarse con el mecanismo disponible; el fallo inicial no prueba incompatibilidad. No se ejecutaron casos de conectividad en CP2. No guardar ni cerrar una sesión de trabajo del usuario con cambios pendientes.

El usuario abrió el PKT y su archivo en disco coincidió por SHA-256 con el baseline. Se abrió Workspace List y se conservó su árbol accesible parcial en `research/advance2/baseline/gui-preflight.txt`, con hash separado. Las filas están virtualizadas: solo se leyeron filas expuestas, no los 42 dispositivos completos. Se observaron MLS0, MLS1, int-server, Switch4, reception y el cluster INTERNET; estos nombres no identifican todavía los clientes de las pruebas. No se guardó el PKT, no se editó configuración y no se registró resultado de conectividad.

## Preflight obligatorio — antes de registrar O

1. Ejecutar inventory.py y validate_evidence.py. Confirmar SHA del PKT seleccionado contra BASELINE.md. Trabajar en copia byte a byte en `research/advance2/runtime/`, ignorada por Git; mantener el original intacto.
2. Si el usuario abrió un archivo, leer título/ruta. No asumir que coincide con baseline. Confirmar hash del archivo en disco y posibles cambios sin guardar; si hay duda abrir copia propia en otra sesión sin descartar su trabajo.
3. Registrar versión desde Help/About o VersionInfo; asociar versión y commit al run. Mantener modo Realtime para conectividad, esperar convergencia y registrar condiciones/tiempo. No reiniciar dispositivos ni cambiar enlaces.
4. Abrir Workspace List con Shift+W. Leer nombres de dispositivos y enlaces. Navegar la tabla por teclado/accesibilidad y abrir dispositivo con Enter sobre Name; evitar coordenadas de topología.
5. En endpoints de VLAN40/50 comprobar Desktop/IP Configuration o `ipconfig`, adaptador inalámbrico, SSID, asociación, IP/máscara/gateway. Verificar que sea un cliente WLAN y no AP/gateway. Las IP unknown del plan se resuelven por lectura, nunca por configuración nueva.
6. Registrar `preflight.json` con endpoint, nombre, IP, máscara, gateway, SSID, VLAN, evidencia y fuente. Verificar bastión existente .60.8, servidor interno .10.5 y WLC .70.5. Si no coinciden con las fuentes, conservar discrepancia y versionar enmienda del plan ANTES de ejecutar; no renumerar dispositivos.
7. Identificar IP/servicios del servidor VLAN80. T010 requiere SSH administrativo representado; si no está disponible, registrar evidencia de esa limitación como indeterminate, valid=false. No habilitar SSH ni sustituir la prueba por ping.
8. Identificar host externo real fuera del ASA con servicio ICMP y ruta de retorno. No usar .100.5, .100.8 ni NAT .60.3/.4 como prueba de Internet. Registrar IP real; no ejecutar contra el representante matemático de generate_tests.py.
9. Obtener de ambos MLS únicamente comandos show: `show vlan brief`, `show ip interface brief`, `show ip interface`, `show access-lists`, `show ip route`, `show standby brief`, `show running-config`. Conservar salidas cuando estén soportadas; si un comando no existe, registrar limitación sin cambiar configuración. Leer también ASA routing/ACL/NAT por show soportados.
10. Comparar estado vivo con fragmentos, dirección in/out y recorrido. Los permisos parciales con C unknown no pasan automáticamente a C allow. Si se consigue información adicional, crear enmienda preflight con fuentes y dejar plan congelado antes del primer run.

## Secuencia por caso

Consultar `research/advance2/tests/test-procedures.md` para los 14 casos. Ejecutar primero T001, T006 y T013 como controles de fuentes. T009 verifica administración WLC, pero no sustituye la verificación de servicios RADIUS o Management.

1. Confirmar copia baseline y endpoint origen. Guardar evidencia de IP/SSID y destino activo. No volver a abrir/reiniciar innecesariamente entre cada caso; conservar condiciones y registrar reinicios si ocurren.
2. Para ICMP: abrir Desktop → Command Prompt **simulado dentro de Packet Tracer** y ejecutar `ipconfig`, luego `ping IP_DESTINO_CONFIRMADA`. Nunca ejecutar estos comandos en la consola Windows por Computer Use.
3. Registrar primer intento y cualquier calentamiento ARP. Ejecutar una segunda serie sin cambios y conservar ambas salidas; no eliminar timeouts iniciales. Si se crea una repetición formal, usar nuevo Rn y explicar causa.
4. Para T009/T014 usar Desktop → Web Browser, URL `https://192.168.70.5`; observar establecimiento/respuesta del servicio. Mostrar página no demuestra resistencia TLS. No cambiar credenciales ni opciones. Si requiere autenticación interactiva no autorizada, intervención del usuario o registrar limitación.
5. Para T010 usar `ssh -l USUARIO_EXISTENTE IP_RADIUS_CONFIRMADA` solo si el destino implementa SSH. No usar credenciales ficticias, no habilitar servicios y no publicar contraseñas en capturas.
6. Registrar allow solo ante respuesta/intercambio efectivo del servicio. Registrar deny como observación de ausencia de entrega/respuesta bajo controles verificados; no atribuir causa automáticamente. Si destino/servicio/ruta no están verificables, indeterminate.
7. Ante deny, inspeccionar Simulation Mode: filtrar protocolo/ARP necesario, observar Event List y abrir PDU Information. Documentar si se entregó la solicitud, dónde se descartó, interfaz/regla aplicable y retorno. Restaurar Realtime; no editar ACL para diagnosticar.
8. Capturar ventana pequeña con origen, destino, comando/acción y salida. Asociar ID al nombre de archivo y manifiesto; no crear screenshots sintéticos ni anotar topología original. Copiar texto de salida mediante la función Copy del terminal cuando sea posible.
9. Crear metadatos reales según evidence/README.md y collect_evidence.py. Conservar capturas de error/limitación, incluso para indeterminate. El registrador asigna hashes y crea Txxx-Rn sin sobrescribir.
10. Regenerar comparación/resumen, ejecutar validadores y hacer commit del checkpoint al terminar la fase. Si se alteró accidentalmente configuración, detener, conservar evidencia del incidente, descartar solo la copia de ejecución de forma auditada y reabrir copia limpia; nunca guardar encima del original.

## Reglas de cierre

- Un negativo sin control de fuente positivo y destino activo no es válido. Un timeout no demuestra que una ACL causó el resultado.
- T012 evalúa intercambio ICMP, no autorización de entrada a Management; una respuesta filtrada no prueba que la solicitud no llegó.
- Comparar ambos MLS; HSRP y caminos alternos pueden cambiar qué ACL se atraviesa.
- `--require-complete` exige una ejecución registrada por caso, incluyendo evidencia de casos indeterminados. No exige fabricar servicios inexistentes.
- Cerrar CP3 y CP4 antes de formular solución sustentada o abrir remediation/. No modificar baseline para conseguir P.

## Fuentes de capacidades

Las referencias de arriba son páginas oficiales incluidas con la instalación, consultadas localmente el 2026-11-05. No se presentan como una búsqueda web ni como garantía de funciones no probadas. Las capturas/árboles de la sesión GUI son preflight de accesibilidad, no resultados experimentales de conectividad.
