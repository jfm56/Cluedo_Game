import unittest
from cluedo_game.game import CluedoGame
from io import StringIO

class TestCluedoGameIntegration(unittest.TestCase):
    def setUp(self):
        self.inputs = []
        self.outputs = []

    def fake_input(self, prompt=""):
        self.outputs.append(prompt)
        if self.inputs:
            return self.inputs.pop(0)
        raise EOFError()

    def fake_output(self, msg):
        self.outputs.append(msg)

    def test_character_selection_and_quit(self):
        # Select first character, then quit at move phase
        self.inputs = ["1", "n", "0"]  # select char, skip suggestion, quit
        game = CluedoGame(input_func=self.fake_input, output_func=self.fake_output)
        game.play()
        # Check that the welcome message, character selection, and quit message appear
        output_str = "\n".join(self.outputs)
        self.assertIn("Welcome to Cluedo!", output_str)
        self.assertIn("Select your character:", output_str)
        self.assertIn("Thanks for playing!", output_str)

    def test_invalid_character_selection(self):
        # Invalid then valid selection
        self.inputs = ["x", "100", "1", "n", "0"]
        game = CluedoGame(input_func=self.fake_input, output_func=self.fake_output)
        game.play()
        output_str = "\n".join(self.outputs)
        self.assertIn("Please enter a valid number.", output_str)
        self.assertIn("Invalid selection.", output_str)
        self.assertIn("You are", output_str)

    # Removed: test_history_command_and_out_of_guesses (out-of-guesses logic no longer applies with unlimited suggestions)

    def test_suggestion_and_win(self):
        # Force the solution to match the first suspect/weapon/room
        self.inputs = ["1", "y", "1", "1", "0"]  # select char, suggest, pick first suspect/weapon, then quit after win
        game = CluedoGame(input_func=self.fake_input, output_func=self.fake_output)
        # Patch solution to match the first options
        first_char = game.characters[0]
        from cluedo_game.weapon import get_weapons
        first_weapon = get_weapons()[0]
        game.solution.character = first_char
        game.solution.weapon = first_weapon
        game.solution.room = first_char.position
        game.play()
        output_str = "\n".join(self.outputs)
        self.assertIn("Congratulations! You Win!", output_str)
        self.assertIn("The solution was:", output_str)

if __name__ == "__main__":
    unittest.main()
