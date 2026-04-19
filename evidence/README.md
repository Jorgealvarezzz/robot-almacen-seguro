# Evidencias

Coloca aquí capturas, logs y outputs que demuestran el funcionamiento y los controles de seguridad.

La mayoría de los archivos se generan automáticamente siguiendo los comandos de **[QUICKSTART.md](../QUICKSTART.md) sección 4**.

## Checklist sugerido

| Archivo | Qué debe mostrar |
|---------|------------------|
| `health.txt` | Salud pública del sistema (200 OK). |
| `401-sin-token.txt` | Respuesta 401 al pedir `/api/telemetry` sin Authorization. |
| `login-admin.json` | JWT obtenido con credenciales admin. |
| `403-operador.txt` | Respuesta 403 del operador intentando `POST /api/comandos`. |
| `202-admin.txt` | Respuesta 202 del admin enviando comando exitosamente. |
| `backend-no-expuesto.txt` | Fallo al intentar conectar directo a `http://localhost:8000`. |
| `telemetria-ok.json` | Telemetría consultada con JWT válido. |
| `logs-edge.txt` | Logs del simulador publicando. |
| `logs-backend.txt` | Logs del backend recibiendo y persistiendo. |
| `tls-handshake.log` | Handshake TLS del broker MQTT. |
| `screenshot-01-login.png` | Pantalla de login del dashboard. |
| `screenshot-02-dashboard-admin.png` | Dashboard con datos en vivo (admin). |
| `screenshot-03-mapa-rastro.png` | Mapa con el rastro del robot. |
| `screenshot-04-403-operador.png` | Toast 403 al intentar comando siendo operador. |
| `screenshot-05-202-admin.png` | Toast verde + nueva fila en auditoría (admin). |
| `screenshot-06-cert-autofirmado.png` | Detalle del cert autofirmado del gateway. |

## Mapeo evidencia → control STRIDE

| Amenaza STRIDE | Evidencia que la demuestra mitigada |
|----------------|-------------------------------------|
| Spoofing (usuario) | `login-admin.json` + `401-sin-token.txt` |
| Tampering (canal) | `tls-handshake.log` |
| Repudiation (comandos) | `202-admin.txt` + registro en tabla `comandos` visible en dashboard |
| Information Disclosure (backend expuesto) | `backend-no-expuesto.txt` |
| Elevation of Privilege (rol) | `403-operador.txt` |
| Denial of Service (rate limit) | Se puede demostrar con 10+ requests rápidos a `/auth/login` → NGINX responde 503 |
