"""
AI controller for the Cluedo game.

This module handles AI player behavior and decision making.
"""
import random
from typing import List, Optional, Dict, Any, Tuple

from cluedo_game.ai import NashAIPlayer
from cluedo_game.player import Player
from cluedo_game.cards import Card, SuspectCard, WeaponCard, RoomCard

class AIController:
    """Manages AI players and their decision making."""
    
    def __init__(self, game):
        """
        Initialize the AI controller.
        
        Args:
            game: Reference to the main game instance
        """
        self.game = game
    
    def get_ai_move(self, ai_player: NashAIPlayer, steps: int) -> str:
        """
        Get the AI's chosen move.
        
        Args:
            ai_player: The AI player making the move
            steps: Number of steps available
            
        Returns:
            The chosen destination
        """
        # Get available moves
        destinations = self.game.movement.get_destinations_from(ai_player.position, steps)
        
        if not destinations:
            return ai_player.position  # Stay in place if no valid moves
        
        # Simple AI: prefer rooms over corridors
        room_destinations = [d for d in destinations if not str(d).startswith('C')]
        
        if room_destinations:
            # Choose a random room
            return random.choice(room_destinations)
        else:
            # Choose a random corridor
            return random.choice(destinations)
    
    def get_ai_suggestion(self, ai_player: NashAIPlayer) -> Tuple[str, str, str]:
        """
        Get the AI's suggestion.
        
        Args:
            ai_player: The AI player making the suggestion
            
        Returns:
            Tuple of (suspect, weapon, room)
        """
        # Simple AI: suggest a random combination
        suspects = [s.name for s in self.game.player_manager.characters]
        weapons = [w.name for w in self.game.weapons]
        
        # The room is the current room
        room = str(ai_player.position)
        
        return random.choice(suspects), random.choice(weapons), room
    
    def get_ai_accusation(self, ai_player: NashAIPlayer) -> Optional[Tuple[str, str, str]]:
        """
        Get the AI's accusation, if any.
        
        Args:
            ai_player: The AI player making the accusation
            
        Returns:
            Tuple of (suspect, weapon, room) if making an accusation, None otherwise
        """
        # Simple AI: randomly decide whether to make an accusation
        if random.random() < 0.1:  # 10% chance to make an accusation
            suspects = [s.name for s in self.game.player_manager.characters]
            weapons = [w.name for w in self.game.weapons]
            rooms = [r.name for r in self.game.mansion.rooms]
            
            return random.choice(suspects), random.choice(weapons), random.choice(rooms)
        
        return None
    
    def update_ai_knowledge(self, ai_player: NashAIPlayer, 
                           suggestion: Dict[str, Any], 
                           refuting_player: Optional[Player] = None, 
                           shown_card: Optional[Card] = None) -> None:
        """
        Update the AI's knowledge based on a suggestion and its outcome.
        
        Args:
            ai_player: The AI player to update
            suggestion: The suggestion that was made
            refuting_player: The player who refuted the suggestion, if any
            shown_card: The card that was shown, if any
        """
        # This is a placeholder for more sophisticated AI knowledge updating
        # In a real implementation, you would update the AI's internal model
        # based on the suggestion and its outcome
        pass
