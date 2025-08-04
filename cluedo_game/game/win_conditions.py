"""
Win condition checking for the Cluedo game.

This module handles checking for win/loss conditions.
"""
from typing import List, Optional, Dict, Any, Tuple

from cluedo_game.player import Player

class WinConditionChecker:
    """Handles checking for win/loss conditions in the game."""
    
    def __init__(self, game):
        """
        Initialize the win condition checker.
        
        Args:
            game: Reference to the main game instance
        """
        self.game = game
    
    def check_win_condition(self) -> Optional[Player]:
        """
        Check if the game has been won.
        
        Returns:
            The winning Player if the game is over, None otherwise
        """
        # Check if any player has made a correct accusation
        if hasattr(self.game, 'last_accusation') and self.game.last_accusation:
            player, suspect, weapon, room = self.game.last_accusation
            if (suspect == self.game.solution.character.name and 
                weapon == self.game.solution.weapon.name and 
                room == self.game.solution.room.name):
                return player
        
        # Check if all but one player has been eliminated
        active_players = [p for p in self.game.player_manager.get_all_active_players() 
                         if not p.eliminated]
        if len(active_players) == 1:
            return active_players[0]
            
        return None
    
    def check_elimination(self, player: Player) -> bool:
        """
        Check if a player should be eliminated.
        
        Args:
            player: The player to check
            
        Returns:
            bool: True if the player should be eliminated, False otherwise
        """
        # Check if the player made an incorrect accusation
        if hasattr(self.game, 'last_accusation') and self.game.last_accusation:
            accuser, suspect, weapon, room = self.game.last_accusation
            if accuser == player and not (suspect == self.game.solution.character.name and 
                                        weapon == self.game.solution.weapon.name and 
                                        room == self.game.solution.room.name):
                return True
                
        return False
    
    def check_game_over(self) -> bool:
        """
        Check if the game is over.
        
        Returns:
            bool: True if the game is over, False otherwise
        """
        # Check if any player has won
        if self.check_win_condition() is not None:
            return True
            
        # Check if all players are eliminated
        active_players = [p for p in self.game.player_manager.get_all_active_players() 
                         if not p.eliminated]
        return len(active_players) == 0
