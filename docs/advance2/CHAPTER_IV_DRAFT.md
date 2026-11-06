# IV. ANÁLISIS DE RESULTADOS — borrador académico

## A. Resultados generales y validez de la evidencia

La campaña experimental evaluó catorce flujos de conectividad definidos antes de ejecutar la simulación. Se registraron dieciséis ejecuciones debido a la repetición de dos controles positivos después de reinicios de sesión. Trece casos produjeron observaciones válidas y uno, T010, permaneció indeterminado porque el servicio SSH previsto para el servidor RADIUS no pudo verificarse. Esta condición se mantuvo como limitación y no se sustituyó por otra prueba que respondiera una pregunta diferente.

Nueve de los trece casos válidos cumplieron la relación estricta P=C=O: la política esperada, la predicción derivada de la configuración y el comportamiento observado coincidieron. En cuatro casos permitidos —T001, T006, T009 y T013— el comportamiento observado coincidió con la política, pero la predicción de configuración se había conservado como desconocida. En consecuencia, el 69,23 % de conformidad estricta no representa un porcentaje de seguridad; expresa solamente la proporción de casos válidos en los que los tres estados pudieron determinarse y coincidieron. Si se compara únicamente la política definida antes del experimento con la observación, los trece casos válidos mostraron el comportamiento esperado.

**TABLA X. Resumen de resultados por zona de origen**

| Zona de origen | Casos | Válidos | P=C=O | P=O con C desconocida | Indeterminado |
|---|---:|---:|---:|---:|---:|
| Guest Wi-Fi | 6 | 6 | 5 | 1 | 0 |
| Corp Wi-Fi | 3 | 3 | 2 | 1 | 0 |
| Management | 2 | 1 | 0 | 1 | 1 |
| Hospitalstaff | 3 | 3 | 2 | 1 | 0 |
| **Total** | **14** | **13** | **9** | **4** | **1** |

La Fig. 4 debe acompañar esta tabla porque permite diferenciar visualmente los tres estados sin inducir una lectura de “pruebas aprobadas y fallidas”.

## B. Red de invitados: aislamiento sin pérdida de funcionalidad

Los resultados de Guest Wi-Fi muestran un patrón consistente de servicio externo con restricción interna. T001 verificó que el cliente de invitados podía alcanzar el host externo. A partir de ese control positivo, T002–T005 y T014 evaluaron destinos con mayor nivel de confianza: Internal Server, Management, RADIUS, Corp Wi-Fi y WLC. Ninguno de esos cinco flujos completó el intercambio previsto.

El significado del conjunto es más relevante que cada prueba individual. Si únicamente se observara un ping sin respuesta, no sería posible diferenciar entre filtrado, un destino inactivo o una falla general de conectividad. T001 permite descartar esta última explicación para el origen Guest, mientras los controles de destino y la configuración observada aumentan la fuerza de atribución en varios casos. T002–T005 presentan una relación coherente entre ACL, ruta y resultado, por lo que su causalidad se clasificó como fuertemente respaldada. T014 conserva una atribución más limitada: el timeout demuestra que Guest no completó la sesión HTTPS con el WLC, pero no identifica directamente el punto de descarte.

Este comportamiento implementa una propiedad fundamental de una red para visitantes: proporcionar el servicio necesario sin extender la misma confianza hacia recursos internos. NIST recomienda administrar las WLAN con configuraciones y políticas acordes con los riesgos y mantener esas configuraciones durante su ciclo de vida [3]. En el escenario analizado, la separación por VLAN y ACL materializa esa recomendación en los flujos seleccionados.

La evidencia visual más útil es el contraste T001/T002: en un panel se observa conectividad externa funcional desde Guest y en el otro la ausencia de alcance hacia Internal Server. La combinación evita presentar el bloqueo como un resultado aislado.

## C. WLAN corporativa: una red privada no implica confianza interna

T006–T008 aportan el contraste más directo con una interpretación simplista de “red privada”. El cliente asociado al SSID corporativo 'wifi' utilizó WPA2-PSK/AES y obtuvo conectividad externa en T006, pero no alcanzó Internal Server en T007 ni Management en T008.

Por tanto, VLAN40 no se comporta como una extensión inalámbrica de la red clínica interna. Se comporta como una zona de movilidad corporativa restringida. Esta distinción es importante porque demuestra que la clasificación privada/corporativa describe quién debería utilizar la WLAN, pero no determina por sí misma qué recursos puede alcanzar después de asociarse.

El resultado es consistente con la hipótesis propuesta en el primer avance. Schmitt et al. cuestionan tratar la etiqueta de Wi-Fi público como una medida suficiente de inseguridad [1]; en sentido complementario, los resultados aquí obtenidos muestran que la etiqueta privada tampoco constituye por sí sola una medida de confianza interna. La autorización efectiva se construye mediante segmentación, ACL, rutas y servicios, además de la autenticación inalámbrica.

