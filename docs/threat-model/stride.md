# Matriz STRIDE — Robot de Almacén Seguro

## Alcance
Se analizan las amenazas sobre los componentes principales: **edge (robot)**, **broker MQTT**, **backend API**, **gateway** y **dashboard**.

## Convención
- **Severidad**: Alta / Media / Baja (probabilidad × impacto, criterio del equipo).
- **Estado**: ✅ mitigado en el MVP | ⚠️ parcial | ❌ pendiente para siguientes iteraciones.

---

## Matriz

| # | Categoría | Amenaza | Componente | Severidad | Mitigación aplicada | Estado |
|---|-----------|---------|------------|-----------|---------------------|--------|
| 1 | **S**poofing | Un atacante se hace pasar por un robot legítimo y publica telemetría falsa al broker. | Broker MQTT | Alta | Autenticación usuario/password obligatoria + TLS. Próximo paso: mTLS con cert por robot. | ⚠️ |
| 2 | **S**poofing | Un atacante se hace pasar por un usuario (operador/admin). | API / Dashboard | Alta | Login con password + JWT firmado (HS256) con `exp` 30 min. | ✅ |
| 3 | **T**ampering | Alguien intercepta y modifica mensajes MQTT entre robot y broker. | Canal MQTT | Alta | Canal cifrado con TLS (puerto 8883, sin listener plano). | ✅ |
| 4 | **T**ampering | Alguien altera el JWT para elevar su rol. | API | Alta | Firma HMAC verificada en cada request; cualquier cambio invalida la firma. | ✅ |
| 5 | **T**ampering | SQL injection en parámetros de consulta. | Backend | Media | SQLAlchemy con consultas parametrizadas + validación Pydantic. | ✅ |
| 6 | **R**epudiation | Un admin ejecuta un comando al robot y luego lo niega. | API / DB | Media | Tabla `comandos` registra usuario (`sub` del JWT), timestamp y comando. | ✅ |
| 7 | **R**epudiation | Un robot publica un evento que el backend no registra → no hay trazabilidad. | Backend | Media | Todo mensaje del broker se persiste en `telemetry`/`eventos` con timestamp. | ✅ |
| 8 | **I**nformation Disclosure | El panel o los errores exponen stack traces o datos sensibles. | Backend / Dashboard | Media | FastAPI sin `debug=True`; errores devuelven mensajes genéricos. | ✅ |
| 9 | **I**nformation Disclosure | El backend se expone directo al exterior sin pasar por el gateway. | Compose / Red | Alta | Backend **no publica puertos** al host; solo accesible desde red Docker interna; único puerto expuesto es el gateway. | ✅ |
| 10 | **I**nformation Disclosure | Secretos (JWT_SECRET, password MQTT) en el repo. | Repo | Alta | `.env` en `.gitignore`; solo se versiona `.env.example`. | ✅ |
| 11 | **D**enial of Service | Un atacante satura el broker con conexiones o mensajes. | Broker | Media | `max_connections` y `max_inflight_messages` configurados en Mosquitto. Próximo: rate limiting por cliente. | ⚠️ |
| 12 | **D**enial of Service | Un atacante hace flooding de requests al gateway. | Gateway | Media | NGINX con `limit_req_zone` (rate limiting) en `/auth/login` y `/api/*`. | ✅ |
| 13 | **E**levation of Privilege | Un operador llama a `/api/comandos` (solo admin). | API | Alta | Dependencia `require_admin` verifica el claim `role` del JWT antes de ejecutar. Retorna 403. | ✅ |
| 14 | **E**levation of Privilege | Un usuario anónimo consulta telemetría. | API | Alta | Dependencia `require_user` exige JWT válido. Sin token → 401. | ✅ |

---

## Priorización (mapa de calor resumido)

**Críticos que YA están mitigados:**
- Autenticación JWT con expiración corta (2, 4, 13, 14).
- TLS en MQTT y HTTPS en el gateway (3, 9).
- Backend no expuesto al exterior (9).
- Secretos fuera del código (10).

**Parciales / pendientes:**
- Sustituir autenticación usuario/password en MQTT por **mTLS** (1).
- Rate limiting más fino en el broker y por cliente (11).
- Implementar refresh tokens y lista de revocación para JWT (2).

---

## Controles transversales

| Control | Dónde se implementa |
|---------|---------------------|
| TLS (MQTT y HTTP) | `config/mosquitto.conf`, `src/gateway/nginx.conf` |
| Autenticación API (JWT) | `src/backend/app/auth.py` |
| Autorización por rol | `src/backend/app/auth.py` (`require_admin`) |
| Validación de entradas | Modelos Pydantic en `src/backend/app/models.py` |
| Segregación de red | `docker-compose.yml` (red `backend-net`) |
| Secretos fuera del código | `.env` + `.gitignore` |
| Auditoría mínima | Tabla `comandos` con usuario y timestamp |
| Exposición mínima | Solo NGINX publica 8443 (dashboard+API); Mosquitto publica 8883 para evidencias |

---

## Qué demostraremos con evidencias

1. `curl` sin token → 401.
2. `curl` con token de operador a `/api/comandos` → 403.
3. `curl` con token de admin a `/api/comandos` → 202.
4. Conexión MQTT intentada **sin credenciales** → rechazada.
5. Captura de handshake TLS del broker.
6. Acceso a `https://localhost:8443` con cert autofirmado (gateway funcionando).
7. Intento de GET al backend directo (`http://localhost:8000`) → rechazado (backend no expuesto).
