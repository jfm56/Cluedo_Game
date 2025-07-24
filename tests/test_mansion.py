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
        # Kitchen is adjacent to corridors, not directly to Ballroom
        kitchen_adj = self.mansion.get_adjacent_spaces("Kitchen")
        self.assertTrue(any(c.startswith("C") for c in kitchen_adj))
        # Indirect adjacency: Kitchen corridor(s) connect to Ballroom
        ballroom_found = False
        for corridor in kitchen_adj:
            if "Ballroom" in self.mansion.get_adjacent_spaces(corridor):
                ballroom_found = True
                break
        self.assertTrue(ballroom_found, "Ballroom should be reachable from Kitchen via a corridor")
        # No direct adjacency to Dining Room in corridor model
        # self.assertIn("Dining Room", self.mansion.get_adjacent_rooms("Kitchen"))
        self.assertEqual(self.mansion.get_adjacent_rooms("Study"), [])

if __name__ == "__main__":
    unittest.main()
