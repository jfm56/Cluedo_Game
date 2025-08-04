"""
Game loop and turn management for the Cluedo game.

This module handles the main game loop and turn management.
"""
import random
from typing import List, Optional, Any, Dict, Tuple, Union

from cluedo_game.player import Player
from cluedo_game.ai import NashAIPlayer
from cluedo_game.cards import Card, SuspectCard, WeaponCard, RoomCard

class GameLoop:
    """Manages the main game loop and turn order."""
    
    def __init__(self, game):
        """
        Initialize the game loop.
        
        Args:
            game: Reference to the main game instance
        """
        self.game = game
        self.turn_counter = 0
    
    def play(self, max_turns: Optional[int] = None) -> bool:
        """
        Main game loop.
        
        Args:
            max_turns: Optional maximum number of turns for testing
            
        Returns:
            bool: True if game completed successfully, False otherwise
        """
        # Initialize play order
        play_order = self._get_play_order()
        if not play_order:
            self.game.ui.show_message("No players in the game. Game over.")
            return False
            
        self.game.ui.show_message("\nGame begins!")
        self.game.print_player_locations()
        
        # Main game loop
        max_iterations = max_turns if max_turns is not None else 100
        current_idx = 0
        
        for _ in range(max_iterations):
            self.turn_counter += 1
            
            # Get current player
            current_player = self._get_next_player(play_order, current_idx)
            if current_player is None:
                self.game.ui.show_message("No active players left! Game over.")
                return False
                
            # Update current index for next turn
            current_idx = (play_order.index(current_player) + 1) % len(play_order)
            
            # Take turn
            game_over = self._handle_player_turn(current_player)
            if game_over:
                return True
                
            # Check for win condition after each turn
            winner = self.game.win_condition_checker.check_win_condition()
            if winner:
                self.game.ui.show_game_over(winner.name)
                return True
                
            # Check if game is over (all players eliminated)
            if self.game.win_condition_checker.check_game_over():
                self.game.ui.show_game_over()
                return True
                
        self.game.ui.show_message(f"\nGame reached maximum turns ({max_iterations}). Game over!")
        return False
    
    def _get_play_order(self) -> List[Player]:
        """Get the play order for the game."""
        if self.game.is_ai_mode() and self.game.player is not None:
            return [self.game.player] + self.game.ai_players
        return self.game.characters
    
    def _get_next_player(self, play_order: List[Player], start_idx: int) -> Optional[Player]:
        """
        Get the next active player in the play order.
        
        Args:
            play_order: List of players in turn order
            start_idx: Index to start searching from
            
        Returns:
            The next active player, or None if no active players
        """
        for i in range(len(play_order)):
            idx = (start_idx + i) % len(play_order)
            player = play_order[idx]
            if not hasattr(player, 'eliminated') or not player.eliminated:
                return player
        return None
    
    def _handle_player_turn(self, player: Player) -> bool:
        """
        Handle a single player's turn.
        
        Args:
            player: The player whose turn it is
            
        Returns:
            bool: True if the game should end after this turn, False otherwise
        """
        self.game.ui.show_player_turn(player.name)
        
        # Skip eliminated players (shouldn't happen, but just in case)
        if hasattr(player, 'eliminated') and player.eliminated:
            self.game.ui.show_message(f"{player.name} is eliminated and cannot take a turn.")
            return False
        
        # Roll dice
        dice_roll = self._roll_dice()
        self.game.ui.show_dice_roll(player.name, dice_roll)
        
        # Handle player movement
        self.game.action_handler.handle_movement(player, dice_roll)
        
        # Handle suggestions/accusations if in a room
        if self._should_make_suggestion(player):
            return self.game.action_handler.handle_suggestion(player)
            
        return False
    
    def _roll_dice(self) -> int:
        """Roll the dice for movement."""
        import random
        return random.randint(1, 6) + random.randint(1, 6)  # 2d6
    
    def _should_make_suggestion(self, player: Player) -> bool:
        """
        Determine if a player should make a suggestion.
        
        Players can only make suggestions when in a room (not in a corridor)
        """
        return not str(player.position).startswith('C')
    
    def get_player_by_name(self, name: str) -> Optional[Player]:
        """
        Get a player by name.
        
        Args:
            name: Name of the player to find
            
        Returns:
            The Player object if found, None otherwise
        """
        for player in self.game.get_all_players():
            if player.name.lower() == name.lower():
                return player
        return None