La Fig. 7 debe mostrar T006 y T007 en paralelo. El objetivo no es ilustrar dos pings, sino demostrar que un mismo origen puede conservar conectividad útil y, simultáneamente, tener restringido el acceso interno.

## D. Plano administrativo y diferenciación de privilegios

El plano de administración presenta controles selectivos, aunque no todos pudieron evaluarse con la misma profundidad. T009 confirmó que el host Management 192.168.60.8 pudo acceder al servicio HTTPS representado por el WLC 192.168.70.5. T014 utilizó el mismo destino desde Guest Wi-Fi y finalizó en timeout. Mantener el destino constante permite atribuir mayor significado al cambio de origen: el servicio está disponible, pero no para la zona Guest en el flujo probado.

Este resultado no debe extenderse a propiedades que Packet Tracer no reproduce. Mostrar la página del WLC no demuestra que el proceso de autenticación sea resistente a ataques ni que los certificados o TLS correspondan a una implementación real. La prueba valida alcance de servicio dentro de la simulación, no seguridad criptográfica.

T010 representa la principal limitación funcional del conjunto. El plan preveía Management→RADIUS mediante TCP/22, pero no se verificó un servicio SSH ni una cuenta existente en el servidor. Ejecutar ICMP como sustituto habría cambiado el instrumento y fabricar un servicio habría modificado el baseline. Por ello, el resultado correcto fue indeterminado. La consecuencia para la propuesta es concreta: antes de validar administración de RADIUS debe definirse cuál es el servicio administrativo real que se pretende permitir.

T011–T013 complementan esta lectura desde Hospitalstaff. El host de VLAN30 alcanzó Internal Server en T013, pero no completó los intercambios seleccionados con RADIUS ni Management. Esto indica que pertenecer a una red interna de personal no equivale a pertenecer al plano administrativo. La arquitectura diferencia acceso funcional de privilegio administrativo.

T012, sin embargo, requiere una formulación cuidadosa. El intercambio ICMP con Management no se completó, pero la configuración permite plantear que el retorno pudo ser filtrado. En ausencia de una traza PDU fiable, el resultado demuestra falta de comunicación bidireccional exitosa, no necesariamente que la solicitud fuera descartada antes de llegar al destino.

## E. Configuración estática frente a comportamiento observado

Cuatro pruebas válidas permitidas conservaron C=unknown: Guest→External, Corp Wi-Fi→External, Management→WLC y Hospitalstaff→Internal. En todos los casos P=O. Esto muestra una limitación práctica del análisis exclusivamente estático.

Las ACL permiten identificar denegaciones o permisos explícitos, pero no describen por sí solas toda la cadena de conectividad. Para anticipar un allow extremo a extremo también deben conocerse routing, gateways, estado del servicio, ASA/NAT y ruta de retorno. Por esa razón, el diseño metodológico congeló C antes de ejecutar y evitó reclasificarla después de observar el resultado.

La Fig. 9, matriz de acceso observado, debe utilizarse para visualizar precisamente esta diferencia. Las celdas no probadas deben permanecer vacías: convertirlas en allow o deny a partir de inferencias produciría una cobertura ficticia.

Este hallazgo justifica conservar pruebas activas como mecanismo de regresión. La revisión de configuración y la ejecución no son instrumentos redundantes; responden preguntas distintas y se complementan.

## F. Deriva documental y calidad de configuración

La comparación entre los fragmentos TXT y el running-config capturado mostró diferencias reales. Entre ellas se encontraron permisos RADIUS para UDP 1812/1813, un permiso relacionado con el host de Management, reglas de respuesta DHCP y diferencias en la terminación de la ACL wifi entre los dos switches multicapa.

Estas diferencias no se clasificaron como una vulnerabilidad explotada porque ningún resultado demostró por sí mismo un impacto adverso. Su relevancia es operativa: la documentación estática no representaba completamente el estado vivo utilizado por el simulador. Una investigación basada únicamente en esos fragmentos habría podido atribuir incorrectamente un comportamiento.

NIST recomienda estandarizar, automatizar y centralizar la implementación y mantenimiento de configuraciones WLAN para facilitar la detección de cambios no autorizados y mantener consistencia [3]. El caso aporta una razón concreta para aplicar ese principio: la configuración ejecutada debe capturarse, versionarse y compararse automáticamente con la documentación antes de utilizarla como evidencia.

## G. Contraste con la hipótesis

