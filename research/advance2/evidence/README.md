# Evidencia real e inmutable

`raw/T001/manifest.template.json` es una plantilla, no una ejecución. Cada ejecución usa `raw/T001-R1/manifest.json`; capturas reales y salidas se copian a ese mismo directorio y cada archivo recibe SHA-256. Esta adaptación mantiene todos los artefactos de una ejecución juntos. `screenshots/` se reserva para índices/enlaces; no crear copias editables como evidencia primaria.

Crear metadatos JSON fuera del directorio de evidencia. Los campos siguientes son una **estructura de entrada**, no resultados:

```json
{
  "test_id": "T001-R1",
  "timestamp": "FECHA_REAL_ISO8601_CON_ZONA",
  "source": "IP_REAL_CONFIRMADA",
  "destination": "IP_REAL_CONFIRMADA",
  "method": "comando real y captura de salida",
  "packet_tracer_version": "VERSION_OBSERVADA",
  "observed": "indeterminate",
  "valid": "false",
  "causality": "unknown",
  "positive_control_runs": [],
  "destination_verified": false,
  "notes": "Explicar resultado, estado del destino, asociación WLAN y limitaciones reales",
  "artifact_sources": ["C:/ruta/real/salida.txt", "C:/ruta/real/captura.png"]
}
```

Sustituir los placeholders solo con datos reales. `source`/`destination` son direcciones IP; incluir nombres de dispositivos y SSID en notes/preflight. Para deny válido, `destination_verified=true` debe sustentarse en artefactos y positive_control_runs debe referenciar controles reales allow válidos del plan. `observed=error/indeterminate` obliga a valid=false.

No confundir timeout con filtrado. Los artefactos de causa pueden incluir ACL aplicada, interfaz/dirección, ruta, contador si está soportado, inspección PDU y estado del servicio. `confirmed` exige evidencia directa de descarte por la regla aplicable; `strongly_supported` exige triangulación consistente; `possible` hipótesis parcial; `unknown` sin atribución.

Una captura debe mostrar origen, destino, comando/acción y resultado. Si la GUI no permite mostrar test_id sin editar la topología, relacionar la captura original con el ID mediante manifest y nombre del archivo; nunca agregar gráficos como si fueran parte de la captura. No usar fotos artificiales ni imágenes históricas como observaciones nuevas.

SHA-256 detecta alteraciones respecto al registro; no garantiza autenticidad si alguien puede reescribir archivo y manifiesto. Los commits y revisión independiente refuerzan la cadena de custodia. No sobrescribir manifiestos; usar nuevos Rn. No ejecutar colectores concurrentemente.
