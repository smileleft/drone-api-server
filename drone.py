from enum import Enum
from datetime import datetime
import logging

class DroneStatus(Enum):
    """
    Enum class to represent the status of a drone.
    """
    UNKNOWN = "unknown"
    IDLE = "idle"
    DOCKED = "docked"
    FLYING = "flying"
    RETURNING = "returning"



class Drone:
    """
    Class to represent a drone.
    """
    def __init__(self, drone_id: str, dock_id=None, status: DroneStatus = DroneStatus.UNKNOWN, last_updated=None):
        """
        Initialize a drone with an ID, dock ID, and status.
        """
        self.drone_id = drone_id
        self.dock_id = dock_id

        #if not isinstance(self.status, DroneStatus):
        #    raise ValueError("Invalid drone status")
        
        self.status = status
        self.last_updated = last_updated if last_updated else datetime.now()
        # Set the last_updated to the current time if not provided
        logging.info(f"Drone {self.drone_id} initialized with status {self.status.name}")


    def takeoff(self):
        """
        Set the drone status to flying.
        """
        self.status = DroneStatus.FLYING
        self.last_updated = datetime.now()
        logging.info(f"Drone {self.drone_id} took off from dock {self.dock_id}")
        
    def land(self, dock_id=None):
        """
        Set the drone status to docked.
        """
        # TODO: dock_id should be given
        self.status = DroneStatus.DOCKED
        self.last_updated = datetime.now()
        self.dock_id = dock_id
        logging.info(f"Drone {self.drone_id} landed at dock {dock_id}")

    def return_home(self):
        """
        Set the drone status to returning.
        """
        self.status = DroneStatus.RETURNING
        self.last_updated = datetime.now()
        logging.info(f"Drone {self.drone_id} is returning to dock {self.dock_id}")

    def update_status(self, status: DroneStatus):
        """
        Update the drone status.
        """
        self.status = status
        self.last_updated = datetime.now()
        logging.info(f"Drone {self.drone_id} status updated to {status.name}")

    def to_dict(self):
        return {
            "drone_id": self.drone_id,
            "dock_id": self.dock_id,
            "status": self.status.name,
            "last_updated": self.last_updated
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a Drone object from a dictionary.
        """
        print(data)
        return cls(
            drone_id = data["drone_id"],
            dock_id = data["dock_id"],
            status = DroneStatus[data["status"].upper()],
            # Convert last_updated to datetime if it's a string
            last_updated = datetime(data.get("last_updated")) if isinstance(data.get("last_updated"), str) else data.get("last_updated")
        )




