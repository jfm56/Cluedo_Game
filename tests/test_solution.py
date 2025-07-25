import unittest
from cluedo_game.cards import SuspectCard, WeaponCard, RoomCard
from cluedo_game.mansion import Mansion
from cluedo_game.solution import Solution

class TestSolution(unittest.TestCase):
    def test_Solution_random_solution_keys(self):
        solution = Solution.random_solution()
        try:
            self.assertTrue(hasattr(solution, "character"))
            self.assertTrue(hasattr(solution, "weapon"))
            self.assertTrue(hasattr(solution, "room"))
        except Exception as e:
            self.fail(f"Solution random_solution keys check failed: {e}")

    def test_solution_types(self):
        solution = Solution.random_solution()
        # Character should be an instance of SuspectCard
        try:
            self.assertIsInstance(solution.character, SuspectCard)
            self.assertIsInstance(solution.weapon, WeaponCard)
            self.assertIsInstance(solution.room, RoomCard)
            self.assertTrue(hasattr(solution.room, 'name'))
            self.assertIn(solution.room.name, [room.name for room in Mansion().get_rooms()])
        except Exception as e:
            self.fail(f"Solution type and room check failed: {e}")

    def test_randomness(self):
        # Run selection multiple times and ensure at least two different solutions
        solutions = set()
        for _ in range(10):
            s = Solution.random_solution()
            solutions.add((s.character.name, s.weapon.name, s.room.name))
        try:
            self.assertGreater(len(solutions), 1)
        except Exception as e:
            self.fail(f"Solution randomness check failed: {e}")

if __name__ == "__main__":
    unittest.main()
