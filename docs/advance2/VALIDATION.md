# Validación de preparación, cierre CP3 y auditoría CP4

Fecha inicial: 2026-11-05. Revisión CP4: 2026-11-06. Python 3.12 local; sin dependencias externas en el workflow preparado.

- Inventario: 57 fuentes originales; 42 TXT, 11 DOCX, 2 PKT, README y LICENSE. SHA-256 verificados contra baseline.
- Parser: 80 reglas ACL explícitas, 10 aplicaciones a interfaces, cero reglas ACL sin reconocer. No se afirma cobertura de IOS completo.
- Plan: 14 IDs únicos, política y objetivo por caso. Categorías primarias: external-connectivity 2, guest-isolation 2, management 3, radius 3, internal-access 1, wlc 2, negative-control 1; segmentation como categoría secundaria.
- C: 9 deny previstos por reglas conocidas, 5 unknown por información incompleta. No se sustituye permiso ACL por conectividad end-to-end.
- Las validaciones preparadas comprueban IDs, rutas, hashes, correspondencia observación/manifiesto, congelamiento de P/C y cobertura.
- Git diff de rutas originales contra commit base: sin cambios de contenido en los originales; main no se modifica.

## Cierre CP3

- 14 IDs cubiertos por 16 ejecuciones; 13 casos válidos y T010 indeterminado por prerrequisito no verificado. Se retienen R1/R2 y se usa la primera ejecución por caso para el resumen.
- `validate_evidence.py`: registrado sin errores críticos en el cierre CP3, incluyendo hashes del preflight, artefactos de ejecución, correspondencia observación/manifiesto, controles y hashes de P/C congelados.
- `validate_results.py --require-complete`: registrado sin errores críticos. Esta cobertura admite una limitación documentada; no afirma que T010 haya ejecutado SSH.
- 7 pruebas de software registradas como exitosas en CP3; incluyen alteración/escape de directorio del preflight mediante fixtures temporales.
- Los 57 archivos originales conservan hashes de baseline. La copia de ejecución fue guardada por el usuario sin cambios de configuración según su declaración y tiene otro hash; véase CP3-02. No se afirma equivalencia binaria ni una causa técnica específica para la diferencia.
- Automatización GUI observada: accesibilidad a veces ausente/atrasada; capturas visuales reales conservadas como evidencia. No hubo PDU fiable ni atribución confirmada a una regla específica.

## Auditoría formal CP4

La revisión CP4 verificó la consistencia lógica y documental de la campaña antes de CP5.

- 14/14 casos del plan están representados.
- 16 manifests reales cubren los 14 casos; T001 y T013 tienen R1/R2.
- 13 casos tienen observación válida; T010 permanece inválido/indeterminado por falta de servicio/cuenta SSH verificable.
- Todos los manifests auditados conservan:
  - baseline commit `2873d7a0cfb71fd768775c32edc6d7b2f9b3ab46`;
  - plan SHA-256 `168f112cc8f169f7297df1cb9223bf1a67cb5b70bffeef31fdd5a9e3922dc5c0`;
  - policy SHA-256 `296306d56fd3990edd27f4229085dab10e74c113bae8b3fec51514608f747cc4`;
  - Packet Tracer 9.0.1.0858;
  - uno o más artefactos asociados.
- 9 casos válidos tienen P=C=O.
- Los 13 casos válidos tienen P=O; `policy_agreement_rate=100 %`.
- Cuatro casos allow válidos —T001, T006, T009 y T013— conservan C=unknown y no se reclasifican.
- No hay contradicciones P/C/O conocidas; `discrepancies.csv` vacío es consistente con esa definición.
- Siete casos deny tienen causalidad `strongly_supported`; T012 y T014 conservan `possible`; no existe causalidad `confirmed`.
- Se identificaron diferencias entre TXT históricos y running-config observado (permisos RADIUS 1812/1813 y host de administración, permisos DHCP y diferencias terminales en ACL wifi). Se registran como discrepancias documentales/configuracionales, no como contradicciones P–C–O.
- La copia runtime guardada tiene SHA-256 `990d282545cc37295af7236228a8acf30981dd4ad835ffc71307b740f9db2812`, diferente al original `1be4c1d7c247c542ceaae24e58f43a782dfe4fcbdd524e7139f6f535b88a50fe`. Esta limitación debe acompañar el análisis académico.
- CP4 concluye `closed_with_documented_limitations` y autoriza continuar a CP5 sin modificar baseline ni iniciar remediación.

La auditoría completa está en `docs/advance2/CP4_AUDIT.md`; el resumen machine-readable está en `research/advance2/results/cp4-audit.json`.

## Procedencia de la copia guardada

La revisión final encontró la copia runtime de 254166 bytes con última escritura 2026-11-05 23:38:40 UTC (17:38:40 Costa Rica), antes de las pruebas posteriores. Los dos originales tienen 258544 bytes y conservan sus hashes. Al consultar, el usuario respondió: «Sí, lo guardé sin cambiar configuración».

Se preservó la copia guardada y un registro de hashes, fechas y ejecuciones posteriores en `research/advance2/evidence/preflight/CP3-02/`. Los manifests originales no se reescribieron. El commit baseline identifica la fuente original, sin certificar igualdad binaria de la copia guardada. Para exigir equivalencia binaria estricta sería necesaria otra campaña desde una copia nueva y verificada; CP4 no la exige para el análisis del segundo avance mientras esta limitación se declare expresamente.


## Cierre CP5

- Se promovieron seis hallazgos analíticos (F01–F06) únicamente después del cierre CP4.
- La propuesta contiene siete controles (C01–C07), clasificados por base experimental, experimental+literatura o literatura fuera del simulador.
- La trazabilidad finding→test→manifest/evidencia→control→verificación se materializa en `research/advance2/analysis/traceability.json`.
- `case-analysis.csv` conserva los 14 casos con P, C, O, validez, clasificación y causalidad.
- Se generaron cinco visualizaciones derivadas de los datos; ninguna se presenta como evidencia primaria.
- Se seleccionaron tres pares de screenshots primarios para el cuerpo y evidencia adicional para anexos.
- `CP5_ANALYSIS.md` contiene la interpretación completa; `CHAPTER_IV_DRAFT.md` contiene la versión académica para integrar al artículo.
- `ANNEX_INDEX.md` separa la data dura del cuerpo sin perder acceso a manifests, screenshots, salidas, running-config, hashes y procedencia.
- No se cambió ningún valor P/C/O, no se reescribió evidencia CP3 y no se inició remediation/.
- La interpretación conserva T010 como indeterminado, T012/T014 con causalidad possible y la limitación de hash de la copia runtime.

CP5 queda cerrado para fines del segundo avance. La siguiente fase documental consiste en integrar Capítulos III y IV al documento IEEE y realizar audit final contra la rúbrica.
