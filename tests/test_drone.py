import unittest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from domain.drone import Drone, DroneStatus
import asyncio

class TestDrone(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        """
        Set up a test drone object before each test.
        """
        # Mock MQTTClient
        mqtt_client = MagicMock()
        mqtt_client.connect = AsyncMock(return_value=None)  # Mock connect method
        mqtt_client.publish = AsyncMock(return_value=None)  # Mock publish method

        # Initialize Drone with mocked MQTT client
        self.drone = asyncio.run(self._initialize_drone(mqtt_client))

    async def _initialize_drone(self, mqtt_client):
        """
        Helper method to initialize the drone asynchronously.
        """
        return Drone(
            drone_id="drone-123",
            mqtt_client=mqtt_client,
            status_topic="drone/status",
            dock_id="dock-1",
            status=DroneStatus.IDLE
        )

    async def test_initialization(self):
        """
        Test the initialization of a Drone object.
        """
        self.assertEqual(self.drone.drone_id, "drone-123")
        self.assertEqual(self.drone.dock_id, "dock-1")
        self.assertEqual(self.drone.status, DroneStatus.IDLE)
        self.assertIsInstance(self.drone.last_updated, datetime)

    async def test_takeoff(self):
        """
        Test the takeoff method.
        """
        self.drone.takeoff()
        self.assertEqual(self.drone.status, DroneStatus.FLYING)
        self.assertIsInstance(self.drone.last_updated, datetime)

    async def test_land(self):
        """
        Test the land method.
        """
        self.drone.land(dock_id="dock-2")
        self.assertEqual(self.drone.status, DroneStatus.DOCKED)
        self.assertEqual(self.drone.dock_id, "dock-2")
        self.assertIsInstance(self.drone.last_updated, datetime)

    async def test_return_home(self):
        """
        Test the return_home method.
        """
        self.drone.return_home()
        self.assertEqual(self.drone.status, DroneStatus.RETURNING)
        self.assertIsInstance(self.drone.last_updated, datetime)

    async def test_from_dict(self):
        """
        Test the from_dict class method.
        """
        drone_data = {
            "drone_id": "drone-456",
            "dock_id": "dock-3",
            "status": "flying",
            "last_updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }
        drone = Drone.from_dict(drone_data)
        self.assertEqual(drone.drone_id, "drone-456")
        self.assertEqual(drone.dock_id, "dock-3")
        self.assertEqual(drone.status, DroneStatus.FLYING)
        self.assertIsInstance(drone.last_updated, datetime)


if __name__ == "__main__":
    unittest.main()