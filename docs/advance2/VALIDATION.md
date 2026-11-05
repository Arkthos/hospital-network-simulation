# Validación de preparación

Fecha: 2026-11-05. Python 3.12 local; sin dependencias externas.

- Inventario: 57 fuentes originales; 42 TXT, 11 DOCX, 2 PKT, README y LICENSE. SHA-256 verificados contra baseline.
- Parser: 80 reglas ACL explícitas, 10 aplicaciones a interfaces, cero reglas ACL sin reconocer. No se afirma cobertura de IOS completo.
- Plan: 14 IDs únicos, política y objetivo por caso. Categorías primarias: external-connectivity 2, guest-isolation 2, management 3, radius 3, internal-access 1, wlc 2, negative-control 1; segmentation como categoría secundaria.
- C: 9 deny previstos por reglas conocidas, 5 unknown por información incompleta. No se sustituye permiso ACL por conectividad end-to-end.
- Pruebas del software: 6 pruebas unittest con aserciones sobre corpus real, primera coincidencia/puertos CAPWAP-DHCP, restricciones de Management/RADIUS, sintaxis no soportada, clasificación P–C–O, rutas fuera del proyecto, registro/repetición inmutable, rechazo de sobrescritura y alteración posterior de artefactos. Fixtures sintéticos exclusivamente temporales, fuera de evidencia experimental.
- validate_evidence.py y validate_results.py: sin inconsistencias críticas en preparación.
- validate_results.py --require-complete: debe retornar !=0 por 14 casos sin ejecución. No es un fallo de los controles de red.
- observations/results/discrepancies: encabezados sin filas de ejecución. Summary: executed=0, valid=0, conformity_rate=null.
- Git diff de rutas originales contra commit base: sin cambios de contenido. No se modifican PKT, configuración ni main.

No se afirma validación de accesibilidad de todas las ventanas de equipos ni ejecución headless. Sí se inspeccionó la ventana principal y Workspace List de la GUI real. No se redactó Capítulo IV ni recomendaciones finales.
