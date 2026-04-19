# Observaciones de Evaluación — Robot de Almacén Seguro

> Este documento fue generado con apoyo de herramientas de análisis estático de repositorios,
> validación de consistencia entre documentación y código, y revisión del historial de trabajo
> colaborativo. Las observaciones son objetivas y están referenciadas a archivos y líneas
> específicas del proyecto.
>
> **Versión analizada:** commit `7c6def1` — rama `main` — 2026-04-19  
> **Ramas revisadas:** `main` (única rama en el repositorio)

---

## Calificación Aproximada

| Criterio | Máx. | Aprox. | Notas |
|---|:-:|:-:|---|
| Comprensión del caso y planteamiento | 15 | 12 | Actores, alcance, riesgos y restricciones documentados en C4 Context; sin documento formal de Etapa 1 |
| Arquitectura propuesta | 15 | 14 | Arquitectura IoT excelente con doble red Docker; estilo no nombrado formalmente |
| Documentación arquitectónica | 15 | 15 | C4 x2, UML con 3 flujos, 2 ADRs con 5 alternativas cada uno, STRIDE con 14 amenazas, 6 trade-offs |
| Implementación funcional | 10 | 10 | Flujo completo funcional; supera el mínimo con roles, auditoría y mapa de rastro |
| Seguridad aplicada | 15 | 13 | 10+ controles implementados; `tls_insecure_set(True)`, CORS abierto y credenciales MQTT en código fuente |
| Análisis de amenazas y calidad | 15 | 14 | STRIDE con 14 amenazas, 7 atributos de calidad, 6 trade-offs, conexión con teorema CAP |
| Trabajo colaborativo y repositorio | 10 | 2 | Un solo contribuidor, cero ramas de feature, cero PRs, cero revisiones — ver Sección 4 |
| Evidencias y defensa técnica | 5 | 5 | README, QUICKSTART, 18 archivos de evidencia, pruebas de seguridad completas |
| **TOTAL** | **100** | **85** | |

> Esta calificación es orientativa y está basada en el análisis estático del repositorio.
> La defensa oral puede modificarla en función de la capacidad del equipo para explicar
> sus decisiones técnicas.

---

## Sección 1 — Validación del Checklist de Entrega

### Repositorio

| Requisito | Estado | Observación |
|---|:---:|---|
| Repositorio accesible | ✅ | `github.com/Jorgealvarezzz/robot-almacen-seguro` |
| Estructura clara de carpetas | ✅ | `docs/`, `src/`, `config/`, `evidence/`, `scripts/` organizados con claridad |
| `README.md` presente y descriptivo | ✅ | 210 líneas; incluye problema, componentes, controles de seguridad, instrucciones y declaración de IA |
| Ramas por feature | ❌ | Solo existe `main`; no hay feature branches |
| Commits comprensibles | ✅ | 10 commits con Conventional Commits (`feat(backend):`, `docs(evidence):`, etc.) |
| Al menos 3 Pull Requests | ❌ | 0 Pull Requests — todo fue commiteado directamente a `main` |
| Al menos 1 revisión por otro integrante | ❌ | Imposible: un solo contribuidor en todo el historial |

### Documentación Arquitectónica

| Requisito | Estado | Observación |
|---|:---:|---|
| C4 Context | ✅ | Actores, alcance, restricciones y riesgos iniciales incluidos |
| C4 Container | ✅ | 6 contenedores, 2 redes Docker, topics MQTT correctos, puertos documentados |
| 1 diagrama UML | ✅ | Secuencia con 3 flujos: telemetría, login+consulta, control de roles |
| 2 ADRs | ✅ | ADR-0001 (MQTT, 5 alternativas) y ADR-0002 (JWT, 4 alternativas) con implicaciones de seguridad |
| Matriz STRIDE | ✅ | 14 amenazas con severidad, mitigación y estado por componente |
| Atributos de calidad y trade-offs | ✅ | 7 atributos priorizados con tácticas; 6 trade-offs con cuándo cambiar; conexión con CAP |

### Implementación Mínima

