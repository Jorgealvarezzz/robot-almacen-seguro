"""Suscriptor MQTT - recibe telemetria/eventos y persiste en DB."""
import json
import os
import ssl
import threading
import time
from datetime import datetime

import paho.mqtt.client as mqtt

from app.models import SessionLocal, TelemetryORM, EventoORM

MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT_TLS", "8883"))
MQTT_USER = os.getenv("MQTT_USER", "robot")
MQTT_PASS = os.getenv("MQTT_PASSWORD", "robotpass")
CA_CERT = os.getenv("CA_CERT", "/certs/ca.crt")


def _parse_ts(s: str):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return datetime.utcnow()


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"[mqtt-sub] Conectado a {MQTT_HOST}:{MQTT_PORT} (TLS)")
        client.subscribe("robot/+/telemetry", qos=1)
        client.subscribe("robot/+/event", qos=1)
        print("[mqtt-sub] Suscrito a robot/+/telemetry y robot/+/event")
    else:
        print(f"[mqtt-sub] Fallo conexion rc={rc}")


def on_message(client, userdata, msg):
    session = SessionLocal()
    try:
        topic = msg.topic
        data = json.loads(msg.payload.decode())
        if topic.endswith("/telemetry"):
            row = TelemetryORM(
                robot_id=data.get("robot_id", "unknown"),
                ts=_parse_ts(data.get("ts", "")),
                x=float(data.get("x", 0)),
                y=float(data.get("y", 0)),
                battery=float(data.get("battery", 0)),
                status=str(data.get("status", "unknown")),
                obstacle=bool(data.get("obstacle", False)),
            )
            session.add(row)
            session.commit()
        elif topic.endswith("/event"):
            row = EventoORM(
                robot_id=data.get("robot_id", "unknown"),
                ts=_parse_ts(data.get("ts", "")),
                tipo=str(data.get("type", "unknown")),
                payload=json.dumps(data)[:1024],
            )
            session.add(row)
            session.commit()
    except Exception as e:
        print(f"[mqtt-sub] Error procesando mensaje: {e}")
        session.rollback()
    finally:
        session.close()


_client = None


def _run():
    global _client
    _client = mqtt.Client(client_id="backend-subscriber", protocol=mqtt.MQTTv5)
    _client.username_pw_set(MQTT_USER, MQTT_PASS)
    _client.tls_set(ca_certs=CA_CERT, tls_version=ssl.PROTOCOL_TLS_CLIENT)
    _client.tls_insecure_set(True)
    _client.on_connect = on_connect
    _client.on_message = on_message
    _client.reconnect_delay_set(min_delay=1, max_delay=30)

    while True:
        try:
            _client.connect(MQTT_HOST, MQTT_PORT, keepalive=30)
            _client.loop_forever()
        except Exception as e:
            print(f"[mqtt-sub] Error: {e}. Reintentando en 5s...")
            time.sleep(5)


def start_subscriber():
    t = threading.Thread(target=_run, daemon=True)
    t.start()
    print("[mqtt-sub] Hilo suscriptor iniciado")


def publish_command(robot_id: str, cmd: str):
    global _client
    if _client is None:
        raise RuntimeError("MQTT client no iniciado")
    topic = f"robot/{robot_id}/cmd"
    _client.publish(topic, json.dumps({"cmd": cmd}), qos=1)
