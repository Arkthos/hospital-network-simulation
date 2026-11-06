# Correspondencia metodológica

Pregunta: ¿Cómo difieren los riesgos y vulnerabilidades de Wi-Fi público y privado, y qué prácticas reducen exposición?

Diseño: estudio de caso hipotético, revisión documental técnica y experimento de conectividad reproducible; unidad de análisis: flujo origen–destino–servicio bajo baseline versionado. No es una muestra estadística de hospitales reales. Instrumentos: ficha documental, parser determinista, matriz de política, plan de pruebas, manifiestos y matriz P–C–O. Selección intencional de 14 casos de alto valor; sin inferencia estadística poblacional.

| Objetivo | Variable/indicador | Instrumento | Casos | Evidencia | Resultado CP5 |
|---|---|---|---|---|---|
| OE1 identificar y clasificar riesgos | autenticación representada, segmentación, configuración, usuario/endpoint y protección de comunicaciones | corpus del primer avance, inventory/document-text.json, running-config observado | caracterización + contexto T001–T014 | literatura IEEE + inventario/configuración hashada | riesgos organizados por capas; Packet Tracer solo valida arquitectura lógica, no RF/TLS/endpoint |
| OE2 comprobar efecto VLAN/ACL | entrega/respuesta por ICMP/TCP, P/C/O, control positivo y causalidad | test-plan, Packet Tracer, manifests, observations/results | T001–T014 | screenshots/salidas, IP/SSID, rutas, ACL, controles | 14 ejecutados, 13 válidos; 9 P=C=O; 13/13 válidos P=O; T010 indeterminado |
| OE3 relacionar riesgos y controles | hallazgo sustentado, brecha, control propuesto y prueba de verificación | findings.md, control-gaps.md, proposed-controls.md, traceability.json | F01–F06 / C01–C07 | finding→test→manifest→SHA + literatura cuando aplica | propuesta separa controles preservados, mejoras operativas y controles fuera del simulador |

## Operacionalización y reglas

- Independiente: zona/VLAN de origen y servicio/destino seleccionados. Configuración baseline constante; ninguna remediación durante CP3.
- Dependiente: allow/deny/indeterminate/error observado. No reducir observaciones a pass/fail.
- Control: endpoint asociado a WLAN correcta, IP/gateway vigentes, destino activo, ruta esperada, tiempo de convergencia y versión del simulador.
- Repetición: T001 y T013 conservan R1/R2; el resumen principal usa primera ejecución y no selecciona el mejor resultado.
- Denominador: 13 pruebas válidas; T010 se reporta aparte y no como deny.
- C requiere toda la cadena conocida. Un allow observado con C=unknown no se convierte retroactivamente en C=allow.
- Causalidad: observed describe comportamiento; strongly_supported/possible/unknown describe fuerza de atribución. Ningún caso se clasifica confirmed.

## Trazabilidad

Pregunta → OE → variable → test_id → evidencia cruda/hash → observación → clasificación P–C–O → finding_id → control → prueba de verificación.

CP5 materializa esta cadena en 'research/advance2/analysis/traceability.json'. La evidencia primaria permanece en 'research/advance2/evidence/raw/' y no se sustituye por las figuras derivadas.

## Formato académico

El cuerpo IEEE debe sintetizar y contrastar resultados, no reproducir el repositorio. La matriz completa, hashes, running-config y screenshots secundarios se remiten a anexos mediante 'docs/advance2/ANNEX_INDEX.md'. El plan visual se encuentra en 'docs/advance2/VISUAL_PLAN.md'.
