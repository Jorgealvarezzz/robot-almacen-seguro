# Genera certificados TLS autofirmados para gateway NGINX y broker Mosquitto.
$ErrorActionPreference = "Stop"

$certDir = "src/gateway/certs"
New-Item -ItemType Directory -Force -Path $certDir | Out-Null

$opensslExe = "openssl"
try { & $opensslExe version | Out-Null } catch {
    $gitSsl = "C:\Program Files\Git\usr\bin\openssl.exe"
    if (Test-Path $gitSsl) { $opensslExe = $gitSsl; Write-Host "Usando openssl de Git: $gitSsl" }
    else { Write-Error "No se encontro openssl. Instala Git for Windows o agrega openssl al PATH."; exit 1 }
}

Push-Location $certDir

Write-Host "`n1/3 Generando CA..." -ForegroundColor Cyan
& $opensslExe req -x509 -newkey rsa:2048 -nodes -days 365 `
    -keyout ca.key -out ca.crt `
    -subj "/C=MX/ST=Ags/L=Ags/O=RobotAlmacen/CN=RobotAlmacenCA"

Write-Host "`n2/3 Generando cert del gateway (CN=localhost)..." -ForegroundColor Cyan
& $opensslExe req -newkey rsa:2048 -nodes `
    -keyout gateway.key -out gateway.csr `
    -subj "/C=MX/ST=Ags/L=Ags/O=RobotAlmacen/CN=localhost"

@"
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
IP.1 = 127.0.0.1
"@ | Out-File -FilePath "gateway.ext" -Encoding ASCII

& $opensslExe x509 -req -in gateway.csr -CA ca.crt -CAkey ca.key `
    -CAcreateserial -out gateway.crt -days 365 -sha256 -extfile gateway.ext

Write-Host "`n3/3 Generando cert de Mosquitto (CN=mosquitto)..." -ForegroundColor Cyan
& $opensslExe req -newkey rsa:2048 -nodes `
    -keyout mosquitto.key -out mosquitto.csr `
    -subj "/C=MX/ST=Ags/L=Ags/O=RobotAlmacen/CN=mosquitto"

@"
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = mosquitto
DNS.2 = localhost
IP.1 = 127.0.0.1
"@ | Out-File -FilePath "mosquitto.ext" -Encoding ASCII

& $opensslExe x509 -req -in mosquitto.csr -CA ca.crt -CAkey ca.key `
    -CAcreateserial -out mosquitto.crt -days 365 -sha256 -extfile mosquitto.ext

Remove-Item *.csr, *.ext, *.srl -ErrorAction SilentlyContinue

Pop-Location

Write-Host "`nCertificados generados en $certDir" -ForegroundColor Green
Get-ChildItem $certDir | Format-Table Name, Length
