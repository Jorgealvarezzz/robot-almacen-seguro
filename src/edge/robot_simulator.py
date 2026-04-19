"""
Simulador del robot de almacen.
Publica telemetria y eventos al broker MQTT sobre TLS.
"""
import json
import os
import random
import ssl
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT_TLS", "8883"))
MQTT_USER = os.getenv("MQTT_USER", "robot")
MQTT_PASS = os.getenv("MQTT_PASSWORD", "robotpass")
ROBOT_ID = os.getenv("ROBOT_ID", "rb-01")
CA_CERT = os.getenv("CA_CERT", "/certs/ca.crt")

TOPIC_TEL = f"robot/{ROBOT_ID}/telemetry"
TOPIC_EVT = f"robot/{ROBOT_ID}/event"
TOPIC_CMD = f"robot/{ROBOT_ID}/cmd"

state = {"x": 0.0, "y": 0.0, "battery": 100.0, "status": "idle"}


def iso_now():
    return datetime.now(timezone.utc).isoformat()


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"[edge] Conectado al broker {MQTT_HOST}:{MQTT_PORT} (TLS)")
        client.subscribe(TOPIC_CMD, qos=1)
        print(f"[edge] Suscrito a {TOPIC_CMD}")
    else:
        print(f"[edge] Fallo conexion rc={rc}")


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        cmd = payload.get("cmd")
        print(f"[edge] Comando recibido: {cmd}")
        if cmd == "STOP":
            state["status"] = "idle"
        elif cmd == "CHARGE":
            state["status"] = "charging"
        elif cmd == "MOVE":
            state["status"] = "moving"
        ack = {
            "ts": iso_now(),
            "robot_id": ROBOT_ID,
            "type": "cmd_ack",
            "cmd": cmd,
            "result": "ok",
        }
        client.publish(TOPIC_EVT, json.dumps(ack), qos=1)
    except Exception as e:
        print(f"[edge] Error procesando comando: {e}")


def tick():
    if state["status"] == "moving":
        state["x"] += random.uniform(-0.5, 0.5)
        state["y"] += random.uniform(-0.5, 0.5)
        state["battery"] -= random.uniform(0.05, 0.15)
    elif state["status"] == "charging":
        state["battery"] = min(100.0, state["battery"] + 0.5)
        if state["battery"] >= 100.0:
            state["status"] = "idle"
    else:
        state["battery"] -= random.uniform(0.0, 0.02)

    if state["battery"] < 20 and state["status"] != "charging":
        state["status"] = "charging"

    obstacle = random.random() < 0.05

    return {
        "ts": iso_now(),
        "robot_id": ROBOT_ID,
        "x": round(state["x"], 2),
        "y": round(state["y"], 2),
        "battery": round(state["battery"], 2),
        "status": state["status"],
        "obstacle": obstacle,
    }


def main():
    client = mqtt.Client(client_id=f"edge-{ROBOT_ID}", protocol=mqtt.MQTTv5)
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.tls_set(ca_certs=CA_CERT, tls_version=ssl.PROTOCOL_TLS_CLIENT)
    client.tls_insecure_set(True)
    client.on_connect = on_connect
    client.on_message = on_message
    client.reconnect_delay_set(min_delay=1, max_delay=30)

    print(f"[edge] Iniciando simulador. Robot={ROBOT_ID}")
    state["status"] = "moving"

    while True:
        try:
            client.connect(MQTT_HOST, MQTT_PORT, keepalive=30)
            client.loop_start()
            while True:
                data = tick()
                client.publish(TOPIC_TEL, json.dumps(data), qos=1)
                if data["obstacle"]:
                    evt = {
                        "ts": data["ts"],
                        "robot_id": ROBOT_ID,
                        "type": "obstacle_detected",
                        "pos": {"x": data["x"], "y": data["y"]},
                    }
                    client.publish(TOPIC_EVT, json.dumps(evt), qos=1)
                    print(f"[edge] Evento: obstaculo en ({data['x']},{data['y']})")
                print(
                    f"[edge] TEL pos=({data['x']},{data['y']}) "
                    f"bat={data['battery']}% status={data['status']}"
                )
                time.sleep(2)
        except Exception as e:
            print(f"[edge] Error: {e}. Reintentando en 5s...")
            try:
                client.loop_stop()
            except Exception:
                pass
            time.sleep(5)


if __name__ == "__main__":
    main()
