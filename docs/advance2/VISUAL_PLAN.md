# Plan visual para el Capítulo IV y anexos

Principio: cada elemento visual debe responder una pregunta analítica o demostrar una observación. No usar screenshots generales de la topología como decoración.

## Cuerpo principal recomendado

| Elemento | Función analítica | Formato IEEE |
|---|---|---|
| Fig. 3 Flujo metodológico | Explicar cómo se obtuvo la evidencia | Una columna |
| Fig. 4 Estado P–C–O | Evitar interpretar 69,23 % como porcentaje de seguridad | Una columna |
| Fig. 6 Par Guest: T001 vs T002 | Mostrar servicio externo funcional + aislamiento interno | Dos columnas, panel A/B |
| Fig. 7 Par Corp Wi-Fi: T006 vs T007 | Mostrar que “privada” no implica confianza interna | Dos columnas, panel A/B |
| Fig. 8 Par Management/WLC: T009 vs T014 | Comparar mismo servicio desde origen autorizado y Guest | Dos columnas, panel A/B |
| Fig. 9 Matriz de acceso observado | Sintetizar los flujos probados y evitar generalizaciones a celdas no ensayadas | Dos columnas |
| Fig. 10 Confianza causal | Separar observación de atribución causal | Una columna |
| Fig. 11 Trazabilidad | Mostrar ruta dato→hallazgo→control | Dos columnas o anexo |

Si el espacio se vuelve restrictivo, conservar como mínimo Fig. 4, Fig. 6, Fig. 9 y Fig. 10 en el cuerpo; mover Fig. 7, Fig. 8 y Fig. 11 a anexos.

## Tablas principales recomendadas

1. **Tabla de operacionalización**: dimensión → indicador → instrumento.
2. **Tabla resumida de resultados por zona**:
   - Guest: 6/6 válidos, 5 P=C=O, 1 C=unknown.
   - Corp Wi-Fi: 3/3 válidos, 2 P=C=O, 1 C=unknown.
   - Management: 1/2 válido, 1 C=unknown, T010 indeterminado.
   - Hospitalstaff: 3/3 válidos, 2 P=C=O, 1 C=unknown.
3. **Tabla de hallazgos F01–F06**: evidencia → significado → límite.
4. **Matriz de propuesta C01–C07**: control → base → verificación.
5. **Tabla de limitaciones**: procedencia, causalidad, cobertura y simulador.

La matriz T001–T014 completa debe ir al Anexo A, no al cuerpo.

## Screenshots

Los screenshots deben conservar recorte suficiente para identificar origen/destino/resultado y no deben editarse para añadir resultados no presentes. Para el artículo se permiten copias de presentación (recorte/escala) mientras la evidencia primaria hashada permanezca intacta en el repositorio.

Pares prioritarios:
- Guest: T001-R2/03-T001-R2-series2-complete-0.jpg + T002-R1/01-T002-series1-0.jpg.
- Corp Wi-Fi: T006-R1/04-T006-series2-complete-0.jpg + T007-R1/01-T007-series1-complete-0.jpg.
- WLC: T009-R1/01-T009-request1-0.jpg + T014-R1/13-T014-request1-observed-0.jpg.

Screenshots secundarios para anexo:
- T010-R1/01-T010-SSH-precondition-0.jpg.
- T012-R1/09-T012-series2-final-0.jpg.
- T013-R2/07-T013-R2-series2-complete-0.jpg.

## Reglas de caption

El caption debe decir qué demuestra la imagen, no solo qué contiene.

Correcto:
“Contraste entre conectividad externa funcional y restricción hacia el servidor interno desde Guest Wi-Fi.”

Evitar:
“Captura de Packet Tracer.”

Cuando una imagen solo demuestra disponibilidad o ausencia de intercambio, no usar palabras como “secure”, “blocked by ACL X” o “authenticated” salvo que la evidencia lo demuestre.
