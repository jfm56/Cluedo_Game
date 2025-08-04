"""
Entry point to play the Cluedo game from the terminal with a human player.
"""
import sys
import os

# Add the parent directory to the path to allow imports from cluedo_game package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from cluedo_game.game import CluedoGame
from cluedo_game.game.game_loop import GameLoop
from cluedo_game.cards import get_suspects

def setup_game():
    """Set up the game with one human player and AI opponents."""
    # Create the game instance with AI enabled
    game = CluedoGame(with_ai=True)
    
    # Get all available suspects
    suspects = get_suspects()
    
    # Let the human player choose their character
    print("\n=== Choose Your Character ===")
    for i, suspect in enumerate(suspects, 1):
        print(f"{i}. {suspect.name}")
    
    while True:
        try:
            choice = int(input("\nSelect your character (1-6): ")) - 1
            if 0 <= choice < len(suspects):
                break
            print(f"Please enter a number between 1 and {len(suspects)}")
        except ValueError:
            print("Please enter a valid number.")
    
    # Set up the human player
    human_suspect = suspects[choice]
    game.player = game.player_manager.characters[[c.name for c in game.player_manager.characters].index(human_suspect.name)]
    game.player.is_human = True
    
    # Set up AI players for the remaining characters
    game.ai_players = []
    for suspect in suspects:
        if suspect.name != human_suspect.name:
            ai_player = game.player_manager.characters[[c.name for c in game.player_manager.characters].index(suspect.name)]
            ai_player.is_human = False
            game.ai_players.append(ai_player)
    
    # Deal cards to all players
    game.player_manager.deal_cards()
    
    # Log the setup
    print(f"\nGame set up with {len(game.ai_players)} AI opponents")
    print(f"You are playing as: {game.player.name}")
    
    return game

def main():
    try:
        # Set up the game with human player
        game = setup_game()
        
        # Start the game
        print("\n=== Starting Cluedo Game ===")
        print("Type 'help' during your turn to see available commands.\n")
        
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
