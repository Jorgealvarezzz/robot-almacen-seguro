# Atributos de calidad y trade-offs

## Atributos priorizados

Siguiendo el marco de la Semana 1 (atributos de calidad):

| Prioridad | Atributo | Por qué importa en este caso |
|-----------|----------|------------------------------|
| 1 | **Seguridad** | Es un sistema que recibirá acciones de control sobre hardware físico. Un actor no autorizado podría causar daños reales. |
| 2 | **Disponibilidad** | El operador necesita ver el estado del robot en tiempo casi real. |
| 3 | **Trazabilidad / auditabilidad** | La empresa necesita saber quién envió qué comando y qué reportó el robot. |
| 4 | **Escalabilidad** | Aunque arrancamos con un robot, la arquitectura debe soportar varios. |
| 5 | **Mantenibilidad** | Componentes conocidos y desacoplados. |
| 6 | **Performance (latencia)** | Segundos son aceptables, no tiempo real duro. |
| 7 | **Usabilidad** | Dashboard simple pero funcional. |

## Tácticas usadas por atributo

### Seguridad
- **Autenticar actores** → JWT en API, usuario/password en MQTT.
- **Limitar exposición** → único puerto público en el gateway.
- **Cifrar en tránsito** → TLS en MQTT y HTTPS en gateway.
- **Autorizar acciones** → verificación de rol para comandos.
- **Validar entradas** → Pydantic en todos los endpoints.
- **Auditar acciones críticas** → tabla `comandos` con usuario y timestamp.

### Disponibilidad
- **Desacoplamiento pub/sub** → si el backend cae, el broker sigue aceptando telemetría.
- **Health endpoint** (`/api/health`).
- **Auto-reconnect** del cliente MQTT.

### Trazabilidad
- Toda telemetría y evento se persiste con timestamp.
- Todo comando incluye el `sub` del JWT que lo originó.

### Escalabilidad
- Backend **stateless** (podría replicarse).
- Broker podría migrarse a cluster.
- Pub/sub permite N suscriptores sin tocar el edge.

### Mantenibilidad
- **Docs as Code**: diagramas en Mermaid versionados.
- **ADRs** para decisiones importantes.
- Cada contenedor tiene una responsabilidad clara.

---

## Trade-offs importantes

### Trade-off 1 — SQLite vs PostgreSQL
**Elegimos:** SQLite.
**Por qué:** simplifica el MVP (sin servicio extra, backup = copiar archivo).
**Costo:** no soporta escrituras concurrentes altas ni múltiples backends replicados.
**Cuándo cambiaría:** al pasar a varias instancias del backend o >50 req/s sostenidos → PostgreSQL.

### Trade-off 2 — JWT (HS256) vs OAuth2/Keycloak
**Elegimos:** JWT HS256 local.
**Por qué:** implementable en horas; Keycloak no cabe en 2 días.
**Costo:** secreto compartido único, sin IdP central, sin SSO.
**Cuándo cambiaría:** antes de producción. Es el primer upgrade del roadmap.

### Trade-off 3 — Usuario/password MQTT vs mTLS
**Elegimos:** usuario/password sobre TLS.
**Por qué:** cubre "no anónimo y no en claro".
**Costo:** si la password se filtra, se suplantan robots.
**Cuándo cambiaría:** con varios robots físicos → un cert por robot y ACLs por topic.

### Trade-off 4 — Polling HTTP vs WebSockets / SSE
**Elegimos:** polling cada 3 s desde el dashboard.
**Por qué:** trivial de implementar y depurar.
**Costo:** más tráfico HTTP y hasta 3 s de latencia.
**Cuándo cambiaría:** con decenas de operadores o latencia sub-segundo → SSE/WebSockets.

### Trade-off 5 — Dashboard HTML vanilla vs framework
**Elegimos:** HTML + JS vanilla.
**Por qué:** cero build, foco en arquitectura y seguridad.
**Costo:** no escala bien si el dashboard crece.
**Cuándo cambiaría:** al superar 3 pantallas o componentes reutilizables.

### Trade-off 6 — Docker Compose vs Kubernetes
**Elegimos:** Docker Compose.
**Por qué:** un comando levanta todo.
**Costo:** no es el deploy productivo real.
**Cuándo cambiaría:** al pasar a staging/producción → Kubernetes.

---

## Conexión con CAP (Semana 5)

El broker MQTT introduce un sistema distribuido. Ante una partición de red entre broker y backend:
- **Privilegiamos disponibilidad + tolerancia a particiones** (AP): el broker acepta publicaciones aunque el backend esté desconectado, y el backend las consumirá al reconectar (con QoS 1, "al menos una vez").
- **Consistencia eventual**: puede haber un retraso pequeño entre que el robot publica y el backend persiste.

Para telemetría de monitoreo es aceptable. Para **comandos críticos de control** (ej. parar el robot), se debe añadir en el futuro un mecanismo de confirmación explícito (ack del robot) y timeouts.
