# Correspondencia metodológica

Pregunta: ¿Cómo difieren los riesgos y vulnerabilidades de Wi-Fi público y privado, y qué prácticas reducen exposición?

Diseño: estudio de caso hipotético, revisión documental técnica y experimento de conectividad reproducible; unidad de análisis: flujo origen–destino–servicio bajo baseline versionado. No es una muestra estadística de hospitales reales. Instrumentos: ficha documental, parser determinista, matriz de política, plan de pruebas, manifiestos y matriz P–C–O. Selección intencional de 14 casos de alto valor; sin inferencia estadística poblacional.

| Objetivo | Variable/indicador | Instrumento | Casos | Evidencia | Resultado actual |
|---|---|---|---|---|---|
| OE1 identificar y clasificar riesgos | autenticación representada, exposición documental, segmentación declarada; dimensiones infraestructura, usuario, configuración y protección de comunicaciones | inventory/document-text.json, ficha documental de riesgos | caracterización previa; contexto de T001–T014 | documentos originales hashados y comandos con línea; fuentes externas académicas pendientes | solo caracterización; no revisión bibliográfica completa ni prueba criptográfica |
| OE2 comprobar efecto VLAN/ACL | entrega/respuesta por ICMP/TCP, P/C/O, control positivo y causa | test-plan.yaml, preflight, Packet Tracer, manifest.json | T001–T014 | captura/salida nueva, IP/SSID y PDU/ACL/routing | pendiente de CP3 |
| OE3 relacionar riesgos y controles | discrepancia sustentada y trazabilidad del control propuesto | results.csv, traceability.json y esquema de solución | casos con observaciones válidas | vínculo finding→test→manifest→SHA | esquema preparado, sin recomendaciones finales |

## Operacionalización y reglas

- Independiente: zona/VLAN de origen y servicio/destino seleccionados. Configuración baseline constante; ninguna intervención de remediación en esta fase.
- Dependiente: allow/deny/indeterminate/error observado. No reducir observaciones a pass/fail.
- Control: endpoint asociado a WLAN correcta, IP/gateway vigentes, destino activo, ruta esperada, tiempo de convergencia, misma copia/hash y versión del simulador.
- Repetición: registrar calentamiento ARP y cada intento; ante divergencia crear R2 sin borrar R1. El resumen principal selecciona primer registro, no el mejor resultado.
- Denominador: pruebas válidas; casos pendientes se reportan por separado, no como deny. Prueba negativa sin control positivo y destino verificado no es válida.
- C requiere toda la cadena conocida. ACL allow se mantiene como dato parcial mientras routing/servicio sean desconocidos. Una comparación indeterminada no es una brecha comprobada.

## Trazabilidad

Pregunta → OE → variable → test_id → evidencia cruda/hash → observación → clasificación P–C–O → finding_id → control → prueba de verificación.

Una afirmación que omita esos vínculos se etiqueta no suficientemente sustentada. Revisar configuración puede producir hipótesis, nunca observaciones de ejecución. Las afirmaciones originales de pruebas exitosas se conservan como documentación histórica, sin recontarlas como resultados de este avance.

## Formato académico posterior

Estos documentos son instrumentos y anexos técnicos de preparación, no Capítulos III/IV terminados. Para la entrega IEEE se debe incorporar la metodología, tablas identificadas y referencias verificadas con numeración IEEE. Todavía no se incorporaron fuentes bibliográficas externas ni citas académicas inventadas. OE1 requiere completar esa revisión; OE3 requiere resultados reales de CP3.
