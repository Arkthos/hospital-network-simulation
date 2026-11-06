# CP4 — Auditoría formal de resultados y evidencia

Fecha de revisión: 2026-11-06  
Baseline de referencia: `2873d7a0cfb71fd768775c32edc6d7b2f9b3ab46`  
Campaña CP3 auditada: 14 casos, 16 ejecuciones registradas.

## 1. Objetivo del checkpoint

CP4 revisa la consistencia y suficiencia de la evidencia generada en CP3 antes de utilizarla en el análisis académico. No modifica P, C, O, los manifiestos ni los artefactos primarios. La revisión se limita a trazabilidad, cobertura, consistencia P–C–O, causalidad, procedencia, discrepancias de configuración y alcance de las afirmaciones permitidas.

## 2. Dictamen

**CP4: APROBADO CON LIMITACIONES DOCUMENTADAS.**

La campaña es suficiente para avanzar a CP5 y redactar el análisis de resultados del segundo avance, siempre que las conclusiones conserven las limitaciones de procedencia, causalidad y alcance indicadas en este documento.

No se identificaron contradicciones entre los resultados consolidados, los manifiestos de las ejecuciones y la política/test plan congelados. No se autoriza interpretar estas pruebas como una medición general de seguridad de la red ni como validación de propiedades criptográficas o de radiofrecuencia.

## 3. Cobertura y consistencia

- 14/14 casos del plan tienen representación en CP3.
- Existen 16 ejecuciones inmutables: T001 y T013 tienen R1/R2; los demás casos tienen R1.
- 13 casos tienen observación válida.
- T010 es indeterminado e inválido para medir acceso SSH porque no se verificó un servidor/cuenta SSH existente en RADIUS.
- Todos los manifiestos auditados conservan el mismo baseline commit.
- Todos los manifiestos conservan el mismo hash del test plan: `168f112cc8f169f7297df1cb9223bf1a67cb5b70bffeef31fdd5a9e3922dc5c0`.
- Todos los manifiestos conservan el mismo hash de policy: `296306d56fd3990edd27f4229085dab10e74c113bae8b3fec51514608f747cc4`.
- Todos los manifiestos identifican Packet Tracer 9.0.1.0858.
- Ningún manifiesto auditado carece de artefactos asociados.

El resumen consolidado registra 14 casos ejecutados, 16 runs, 13 casos válidos, 9 conformes P=C=O, 5 clasificaciones P–C–O indeterminadas y 0 discrepancias P/C/O conocidas.

## 4. Interpretación correcta de las métricas

El valor `conformity_rate = 69.23 %` corresponde a 9/13 casos válidos cuyo P, C y O son conocidos y coinciden. **No representa un porcentaje de seguridad de la red.**

Cuatro casos válidos —T001, T006, T009 y T013— observaron `allow` y coinciden con la política P, pero conservaron `C=unknown` porque la conectividad extremo a extremo no podía predecirse con suficiente certeza antes de ejecutar. Estos casos no deben reclasificarse retroactivamente.

Para los 13 casos válidos, P y O coinciden: `policy_agreement_rate = 100 %`. Este valor significa únicamente que el comportamiento observado coincidió con la política definida para los flujos seleccionados.

T010 no entra en el denominador de casos válidos.

## 5. Revisión caso por caso

| Caso | P | C | O | Validez | Causalidad / interpretación CP4 |
|---|---|---|---|---|---|
| T001 | allow | unknown | allow | válida | Conectividad Guest→externo observada; no atribuir causa de las pérdidas iniciales. |
| T002 | deny | deny | deny | válida | ACL/ruta y controles positivos apoyan fuertemente el aislamiento Guest→Internal; regla exacta no confirmada por PDU/contadores. |
| T003 | deny | deny | deny | válida | Aislamiento Guest→Management fuertemente respaldado por configuración y controles. |
| T004 | deny | deny | deny | válida | Guest→RADIUS bloqueado; más de una ACL puede intervenir, por lo que no debe atribuirse a una regla única. |
| T005 | deny | deny | deny | válida | Guest→Corp Wi-Fi bloqueado; controles de ambos extremos respaldan el resultado. |
| T006 | allow | unknown | allow | válida | Conectividad Corp Wi-Fi→externo observada; C permanece unknown. |
| T007 | deny | deny | deny | válida | Corp Wi-Fi→Internal bloqueado; resultado consistente con política de movilidad restringida. |
| T008 | deny | deny | deny | válida | Corp Wi-Fi→Management bloqueado; causalidad ACL fuertemente respaldada, no confirmada a nivel de regla exacta. |
| T009 | allow | unknown | allow | válida | Management→WLC HTTPS responde. Solo demuestra disponibilidad del servicio simulado; no autenticación ni TLS real. |
| T010 | allow | unknown | indeterminate | inválida | Falta prerrequisito SSH verificable. No es allow ni deny y no debe convertirse en fallo de red. |
| T011 | deny | deny | deny | válida | VLAN30→RADIUS sin intercambio ICMP; ACL/routing apoyan fuertemente el bloqueo, pero no existe control ICMP remoto positivo al RADIUS. |
| T012 | deny | deny | deny | válida | El intercambio ICMP falla; causalidad solo possible. La ACL de Management puede bloquear el retorno, por lo que no prueba que la solicitud no llegue a VLAN60. |
| T013 | allow | unknown | allow | válida | VLAN30→Internal responde de forma estable; funciona como control positivo. |
| T014 | deny | deny | deny | válida | Guest→WLC HTTPS termina en Request Timeout; controles de origen/destino existen, pero el punto exacto de descarte no fue confirmado. |

