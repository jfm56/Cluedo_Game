"""
Entry point to play the Cluedo game from the terminal.
This is an AI-only version where all players are controlled by AI.
"""
import sys
import os
import random

# Add the parent directory to the path to allow imports from cluedo_game package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Import required classes
from cluedo_game.game import CluedoGame
from cluedo_game.game.core import create_solution
from cluedo_game.game.game_loop import GameLoop
from cluedo_game.game.player_management import PlayerManager
from cluedo_game.cards import get_suspects, CHARACTER_STARTING_SPACES

def setup_ai_players(game):
    """Set up AI players for the game."""
    # Get all available suspects
    suspects = get_suspects()
    
    # Initialize the solution before dealing cards
    game.solution = create_solution()
    
    # Randomly select one AI player to be the human player (for compatibility)
    human_suspect = random.choice(suspects)
    game.player = game.player_manager.characters[[c.name for c in game.player_manager.characters].index(human_suspect.name)]
    game.player.is_ai = False
    
    # Set up the rest as AI players
    for suspect in suspects:
        if suspect.name != human_suspect.name:
            ai_player = game.player_manager.characters[[c.name for c in game.player_manager.characters].index(suspect.name)]
            ai_player.is_ai = True
            game.ai_players.append(ai_player)
    
    # Deal cards to all players
    game.player_manager.deal_cards()
    
    # Log the setup
    print(f"Game set up with {len(game.ai_players)} AI players")
    for i, player in enumerate(game.get_all_players()):
        print(f"  Player {i+1}: {player.name} (AI: {hasattr(player, 'is_ai') and player.is_ai})")

def main():
    try:
        # Create the game instance with AI enabled
        game = CluedoGame(with_ai=True)
        
        # Set up AI players
        setup_ai_players(game)
        
        # Create and start the game loop
        game_loop = GameLoop(game)
        game_loop.play()
        
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
