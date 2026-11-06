# Procedimientos por caso

Aplicar primero docs/advance2/PACKET_TRACER_EXECUTION.md; IP unknown se resuelve mediante inspección, nunca por asignación de nuevas IP. Controles T001/T006/T013 se ejecutan primero.

## T001 — Guest Wi-Fi → External fuera del ASA

P=allow; C=unknown; decisión del intercambio en ACL conocidas=allow.

Origen: VLAN 50, IP unknown. Destino: VLAN external, IP unknown.

Acción: `Packet Tracer GUI: Desktop Command Prompt: ping <confirmed_destination_ip>`.

Controles: T001. Registrar entrega/respuesta real por servicio; timeout solo no demuestra ACL. Para deny válido verificar control positivo y destino activo; indeterminate ante prerrequisito ausente.

C derivada exclusivamente de fragmentos textuales; validar su aplicación en ambos MLS y su correspondencia con PKT. Las ACL MLS conocidas no bloquean este intercambio; routing/ASA/NAT o servicio del destino no verificados impiden predecir conectividad completa. Seleccionar host externo real de la topología; no usar DMZ ni IP pública hairpin como sustituto de Internet. 203.0.113.254 solo se usa internamente como representante matemático; no es un objetivo a ejecutar.

Evidencia: `evidence/raw/T001/` (plantilla únicamente); crear ejecución inmutable `T001-R1` con collect_evidence.py. Registrar IP, comando, salida, hora, controles y causa.

## T002 — Guest Wi-Fi → Internal Server

P=deny; C=deny; decisión del intercambio en ACL conocidas=deny.

Origen: VLAN 50, IP unknown. Destino: VLAN 10, IP 192.168.10.5.

Acción: `Packet Tracer GUI: Desktop Command Prompt: ping <confirmed_destination_ip>`.

Controles: T001, T013. Registrar entrega/respuesta real por servicio; timeout solo no demuestra ACL. Para deny válido verificar control positivo y destino activo; indeterminate ante prerrequisito ausente.

C derivada exclusivamente de fragmentos textuales; validar su aplicación en ambos MLS y su correspondencia con PKT.

Evidencia: `evidence/raw/T002/` (plantilla únicamente); crear ejecución inmutable `T002-R1` con collect_evidence.py. Registrar IP, comando, salida, hora, controles y causa.

## T003 — Guest Wi-Fi → Management autorizado

P=deny; C=deny; decisión del intercambio en ACL conocidas=deny.

Origen: VLAN 50, IP unknown. Destino: VLAN 60, IP unknown.

Acción: `Packet Tracer GUI: Desktop Command Prompt: ping <confirmed_destination_ip>`.

Controles: T001. Registrar entrega/respuesta real por servicio; timeout solo no demuestra ACL. Para deny válido verificar control positivo y destino activo; indeterminate ante prerrequisito ausente.

C derivada exclusivamente de fragmentos textuales; validar su aplicación en ambos MLS y su correspondencia con PKT.

Evidencia: `evidence/raw/T003/` (plantilla únicamente); crear ejecución inmutable `T003-R1` con collect_evidence.py. Registrar IP, comando, salida, hora, controles y causa.

## T004 — Guest Wi-Fi → RADIUS

P=deny; C=deny; decisión del intercambio en ACL conocidas=deny.

Origen: VLAN 50, IP unknown. Destino: VLAN 80, IP unknown.

Acción: `Packet Tracer GUI: Desktop Command Prompt: ping <confirmed_destination_ip>`.

Controles: T001. Registrar entrega/respuesta real por servicio; timeout solo no demuestra ACL. Para deny válido verificar control positivo y destino activo; indeterminate ante prerrequisito ausente.

C derivada exclusivamente de fragmentos textuales; validar su aplicación en ambos MLS y su correspondencia con PKT.

Evidencia: `evidence/raw/T004/` (plantilla únicamente); crear ejecución inmutable `T004-R1` con collect_evidence.py. Registrar IP, comando, salida, hora, controles y causa.

## T005 — Guest Wi-Fi → Corp Wi-Fi movilidad

P=deny; C=deny; decisión del intercambio en ACL conocidas=deny.

Origen: VLAN 50, IP unknown. Destino: VLAN 40, IP unknown.

Acción: `Packet Tracer GUI: Desktop Command Prompt: ping <confirmed_destination_ip>`.

Controles: T001, T006. Registrar entrega/respuesta real por servicio; timeout solo no demuestra ACL. Para deny válido verificar control positivo y destino activo; indeterminate ante prerrequisito ausente.

