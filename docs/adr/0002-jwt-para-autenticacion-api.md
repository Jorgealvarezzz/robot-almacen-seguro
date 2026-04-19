# ADR-0002: JWT para autenticación de la API

**Fecha:** 2026-04-18
**Estado:** Aceptado (para el MVP)
**Contexto:** Proyecto Robot de Almacén Seguro, fase inicial.

## Contexto

La API del backend debe distinguir entre usuarios anónimos, operadores y administradores. Se necesitan decisiones sobre:
- Cómo se autentican los usuarios.
- Cómo se mantiene la sesión.
- Cómo se transportan permisos (rol) en cada request.

Opciones evaluadas:

- **Sesiones con cookies** (server-side).
- **JWT con HMAC (HS256)**.
- **OAuth2 / OIDC con Keycloak** como Identity Provider externo.
- **Basic Auth** con credenciales en cada request.

Restricciones:
- El plazo son 2 días: no hay tiempo de desplegar y configurar Keycloak completo.
- La API es stateless por diseño, detrás de un gateway; queremos que siga siéndolo.
- Debemos poder demostrar controles de seguridad reales, no solo declarativos.

## Decisión

**Usaremos JWT firmado con HS256** para autenticar las llamadas a la API.

- Endpoint `POST /auth/login` recibe `{username, password}` y devuelve `{access_token}`.
- El JWT incluye `sub` (usuario), `role` (admin | operador) y `exp` (30 min).
- Cada endpoint protegido valida firma y expiración antes de ejecutar.
- El secreto vive en `JWT_SECRET`, cargado desde `.env`.
- El frontend guarda el token **en memoria** (no en `localStorage`) para reducir superficie XSS.

## Alternativas consideradas

| Opción | Por qué no |
|--------|------------|
| Sesiones con cookies | Requiere estado server-side y cuidado con CSRF. Mayor complejidad. |
| OAuth2 + Keycloak | La opción **correcta a largo plazo**, pero desproporcionada para 2 días. Se documenta como siguiente paso. |
| Basic Auth | Credenciales en cada request; sin expiración; sin rol embebido. |

## Consecuencias

### Positivas
- **Stateless**: el backend no guarda sesión; cualquier instancia futura puede validar el token.
- **Rol embebido en el token** → autorización se resuelve al validar.
- Fácil de probar y de mostrar evidencia (curl con/sin token, con rol equivocado).
- Consistente con Semana 11 (OAuth2/JWT).

### Negativas / Trade-offs
- **Revocación difícil**: si un token es robado, sigue válido hasta que expire. Mitigado con expiración corta (30 min).
- **Secreto compartido**: HS256 usa un solo secreto; si se filtra, se comprometen todos los tokens. Iteración futura: RS256.
- **Autenticación local**: usuarios hardcodeados en MVP desde `.env`. Se migrará a IdP.

## Camino a futuro
1. Migrar a **Keycloak** (OIDC) como IdP; el backend solo valida tokens emitidos por el IdP.
2. Usar **RS256** (clave asimétrica) para que la validación no requiera compartir secretos.
3. Implementar **refresh tokens** y lista de revocación.
4. Gestión real de usuarios (CRUD admin protegido) fuera del `.env`.

## Controles de seguridad derivados
- Secretos fuera del código (`.env`, ignorado por Git).
- Expiración corta de tokens (30 min).
- TLS obligatorio para que el token no viaje en claro.
- Verificación de rol en endpoints sensibles (`/api/comandos`).
