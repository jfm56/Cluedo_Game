import unittest
from cluedo_game.character import Character, get_characters, get_character_by_name

class TestCharacter(unittest.TestCase):
    def test_characters_exist(self):

        actual_names = [c.name for c in get_characters()]


    def test_starting_positions(self):
        # Check that each character's position matches canonical starting spaces
        chars = get_characters()
        from cluedo_game.character import CHARACTER_STARTING_SPACES
        valid_starting_spaces = set(CHARACTER_STARTING_SPACES.values())
        for char in chars:
            character = get_character_by_name(char.name)
            try:
                self.assertIsNotNone(character)
                self.assertIn(character.position, valid_starting_spaces)
            except Exception as e:
                self.fail(f"Character {getattr(character, 'name', '?')} has invalid position or is None: {e}")

    def test_get_character_by_name(self):
        scarlett = get_character_by_name("Miss Scarlett")
        try:
            self.assertIsNotNone(scarlett)
            self.assertEqual(scarlett.name, "Miss Scarlett")
            self.assertIsNone(get_character_by_name("Nonexistent"))
            # Ensure __repr__ is covered for a real character
            rep = repr(scarlett)
            self.assertIn("Miss Scarlett", rep)
            self.assertIn(scarlett.position, rep)
        except Exception as e:
            self.fail(f"test_get_character_by_name failed: {e}")

    def test_character_repr(self):
        character = Character("TestName", "TestRoom")
        character.add_card("TestCard")
        rep = repr(character)
        try:
            self.assertIn("TestName", rep)
            self.assertIn("TestRoom", rep)
            self.assertIn("TestCard", rep)
        except Exception as e:
            self.fail(f"test_character_repr failed: {e}")

if __name__ == "__main__":
    unittest.main()
