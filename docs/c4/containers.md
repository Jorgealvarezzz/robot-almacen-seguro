# C4 — Nivel 2: Container

## Propósito
Descomponer el sistema en sus contenedores (procesos/servicios) y mostrar los protocolos de comunicación entre ellos.

## Diagrama

```mermaid
C4Container
    title Container - Robot de Almacen Seguro

    Person(usuario, "Operador / Admin", "Usa el dashboard")
    System_Ext(robot, "Robot Fisico (simulado)", "Edge device")

    System_Boundary(sistema, "Robot de Almacen Seguro") {
        Container(edge, "Robot Simulator", "Python, paho-mqtt", "Simula telemetria del robot y la publica.")
        Container(broker, "Mosquitto Broker", "Mosquitto + TLS + auth", "Transporte de eventos edge a backend.")
        Container(backend, "Backend API", "Python, FastAPI, SQLite", "Suscripcion MQTT, persistencia, API REST con JWT.")
        ContainerDb(db, "Base de datos", "SQLite", "Almacena eventos, usuarios y comandos.")
        Container(gateway, "Gateway", "NGINX reverse proxy + TLS", "Termina TLS y enruta al backend. Unico componente expuesto.")
        Container(dashboard, "Dashboard Web", "HTML + JS vanilla", "UI de login y visualizacion.")
    }

    Rel(usuario, gateway, "Navega al dashboard y consume API", "HTTPS/8443")
    Rel(gateway, dashboard, "Sirve estaticos", "HTTP interno")
    Rel(gateway, backend, "Proxy /api/*", "HTTP interno")
    Rel(dashboard, gateway, "Peticiones con JWT", "HTTPS")

    Rel(robot, edge, "Genera senal simulada", "in-process")
    Rel(edge, broker, "Publica telemetria", "MQTT/TLS + user/pass")
    Rel(backend, broker, "Suscribe a topics", "MQTT/TLS + user/pass")
    Rel(backend, db, "Lee y escribe", "SQL")
```

## Contenedores

### 1. Robot Simulator (edge)
- **Tecnología:** Python 3.11 + `paho-mqtt`.
- **Responsabilidad:** generar telemetría realista (posición XY, batería %, estado, obstáculo detectado) y publicarla cada 2 segundos.
- **Topics que publica:**
  - `robot/{id}/telemetry` — estado continuo
  - `robot/{id}/event` — eventos discretos (obstáculo detectado, batería baja)
- **Autenticación:** usuario/password contra el broker, sobre TLS.

### 2. Mosquitto Broker
- **Tecnología:** Eclipse Mosquitto 2.x.
- **Puerto interno/externo:** 8883 (TLS only).
- **Sin listener no cifrado.**
- Lista de usuarios hasheados en `passwd` (generada por script).

### 3. Backend API (FastAPI)
- **Tecnología:** Python 3.11, FastAPI, Uvicorn, SQLAlchemy, paho-mqtt.
- **Responsabilidades:**
  - Suscriptor MQTT que escucha `robot/+/telemetry` y `robot/+/event` y persiste en SQLite.
  - API REST con:
    - `POST /auth/login` → entrega JWT.
    - `GET /api/health` → público.
    - `GET /api/telemetry` → requiere JWT.
    - `GET /api/eventos` → requiere JWT.
    - `POST /api/comandos` → requiere JWT **y rol admin**.
- **No expuesto al exterior**: solo accesible desde la red Docker interna.

### 4. Base de datos (SQLite)
- Archivo en volumen Docker `backend-data`.
- Tablas: `telemetry`, `eventos`, `comandos`.
- Trade-off documentado.

### 5. Gateway (NGINX)
- **Único componente que expone puerto al host (8443).**
- Termina TLS con cert autofirmado.
- Enruta `/api/*` y `/auth/*` al backend, resto al dashboard.
- Rate limiting activo.

### 6. Dashboard Web
- HTML + JS vanilla servido por NGINX.
- Login → obtiene JWT → almacena en memoria (no localStorage) → polling cada 3 s.

## Red y exposición

| Puerto host | Servicio | Propósito |
|-------------|----------|-----------|
| 8443 | gateway (nginx) | **HTTPS** — dashboard y API |
| 8883 | mosquitto | **MQTT/TLS** — exposición para demostración |

El **backend no expone puertos al host**. Tampoco el dashboard.

## Flujo principal
1. El simulador publica telemetría cada 2 s.
2. El backend (suscriptor MQTT) la recibe y guarda en SQLite.
3. El usuario abre `https://localhost:8443`, hace login, obtiene un JWT.
4. El dashboard hace `GET /api/telemetry` con el JWT cada 3 s.
5. El admin puede hacer `POST /api/comandos`; el operador no.
