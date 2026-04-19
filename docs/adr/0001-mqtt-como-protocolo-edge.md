# ADR-0001: MQTT como protocolo de comunicación edge-backend

**Fecha:** 2026-04-18
**Estado:** Aceptado
**Contexto:** Proyecto Robot de Almacén Seguro, fase inicial.

## Contexto

Necesitamos un mecanismo para que el robot (edge) envíe telemetría y eventos al backend. Opciones consideradas:

- **HTTP/REST directo edge → backend**
- **WebSockets**
- **MQTT con broker intermediario**
- **AMQP (RabbitMQ)**
- **gRPC streaming**

El escenario tiene estas características:
- Potencialmente muchos robots publicando en paralelo.
- Enlaces de red de almacén que pueden ser inestables (Wi-Fi industrial).
- Cargas pequeñas (JSON de decenas a cientos de bytes), pero frecuentes.
- Requisito de desacoplamiento edge ↔ backend para poder escalar o reiniciar el backend sin perder mensajes.

## Decisión

**Usaremos MQTT con un broker Mosquitto intermedio** para toda la comunicación edge → backend.

Topics adoptados:
- `robot/{id}/telemetry` — estado continuo del robot.
- `robot/{id}/event` — eventos discretos (obstáculo, batería baja).
- `robot/{id}/cmd` — comandos desde el backend hacia el robot.

El canal será **MQTT sobre TLS** (puerto 8883) con autenticación usuario/password.

## Alternativas consideradas

| Opción | Pro | Contra | Por qué no |
|--------|-----|--------|------------|
| HTTP/REST directo | Simple, conocido | Acoplamiento fuerte, sin colas, mala tolerancia a caídas | No escala bien a N robots con red inestable |
| WebSockets | Push bidireccional | Gestión de reconexión manual, no hay broker nativo | Reinventar lo que MQTT ya resuelve |
| AMQP/RabbitMQ | Potente, rico en features | Pesado para edge, mayor footprint | Sobredimensionado para el MVP |
| gRPC streaming | Rápido, tipado | Requiere servidor siempre disponible, no hay colas nativas | Mismo problema de acoplamiento |

## Consecuencias

### Positivas
- **Desacoplamiento** entre el robot y el backend: si el backend cae, los mensajes pueden persistir brevemente en el broker.
- **Patrón pub/sub**: agregar más suscriptores (ej. servicio de analítica) es trivial.
- **Footprint bajo** en el edge: `paho-mqtt` es ligero.
- **Buena adopción en IoT**, consistente con Semanas 9 y 10 del curso.

### Negativas / Trade-offs
- **Punto único de falla añadido**: el broker. Se mitiga monitoreándolo y, en el futuro, desplegándolo en HA.
- **Curva de aprendizaje**: QoS, retained messages, LWT — conceptos nuevos para parte del equipo.
- **Orden y entrega exactos dependen del QoS elegido** (usamos QoS 1 para telemetría: "al menos una vez").

### Controles de seguridad derivados
- TLS obligatorio (puerto 8883, sin listener plano).
- Autenticación usuario/password.
- ACLs por topic (próxima iteración).

## Estado futuro (no en este MVP)
- Migrar a **mTLS** para autenticación por certificado del robot.
- Cluster Mosquitto con bridging para alta disponibilidad.
- ACLs por robot individual.
