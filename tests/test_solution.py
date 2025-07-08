import unittest
from cluedo_game.solution import select_solution
from cluedo_game.character import get_characters, Character
from cluedo_game.weapon import get_weapons, Weapon
from cluedo_game.mansion import Mansion

class TestSolution(unittest.TestCase):
    def test_select_solution_keys(self):
        solution = select_solution()
        self.assertIn("character", solution)
        self.assertIn("weapon", solution)
        self.assertIn("room", solution)

    def test_solution_types(self):
        solution = select_solution()
        # Character should be an instance of Character
        self.assertIsInstance(solution["character"], Character)
        # Weapon should be an instance of Weapon
        self.assertIsInstance(solution["weapon"], Weapon)
        # Room should be a string and in mansion rooms
        self.assertIsInstance(solution["room"], str)
        self.assertIn(solution["room"], Mansion().get_rooms())

    def test_randomness(self):
        # Run selection multiple times and ensure at least two different solutions
        solutions = set()
        for _ in range(10):
            s = select_solution()
            solutions.add((s["character"].name, s["weapon"].name, s["room"]))
        self.assertGreater(len(solutions), 1)

if __name__ == "__main__":
    unittest.main()
