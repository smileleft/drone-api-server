import os
import asyncio
import uuid
from datetime import datetime
import json
from gmqtt import Client as MQTTClient
import logging

# MAP: command → status
COMMAND_STATUS_MAP = {
    "takeoff": "flying",
    "return-home": "returning",
    "land": "docked"
}

# environment variables
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_SUB_TOPIC = os.getenv("MQTT_TOPIC", "drone/commands")
MQTT_PUB_TOPIC = os.getenv("MQTT_TOPIC", "drone/status")

# MQTT client Init
class DroneCommandListener:
    def __init__(self, client_id="drone-command-handler"):
        self.client = MQTTClient(client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    async def connect(self):
        await self.client.connect(MQTT_HOST, MQTT_PORT)

    def on_connect(self, client, flags, rc, properties):
        logging.info(f"Connected to MQTT broker at {MQTT_HOST}:{MQTT_PORT}")
        client.subscribe(MQTT_SUB_TOPIC)

    async def on_message(self, client, topic, payload, qos, properties):
        try:
            message = json.loads(payload)
            logging.info(f"Received message on {topic}: {message}")

            drone_id = message.get("drone_id")
            command = message.get("command")

            if not drone_id or not command:
                logging.error("Invalid payload: missing 'drone_id' or 'command'")
                return

            new_status = COMMAND_STATUS_MAP.get(command)
            if not new_status:
                logging.error(f"Unknown command: {command}")
                return

            status_msg = {
                "tid": str(uuid.uuid4()),
                "timestamp": datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S"),
                "data": {
                    "drone_id": drone_id,
                    "dock_id": None,  # Assuming dock_id is not provided in the command
                    "status": new_status,
                    "last_updated": datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S")
                }
            }

            self.client.publish(MQTT_PUB_TOPIC, json.dumps(status_msg), qos=1)
            logging.info(f"Published new status: {status_msg}")

        except Exception as e:
            logging.error(f"Error processing message: {e}")


async def main():
    handler = DroneCommandListener()
    await handler.connect()

    # Keep the event loop running
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())