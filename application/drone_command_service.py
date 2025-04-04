from datetime import datetime
from domain.drone import Drone, DroneStatus
from infrastructure.repository.drone_repository import DroneRepository
from infrastructure.mqtt_handler import MQTTHandler
from typing import Dict
from pydantic import BaseModel

import logging
import uuid

class DroneTopic(BaseModel):
    tid: uuid.UUID
    timestamp: datetime
    data: Dict


class DroneCommandService:
    def __init__(self, drone_repository: DroneRepository):
        self.drone_repository = drone_repository
        self.subscriber = MQTTHandler()
        self.subscriber.subscribe_to_topics()
        

    async def get_status(self, drone_id: str) -> DroneStatus:
        drone = await self.drone_repository.find_by_id(drone_id)
        return drone.status

    async def execute_takeoff(self, drone_id: str):
        drone = await self.drone_repository.find_by_id(drone_id)
        if not drone:
            raise ValueError(f"Drone with id {drone_id} not found")

        drone.takeoff()
        
        return f"takeoff command sent to Drone {drone_id}"

    async def execute_land(self, drone_id: str):
        # TODO: Make Command and Publish MQTT
        drone = await self.drone_repository.find_by_id(drone_id)
        if not drone:
            raise ValueError(f"Drone with id {drone_id} not found")
        
        drone.land()

        return f"land command sent to Drone {drone_id}"

    async def execute_return_home(self, drone_id: str):
        drone = await self.drone_repository.find_by_id(drone_id)
        if not drone:
            raise ValueError(f"Drone with id {drone_id} not found")
        
        drone.return_home()

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

