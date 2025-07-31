"""
Minimal test file to isolate the test environment issue.
"""
import pytest
from cluedo_game.game import CluedoGame

def test_minimal():
    """A minimal test to verify the test environment."""
    # Create a game instance with minimal setup
    game = CluedoGame(input_func=lambda x: "1", output_func=print)
    assert game is not None
    assert game.with_ai is False
    print("Minimal test completed successfully")
