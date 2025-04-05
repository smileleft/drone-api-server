import os
from typing import Dict
from domain.drone import Drone
from motor.motor_asyncio import AsyncIOMotorClient

class DroneRepository:
    def __init__(self, mongo_uri: str):
        
        #username = os.getenv("DRONE_DB_USERNAME")
        #password = os.getenv("DRONE_DB_PASSWORD")
        #host = os.getenv("DRONE_DB_HOST")
        #port = os.getenv("DRONE_DB_PORT")
        #if not all([username, password, host, port]):
        #    raise ValueError("Database credentials are not set in environment variables")
        
        db_name = "drone_db"
        db_url = f"{mongo_uri}"
        
        self.client = AsyncIOMotorClient(db_url)
        self.collection = self.client[db_name]["drones"]

    async def find_by_id(self, drone_id: str) -> Drone:
        doc = await self.collection.find_one({"drone_id": drone_id})
        if not doc:
            raise ValueError(f"Drone with ID {drone_id} not found")
        return Drone.from_dict(doc)
    
    async def save(self, data: Dict):
        await self.collection.update_one(
            {"drone_id": data['drone_id']},
            {"$set": data},
            upsert=True
        )

    async def delete_drone_by_id(self, drone_id: str) -> str:
        result = await self.collection.delete_one({"drone_id": drone_id})
        if result.deleted_count:
            return f"Deleted drone with ID: {drone_id}"
        else:
            return f"No drone found with ID: {drone_id}"
    