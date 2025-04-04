from enum import Enum
from datetime import datetime
import logging
import json
from gmqtt import Client as MQTTClient


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
    def __init__(self, drone_id: str, mqtt_client: MQTTClient, status_topic: str, dock_id=None, status: DroneStatus = DroneStatus.UNKNOWN):
        """
        Initialize a drone with an ID, dock ID, and status.
        """
        self.drone_id = drone_id
        self.dock_id = dock_id
        self.status = status
        self.last_updated = datetime.now()
        self.mqtt_client = mqtt_client
        self.status_topic = status_topic

        logging.info(f"Drone {self.drone_id} initialized with status {self.status.name}")

    def _publish_status(self):
        """
        Publish the current status of the drone to the MQTT status topic.
        """
        status_msg = {
            "drone_id": self.drone_id,
            "dock_id": self.dock_id,
            "status": self.status.name,
            "last_updated": self.last_updated.strftime("%Y-%m-%dT%H:%M:%S")
        }
        self.mqtt_client.publish(self.status_topic, json.dumps(status_msg), qos=1)
        logging.info(f"Drone {self.drone_id} published status: {status_msg}")

    def takeoff(self):
        """
        Set the drone status to flying and publish the status.
        """
        self.status = DroneStatus.FLYING
        self.last_updated = datetime.now()
        logging.info(f"Drone {self.drone_id} took off from dock {self.dock_id}")
        self._publish_status()

    def land(self, dock_id=None):
        """
        Set the drone status to docked and publish the status.
        """
        self.status = DroneStatus.DOCKED
        self.last_updated = datetime.now()
        self.dock_id = dock_id
        logging.info(f"Drone {self.drone_id} landed at dock {dock_id}")
        self._publish_status()

    def return_home(self):
        """
        Set the drone status to returning and publish the status.
        """
        self.status = DroneStatus.RETURNING
        self.last_updated = datetime.now()
        logging.info(f"Drone {self.drone_id} is returning to dock {self.dock_id}")
        self._publish_status()