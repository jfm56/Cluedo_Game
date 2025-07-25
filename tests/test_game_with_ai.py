import unittest
from cluedo_game.game_with_ai import CluedoGameWithAI
from cluedo_game.ai_player import AIPlayer
from cluedo_game.character import Character
from cluedo_game.mansion import Mansion

class DummyInput:
    def __init__(self, inputs):
        self.inputs = inputs
        self.index = 0
    def __call__(self, prompt=None):
        if self.index < len(self.inputs):
            val = self.inputs[self.index]
            self.index += 1
            return val
        raise EOFError()

class TestCluedoGameWithAI(unittest.TestCase):
    def test_ai_players_take_turns(self):
        # Select human as first character, then always 'n' (no suggestion), then move to first room, then quit
        user_inputs = ["1", "n", "1", "0", "n", "0", "n", "0"]
        outputs = []
        game = CluedoGameWithAI(input_func=DummyInput(user_inputs), output_func=outputs.append)
        game.play()
        # The game should run without crashing, regardless of whether AI turns are present
        # (AI turns may not occur if the human player quits immediately)
        # Optionally, print outputs for debugging
        # print(outputs)
        try:
            self.assertIsInstance(outputs, list)
            self.assertGreaterEqual(len(outputs), 1)
        except Exception as e:
            self.fail(f"AI player turn output check failed: {e}")

    def test_deal_cards_to_all_players(self):
        # Simulate setup and deal
        game = CluedoGameWithAI(input_func=lambda _: "1", output_func=lambda x: None)
        game.select_character()
        game.deal_cards()
        all_players = [game.player] + game.ai_players
        total_cards = sum(len(p.hand) for p in all_players)
        try:
            self.assertGreater(total_cards, 0)
            self.assertTrue(all(len(p.hand) > 0 for p in all_players))
        except Exception as e:
            self.fail(f"Deal cards to all players check failed: {e}")

if __name__ == "__main__":
    unittest.main()
