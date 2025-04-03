import os
import json
import asyncio
from gmqtt import Client as MQTTClient

class Publisher:
    def __init__(self):
        self.broker = os.getenv("MQTT_BROKER", "localhost")
        self.broker_port = int(os.getenv("MQTT_PORT", 1883))
        self.client = MQTTClient(client_id="drone_command_publisher")
        self.topic = os.getenv("MQTT_TOPIC", "drone/commands")
        
        self._is_connected = asyncio.Event()
        self.client.on_connect = self.on_connect

    def on_connect(self, client, flags, rc, properties):
        self._is_connected.set()

    async def connect(self):
        await self.client.connect(self.broker, self.broker_port)
        await self._is_connected.wait()

    async def publish_command(self, drone_id: str, command: str):
        payload = json.dumps({
            "drone_id": drone_id,
            "command": command
        })
        await self.client.publish(self.topic, payload, qos=1)