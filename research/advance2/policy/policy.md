# Política propuesta del caso

JSON compatible con YAML 1.2; Python estándar evita una dependencia de parsing YAML.

- VLAN40: movilidad no clínica; acceso interno denegado por diseño del caso, no por deducción del nombre staff
- No se evalúa autenticación RADIUS de clientes hasta confirmar AAA efectivo
- Management administrativo por TCP443 WLC y TCP22 RADIUS solo si servicio existe; ICMP no sustituye administración

- P001: Guest Wi-Fi → External fuera del ASA, icmp echo: **allow**. Política propuesta del caso: conectividad funcional de control y servicios autorizados.
- P002: Guest Wi-Fi → Internal Server, icmp echo: **deny**. Política propuesta del caso: aislamiento de invitados y protección de zonas administrativas.
- P003: Guest Wi-Fi → Management autorizado, icmp echo: **deny**. Política propuesta del caso: aislamiento de invitados y protección de zonas administrativas.
- P004: Guest Wi-Fi → RADIUS, icmp echo: **deny**. Política propuesta del caso: aislamiento de invitados y protección de zonas administrativas.
- P005: Guest Wi-Fi → Corp Wi-Fi movilidad, icmp echo: **deny**. Política propuesta del caso: aislamiento de invitados y protección de zonas administrativas.
- P006: Corp Wi-Fi movilidad → External fuera del ASA, icmp echo: **allow**. Política propuesta del caso: acceso externo para movilidad sin acceso clínico interno.
- P007: Corp Wi-Fi movilidad → Internal Server, icmp echo: **deny**. Política propuesta del caso: acceso externo para movilidad sin acceso clínico interno.
- P008: Corp Wi-Fi movilidad → Management autorizado, icmp echo: **deny**. Política propuesta del caso: acceso externo para movilidad sin acceso clínico interno.
- P009: Management autorizado → WLC, tcp/443: **allow**. Política propuesta del caso: acceso administrativo mínimo desde bastión autorizado.
- P010: Management autorizado → RADIUS, tcp/22: **allow**. Política propuesta del caso: acceso administrativo mínimo desde bastión autorizado.
- P011: Hospitalstaff cableado → RADIUS, icmp echo: **deny**. Política propuesta del caso: aislamiento de invitados y protección de zonas administrativas.
- P012: Hospitalstaff cableado → Management autorizado, icmp echo: **deny**. Política propuesta del caso: aislamiento de invitados y protección de zonas administrativas.
- P013: Hospitalstaff cableado → Internal Server, icmp echo: **allow**. Política propuesta del caso: conectividad funcional de control y servicios autorizados.
- P014: Guest Wi-Fi → WLC, tcp/443: **deny**. Política propuesta del caso: aislamiento de invitados y protección de zonas administrativas.

La documentación original afirma Corp Wi-Fi sin acceso clínico; se adopta una política hospitalaria explícita de movilidad restringida. No representa una WLAN clínica autorizada. Un cambio a acceso clínico sería otra política versionada antes de CP3, sin cambiar baseline.
