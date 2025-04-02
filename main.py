from fastapi import FastAPI, HTTPException , APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
import uvicorn

app = FastAPI()
router = APIRouter()

@router.get("/drones/{drone_id}/status")
async def get_drone_status(drone_id: str):
    """
    Simulate an asynchronous function to get the drone status.
    """
    await asyncio.sleep(1)  # Simulate a network delay
    return {"drone_id": drone_id, "status": "flying"}


@router.post("/drones/{drone_id}/takeoff")
async def takeoff_drone(drone_id: str):
    """
    Simulate an asynchronous function to take off a drone.
    """
    await asyncio.sleep(1)  # Simulate a network delay
    return {"drone_id": drone_id, "status": "flying"}


@router.post("/drones/{drone_id}/land")
async def land_drone(drone_id: str):
    """
    Simulate an asynchronous function to land a drone.
    """
    await asyncio.sleep(1)  # Simulate a network delay
    return {"drone_id": drone_id, "status": "docked"}


@router.post("/drones/{drone_id}/return-home")
async def return_home(drone_id: str):
    """
    Simulate an asynchronous function to return a drone home.
    """
    await asyncio.sleep(1)  # Simulate a network delay
    return {"drone_id": drone_id, "status": "returning"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