C derivada exclusivamente de fragmentos textuales; validar su aplicación en ambos MLS y su correspondencia con PKT.

Evidencia: `evidence/raw/T005/` (plantilla únicamente); crear ejecución inmutable `T005-R1` con collect_evidence.py. Registrar IP, comando, salida, hora, controles y causa.

## T006 — Corp Wi-Fi movilidad → External fuera del ASA

P=allow; C=unknown; decisión del intercambio en ACL conocidas=allow.

Origen: VLAN 40, IP unknown. Destino: VLAN external, IP unknown.

Acción: `Packet Tracer GUI: Desktop Command Prompt: ping <confirmed_destination_ip>`.

Controles: T006. Registrar entrega/respuesta real por servicio; timeout solo no demuestra ACL. Para deny válido verificar control positivo y destino activo; indeterminate ante prerrequisito ausente.

C derivada exclusivamente de fragmentos textuales; validar su aplicación en ambos MLS y su correspondencia con PKT. Las ACL MLS conocidas no bloquean este intercambio; routing/ASA/NAT o servicio del destino no verificados impiden predecir conectividad completa. Seleccionar host externo real de la topología; no usar DMZ ni IP pública hairpin como sustituto de Internet. 203.0.113.254 solo se usa internamente como representante matemático; no es un objetivo a ejecutar.

Evidencia: `evidence/raw/T006/` (plantilla únicamente); crear ejecución inmutable `T006-R1` con collect_evidence.py. Registrar IP, comando, salida, hora, controles y causa.

## T007 — Corp Wi-Fi movilidad → Internal Server

P=deny; C=deny; decisión del intercambio en ACL conocidas=deny.

Origen: VLAN 40, IP unknown. Destino: VLAN 10, IP 192.168.10.5.

Acción: `Packet Tracer GUI: Desktop Command Prompt: ping <confirmed_destination_ip>`.

Controles: T006, T013. Registrar entrega/respuesta real por servicio; timeout solo no demuestra ACL. Para deny válido verificar control positivo y destino activo; indeterminate ante prerrequisito ausente.

C derivada exclusivamente de fragmentos textuales; validar su aplicación en ambos MLS y su correspondencia con PKT.

Evidencia: `evidence/raw/T007/` (plantilla únicamente); crear ejecución inmutable `T007-R1` con collect_evidence.py. Registrar IP, comando, salida, hora, controles y causa.

## T008 — Corp Wi-Fi movilidad → Management autorizado

P=deny; C=deny; decisión del intercambio en ACL conocidas=deny.

Origen: VLAN 40, IP unknown. Destino: VLAN 60, IP unknown.

Acción: `Packet Tracer GUI: Desktop Command Prompt: ping <confirmed_destination_ip>`.

Controles: T006. Registrar entrega/respuesta real por servicio; timeout solo no demuestra ACL. Para deny válido verificar control positivo y destino activo; indeterminate ante prerrequisito ausente.

C derivada exclusivamente de fragmentos textuales; validar su aplicación en ambos MLS y su correspondencia con PKT.

Evidencia: `evidence/raw/T008/` (plantilla únicamente); crear ejecución inmutable `T008-R1` con collect_evidence.py. Registrar IP, comando, salida, hora, controles y causa.

## T009 — Management autorizado → WLC

P=allow; C=unknown; decisión del intercambio en ACL conocidas=allow.

Origen: VLAN 60, IP 192.168.60.8. Destino: VLAN 70, IP 192.168.70.5.

Acción: `Packet Tracer GUI: Desktop Web Browser: https://192.168.70.5`.

Controles: T009. Registrar entrega/respuesta real por servicio; timeout solo no demuestra ACL. Para deny válido verificar control positivo y destino activo; indeterminate ante prerrequisito ausente.

C derivada exclusivamente de fragmentos textuales; validar su aplicación en ambos MLS y su correspondencia con PKT. Las ACL MLS conocidas no bloquean este intercambio; routing/ASA/NAT o servicio del destino no verificados impiden predecir conectividad completa.

Evidencia: `evidence/raw/T009/` (plantilla únicamente); crear ejecución inmutable `T009-R1` con collect_evidence.py. Registrar IP, comando, salida, hora, controles y causa.

## T010 — Management autorizado → RADIUS

P=allow; C=unknown; decisión del intercambio en ACL conocidas=allow.

Origen: VLAN 60, IP 192.168.60.8. Destino: VLAN 80, IP unknown.

