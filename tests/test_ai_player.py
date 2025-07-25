import unittest
from cluedo_game.ai_player import AIPlayer
from cluedo_game.cards import SuspectCard, WeaponCard, RoomCard
from cluedo_game.mansion import Mansion
from cluedo_game.solution import Solution

class DummyGame:
    def __init__(self):
        self.mansion = Mansion()
        self.suggestion_history = DummyHistory()
        self.solution = Solution(
            SuspectCard("Miss Scarlett"),
            WeaponCard("Candlestick"),
            RoomCard("Lounge")
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
        char = SuspectCard("Colonel Mustard")
        ai = AIPlayer(char)
        game = DummyGame()
        ai.position = "Dining Room"  # Explicitly set position since it's not set in __init__ anymore
        win = ai.take_turn(game)
        try:
            self.assertIn(ai.position, [r.name for r in game.mansion.get_rooms()])
        except Exception as e:
            self.fail(f"ai.position not in mansion rooms: {e}")
        try:
            self.assertIn("AI", game.output_msgs[0] or "")
        except Exception as e:
            self.fail(f"'AI' not in output_msgs[0]: {e}")
        try:
            self.assertFalse(win or False)  # AI should not win with random suggestion
        except Exception as e:
            self.fail(f"AI won unexpectedly: {e}")

    def test_ai_make_suggestion_structure(self):
        char = SuspectCard("Professor Plum")
        ai = AIPlayer(char)
        class DummyGame2:
            mansion = Mansion()
        suggestion = ai.make_suggestion(DummyGame2())
        try:
            self.assertIn('character', suggestion)
            self.assertIn('weapon', suggestion)
            self.assertIn('room', suggestion)
        except Exception as e:
            self.fail(f"Suggestion missing keys: {e}")
        try:
            self.assertIsInstance(suggestion['character'], SuspectCard)
        except Exception as e:
            self.fail(f"'character' is not a SuspectCard instance: {e}")

if __name__ == "__main__":
    unittest.main()