Los resultados respaldan parcialmente la hipótesis de trabajo. La parte comprobada experimentalmente corresponde a segmentación, configuración y control de acceso. Guest Wi-Fi conservó conectividad externa y no alcanzó los recursos internos seleccionados. Corp Wi-Fi también conservó conectividad externa y, pese a ser una WLAN privada, no obtuvo acceso automático a Internal Server ni Management.

La evidencia, por tanto, no muestra una relación simple en la que “pública” equivalga a insegura y “privada” a segura. Muestra que el acceso efectivo depende de políticas concretas aplicadas después de la asociación inalámbrica.

No se considera comprobada la parte de la hipótesis relacionada con comportamiento del usuario, asociación, TLS real o seguridad del endpoint. Esas dimensiones permanecen respaldadas por el marco teórico. Los ataques de asociación dependen de cómo el cliente identifica y valida redes [7]; las aplicaciones pueden reintroducir comunicaciones HTTP incluso cuando HTTPS es predominante [9]; y las decisiones de conexión del usuario responden también a factores de contexto [12]. El simulador no sustituye esa evidencia.

## H. Propuesta de solución

La propuesta no parte de que la topología esté “mal configurada”. Varios controles evaluados funcionan de acuerdo con la política y deben preservarse.

Primero, Guest Wi-Fi debe conservarse como zona independiente con salida externa y restricciones hacia recursos internos y administrativos. Estas rutas pueden mantenerse como casos de regresión T001–T005 y T014.

Segundo, VLAN40 debe documentarse explícitamente como WLAN de movilidad corporativa restringida. Si el caso requiriera dispositivos clínicos inalámbricos con acceso a servicios internos, la opción más controlable sería un SSID/VLAN separado con permisos mínimos específicos, no ampliar globalmente los privilegios de VLAN40.

Tercero, el uso observado de WPA2-PSK/AES en la WLAN corporativa debería revisarse en un despliegue real. La segmentación limita el impacto posterior, pero una PSK compartida no proporciona identidad individual. Debe evaluarse 802.1X/EAP con RADIUS y validación correcta de la infraestructura, junto con WPA3 cuando exista compatibilidad. Esta recomendación se apoya en la literatura y no se presenta como una capacidad validada por CP3 [2], [3], [7].

Cuarto, la organización debe definir explícitamente los servicios administrativos permitidos. T009 demuestra el acceso representado al WLC desde Management; T010 demuestra que no debe asumirse un protocolo administrativo para RADIUS sin verificar que exista.

Quinto, la configuración viva debe convertirse en evidencia versionada. Antes de cada campaña o cambio, el running-config debe capturarse, compararse mediante diff y asociarse a un commit/hash. La suite P–C–O puede ejecutarse después de cambios para comprobar si la política continúa cumpliéndose.

Finalmente, estos controles lógicos deben complementarse con defensas que Packet Tracer no evalúa: validación de certificados, actualización de endpoints, control de auto-asociación, HTTPS/TLS y monitoreo de WLAN y puntos de acceso no autorizados [1], [3], [7], [9].

**TABLA XI. Síntesis de la propuesta**

| Acción | Evidencia principal | Tipo |
|---|---|---|
| Preservar aislamiento Guest | T001–T005, T014 | Control observado |
| Formalizar Corp Wi-Fi restringida | T006–T008 | Control observado |
| Evaluar autenticación individual 802.1X/EAP | Preflight + [2], [3], [7] | Mejora fuera del simulador |
| Formalizar matriz de administración WLC/RADIUS | T009, T010, T014 | Mejora operativa |
| Versionar running-config y detectar drift | Diferencias TXT/running-config + [3] | Gobernanza |
| Mantener suite P–C–O de regresión | T001–T014 | Validación continua |
| Añadir controles endpoint/TLS/WLAN monitoring | [1], [3], [7], [9], [12] | Capa complementaria |

## I. Limitaciones

La interpretación se circunscribe al escenario simulado y a los flujos seleccionados. La campaña no prueba todos los protocolos entre todas las zonas. La copia runtime guardada tiene un hash diferente al PKT original; el usuario indicó que la guardó sin cambios de configuración y ambos artefactos fueron preservados, pero no se afirma equivalencia binaria. T010 permanece indeterminado. T012 y T014 no identifican directamente el punto exacto de descarte. Finalmente, Packet Tracer [13] permite validar la arquitectura lógica representada, pero no debe utilizarse como evidencia experimental de WPA3 real, OWE, RF, Evil Twin, certificados o TLS criptográfico.

La data detallada, manifests, hashes, screenshots, outputs y running-config no se reproducen íntegramente en el cuerpo para evitar convertir el artículo en un informe forense. Permanecen disponibles en los anexos y en el repositorio de investigación, manteniendo la trazabilidad entre cada afirmación y su evidencia primaria.
