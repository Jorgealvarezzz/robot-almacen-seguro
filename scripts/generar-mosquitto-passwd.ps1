# Genera config/passwd con usuario/password hasheado usando mosquitto_passwd.
$ErrorActionPreference = "Stop"

if (-not (Test-Path ".env")) {
    Write-Error "No existe .env. Ejecuta: Copy-Item .env.example .env"
    exit 1
}

$envVars = @{}
Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*([A-Z_]+)=(.*)$') {
        $envVars[$matches[1]] = $matches[2]
    }
}

$user = $envVars["MQTT_USER"]
$pass = $envVars["MQTT_PASSWORD"]

if (-not $user -or -not $pass) {
    Write-Error "MQTT_USER o MQTT_PASSWORD no definidos en .env"
    exit 1
}

Write-Host "Generando config/passwd para usuario '$user'..." -ForegroundColor Cyan

New-Item -ItemType File -Force -Path "config/passwd" | Out-Null

docker run --rm -v "${PWD}/config:/mosquitto/config" eclipse-mosquitto:2 `
    mosquitto_passwd -b /mosquitto/config/passwd $user $pass

if ($LASTEXITCODE -ne 0) {
    Write-Error "Fallo al generar passwd"
    exit 1
}

Write-Host "config/passwd generado" -ForegroundColor Green
Get-Content config/passwd
