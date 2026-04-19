#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
[ -f .env ] || { echo "Falta .env"; exit 1; }
export $(grep -v '^#' .env | xargs)
: "${MQTT_USER:?}"
: "${MQTT_PASSWORD:?}"
: > config/passwd
docker run --rm -v "$(pwd)/config:/mosquitto/config" eclipse-mosquitto:2 \
    mosquitto_passwd -b /mosquitto/config/passwd "$MQTT_USER" "$MQTT_PASSWORD"
echo "config/passwd generado"
cat config/passwd
