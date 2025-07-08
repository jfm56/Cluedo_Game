import unittest
from cluedo_game.cluedo_game import *

class TestCluedoGame(unittest.TestCase):
    def test_game_import(self):
        # Check if the main game module imports without error
        try:
            import cluedo_game.cluedo_game
        except Exception as e:
            self.fail(f"Importing cluedo_game module failed: {e}")

    def test_player_movement(self):
        from cluedo_game.mansion import Mansion
        from cluedo_game.character import get_characters
        mansion = Mansion()
        player = get_characters()[0]  # Miss Scarlett, starts in Lounge
        # Move from Lounge to Hall (valid move)
        self.assertIn("Hall", mansion.get_adjacent_rooms(player.position))
        player.position = "Hall"
        self.assertEqual(player.position, "Hall")
        # Move from Hall to Study (valid move)
        self.assertIn("Study", mansion.get_adjacent_rooms(player.position))
        player.position = "Study"
        self.assertEqual(player.position, "Study")
        # Attempt invalid move (Study to Kitchen)
        self.assertNotIn("Kitchen", mansion.get_adjacent_rooms(player.position))

    def test_make_suggestion(self):
        from cluedo_game.character import get_characters
        from cluedo_game.weapon import get_weapons
        # Simulate a suggestion: character, weapon, room
        characters = get_characters()
        weapons = get_weapons()
        player = characters[0]
        player.position = "Lounge"
        suggested_character = characters[1]  # Colonel Mustard
        suggested_weapon = weapons[2]       # Lead Pipe
        suggested_room = player.position
        # Check suggestion structure
        self.assertEqual(suggested_character.name, "Colonel Mustard")
        self.assertEqual(suggested_weapon.name, "Lead Pipe")
        self.assertEqual(suggested_room, "Lounge")

if __name__ == "__main__":
    unittest.main()
