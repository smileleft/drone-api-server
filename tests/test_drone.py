import unittest
from datetime import datetime
from domain.drone import Drone, DroneStatus

class TestDrone(unittest.TestCase):
    def setUp(self):
        """
        Set up a test drone object before each test.
        """
        self.drone = Drone(drone_id="drone-123", dock_id="dock-1", status=DroneStatus.IDLE)

    def test_initialization(self):
        """
        Test the initialization of a Drone object.
        """
        self.assertEqual(self.drone.drone_id, "drone-123")
        self.assertEqual(self.drone.dock_id, "dock-1")
        self.assertEqual(self.drone.status, DroneStatus.IDLE)
        self.assertIsInstance(self.drone.last_updated, datetime)

    def test_takeoff(self):
        """
        Test the takeoff method.
        """
        self.drone.takeoff()
        self.assertEqual(self.drone.status, DroneStatus.FLYING)
        self.assertIsInstance(self.drone.last_updated, datetime)

    def test_land(self):
        """
        Test the land method.
        """
        self.drone.land(dock_id="dock-2")
        self.assertEqual(self.drone.status, DroneStatus.DOCKED)
        self.assertEqual(self.drone.dock_id, "dock-2")
        self.assertIsInstance(self.drone.last_updated, datetime)

    def test_return_home(self):
        """
        Test the return_home method.
        """
        self.drone.return_home()
        self.assertEqual(self.drone.status, DroneStatus.RETURNING)
        self.assertIsInstance(self.drone.last_updated, datetime)

    def test_update_status(self):
        """
        Test the update_status method.
        """
        self.drone.update_status(DroneStatus.FLYING)
        self.assertEqual(self.drone.status, DroneStatus.FLYING)
        self.assertIsInstance(self.drone.last_updated, datetime)

    def test_to_dict(self):
        """
        Test the to_dict method.
        """
        drone_dict = self.drone.to_dict()
        self.assertEqual(drone_dict["drone_id"], "drone-123")
        self.assertEqual(drone_dict["dock_id"], "dock-1")
        self.assertEqual(drone_dict["status"], "idle")
        self.assertIsInstance(drone_dict["last_updated"], datetime)

    def test_from_dict(self):
        """
        Test the from_dict class method.
        """
        drone_data = {
            "drone_id": "drone-456",
            "dock_id": "dock-3",
            "status": "flying",
            "last_updated": datetime.now().isoformat()
        }
        drone = Drone.from_dict(drone_data)
        self.assertEqual(drone.drone_id, "drone-456")
        self.assertEqual(drone.dock_id, "dock-3")
        self.assertEqual(drone.status, DroneStatus.FLYING)
        self.assertIsInstance(drone.last_updated, datetime)


if __name__ == "__main__":
    unittest.main()