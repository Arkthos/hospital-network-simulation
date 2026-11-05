# Baseline del segundo avance

Fecha de captura: 2026-11-05, America/Costa_Rica. Repositorio: https://github.com/Arkthos/hospital-network-simulation

Commit inmutable: `2873d7a0cfb71fd768775c32edc6d7b2f9b3ab46`.
Rama de investigación: `research/advance2-automation`. No se modifica main ni configuración original.

## Artefactos

Los dos archivos tienen 258544 bytes y SHA-256 `1be4c1d7c247c542ceaae24e58f43a782dfe4fcbdd524e7139f6f535b88a50fe`:

- `Hospital network  simulation/hospital netowrk simulation.pkt` — archivo seleccionado.
- `Hospital network  simulation/newtry.pkt` — duplicado byte a byte; no constituye segunda réplica experimental.

57 archivos originales inventariados. `research/advance2/baseline/hashes.json` registra rutas, tamaños y SHA-256. El inventario debe conservar este commit incluso después de agregar commits de investigación. Los scripts abortan ante cambios del baseline.

Packet Tracer instalado: `9.0.1.0858`, obtenido de ProductVersion/FileVersion del ejecutable local. La versión usada para crear el PKT es **unknown**; no se infiere de la instalación.

VLAN declaradas: 10 internal, 20 reception, 30 hospitalstaff, 40 wifi, 50 guestwifi, 60 management, 70 wlc, 80 radius, 90 voip, 99 native, 100 dmz y 999 blackhole. SVI VLAN10–90 con /24, VIP HSRP .1 y MLS .2/.3. Transit /30 y enlaces externos se conservan en networks.csv; no se confunden con VLAN de usuario.

## Procedencia y alcance

`acl_rules.csv`: 80 reglas explícitas; `acl_bindings.csv`: 10 aplicaciones textuales IOS/ASA. No se considera que los fragmentos sean running-config exportadas. El orden entre archivos no está documentado; comandos abreviados y errores tipográficos originales se retienen. No se aplica ningún fragmento a equipos.

Las configuraciones y documentos están inventariados con archivo y línea cuando corresponde. El texto OOXML se extrae con Python estándar. Dos `.docx` originales tienen firma OLE en lugar de ZIP; no se convierten ni se asume su contenido. Las imágenes incrustadas se cuentan, pero no se tratan como observaciones nuevas. No se afirma haber verificado visualmente todas esas imágenes históricas.

## Incidencia del entorno y preservación

La primera clonación dentro de OneDrive mostró cambios automáticos en documentos Word después de ser leídos: Git detectó tamaños mayores y algunos archivos pasaron a firma OLE. [Unverified] La causa no fue determinada; podría intervenir software de protección documental. Esa copia se conserva sin incorporar sus cambios.

Se continuó en `C:/Users/kerodri/hospital-network-simulation-advance2`, fuera de OneDrive. El manifiesto se contrastó con los bytes de objetos del commit original. LICENSE/README se materializaron con los bytes originales de Git para evitar diferencias CRLF de checkout; no se cambió su contenido del commit. Las validaciones incluyen todos los archivos originales. Cualquier nueva alteración se considera bloqueo antes de CP3.

## Desconocidos que deben resolverse

- Correspondencia entre fragmentos y estado guardado del PKT, ambas ACL MLS, rutas y HSRP activo.
- Nombres/IP de clientes WLAN, SSID efectivo, asociación, gateway y servicio externo real.
- IP/servicios activos del servidor RADIUS; existencia de SSH administrativo.
- Disponibilidad de funciones GUI/IPC en la sesión local; no se ha establecido un ejecutor headless confiable.

No hay observaciones experimentales nuevas en CP1/CP2. La evidencia documental histórica permanece separada. Remediación solo se abre después de cerrar baseline experimental, en rama/copia y directorio independientes.
