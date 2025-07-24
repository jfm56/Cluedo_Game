import unittest
from cluedo_game.character import get_characters, Character
from cluedo_game.weapon import get_weapons, Weapon
from cluedo_game.mansion import Mansion
from cluedo_game.solution import Solution

class TestSolution(unittest.TestCase):
    def test_Solution_random_solution_keys(self):
        solution = Solution.random_solution()
        self.assertTrue(hasattr(solution, "character"))
        self.assertTrue(hasattr(solution, "weapon"))
        self.assertTrue(hasattr(solution, "room"))

    def test_solution_types(self):
        solution = Solution.random_solution()
        # Character should be an instance of Character
        self.assertIsInstance(solution.character, Character)
        # Weapon should be an instance of Weapon
        self.assertIsInstance(solution.weapon, Weapon)
        # Room should be a string and in mansion rooms
        self.assertTrue(hasattr(solution.room, 'name'))
        self.assertIn(solution.room.name, [room.name for room in Mansion().get_rooms()])

    def test_randomness(self):
        # Run selection multiple times and ensure at least two different solutions
        solutions = set()
        for _ in range(10):
            s = Solution.random_solution()
            solutions.add((s.character.name, s.weapon.name, s.room))
        self.assertGreater(len(solutions), 1)

if __name__ == "__main__":
    unittest.main()
