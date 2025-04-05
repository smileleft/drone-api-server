from datetime import datetime
from domain.drone import Drone, DroneStatus
from infrastructure.repository.drone_repository import DroneRepository
from infrastructure.mqtt_handler import MQTTHandler
from typing import Dict
from pydantic import BaseModel
import json

import logging
import uuid

class DroneTopic(BaseModel):
    tid: uuid.UUID
    timestamp: datetime
    data: Dict


class DroneCommandService:
    def __init__(self, drone_repository: DroneRepository, mqtt_handler: MQTTHandler):
        self.drone_repository = drone_repository
        self.subscriber = mqtt_handler
        

    async def connect(self):
        """
        Connect to the MQTT broker.
        """
        await self.subscriber.connect()
        logging.info("Connected to MQTT broker")
        self.subscriber.subscribe_to_topics()
        

    async def get_status(self, drone_id: str) -> DroneStatus:
        drone = await self.drone_repository.find_by_id(drone_id)
        return drone.status

    async def execute_takeoff(self, drone_id: str):
        drone_data = await self.drone_repository.find_by_id(drone_id)
        if not drone_data:
            raise ValueError(f"Drone with id {drone_id} not found")
        # Simulate a drone object
        drone = Drone(drone_id, self.subscriber.mqtt_client, self.subscriber.status_topic)
        if not drone:
            raise ValueError(f"Faied to Simulate Drone object with id {drone_id}")

        drone.takeoff()
        await self.publish_status(drone.to_dict())
        
        return f"takeoff command sent to Drone {drone_id}"

    async def execute_land(self, drone_id: str):
        # TODO: Make Command and Publish MQTT
        drone = await self.drone_repository.find_by_id(drone_id)
        if not drone:
            raise ValueError(f"Drone with id {drone_id} not found")
        
        drone_data = drone.land()
        await self.publish_status(drone_data)

        return f"land command sent to Drone {drone_id}"

    async def execute_return_home(self, drone_id: str):
        drone = await self.drone_repository.find_by_id(drone_id)
        if not drone:
            raise ValueError(f"Drone with id {drone_id} not found")
        
        drone_data = drone.return_home()
        await self.publish_status(drone_data)

        return f"return_home command sent to Drone {drone_id}"
    

    async def execute_update_dock(self, drone_id: str, dock_id: str):
        drone = await self.drone_repository.find_by_id(drone_id)
        if not drone:
            raise ValueError(f"Drone with id {drone_id} not found")
        if not dock_id:
            raise ValueError("Dock ID cannot be empty")
        if drone.dock_id == dock_id:
            raise ValueError(f"Drone {drone_id} is already assigned to dock {dock_id}")
        if drone.status != DroneStatus.DOCKED:
            raise ValueError(f"Drone {drone_id} is not docked and cannot be assigned to a new dock")
        
        # Update the dock ID
        drone.dock_id = dock_id
        await self.drone_repository.save(drone)
        return f"update_dock command sent to Drone {drone_id}"
    

    async def execute_register(self, drone_id: str, dock_id: str):
        drone = Drone(drone_id=drone_id, dock_id=dock_id)
        await self.drone_repository.save(drone)
        return f"Drone {drone_id} registered with dock {dock_id}"


    async def execute_unregister(self, drone_id: str):
        drone = await self.drone_repository.get(drone_id)
        if not drone:
            raise ValueError(f"Drone with id {drone_id} not found")
        
        await self.drone_repository.delete(drone_id)
        return f"Drone {drone_id} unregistered"
    
    async def publish_status(self, drone_data):
        """
        Publish the current status of the drone to the MQTT status topic.
        """
        print(f"drone_data: {drone_data}")
        status = drone_data.get("status")
        print(f"status: {status}")
        status_msg = {
            "drone_id": drone_data['drone_id'],
            "dock_id": drone_data['dock_id'],
            #"status": status.value if isinstance(status, DroneStatus) else DroneStatus.UNKNOWN.value,
            "status": status,
            "last_updated": drone_data.get("last_updated")
        }
        print(f"status_msg: {status_msg}")
        self.subscriber.mqtt_client.publish(self.subscriber.status_topic, json.dumps(status_msg), qos=1)
        #logging.info(f"Drone {drone_data.get('drone_id')} published status: {status_msg})")

