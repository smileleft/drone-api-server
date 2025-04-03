from drone import Drone, DroneStatus
from repository import DroneRepository
from typing import Dict


class DroneCommandService:
    def __init__(self, drone_repository: DroneRepository):
        self.drone_repository = drone_repository

    async def get_status(self, drone_id: str) -> DroneStatus:
        drone = await self.drone_repository.get(drone_id)
        return drone.status

    async def execute_takeoff(self, drone_id: str):
        # TODO: Make Command and Publish MQTT 
        drone = await self.drone_repository.get(drone_id)
        drone.takeoff()
        await self.drone_repository.save(drone)
        return f"takeoff command sent to Drone {drone_id}"

    async def execute_land(self, drone_id: str):
        # TODO: Make Command and Publish MQTT
        drone = await self.drone_repository.get(drone_id)
        drone.land()
        await self.drone_repository.save(drone)
        return f"land command sent to Drone {drone_id}"

    async def execute_return_home(self, drone_id: str):
        drone = await self.drone_repository.get(drone_id)
        drone.return_home()
        await self.drone_repository.save(drone)
        return f"return_home command sent to Drone {drone_id}"
    
    async def execute_update_status(self, drone_id: str, status: DroneStatus):
        drone = await self.drone_repository.get(drone_id)
        drone.update_status(status)
        await self.drone_repository.save(drone)
        return f"update_status command sent to Drone {drone_id}"
    
    async def execute_update_dock(self, drone_id: str, dock_id: str):
        drone = await self.drone_repository.get(drone_id)
        drone.dock_id = dock_id
        await self.drone_repository.save(drone)
        return f"update_dock command sent to Drone {drone_id}"

