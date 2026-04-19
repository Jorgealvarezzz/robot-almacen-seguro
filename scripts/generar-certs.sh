#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
CERT_DIR="src/gateway/certs"
mkdir -p "$CERT_DIR"
cd "$CERT_DIR"

echo "1/3 Generando CA..."
openssl req -x509 -newkey rsa:2048 -nodes -days 365 \
    -keyout ca.key -out ca.crt \
    -subj "/C=MX/ST=Ags/L=Ags/O=RobotAlmacen/CN=RobotAlmacenCA"

echo "2/3 Generando cert del gateway..."
openssl req -newkey rsa:2048 -nodes \
    -keyout gateway.key -out gateway.csr \
    -subj "/C=MX/ST=Ags/L=Ags/O=RobotAlmacen/CN=localhost"

cat > gateway.ext <<EOT
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
IP.1 = 127.0.0.1
EOT

openssl x509 -req -in gateway.csr -CA ca.crt -CAkey ca.key \
    -CAcreateserial -out gateway.crt -days 365 -sha256 -extfile gateway.ext

echo "3/3 Generando cert de Mosquitto..."
openssl req -newkey rsa:2048 -nodes \
    -keyout mosquitto.key -out mosquitto.csr \
    -subj "/C=MX/ST=Ags/L=Ags/O=RobotAlmacen/CN=mosquitto"

cat > mosquitto.ext <<EOT
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = mosquitto
DNS.2 = localhost
IP.1 = 127.0.0.1
EOT

openssl x509 -req -in mosquitto.csr -CA ca.crt -CAkey ca.key \
    -CAcreateserial -out mosquitto.crt -days 365 -sha256 -extfile mosquitto.ext

rm -f *.csr *.ext *.srl
ls -la
echo "Certificados generados."
