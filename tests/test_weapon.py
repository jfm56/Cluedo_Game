import unittest
from cluedo_game.cards import WeaponCard
from cluedo_game.weapon import get_weapons, get_weapon_by_name

class TestWeapon(unittest.TestCase):
    def test_weapons_exist(self):
        actual_names = [w.name for w in get_weapons()]
        try:
            self.assertGreaterEqual(len(actual_names), 6)
        except Exception as e:
            self.fail(f"Weapons existence check failed: {e}")

    def test_get_weapon_by_name(self):
        revolver = get_weapon_by_name("Revolver")
        try:
            self.assertIsInstance(revolver, WeaponCard)
            self.assertEqual(revolver.name, "Revolver")
            self.assertIsNone(get_weapon_by_name("Nonexistent"))
            # Ensure __repr__ is covered for a real weapon
            rep = repr(revolver)
            self.assertIn("Revolver", rep)
        except Exception as e:
            self.fail(f"Get weapon by name check failed: {e}")

    def test_weapon_repr(self):
        weapon = WeaponCard("TestWeapon")
        rep = repr(weapon)
        try:
            self.assertIn("TestWeapon", rep)
        except Exception as e:
            self.fail(f"WeaponCard __repr__ check failed: {e}")

if __name__ == "__main__":
    unittest.main()
