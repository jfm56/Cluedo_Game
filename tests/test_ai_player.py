import unittest
from cluedo_game.ai_player import AIPlayer
from cluedo_game.character import Character
from cluedo_game.mansion import Mansion
from cluedo_game.weapon import get_weapons
from cluedo_game.solution import Solution
from cluedo_game.game import CluedoGame

class DummyGame:
    def __init__(self):
        self.mansion = Mansion()
        self.suggestion_history = DummyHistory()
        self.solution = Solution(
            Character("Miss Scarlett", "Lounge"),
            get_weapons()[0],
            "Lounge"
        )
        self.output_msgs = []
    def handle_refutation(self, character, weapon, room):
        # Always refute with first card
        return ("AI", "Candlestick")
    def output(self, msg):
        self.output_msgs.append(msg)

class DummyHistory:
    def add(self, *args, **kwargs):
        pass

class TestAIPlayer(unittest.TestCase):
    def test_ai_move_and_suggest(self):
        char = Character("Colonel Mustard", "Dining Room")
        ai = AIPlayer(char)
        game = DummyGame()
        ai.position = "Dining Room"
        win = ai.take_turn(game)
        self.assertIn(ai.position, game.mansion.get_rooms())
        self.assertIn("AI", game.output_msgs[0] or "")
        self.assertFalse(win or False)  # AI should not win with random suggestion

    def test_ai_make_suggestion_structure(self):
        char = Character("Professor Plum", "Study")
        ai = AIPlayer(char)
        class DummyGame2:
            mansion = Mansion()
        suggestion = ai.make_suggestion(DummyGame2())
        self.assertIn('character', suggestion)
        self.assertIn('weapon', suggestion)
        self.assertIn('room', suggestion)
        self.assertIsInstance(suggestion['character'], Character)

if __name__ == "__main__":
    unittest.main()
