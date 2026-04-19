# Robot de Almacén Seguro

Solución integradora de arquitectura de sistemas para un robot móvil de almacén que reporta telemetría, es monitoreado desde una interfaz web y permite operaciones autenticadas.

> Examen final — Arquitectura de Sistemas. Caso: Robot de almacén seguro.

---

## 1. Problema que resuelve

Una empresa quiere modernizar una parte de su almacén con un robot móvil que detecta obstáculos, reporta su estado y envía telemetría. La empresa necesita una arquitectura base que defina:

- Cómo se comunica el robot con el resto del sistema.
- Qué se ejecuta en edge, backend y visualización.
- Cómo se protege la comunicación y el acceso.
- Cómo se documentan las decisiones técnicas.
- Qué riesgos de seguridad existen desde el inicio.

Este repositorio entrega una propuesta funcional mínima pero coherente: **edge → broker MQTT → backend → gateway → dashboard**, con controles de seguridad reales aplicados.

---

## 2. Componentes del sistema

| Componente | Tecnología | Responsabilidad |
|------------|------------|-----------------|
| **Edge (robot simulador)** | Python + paho-mqtt | Simula telemetría del robot (posición, batería, obstáculos) y publica en MQTT |
| **Broker MQTT** | Mosquitto + TLS + auth | Transporte desacoplado de eventos edge → backend |
| **Backend API** | FastAPI + SQLite | Se suscribe al broker, persiste eventos, expone REST con JWT |
| **Gateway** | NGINX (reverse proxy + TLS) | Único punto expuesto. Termina TLS y enruta al backend |
| **Dashboard** | HTML + JS vanilla | Login con JWT y visualización de telemetría y estado del robot |

Todo corre en **Docker Compose**. Los secretos viven en `.env` (no en el código).

---

## 3. Arquitectura en una imagen

```
  ┌─────────────┐    MQTT/TLS    ┌──────────────┐
  │  Robot sim  │ ─────────────▶ │  Mosquitto   │
  │   (edge)    │   user+pass    │   (broker)   │
  └─────────────┘                └──────┬───────┘
                                        │ suscripción
                                        ▼
                                 ┌──────────────┐
                                 │   Backend    │
                                 │  (FastAPI)   │
                                 │    + JWT     │
                                 │   + SQLite   │
                                 └──────┬───────┘
                                        │ HTTP interno
                                        ▼
                                 ┌──────────────┐
                HTTPS             │   NGINX      │     HTTPS
  Usuario  ◀──────────────────▶  │   Gateway    │ ◀──────────── Dashboard
                                 └──────────────┘
```

Diagramas formales (C4 Context, C4 Container, UML secuencia) en [`docs/`](./docs/).

---

## 4. Cómo correrlo (PowerShell en Windows)

### Requisitos
- Docker Desktop instalado y corriendo.
- OpenSSL (viene con Git for Windows: `C:\Program Files\Git\usr\bin\openssl.exe`).
- Puerto 8443 libre (HTTPS del gateway) y 8883 libre (MQTT TLS).

### Pasos

```powershell
# 1. Entrar a la carpeta
cd robot-almacen-seguro

# 2. Copiar variables de entorno de ejemplo
Copy-Item .env.example .env

# 3. Generar certificados TLS
.\scripts\generar-certs.ps1

# 4. Generar password hasheado para Mosquitto
.\scripts\generar-mosquitto-passwd.ps1

# 5. Levantar todo
docker compose up --build

# 6. Abrir dashboard en el navegador
# https://localhost:8443
# (aceptar el warning de cert autofirmado)
```

### Usuarios de prueba
- `admin` / `admin123` (rol: **admin** — puede enviar comandos)
- `operador` / `op123` (rol: **operador** — solo lectura)

Ver **QUICKSTART.md** para la secuencia exacta de comandos PowerShell paso a paso, incluyendo cómo generar todas las evidencias.

---

## 5. Controles de seguridad aplicados

| Control | Dónde | Evidencia |
|---------|-------|-----------|
| **TLS** en canal MQTT | broker ↔ edge, broker ↔ backend | `evidence/tls-handshake.log` |
| **TLS** en canal HTTP | usuario ↔ gateway | `evidence/screenshot-06-cert.png` |
| **Autenticación JWT** | API del backend | `evidence/login-admin.json` |
| **Autorización por rol** | `POST /api/comandos` (solo admin) | `evidence/403-operador.txt` |
| **Gateway reverse proxy** | backend no expuesto al exterior | `evidence/backend-no-expuesto.txt` |
| **Autenticación MQTT** | usuario/password en broker | `config/mosquitto.conf` |
| **Secretos fuera del código** | `.env` ignorado por Git | `.gitignore`, `.env.example` |
| **Validación de entradas** | Pydantic en FastAPI | `src/backend/app/models.py` |
| **Rate limiting** | NGINX sobre `/api/` y `/auth/login` | `src/gateway/nginx.conf` |

