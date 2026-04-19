# UML — Diagrama de Secuencia

## Caso: Ciclo completo de telemetría + consulta autenticada

```mermaid
sequenceDiagram
    autonumber
    actor User as Operador
    participant Dash as Dashboard
    participant GW as Gateway (NGINX)
    participant API as Backend (FastAPI)
    participant DB as SQLite
    participant MQTT as Mosquitto
    participant Robot as Edge Simulator

    Note over Robot,MQTT: Flujo 1 - Telemetria (continuo, cada 2s)

    Robot->>MQTT: CONNECT (TLS + user/pass)
    MQTT-->>Robot: CONNACK OK
    API->>MQTT: SUBSCRIBE robot/+/telemetry (TLS)
    MQTT-->>API: SUBACK OK

    loop Cada 2 segundos
        Robot->>MQTT: PUBLISH robot/rb-01/telemetry {pos, bat, estado}
        MQTT-->>API: Deliver message
        API->>DB: INSERT INTO telemetry(...)
        DB-->>API: OK
    end

    Note over User,API: Flujo 2 - Login y consulta autenticada

    User->>Dash: Abre https://localhost:8443
    Dash->>GW: GET /
    GW-->>Dash: index.html + app.js

    User->>Dash: Ingresa usuario + password
    Dash->>GW: POST /auth/login (HTTPS)
    GW->>API: POST /auth/login (HTTP interno)
    API->>API: Verifica credenciales
    API-->>GW: 200 {access_token: JWT}
    GW-->>Dash: 200 {access_token: JWT}
    Dash->>Dash: Guarda JWT en memoria

    loop Polling cada 3s
        Dash->>GW: GET /api/telemetry (Authorization: Bearer JWT)
        GW->>API: GET /api/telemetry
        API->>API: Valida JWT (firma + expiracion + rol)
        alt JWT valido
            API->>DB: SELECT ultimas 50 filas
            DB-->>API: rows
            API-->>GW: 200 [{...}]
            GW-->>Dash: 200 [{...}]
            Dash->>User: Renderiza telemetria
        else JWT invalido o expirado
            API-->>GW: 401 Unauthorized
            GW-->>Dash: 401
            Dash->>User: Redirige al login
        end
    end

    Note over User,API: Flujo 3 - Intento de comando (control de rol)

    User->>Dash: Click "Enviar comando STOP"
    Dash->>GW: POST /api/comandos {cmd: STOP}
    GW->>API: POST /api/comandos
    API->>API: Valida JWT + verifica rol == admin
    alt Rol admin
        API->>MQTT: PUBLISH robot/rb-01/cmd {STOP}
        API->>DB: INSERT INTO comandos
        API-->>Dash: 202 Accepted
    else Rol operador
        API-->>Dash: 403 Forbidden
        Dash->>User: "No autorizado"
    end
```

## Lecciones que ilustra este diagrama

- **Separación de canales:** el robot nunca habla directamente con el backend ni con el dashboard. Todo pasa por el broker.
- **Único punto de entrada:** el usuario solo toca el gateway.
- **Zero Trust básico:** cada request a `/api/*` valida el JWT; no hay "confianza por estar en la red interna".
- **Control de autorización:** la pertenencia a la red no basta; se requiere el rol correcto para acciones sensibles.
