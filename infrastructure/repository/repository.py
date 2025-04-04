import os
from typing import Dict
from drone import Drone
from motor.motor_asyncio import AsyncIOMotorClient

class DroneRepository:
    def __init__(self, db_name: str = "drone_db"):
        # TODO: Get Drone Info from DB
        username = os.getenv("DRONE_DB_USERNAME")
        password = os.getenv("DRONE_DB_PASSWORD")
        host = os.getenv("DRONE_DB_HOST")
        port = os.getenv("DRONE_DB_PORT")
        if not all([username, password, host, port]):
            raise ValueError("Database credentials are not set in environment variables")
        
        db_url = f"mongodb://{username}:{password}@{host}:{port}/{db_name}"
        self.client = AsyncIOMotorClient(db_url)
        self.collection = self.client[db_name]["drones"]

    async def get(self, drone_id: str) -> Drone:
        doc = await self.collection.find_one({"drone_id": drone_id})
        if not doc:
            raise ValueError(f"Drone with ID {drone_id} not found")
        return Drone.from_dict(doc)
    
    async def save(self, drone: Drone):
        await self.collection.update_one(
            {"drone_id": drone.drone_id},
            {"$set": drone.to_dict()},
            upsert=True
        )

    