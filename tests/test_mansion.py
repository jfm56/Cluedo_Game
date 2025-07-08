import unittest
from cluedo_game.mansion import Mansion

class TestMansion(unittest.TestCase):
    def setUp(self):
        self.mansion = Mansion()

    def test_rooms_exist(self):
        expected_rooms = [
            "Kitchen", "Ballroom", "Conservatory", "Dining Room",
            "Billiard Room", "Library", "Lounge", "Hall", "Study"
        ]
        self.assertEqual(set(self.mansion.get_rooms()), set(expected_rooms))

    def test_adjacency(self):
        self.assertIn("Ballroom", self.mansion.get_adjacent_rooms("Kitchen"))
        self.assertIn("Dining Room", self.mansion.get_adjacent_rooms("Kitchen"))
        self.assertEqual(self.mansion.get_adjacent_rooms("Study"), ["Hall", "Library"])

if __name__ == "__main__":
    unittest.main()
