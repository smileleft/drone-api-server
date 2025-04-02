from drone import Drone, DroneStatus
from typing import Dict
import asyncio
import logging

class DroneRepository:
    def __init__(self):
        # TODO: Get Drone Info from DB
        self._drones: Dict[str, Drone] = {}

    async def get(self, drone_id: str) -> Drone:
        if drone_id not in self._drones:
            self._drones[drone_id] = Drone(drone_id)
        return self._drones[drone_id]


class DroneCommandService:
    def __init__(self, drone_repository: DroneRepository):
        self.drone_repository = drone_repository

    async def get_status(self, drone_id: str) -> DroneStatus:
        drone = await self.drone_repository.get(drone_id)
        return drone.status

    async def execute_takeoff(self, drone_id: str):
        # TODO: Make Command and Publish MQTT
        #logging.info('execute_takeoff start.')
        drone = await self.drone_repository.get(drone_id)
        #logging.info('execute_takeoff completed.')
        drone.takeoff()
        #logging.info('ready to send result')
        return "takeoff command sent"

    async def execute_land(self, drone_id: str):
        # TODO: Make Command and Publish MQTT
        drone = await self.drone_repository.get(drone_id)
        drone.land()
        return "land command sent"

    async def execute_return_home(self, drone_id: str):
        drone = await self.drone_repository.get(drone_id)
        drone.return_home()
        return "return_home command sent"