Análisis completo en [`docs/threat-model/stride.md`](./docs/threat-model/stride.md).

---

## 6. Qué funciona y qué quedó fuera

**Funciona:**
- Publicación de telemetría desde el simulador vía MQTT/TLS.
- Persistencia de eventos en SQLite.
- Login con JWT y dashboard con polling cada 3 s.
- Gateway terminando TLS; backend no expuesto.
- Dos roles (admin, operador) con permisos distintos.
- Rate limiting en gateway.
- Auditoría de comandos (quién, cuándo, qué).

**Fuera del alcance del MVP:**
- OAuth2 completo con Keycloak (documentado en ADR-0002).
- mTLS entre componentes (se usa user/password sobre TLS).
- PostgreSQL (se usa SQLite por simplicidad).
- WebSockets push real-time.
- CI/CD y tests automatizados.
- Escalado horizontal.

Justificación en los ADRs y en el documento de trade-offs.

---

## 7. Estructura del repositorio

```
/
├── README.md
├── QUICKSTART.md
├── docker-compose.yml
├── .env.example
├── docs/
│   ├── c4/               ← Context y Container
│   ├── uml/              ← Secuencia de telemetría
│   ├── adr/              ← 2 Architecture Decision Records
│   ├── threat-model/     ← Matriz STRIDE
│   └── calidad/          ← Atributos y trade-offs
├── src/
│   ├── edge/             ← Simulador del robot
│   ├── backend/          ← API FastAPI
│   ├── gateway/          ← NGINX + certs
│   └── dashboard/        ← HTML + JS
├── config/               ← mosquitto.conf, passwd
├── scripts/              ← Generación de certs y passwords
└── evidence/             ← Screenshots, logs, pruebas
```

---

## 8. Documentación arquitectónica

- [C4 Context](./docs/c4/context.md)
- [C4 Container](./docs/c4/containers.md)
- [UML — diagrama de secuencia](./docs/uml/secuencia-telemetria.md)
- [ADR-0001 — MQTT como protocolo edge](./docs/adr/0001-mqtt-como-protocolo-edge.md)
- [ADR-0002 — JWT para autenticación de la API](./docs/adr/0002-jwt-para-autenticacion-api.md)
- [Matriz STRIDE](./docs/threat-model/stride.md)
- [Atributos de calidad y trade-offs](./docs/calidad/atributos-y-tradeoffs.md)

---

## 9. Declaración de uso ético de IA

### 1. Herramientas de IA usadas
Claude (Anthropic) como asistente de diseño, estructuración de repositorio y generación inicial de código y documentación.

### 2. En qué parte del trabajo se usó
- Estructuración inicial del repositorio y esqueleto de archivos.
- Generación de borradores de diagramas C4/UML en notación Mermaid.
- Generación inicial de ADRs y matriz STRIDE.
- Apoyo en configuración de Mosquitto, NGINX y Docker Compose.
- Generación de boilerplate de FastAPI y del simulador edge.

### 3. Para qué se usó exactamente
Para acelerar el andamiaje del proyecto y evitar reescribir código de configuración repetitivo, concentrando el tiempo humano en decisiones arquitectónicas, aplicación real de seguridad, y pruebas de funcionamiento.

### 4. Qué parte fue revisada, corregida o adaptada por el equipo
- Validación de que los diagramas C4 reflejen la solución realmente implementada.
- Ajuste de los ADRs para reflejar decisiones concretas tomadas.
- Verificación del funcionamiento end-to-end (MQTT → backend → dashboard).
- Pruebas de los controles de seguridad: intentos con/sin token, acceso denegado por rol, inspección de TLS.
- Corrección de configuraciones de Mosquitto y NGINX para que funcionaran juntas.
- Captura manual de todas las evidencias.

### 5. Qué parte NO fue generada por IA
- La elección del caso de implementación mínimo (qué se incluye y qué queda fuera).
- La ejecución real del sistema y la validación de su funcionamiento.
- Las capturas de pantalla, logs y evidencias.
- La defensa técnica de las decisiones.
- La revisión y edición crítica de todo el contenido antes de entregar.
