# Inventario baseline

Commit: `2873d7a0cfb71fd768775c32edc6d7b2f9b3ab46`. 57 archivos originales; 2 PKT idénticos por SHA-256.

VLAN declaradas: 10, 20, 30, 40, 50, 60, 70, 80, 90, 99, 100, 999.

Fuentes: inventory.json (interfaces y comandos con línea), vlans.csv, networks.csv, acl_rules.csv, acl_bindings.csv y document-text.json. Las filas repetidas conservan procedencia por dispositivo; no son nuevas VLAN. OSPF utiliza wildcard IOS y máscara ASA; se conserva el valor original.

## Desconocidos

- Saved .pkt state vs text configurations not yet compared
- Live endpoint names/IPs and external target unknown
- RADIUS IP and enabled services unknown
- SSID/authentication documented, not yet observed
- Embedded historical screenshots not re-executed
- Two misnamed .docx files not readable as OOXML