| Requisito | Estado | Observación |
|---|:---:|---|
| Simulador del robot o edge | ✅ | `src/edge/robot_simulator.py`: movimiento, batería, obstáculos, recepción de comandos |
| Envío de telemetría o eventos | ✅ | MQTT/TLS cada 2s; eventos en detección de obstáculos; ACK de comandos |
| Backend o servicio receptor | ✅ | FastAPI: suscripción MQTT, persistencia SQLite, API REST con JWT |
| Visualización o dashboard | ✅ | Login, KPIs, mapa de rastro, tabla de eventos, tabla de auditoría de comandos |
| Punto de entrada definido | ✅ | Solo NGINX en puerto 8443; backend sin puertos expuestos al host |

### Seguridad Mínima

| Requisito | Estado | Observación |
|---|:---:|---|
| Al menos dos controles aplicados | ✅ | 10+ controles — ver Sección 5 |
| Evidencia de protección de ruta o canal | ✅ | 401 sin token, 403 sin rol admin, 202 con rol admin, TLS handshake — todo documentado en `/evidence` |
| Exposición mínima de servicios | ✅ | Solo 8443 (gateway) y 8883 (MQTT/TLS); backend en red interna |
| Validación o control de acceso | ✅ | JWT con expiración, rol embebido, validación Pydantic con regex en rutas y comandos |

### Análisis

| Requisito | Estado | Observación |
|---|:---:|---|
| Matriz STRIDE | ✅ | 14 amenazas con estado ✅/⚠️ por componente |
| Mitigaciones propuestas | ✅ | Cada amenaza con control implementado y estado |
| Atributos de calidad priorizados | ✅ | Seguridad > Disponibilidad > Trazabilidad justificado con tácticas |
| Trade-offs explicados | ✅ | 6 trade-offs con columna "cuándo cambiar" — útil para roadmap futuro |

### Evidencias

| Requisito | Estado | Observación |
|---|:---:|---|
| Instrucciones de ejecución | ✅ | `QUICKSTART.md` paso a paso para Windows PowerShell |
| Screenshots, logs o comandos | ✅ | 18 archivos: logs, JSON, screenshots, TLS handshake, rate-limit |
| Evidencia de funcionamiento principal | ✅ | Telemetría real, login exitoso, JWT válido, flujo de comandos completo |

---

## Sección 2 — Diagramas C4

### C4 Context — completo

`docs/c4/context.md` define correctamente:
- **3 actores:** Operador (solo lectura), Administrador (lectura + comandos), Robot físico (simulado)
- **Alcance del sistema:** dentro/fuera claramente delimitado
- **4 restricciones explícitas** (único punto de entrada, sin conexión directa robot↔backend, TLS obligatorio, etc.)
- **4 riesgos iniciales** con mitigación anotada

Es uno de los C4 Context más completos vistos — incluye restricciones y riesgos que normalmente van en un documento de Etapa 1 separado.

### C4 Container — completo

`docs/c4/containers.md` descompone el sistema en **6 contenedores** con:
- Tecnología, responsabilidad y red de cada componente
- Topics MQTT correctos (`robot/{id}/telemetry`, `robot/{id}/event`, `robot/{id}/cmd`)
- Puertos documentados (8443 expuesto, 8883 para demo, backend interno)
- **2 redes Docker** separadas (`backend-net`, `gateway-net`) explicadas

El diagrama es coherente con la implementación real en `docker-compose.yml`.

---

## Sección 3 — ADRs

Ambos ADRs superan el estándar esperado:

| ADR | Alternativas evaluadas | Implicaciones de seguridad | Consecuencias negativas | Roadmap |
|---|:---:|:---:|:---:|:---:|
| 0001 — MQTT | 5 (HTTP, WS, AMQP, gRPC, MQTT) | ✅ TLS, user/pass, ACLs futuros | ✅ SPOF, curva de aprendizaje | ✅ mTLS, cluster |
| 0002 — JWT | 4 (sesiones, JWT, OAuth2, Basic) | ✅ Expiración corta, secreto en .env | ✅ Revocación difícil, HS256 | ✅ RS256, Keycloak |

**Destacable:** el ADR-0002 documenta explícitamente por qué OAuth2/Keycloak fue rechazado para el MVP (desproporcionado en 2 días) pero se señala como camino a producción — esto demuestra pensamiento arquitectónico maduro.

