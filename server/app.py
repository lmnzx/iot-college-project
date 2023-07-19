import ssl
from fastapi import FastAPI,  WebSocket
import paho.mqtt.client as paho
import os

app = FastAPI()


def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


# Connecting to MQTT Broker
client = paho.Client(client_id="server", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

client.tls_set(tls_version=ssl.PROTOCOL_TLS)

client_name = os.environ.get("NAME", "")
client_password = os.environ.get("PASSWORD", "")
client.username_pw_set(client_name, client_password)

client.connect("3b12b2e9a5504cd797ca6637b4b1a86b.s2.eu.hivemq.cloud", 8883)


client.loop_start()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
