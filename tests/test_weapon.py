import unittest
from cluedo_game.weapon import Weapon, get_weapons, get_weapon_by_name

class TestWeapon(unittest.TestCase):
    def test_weapons_exist(self):
        actual_names = [w.name for w in get_weapons()]
        self.assertGreaterEqual(len(actual_names), 6)

    def test_get_weapon_by_name(self):
        revolver = get_weapon_by_name("Revolver")
        self.assertIsInstance(revolver, Weapon)
        self.assertEqual(revolver.name, "Revolver")
        self.assertIsNone(get_weapon_by_name("Nonexistent"))
        # Ensure __repr__ is covered for a real weapon
        rep = repr(revolver)
        self.assertIn("Revolver", rep)

    def test_weapon_repr(self):
        weapon = Weapon("TestWeapon")
        rep = repr(weapon)
        self.assertIn("TestWeapon", rep)

if __name__ == "__main__":
    unittest.main()