---

## Sección 4 — Trabajo Colaborativo

### Distribución de commits en `main`

| Integrante | Commits en main |
|---|:-:|
| Jorgealvarezzz (`gu24IA0016@globaluniversity.edu.mx`) | 10 |

### Observaciones

**Esta es la debilidad más severa del proyecto y la única que impacta significativamente la calificación.**

El repositorio muestra **un solo contribuidor en todo el historial**. No existe evidencia de trabajo en equipo:

| Criterio del checklist | Estado |
|---|:---:|
| Ramas por feature | ❌ Solo `main` |
| Al menos 3 Pull Requests | ❌ 0 PRs |
| Al menos 1 revisión por otro integrante | ❌ Imposible con 1 integrante |

El examen establece explícitamente:

> *"si una persona no tiene evidencia de trabajo subida al repositorio, esa falta de participación sí afectará la evaluación del trabajo colaborativo."*

**Lo que sí cumple:** los 10 commits usan Conventional Commits (`feat(backend):`, `docs(evidence):`, `docs(c4):`) con mensajes descriptivos y atómicos — la calidad individual de la contribución es excelente. La estructura del repositorio es ordenada.

**Lo que falta completamente:** ramas de trabajo, Pull Requests, revisión de código entre pares, distribución visible del trabajo.

---

## Sección 5 — Seguridad: Estado Actual

### Controles implementados y verificados

| Control | Implementación | Evidencia | Estado |
|---|---|---|:---:|
| TLS en MQTT | `mosquitto.conf`: listener 8883, TLS 1.2, certs firmados por CA propia | `evidence/tls-handshake.log` | ✅ |
| TLS en HTTP | `nginx.conf`: TLSv1.2+, ciphers fuertes, HSTS 1 año | `evidence/screenshot-06-cert-autofirmado.png` | ✅ |
| Autenticación MQTT | `allow_anonymous false` + `passwd` hasheado | `config/mosquitto.conf:14–16` | ✅ |
| JWT con expiración | HS256, exp 30 min, rol embebido | `src/backend/app/auth.py:1–69` | ✅ |
| Autorización por rol | `require_admin` → 403 si rol != admin | `evidence/403-operador.txt` | ✅ |
| Backend no expuesto | Sin puertos en `docker-compose.yml`, solo en `backend-net` | `evidence/backend-no-expuesto.txt` (HTTP 000) | ✅ |
| Secretos fuera del código | `.env` en `.gitignore`; `.env.example` en repo | `.gitignore:1` | ✅ |
| Validación de entradas | Pydantic con regex: `robot_id` y `cmd` restringidos | `src/backend/app/models.py:60–66` | ✅ |
| Rate limiting | Login: 5 req/min; API: 30 req/s | `nginx.conf:2–3`, `evidence/rate-limit-test.txt` | ✅ |
| Seguridad DoS en broker | `max_connections 100`, `max_inflight 50`, `max_queued 1000` | `config/mosquitto.conf:20–22` | ✅ |
| Headers HTTP de seguridad | `nosniff`, `X-Frame-Options: DENY`, `HSTS`, `Referrer-Policy` | `nginx.conf:15–18` | ✅ |
| Auditoría de comandos | Tabla `comandos` con usuario (del JWT) + timestamp | `src/backend/app/models.py:72–80` | ✅ |

---

### Observación técnica — `tls_insecure_set(True)` en MQTT

Tanto el backend (`mqtt_subscriber.py`) como el edge (`robot_simulator.py`) incluyen:
```python
client.tls_insecure_set(True)
```

Esta llamada **desactiva la verificación del hostname** del certificado TLS. Con esta configuración, un certificado emitido para `mosquitto` es aceptado aunque el cliente se conecte a un host con nombre diferente. En un entorno de producción esto eliminaría la protección contra ataques MITM que el TLS debería proveer.

Para el MVP con certs autofirmados es comprensible (se conectan por nombre DNS de Docker), pero debe documentarse en el STRIDE y corregirse antes de producción usando el CN correcto del certificado.

---

### Observación técnica — Credenciales MQTT en código fuente

