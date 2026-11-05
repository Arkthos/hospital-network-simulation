# Hallazgos

Sin hallazgos experimentales: CP3 pendiente. Las observaciones documentales siguientes son hipótesis para verificar, no resultados de conectividad:

| ID preliminar | Base documental | Implicación para el diseño | Casos |
|---|---|---|---|
| D01 | Acceslist planning.docx: Corp Wifi solo movilidad, servidor interno denegado | No asumir que VLAN40 sea una WLAN clínica | T006–T008 |
| D02 | WLC/wlc.txt configura switch; wlc setp.docx describe WPA2-PSK/FlexConnect | WLC, SSID y autenticación efectiva deben inspeccionarse en GUI | preflight de todos los casos WLAN |
| D03 | Firewall/SSH testing from inside host.docx dice que AAA RADIUS no se logró | No equiparar presencia de VLAN80 con autenticación WLAN RADIUS | T004, T010, T011; inventario AAA |
| D04 | mgmtacl mls.txt: DHCP, SSH desde .60.8 y HTTPS .60.8→.70.5, luego deny | No usar ping como sustituto de autorización administrativa | T009,T010,T012 |
| D05 | wifiaclmls.txt repite permisos CAPWAP; guestwifi permite CAPWAP por subnet | Excepción textual no está restringida a una IP de AP | T014; revisión estática, no generalizar a clientes autenticados |
| D06 | radiusacl out y wlcacl in bloquean VLAN70→80 | [Inference] AAA WLC→RADIUS sería incompatible con estas reglas si se aplican así | preflight AAA; no se configura AAA |
| D07 | Management ACL aplicada in en VLAN60, no out | Un ping sin respuesta desde otra VLAN puede deberse al retorno; no demuestra bloqueo de solicitud | T012 |
| D08 | firewall.txt usa DMZ 192.168.100.1/30; NAT/OSPF/doc usan /24 y .100.5/.8 | [Inference] inconsistencia de fragmentos, pendiente de running-config | T001,T006; no usar DMZ como Internet |
| D09 | planificación indica 443/587/993; ACL ASA incluyen 25/110 y permit ip any any inside | Diferencia entre intención textual y reglas, sin inferir explotación | revisión documental |

Para promover un hallazgo experimental: registrar finding_id, test_ids válidos, observado, riesgo contextual y evidence_basis con manifiestos hashados. La validación rechaza findings sin test_ids/evidencia. No existe recomendación final todavía.
