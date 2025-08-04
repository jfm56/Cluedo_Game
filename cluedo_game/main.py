"""
Main entry point for the Cluedo game.

This module initializes and starts the game.
"""
import sys
from typing import Callable, Optional

from cluedo_game.game import CluedoGame, GameUI

def main():
    """
    Main entry point for the Cluedo game.
    
    This function initializes the game and starts the main game loop.
    """
    # Set up the game with default input/output functions
    game = CluedoGame(input_func=input, output_func=print, with_ai=True)
    
    # Set up the UI
    ui = GameUI(input_func=input, output_func=print)
    
    try:
        # Start the game
        ui.show_welcome()
        
        # Set up players and deal cards
        game.player_manager.select_character()
        game.player_manager.deal_cards()
        
        # Start the game loop
        game_loop = game.game_loop
        game_over = False
        
        while not game_over:
            # Play a turn
            game_over = game_loop.play()
            
            # Check for win condition
            winner = game.win_condition_checker.check_win_condition()
            if winner:
                ui.show_game_over(winner.name)
                break
            
            # Check if the game is over
            if game.win_condition_checker.check_game_over():
                ui.show_game_over()
                break
                
    except KeyboardInterrupt:
        print("\nGame interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        if hasattr(game, 'logger'):
            game.logger.exception("Game crashed")
        raise

if __name__ == "__main__":
    main()
