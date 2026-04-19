# QUICKSTART — comandos PowerShell de principio a fin

> Asume Windows 10/11 con Docker Desktop + Git for Windows instalados.

## 0. Antes de empezar
- Abre Docker Desktop y espera a que esté corriendo (ícono verde).
- Abre PowerShell (NO como administrador).
- Navega a la carpeta del proyecto:
  ```powershell
  cd C:\ruta\a\robot-almacen-seguro
  ```

## 1. Preparación (solo la primera vez)

```powershell
# Copiar variables de entorno
Copy-Item .env.example .env

# Generar un JWT_SECRET fuerte (opcional pero recomendado)
$secret = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 48 | ForEach-Object {[char]$_})
(Get-Content .env) -replace 'JWT_SECRET=.*', "JWT_SECRET=$secret" | Set-Content .env

# Generar certificados TLS
.\scripts\generar-certs.ps1

# Generar password hasheado para Mosquitto
.\scripts\generar-mosquitto-passwd.ps1
```

## 2. Levantar el sistema

```powershell
docker compose up --build
```

Espera a ver:
- `mosquitto ... Opening ipv4 listen socket on port 8883`
- `backend ... Uvicorn running on http://0.0.0.0:8000`
- `backend ... [mqtt-sub] Conectado a mosquitto:8883 (TLS)`
- `edge ... [edge] Conectado al broker mosquitto:8883 (TLS)`
- `edge ... [edge] TEL pos=... bat=... status=moving`

Déjalo corriendo y abre **otra ventana de PowerShell** para las pruebas.

## 3. Probar desde el navegador

Abre `https://localhost:8443`
- Acepta el warning de cert autofirmado.
- Login como `admin` / `admin123`.
- Verás el dashboard con telemetría en vivo, mapa y tablas.

## 4. Generar evidencias (PowerShell)

```powershell
# Crear carpeta de evidencia si no existe
New-Item -ItemType Directory -Force -Path evidence | Out-Null

# --- Evidencia: salud pública ---
curl.exe -k -s https://localhost:8443/api/health | Out-File -Encoding UTF8 evidence\health.txt

# --- Evidencia: 401 sin token ---
curl.exe -k -s -o evidence\401-sin-token-body.txt -w "HTTP %{http_code}`n" https://localhost:8443/api/telemetry | Out-File -Encoding UTF8 evidence\401-sin-token.txt
Write-Host "Contenido:"
Get-Content evidence\401-sin-token.txt

# --- Evidencia: login admin ---
$resp = curl.exe -k -s -X POST https://localhost:8443/auth/login `
    -H "Content-Type: application/json" `
    -d '{\"username\":\"admin\",\"password\":\"admin123\"}'
$resp | Out-File -Encoding UTF8 evidence\login-admin.json
$adminToken = ($resp | ConvertFrom-Json).access_token
Write-Host "Token admin obtenido (primeros 40 chars):"
Write-Host $adminToken.Substring(0, [Math]::Min(40, $adminToken.Length))

# --- Evidencia: login operador ---
$respOp = curl.exe -k -s -X POST https://localhost:8443/auth/login `
    -H "Content-Type: application/json" `
    -d '{\"username\":\"operador\",\"password\":\"op123\"}'
$opToken = ($respOp | ConvertFrom-Json).access_token

# --- Evidencia: operador NO puede enviar comando (403) ---
curl.exe -k -s -o evidence\403-operador-body.txt -w "HTTP %{http_code}`n" `
    -X POST https://localhost:8443/api/comandos `
    -H "Authorization: Bearer $opToken" `
    -H "Content-Type: application/json" `
    -d '{\"robot_id\":\"rb-01\",\"cmd\":\"STOP\"}' | Out-File -Encoding UTF8 evidence\403-operador.txt
Write-Host "403 operador:"
Get-Content evidence\403-operador.txt

# --- Evidencia: admin SÍ puede (202) ---
curl.exe -k -s -o evidence\202-admin-body.txt -w "HTTP %{http_code}`n" `
    -X POST https://localhost:8443/api/comandos `
    -H "Authorization: Bearer $adminToken" `
    -H "Content-Type: application/json" `
    -d '{\"robot_id\":\"rb-01\",\"cmd\":\"STOP\"}' | Out-File -Encoding UTF8 evidence\202-admin.txt
Write-Host "202 admin:"
Get-Content evidence\202-admin.txt

# --- Evidencia: backend NO expuesto al host ---
curl.exe -s -o evidence\backend-directo-body.txt -w "HTTP %{http_code}`n" --max-time 3 http://localhost:8000/api/health 2>&1 | Out-File -Encoding UTF8 evidence\backend-no-expuesto.txt
Write-Host "Intento directo al backend:"
Get-Content evidence\backend-no-expuesto.txt

# --- Evidencia: telemetría con token válido ---
curl.exe -k -s "https://localhost:8443/api/telemetry?limit=5" `
    -H "Authorization: Bearer $adminToken" | Out-File -Encoding UTF8 evidence\telemetria-ok.json
Write-Host "Ultimas 5 lecturas guardadas en telemetria-ok.json"

# --- Evidencia: logs del edge y backend ---
docker compose logs --tail 30 edge | Out-File -Encoding UTF8 evidence\logs-edge.txt
docker compose logs --tail 30 backend | Out-File -Encoding UTF8 evidence\logs-backend.txt

# --- Evidencia: handshake TLS del broker ---
$openssl = "C:\Program Files\Git\usr\bin\openssl.exe"
if (Test-Path $openssl) {
    & $openssl s_client -connect localhost:8883 -CAfile src\gateway\certs\ca.crt -servername mosquitto < NUL 2> evidence\tls-handshake.log
    Write-Host "TLS handshake guardado"
} else {
    Write-Host "openssl no encontrado; salta este paso"
}

Write-Host ""
Write-Host "=== Evidencias generadas ===" -ForegroundColor Green
Get-ChildItem evidence | Format-Table Name, Length
```

## 5. Hacer screenshots del navegador

Captura y guarda en `evidence/`:

1. **`screenshot-01-login.png`** — pantalla de login.
2. **`screenshot-02-dashboard-admin.png`** — dashboard con datos, logueado como admin.
3. **`screenshot-03-mapa-rastro.png`** — el mapa con el rastro del robot.
4. **`screenshot-04-403-operador.png`** — login como `operador`, clic en un botón de comando, captura el toast 403.
5. **`screenshot-05-202-admin.png`** — login como `admin`, clic en MOVE, captura el toast verde + la nueva fila en "Comandos ejecutados".
6. **`screenshot-06-cert-autofirmado.png`** — clic en el candado del navegador y captura el aviso del cert autofirmado.

## 6. Detener

```powershell
# Ctrl+C en la ventana donde está docker compose up, luego:
docker compose down

# Para borrar también volúmenes (datos):
docker compose down -v
```

## Troubleshooting

**"Cannot connect to the Docker daemon"** → Docker Desktop no está corriendo.

**El edge no conecta al broker** → probablemente el cert de Mosquitto no se generó. Re-ejecuta `.\scripts\generar-certs.ps1`.

**"permission denied" al leer `config/passwd`** → en Windows no debería pasar; si pasa, asegúrate de correr el script de passwd después del de certs.

**El navegador rechaza el cert** → acéptalo como excepción. Es autofirmado. En producción usaríamos Let's Encrypt.

**El backend devuelve 500** → revisa `docker compose logs backend`. Lo más común: el `.env` no existe o `JWT_SECRET` está vacío.

**Puerto 8443 ocupado** → cambia la primera columna del port mapping en `docker-compose.yml`.
