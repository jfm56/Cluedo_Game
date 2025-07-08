import unittest
from cluedo_game.character import Character, get_characters, get_character_by_name

class TestCharacter(unittest.TestCase):
    def test_characters_exist(self):
        expected_names = [
            "Miss Scarlett",
            "Colonel Mustard",
            "Mrs. White",
            "Reverend Green",
            "Mrs. Peacock",
            "Professor Plum"
        ]
        actual_names = [c.name for c in get_characters()]
        self.assertEqual(set(actual_names), set(expected_names))

    def test_starting_positions(self):
        expected_positions = {
            "Miss Scarlett": "Lounge",
            "Colonel Mustard": "Dining Room",
            "Mrs. White": "Kitchen",
            "Reverend Green": "Conservatory",
            "Mrs. Peacock": "Library",
            "Professor Plum": "Study"
        }
        for name, pos in expected_positions.items():
            character = get_character_by_name(name)
            self.assertIsNotNone(character)
            self.assertEqual(character.position, pos)

    def test_get_character_by_name(self):
        scarlett = get_character_by_name("Miss Scarlett")
        self.assertIsInstance(scarlett, Character)
        self.assertEqual(scarlett.name, "Miss Scarlett")
        self.assertEqual(scarlett.position, "Lounge")
        self.assertIsNone(get_character_by_name("Nonexistent"))

if __name__ == "__main__":
    unittest.main()
