import os
import json
from datetime import datetime
from typing import Dict, Any
import uuid
from pydantic import BaseModel
from gmqtt import Client as MQTTClient
from motor.motor_asyncio import AsyncIOMotorClient
import logging
import asyncio

class DroneTopic(BaseModel):
    tid: uuid.UUID
    timestamp: datetime
    data: Dict

mongo_client = AsyncIOMotorClient(os.getenv("DRONE_DB_URL", "mongodb://localhost:27017"))
drone_db = mongo_client["drone_db"]
collection = drone_db["drones"]

class DroneStatusSubscriber:
    def __init__(self, client_id="dorne_status_subscriber"):
        self.broker = os.getenv("MQTT_BROKER", "localhost")
        self.broker_port = int(os.getenv("MQTT_PORT", 1883))
        self.client_id = client_id
        self.topic = os.getenv("MQTT_TOPIC", "drone/status")
        self.client = MQTTClient(client_id=self.client_id)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self._is_connected = False

    async def connect(self):
        """
        Connect to the MQTT broker.
        """
        await self.client.connect(self.broker, self.broker_port)
        logging.info(f"Connected to MQTT broker at {self.broker}:{self.broker_port}")
        await self._is_connected.wait()
        logging.info("Waiting for connection to complete...")
        while not self._is_connected.is_set():
            await asyncio.sleep(0.1)

    def on_connect(self, client, flags, rc, properties):
        logging.info("Connected to MQTT broker")
        self._is_connected = True
        client.subscribe(self.topic, qos=1)
        logging.info(f"Subscribed to topic {self.topic}")

    async def on_message(self, client, topic, payload, qos, properties):
        try:
            payload = json.loads(payload)
            drone_topic = DroneTopic(**payload)
            logging.info(f"Received message: {drone_topic}")
            await self.update_drone_status(drone_topic)
        except Exception as e:
            logging.error(f"Error processing message: {e}")
        
    async def update_drone_status(self, drone_topic: DroneTopic):
        """
        Update the drone status in the database.
        """
        data = drone_topic.data
        drone_id = data.get("drone_id")
        if not drone_id:
            logging.error("Drone ID not found in message")
            return
        
        # Update the drone status in the database
        update_data = {
            "status": data.get("status"),
            "dock_id": data.get("dock_id"),
            "last_updated": drone_topic.timestamp,
        }

        result = await collection.update_one(
            {"drone_id": drone_id},
            {"$set": update_data},
            upsert=False
        )

        if result.matched_count:
            logging.info(f"Updated status for drone {drone_id}")
        else:
            logging.info(f"No drone found with ID {drone_id}")