`src/backend/app/mqtt_subscriber.py` y `src/edge/robot_simulator.py` definen:
```python
MQTT_USER = "robot"
MQTT_PASSWORD = "robotpass"
```

El `docker-compose.yml` pasa `env_file: .env` a estos servicios, y el `.env.example` define `MQTT_USER` y `MQTT_PASSWORD`. Sin embargo, el código no lee esas variables de entorno — usa los valores hardcodeados. Las credenciales MQTT deberían leerse con:
```python
MQTT_USER = os.getenv("MQTT_USER", "robot")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "robotpass_cambiame")
```

---

### Observación técnica — CORS abierto (`allow_origins=["*"]`)

`src/backend/app/main.py:8`:
```python
allow_origins=["*"]
```

En producción esto permitiría que cualquier origen haga peticiones autenticadas al backend. Para el MVP es tolerable (el JWT mitiga el riesgo), pero debe restringirse a los dominios conocidos antes de despliegue real.

---

### Observación menor — Puerto 8883 expuesto al host

`docker-compose.yml` publica `"8883:8883"`. Esto no es necesario para la operación del sistema (todos los clientes MQTT están en la red Docker interna). El puerto está expuesto únicamente para facilitar las evidencias de demostración, lo que es aceptable para el MVP — basta con documentarlo.

---

## Sección 6 — Lo que funcionó bien

- **Documentación arquitectónica de primer nivel.** C4 Context con restricciones y riesgos, C4 Container con doble red Docker, UML con 3 flujos diferenciados, 2 ADRs con 5 alternativas cada uno, STRIDE con 14 amenazas — este nivel de documentación supera ampliamente el mínimo.
- **TLS en ambos canales.** MQTT/TLS y HTTPS implementados con infraestructura PKI propia (CA, certs firmados, scripts de generación). La mayoría de equipos no implementa TLS en MQTT.
- **Autorización por roles correctamente implementada.** `require_admin` en FastAPI, 403 cuando el operador intenta POST `/api/comandos`, evidenciado con screenshots y logs.
- **Auditoría de comandos.** La tabla `comandos` almacena `usuario` extraído del JWT — cierra la amenaza de Repudiation del STRIDE.
- **Rate limiting diferenciado.** 5 req/min en `/auth/login` (contra brute force) vs 30 req/s en `/api/` (uso normal) — pocos proyectos implementan esto.
- **Headers de seguridad HTTP.** `HSTS`, `X-Frame-Options`, `nosniff`, `Referrer-Policy` en NGINX — va más allá del mínimo esperado.
- **Evidence package completo.** 18 archivos que demuestran cada control de seguridad: 401, 403, 202, timeout, TLS handshake, rate limiting, screenshots de UI.
- **QUICKSTART.md.** Guía reproducible paso a paso con generación de certificados y passwords — cualquier revisor puede levantar el sistema desde cero.
- **Declaración de IA honesta y específica.** Detalla exactamente qué hizo y qué no hizo la IA, con distinción entre estructura asistida y ejecución/validación del equipo.
- **Trade-offs con columna "cuándo cambiar".** No solo explica el trade-off sino cuándo debe revisarse — indica visión de arquitectura más allá del MVP.

---

## Sección 7 — Brechas Abiertas al Cierre

| # | Brecha | Severidad |
|---|---|:---:|
| A | **Sin ramas, sin PRs, sin revisión cruzada** — todo el historial es de un solo contribuidor sin evidencia de trabajo en equipo | 🔴 Crítica (requisito de evaluación) |
| B | `tls_insecure_set(True)` en backend y edge — desactiva verificación de hostname, elimina protección MITM de TLS | 🟡 |
| C | Credenciales MQTT hardcodeadas en código fuente (`MQTT_USER`, `MQTT_PASSWORD`) — no se leen de las variables de entorno pese a que `.env.example` las define | 🟡 |
| D | `allow_origins=["*"]` en CORS — cualquier origen puede hacer peticiones autenticadas | 🟡 |
| E | Screenshots 03 y 05 ausentes de `/evidence/` (QUICKSTART lista 6 screenshots; solo hay 4) | 🟢 Menor |
