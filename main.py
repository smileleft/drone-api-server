from fastapi import FastAPI, HTTPException , APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
import uvicorn
from drone import DroneStatus
from service import DroneRepository, DroneCommandService
import logging

app = FastAPI()
router = APIRouter()

# repository init
drone_repository = DroneRepository()

# service init
drone_service = DroneCommandService(drone_repository)

# region Response definition
class DroneStatusResponse(BaseModel):
    drone_id: str
    drone_status: DroneStatus

class DroneCommandResponse(BaseModel):
    message: str
# endregion

@router.get("/drones/{drone_id}/status")
async def get_drone_status(drone_id: str):
    
    try:
        result = await drone_service.get_status(drone_id)
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
        result = await drone_service.execute_takeoff(drone_id=drone_id)
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
        result = await drone_service.execute_land(drone_id=drone_id)
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
        result = await drone_service.execute_return_home(drone_id=drone_id)
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
