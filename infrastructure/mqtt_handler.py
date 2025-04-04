import json
import logging
from domain.drone import Drone, DroneStatus
from infrastructure.repository.drone_repository import DroneRepository


class MQTTHandler:
    def __init__(self, mqtt_client, command_topic, status_topic, repository: DroneRepository):
        self.mqtt_client = mqtt_client
        self.command_topic = command_topic
        self.status_topic = status_topic
        self.repository = repository

        self.mqtt_client.on_message = self.on_message

    def subscribe_to_topics(self):
        """
        Subscribe to the command and status topics.
        """
        self.mqtt_client.subscribe(self.command_topic)
        self.mqtt_client.subscribe(self.status_topic)
        logging.info(f"Subscribed to topics: {self.command_topic}, {self.status_topic}")

    async def on_message(self, client, topic, payload, qos, properties):
        """
        Handle incoming MQTT messages.
        """
        try:
            message = json.loads(payload)
            logging.info(f"Received message on {topic}: {message}")

            if topic == self.command_topic:
                # Handle command messages
                drone_id = message.get("drone_id")
                command = message.get("command")

                if not drone_id or not command:
                    logging.error("Invalid command payload: missing 'drone_id' or 'command'")
                    return

                # Simulate a drone object
                drone = Drone(drone_id, self.mqtt_client, self.status_topic)
                if command == "takeoff":
                    drone.takeoff()
                elif command == "land":
                    drone.land(dock_id=message.get("dock_id"))
                elif command == "return-home":
                    drone.return_home()
                else:
                    logging.error(f"Unknown command: {command}")

            elif topic == self.status_topic:
                # Handle status messages
                drone_data = message

                # Save the drone status to the database

                # validate the payload
                if not drone_data.get("drone_id"):
                    logging.error("Invalid status payload: missing 'drone_id'")
                    return
                if not drone_data.get("status"):
                    logging.error("Invalid status payload: missing 'status'")
                    return
                self.repository.save(Drone.from_dict(drone_data))
                logging.info(f"Drone status saved to database: {drone_data}")

        except Exception as e:
            logging.error(f"Error processing message: {e}")