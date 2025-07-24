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
        self.assertEqual(set(r.name if hasattr(r, 'name') else r for r in self.mansion.get_rooms()), set(expected_rooms))

    def test_adjacency(self):
        # Kitchen is adjacent to corridors, not directly to Ballroom
        kitchen = next(r for r in self.mansion.get_rooms() if r.name == "Kitchen")
        ballroom = next(r for r in self.mansion.get_rooms() if r.name == "Ballroom")
        study = next(r for r in self.mansion.get_rooms() if r.name == "Study")
        kitchen_adj = self.mansion.get_adjacent_spaces(kitchen)
        self.assertTrue(any(str(c).startswith("C") or (hasattr(c, 'name') and c.name.startswith("C")) for c in kitchen_adj))
        # Indirect adjacency: Kitchen should be able to reach Ballroom via corridors (multi-step)
        def bfs(start, goal):
            visited = set()
            queue = [start]
            def node_id(node):
                return node.name if hasattr(node, 'name') else str(node)
            goal_id = node_id(goal)
            while queue:
                current = queue.pop(0)
                curr_id = node_id(current)
                if curr_id == goal_id:
                    return True
                visited.add(curr_id)
                for neighbor in self.mansion.get_adjacent_spaces(current):
                    neigh_id = node_id(neighbor)
                    if neigh_id not in visited:
                        queue.append(neighbor)
            return False
        self.assertTrue(bfs(kitchen, ballroom), "Ballroom should be reachable from Kitchen via corridors")
        # No direct adjacency to Dining Room in corridor model
        # self.assertIn("Dining Room", self.mansion.get_adjacent_rooms(kitchen))
        self.assertEqual(self.mansion.get_adjacent_rooms(study), [])

if __name__ == "__main__":
    unittest.main()
