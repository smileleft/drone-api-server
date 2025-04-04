from datetime import datetime
from drone import Drone, DroneStatus
from repository import DroneRepository
from publisher import Publisher
from subscriber import DroneStatusSubscriber
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
        self.publisher = Publisher()
        self.subscriber = DroneStatusSubscriber()

    async def get_status(self, drone_id: str) -> DroneStatus:
        drone = await self.drone_repository.get(drone_id)
        return drone.status

    async def execute_takeoff(self, drone_id: str):
        # TODO: Make Command and Publish MQTT 
        drone = await self.drone_repository.get(drone_id)
        if not drone:
            raise ValueError(f"Drone with id {drone_id} not found")
        
        #drone.takeoff()
        #await self.drone_repository.save(drone)

        await self.publisher.publish_command(drone_id, "takeoff")
        
        return f"takeoff command sent to Drone {drone_id}"

    async def execute_land(self, drone_id: str):
        # TODO: Make Command and Publish MQTT
        drone = await self.drone_repository.get(drone_id)
        if not drone:
            raise ValueError(f"Drone with id {drone_id} not found")
        
        #drone.land()
        #await self.drone_repository.save(drone)

        await self.publisher.publish_command(drone_id, "land")
        return f"land command sent to Drone {drone_id}"

    async def execute_return_home(self, drone_id: str):
        drone = await self.drone_repository.get(drone_id)
        if not drone:
            raise ValueError(f"Drone with id {drone_id} not found")
        
        #drone.return_home()
        #await self.drone_repository.save(drone)

        await self.publisher.publish_command(drone_id, "return_home")

        return f"return_home command sent to Drone {drone_id}"
    
    async def execute_update_status(self, drone_id: str, status: DroneStatus):
        # TODO: subscribe mqtt topic and update status
        drone = await self.drone_repository.get(drone_id)
        drone.update_status(status)
        await self.drone_repository.save(drone)
        return f"update_status command sent to Drone {drone_id}"
    
    async def execute_update_dock(self, drone_id: str, dock_id: str):
        drone = await self.drone_repository.get(drone_id)
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

