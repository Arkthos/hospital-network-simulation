# Brechas y límites promovidos en CP5

CP5 distingue entre **brecha de seguridad observada**, **brecha de gobernanza**, **brecha de evidencia** y **control conforme**. No todo resultado deny constituye una brecha y no toda limitación metodológica constituye un fallo de la red.

| ID | Tipo | Descripción | Evidencia | Tratamiento |
|---|---|---|---|---|
| G01 | Gobernanza | Los fragmentos TXT no representan de forma exhaustiva el running-config observado. | CP3 running-config; F06. | Establecer captura/versionado de configuración viva y diff automático. |
| G02 | Evidencia | No se verificó un servicio/cuenta SSH existente en RADIUS para T010. | T010. | Definir el protocolo administrativo real y repetir solo ese caso en una futura validación. |
| G03 | Evidencia causal | T012 no permite afirmar que la solicitud hacia Management fue descartada antes de llegar al destino. | T012. | Mantener causalidad possible; usar PDU/contadores o prueba de servicio dirigida en una campaña futura. |
| G04 | Evidencia causal | T014 demuestra timeout de HTTPS Guest→WLC, pero no el punto exacto de descarte. | T014. | Mantener causalidad possible; no atribuir a una regla exacta sin evidencia directa. |
| G05 | Procedencia experimental | La copia runtime guardada no es binariamente idéntica al PKT original. | CP3-02 provenance. | Declarar limitación; conservar original y copia hashada; repetir desde copia nueva si se exige equivalencia binaria estricta. |
| G06 | Cobertura | Packet Tracer no valida propiedades criptográficas, asociación real, RF, TLS real ni comportamiento moderno del endpoint. | Alcance metodológico. | Tratar esos controles mediante literatura y, si fuera necesario, laboratorio físico especializado. |

## Controles conformes que no deben remediarse

- Guest→External funcional y Guest→recursos seleccionados restringido.
- Corp Wi-Fi→External funcional y Corp Wi-Fi→Internal/Management restringido.
- Management→WLC HTTPS funcional desde el bastión seleccionado.
- Hospitalstaff→Internal funcional y flujos seleccionados hacia infraestructura administrativa restringidos.

La propuesta de solución debe preservar estos comportamientos y evitar introducir cambios solo para que el laboratorio parezca más completo.
