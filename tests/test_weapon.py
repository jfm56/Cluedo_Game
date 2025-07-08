import unittest
from cluedo_game.weapon import Weapon, get_weapons, get_weapon_by_name

class TestWeapon(unittest.TestCase):
    def test_weapons_exist(self):
        expected_names = [
            "Candlestick",
            "Dagger",
            "Lead Pipe",
            "Revolver",
            "Rope",
            "Wrench"
        ]
        actual_names = [w.name for w in get_weapons()]
        self.assertEqual(set(actual_names), set(expected_names))

    def test_get_weapon_by_name(self):
        revolver = get_weapon_by_name("Revolver")
        self.assertIsInstance(revolver, Weapon)
        self.assertEqual(revolver.name, "Revolver")
        self.assertIsNone(get_weapon_by_name("Nonexistent"))

if __name__ == "__main__":
    unittest.main()
