from fastapi import FastAPI, HTTPException , APIRouter, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
import asyncio
import uvicorn
from domain.drone import DroneStatus, Drone
import logging

import os
from gmqtt import Client as MQTTClient
from infrastructure.mqtt_handler import MQTTHandler
from infrastructure.repository.drone_repository import DroneRepository
import application.drone_command_service as drone_command_service

# MQTT configuration
COMMAND_TOPIC = "drone/command"
STATUS_TOPIC = "drone/status"

# MongoDB configuration
MONGO_URI = "mongodb://hkcho:hkcho1234@localhost:27017/?authSource=drone_db"


# Initialize MQTT client and repository
mqtt_client = MQTTClient("drone-api-server")
repository = DroneRepository(mongo_uri=MONGO_URI)

# Initialize MQTT handler
mqtt_handler = MQTTHandler(mqtt_client, COMMAND_TOPIC, STATUS_TOPIC, repository)


# Initialize DroneCommandService
drone_command_service = drone_command_service.DroneCommandService(drone_repository=repository, mqtt_handler=mqtt_handler)


# region Response definition
class DroneStatusResponse(BaseModel):
    drone_id: str
    drone_status: DroneStatus

class DroneCommandResponse(BaseModel):
    message: str
# endregion

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Start the MQTT client.
    """
    await mqtt_handler.connect()
    #logging.info(f"Connected to MQTT broker at {MQTT_HOST}:{MQTT_PORT}")
    mqtt_handler.subscribe_to_topics()
    
    yield
    #mqtt_client.unsubscribe(COMMAND_TOPIC)
    #logging.info(f"Unsubscribed from topic {COMMAND_TOPIC}")
    await mqtt_client.disconnect()
    logging.info("Disconnected from MQTT broker")
    

app = FastAPI(lifespan=lifespan)
app.title = "Drone Command API"
app.description = "API for controlling drones and retrieving their status."
app.version = "1.0.0"
router = APIRouter()

@router.get("/drones/{drone_id}/status")
async def get_drone_status(drone_id: str):
    
    try:
        result = await drone_command_service.get_status(drone_id)
        return DroneStatusResponse(drone_id=drone_id, drone_status=result)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Request timed out")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/drones/{drone_id}/takeoff")
async def takeoff_drone(drone_id: str):
    
    try:
        logging.info("takeoff start.")
        result = await drone_command_service.execute_takeoff(drone_id=drone_id)
        return DroneCommandResponse(message=result)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Request timed out")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/drones/{drone_id}/land")
async def land_drone(drone_id: str):
    
    try:
        result = await drone_command_service.execute_land(drone_id=drone_id)
        return DroneCommandResponse(message=result)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Request timed out")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/drones/{drone_id}/return-home")
async def return_home(drone_id: str):
    
    try:
        result = await drone_command_service.execute_return_home(drone_id=drone_id)
        return DroneCommandResponse(message=result)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Request timed out")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
