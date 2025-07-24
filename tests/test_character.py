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
            self.assertIsNotNone(character)
            self.assertIn(character.position, valid_starting_spaces)

    def test_get_character_by_name(self):
        scarlett = get_character_by_name("Miss Scarlett")
        self.assertIsNotNone(scarlett)
        self.assertEqual(scarlett.name, "Miss Scarlett")
        self.assertIsNone(get_character_by_name("Nonexistent"))
        # Ensure __repr__ is covered for a real character
        rep = repr(scarlett)
        self.assertIn("Miss Scarlett", rep)
        self.assertIn(scarlett.position, rep)

    def test_character_repr(self):
        character = Character("TestName", "TestRoom")
        character.add_card("TestCard")
        rep = repr(character)
        self.assertIn("TestName", rep)
        self.assertIn("TestRoom", rep)
        self.assertIn("TestCard", rep)

if __name__ == "__main__":
    unittest.main()
