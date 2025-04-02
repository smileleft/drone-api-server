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
    def __init__(self, drone_id: str, dock_id=None):
        """
        Initialize a drone with an ID, dock ID, and status.
        """
        self.drone_id = drone_id
        self.dock_id = dock_id
        self.status = DroneStatus.UNKNOWN
        self.last_updated = datetime.now()


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

    