Acción: `Packet Tracer GUI: Desktop Command Prompt: ssh -l <existing_user> <confirmed_radius_ip>`.

Controles: T009. Registrar entrega/respuesta real por servicio; timeout solo no demuestra ACL. Para deny válido verificar control positivo y destino activo; indeterminate ante prerrequisito ausente.

C derivada exclusivamente de fragmentos textuales; validar su aplicación en ambos MLS y su correspondencia con PKT. Las ACL MLS conocidas no bloquean este intercambio; routing/ASA/NAT o servicio del destino no verificados impiden predecir conectividad completa. No consta que el servidor RADIUS simule SSH; no habilitarlo para que la prueba funcione. Si no existe, resultado indeterminate.

Evidencia: `evidence/raw/T010/` (plantilla únicamente); crear ejecución inmutable `T010-R1` con collect_evidence.py. Registrar IP, comando, salida, hora, controles y causa.

## T011 — Hospitalstaff cableado → RADIUS

P=deny; C=deny; decisión del intercambio en ACL conocidas=deny.

Origen: VLAN 30, IP unknown. Destino: VLAN 80, IP unknown.

Acción: `Packet Tracer GUI: Desktop Command Prompt: ping <confirmed_destination_ip>`.

Controles: T013. Registrar entrega/respuesta real por servicio; timeout solo no demuestra ACL. Para deny válido verificar control positivo y destino activo; indeterminate ante prerrequisito ausente.

C derivada exclusivamente de fragmentos textuales; validar su aplicación en ambos MLS y su correspondencia con PKT.

Evidencia: `evidence/raw/T011/` (plantilla únicamente); crear ejecución inmutable `T011-R1` con collect_evidence.py. Registrar IP, comando, salida, hora, controles y causa.

## T012 — Hospitalstaff cableado → Management autorizado

P=deny; C=deny; decisión del intercambio en ACL conocidas=deny.

Origen: VLAN 30, IP unknown. Destino: VLAN 60, IP unknown.

Acción: `Packet Tracer GUI: Desktop Command Prompt: ping <confirmed_destination_ip>`.

Controles: T013. Registrar entrega/respuesta real por servicio; timeout solo no demuestra ACL. Para deny válido verificar control positivo y destino activo; indeterminate ante prerrequisito ausente.

C derivada exclusivamente de fragmentos textuales; validar su aplicación en ambos MLS y su correspondencia con PKT. La solicitud ICMP no tiene deny de entrada a Management identificado; la respuesta sería bloqueada por management in. No equivale a demostrar aislamiento de solicitudes.

Evidencia: `evidence/raw/T012/` (plantilla únicamente); crear ejecución inmutable `T012-R1` con collect_evidence.py. Registrar IP, comando, salida, hora, controles y causa.

## T013 — Hospitalstaff cableado → Internal Server

P=allow; C=unknown; decisión del intercambio en ACL conocidas=allow.

Origen: VLAN 30, IP unknown. Destino: VLAN 10, IP 192.168.10.5.

Acción: `Packet Tracer GUI: Desktop Command Prompt: ping <confirmed_destination_ip>`.

Controles: T013. Registrar entrega/respuesta real por servicio; timeout solo no demuestra ACL. Para deny válido verificar control positivo y destino activo; indeterminate ante prerrequisito ausente.

C derivada exclusivamente de fragmentos textuales; validar su aplicación en ambos MLS y su correspondencia con PKT. Las ACL MLS conocidas no bloquean este intercambio; routing/ASA/NAT o servicio del destino no verificados impiden predecir conectividad completa.

Evidencia: `evidence/raw/T013/` (plantilla únicamente); crear ejecución inmutable `T013-R1` con collect_evidence.py. Registrar IP, comando, salida, hora, controles y causa.

## T014 — Guest Wi-Fi → WLC

P=deny; C=deny; decisión del intercambio en ACL conocidas=deny.

Origen: VLAN 50, IP unknown. Destino: VLAN 70, IP 192.168.70.5.

Acción: `Packet Tracer GUI: Desktop Web Browser: https://192.168.70.5`.

Controles: T001, T009. Registrar entrega/respuesta real por servicio; timeout solo no demuestra ACL. Para deny válido verificar control positivo y destino activo; indeterminate ante prerrequisito ausente.

C derivada exclusivamente de fragmentos textuales; validar su aplicación en ambos MLS y su correspondencia con PKT.

Evidencia: `evidence/raw/T014/` (plantilla únicamente); crear ejecución inmutable `T014-R1` con collect_evidence.py. Registrar IP, comando, salida, hora, controles y causa.
