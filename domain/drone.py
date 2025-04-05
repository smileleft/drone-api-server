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

        #logging.info(f"Drone {self.drone_id} initialized with status {self.status.name}")

    def _publish_status(self):
        """
        Publish the current status of the drone to the MQTT status topic.
        """
        status_msg = {
            "drone_id": self.drone_id,
            "dock_id": self.dock_id,
            "status": self.status.value,
            "last_updated": self.last_updated.strftime("%Y-%m-%dT%H:%M:%S")
        }
        self.mqtt_client.publish(self.status_topic, json.dumps(status_msg), qos=1)
        logging.info(f"Drone {self.drone_id} published status: {status_msg}")

    def takeoff(self):
        """
        Set the drone status to flying and publish the status.
        """
        #self.status = DroneStatus.FLYING
        self.status = "flying"
        self.last_updated = datetime.now()
        #logging.info(f"Drone {self.drone_id} took off from dock {self.dock_id}")
        #self._publish_status()
        

    def return_home(self):
        """
        Set the drone status to returning and publish the status.
        """
        self.status = DroneStatus.RETURNING
        self.last_updated = datetime.now()
        #logging.info(f"Drone {self.drone_id} is returning to dock {self.dock_id}")
        #self._publish_status()
        return self.to_dict()

    def land(self, dock_id=None):
        """
        Set the drone status to docked and publish the status.
        """
        self.status = DroneStatus.DOCKED
        self.last_updated = datetime.now()
        self.dock_id = dock_id
        #logging.info(f"Drone {self.drone_id} landed at dock {dock_id}")
        #self._publish_status()
        return self.to_dict()



    @classmethod
    def from_dict(cls, data: dict):
        """
        Create a Drone instance from a dictionary.
        """
        drone_id = data.get("drone_id")
        dock_id = data.get("dock_id")

        # Convert status to DroneStatus or set to UNKNOWN
        status_str = data.get("status", DroneStatus.UNKNOWN.value)
        try:
            status = DroneStatus(status_str.lower())  # Convert string to DroneStatus
        except ValueError:
            raise ValueError(f"Invalid status: {status_str}")

        last_updated = datetime.strptime(data["last_updated"], "%Y-%m-%dT%H:%M:%S")
        
        mqtt_client = data.get("mqtt_client")
        status_topic = data.get("status_topic", "drone/status")

        return cls(
            drone_id=drone_id,
            mqtt_client=mqtt_client,
            status_topic=status_topic,
            dock_id=dock_id,
            status=status
        )
    
    # def to_dict(self):
    #     """
    #     Convert the Drone instance to a dictionary.
    #     """
    #     return {
    #         "drone_id": self.drone_id,
    #         "dock_id": self.dock_id,
    #         "status": self.status,
    #         "last_updated": self.last_updated.strftime("%Y-%m-%dT%H:%M:%S"),
    #     }

    def to_dict(self):
        """
        Convert the Drone instance to a dictionary.
        """
        return {
            "drone_id": self.drone_id,
            "dock_id": self.dock_id,
            "status": self.status.value if isinstance(self.status, DroneStatus) else self.status,
            "last_updated": self.last_updated.strftime("%Y-%m-%dT%H:%M:%S"),
        }