## 6. Fuerza causal

A nivel de los 14 casos principales:

- 7 casos deny tienen causalidad `strongly_supported`.
- 2 casos deny —T012 y T014— tienen causalidad `possible`.
- 4 casos allow válidos conservan causalidad `unknown`, porque la prueba demuestra conectividad, no cuál componente hizo posible el flujo.
- T010 conserva causalidad `unknown` y es inválido por prerrequisito no disponible.
- Ningún caso debe elevarse a causalidad `confirmed` porque no se obtuvo una traza PDU o delta de contadores suficientemente fiable para identificar una regla exacta.

CP5 debe distinguir siempre entre **comportamiento observado** y **mecanismo causal atribuido**.

## 7. Discrepancias de configuración/documentación

Durante CP3 se observaron diferencias entre fragmentos TXT históricos y el running-config de la simulación:

1. Las ACL RADIUS observadas incluyen permisos UDP 1812/1813 y un permiso para el host de administración `192.168.60.8`.
2. Las ACL wifi/guestwifi observadas incluyen permisos de respuesta DHCP no reflejados de la misma forma en todos los fragmentos.
3. El final de la ACL wifi no es idéntico entre MLS0 y MLS1: una instancia termina permitiendo el subnet 40 hacia any y otra utiliza una forma más amplia.

Estas diferencias son **discrepancias documentales/configuracionales**, no discrepancias P–C–O. No se modificó C retrospectivamente. Para describir el estado realmente ejecutado, CP5 debe priorizar el running-config capturado durante la campaña y tratar los TXT como fuentes de preparación/baseline histórico, no como representación exhaustiva del estado vivo.

El archivo `discrepancies.csv` permanece correctamente vacío porque su función es registrar contradicciones P/C/O, no divergencias entre fuentes documentales.

## 8. Procedencia del runtime

Los dos PKT originales conservan SHA-256 `1be4c1d7c247c542ceaae24e58f43a782dfe4fcbdd524e7139f6f535b88a50fe`.

La copia runtime guardada tiene SHA-256 `990d282545cc37295af7236228a8acf30981dd4ad835ffc71307b740f9db2812` y no es binariamente idéntica al original. El usuario declaró haberla guardado sin cambios de configuración. La copia, timestamps, hashes y lista de runs afectados están preservados en `evidence/preflight/CP3-02`.

**Evaluación CP4:** esta diferencia debe conservarse como limitación de procedencia. No existe base para afirmar equivalencia binaria ni para atribuir técnicamente la diferencia solo a serialización/estado de Packet Tracer. Al mismo tiempo, los originales permanecen intactos y la campaña conserva running-config, controles, artefactos y manifiestos suficientes para analizar los resultados dentro del alcance académico planteado.

Una repetición desde una copia nueva y hash-verificada aumentaría la fuerza de reproducibilidad si se exigiera equivalencia binaria estricta, pero CP4 no la considera necesaria para continuar al análisis del segundo avance, siempre que la limitación se declare expresamente.

## 9. Alcance permitido para CP5

La evidencia permite sostener, para los flujos evaluados, que:

- Guest Wi-Fi mantiene conectividad externa y los accesos seleccionados hacia Internal Server, Management, RADIUS, Corp Wi-Fi y WLC no completaron intercambio exitoso.
- Corp Wi-Fi mantiene conectividad externa y los flujos seleccionados hacia Internal Server y Management fueron bloqueados.
- El host de Management alcanzó el servicio HTTPS representado del WLC.
- Hospitalstaff VLAN30 alcanzó Internal Server, mientras los intercambios seleccionados hacia RADIUS y Management no tuvieron éxito.
- El patrón observado es coherente con una arquitectura segmentada y con una WLAN corporativa de movilidad restringida, no con una WLAN clínica de acceso interno amplio.

La evidencia **no permite** sostener que:

- toda comunicación entre esas zonas esté bloqueada o permitida para cualquier protocolo/puerto;
- la red sea “69.23 % segura” o “100 % segura”;
- una ACL específica causó cada deny con certeza absoluta;
- el WLC tenga autenticación segura o TLS real por mostrar su página;
- RADIUS sea inaccesible por SSH;
- Packet Tracer valide WPA3, Evil Twin, RF, OWE, certificados o criptografía real;
- los resultados representen a hospitales reales fuera del caso simulado.

## 10. Decisión de cierre

CP4 queda **cerrado con limitaciones documentadas**.

No se requiere modificar el baseline ni repetir resultados para iniciar CP5. No debe iniciarse remediación antes de que CP5 transforme estos resultados en hallazgos académicos y determine si existe una brecha que realmente requiera cambio.

Próximo checkpoint: **CP5 — análisis académico, relación riesgo–control, propuesta de solución y paquete de evidencia para el Capítulo IV.**
