"""
Movement strategy for the Nash AI player.

This module handles all movement-related decisions, including:
- Choosing optimal destinations
- Pathfinding
- Room value assessment
"""

from typing import List, Dict, Any, Optional, Set, Tuple, Union
import random
from dataclasses import dataclass, field

from cluedo_game.cards import RoomCard
from cluedo_game.mansion import Room
from .bayesian_model import BayesianModel


@dataclass
class MovementStrategy:
    """
    Handles movement decisions for the Nash AI player.
    
    This class is responsible for:
    - Selecting optimal movement destinations
    - Calculating the value of different locations
    - Managing pathfinding between locations
    """
    
    model: BayesianModel
    visited_rooms: Set[str] = field(default_factory=set)
    
    def choose_destination(self, current_position: str, 
                         destinations: List[str], 
                         game_state: Any) -> str:
        """
        Choose the best destination from available options.
        
        Args:
            current_position: Current position of the AI player
            destinations: List of possible destinations
            game_state: Current game state object
            
        Returns:
            str: Chosen destination
        """
        if not destinations:
            return current_position
            
        if len(destinations) == 1:
            return destinations[0]
        
        # Score each destination
        scored_destinations = []
        for dest in destinations:
            score = self._calculate_destination_score(dest, current_position, game_state)
            scored_destinations.append((dest, score))
        
        # Sort by score (descending)
        scored_destinations.sort(key=lambda x: x[1], reverse=True)
        
        # Return the best destination
        return scored_destinations[0][0]
    
    def _calculate_destination_score(self, destination: Union[str, Room], 
                                   current_position: Union[str, Room],
                                   game_state: Any) -> float:
        """
        Calculate a score for a potential destination.
        
        Args:
            destination: The destination to score (can be a Room object or corridor string)
            current_position: Current position of the AI player (can be a Room object or corridor string)
            game_state: Current game state object
            
        Returns:
            float: Score for this destination (higher is better)
        """
        score = 0.0
        
        # Handle case where destination is a Room object
        if isinstance(destination, Room):
            room_name = destination.name
            score += self._score_room_destination(room_name, game_state)
        # Handle case where destination is a corridor (string starting with 'C')
        elif isinstance(destination, str) and destination.startswith('C'):
            # For current_position, convert to string if it's a Room object
            current_pos_str = current_position.name if isinstance(current_position, Room) else current_position
            score += self._score_corridor_destination(destination, current_pos_str, game_state)
        else:
            # Fallback for any other case
            try:
                # Try to get the name if it's an object with a name attribute
                room_name = getattr(destination, 'name', str(destination))
                score += self._score_room_destination(room_name, game_state)
            except Exception:
                # If all else fails, log a warning and return a neutral score
                import logging
                logging.warning(f"Could not determine destination type: {destination}")
                return 0.5
        
        # Add some randomness to avoid predictable behavior
        score += random.uniform(0, 0.1)
        
        return score
    
    def _score_room_destination(self, room: Union[str, Room], game_state: Any) -> float:
        """
        Calculate a score for moving to a room.
        
        Args:
            room: The room to score (can be a Room object or room name string)
            game_state: Current game state object
            
        Returns:
            float: Score for this room (higher is better)
        """
        score = 0.0
        
        # Get room name if it's a Room object
        room_name = room.name if hasattr(room, 'name') else str(room)
        
        # Base score for any room
        score += 50.0
        
        # Check if we've been here recently
        if room_name in self.visited_rooms:
            score -= 20.0  # Penalty for recently visited rooms
        
        # Get room probability from the model
        room_prob = self.model.get_card_probability('rooms', room_name)
        
        # Higher score for rooms we're less certain about
        # (Maximum uncertainty at p=0.5)
        uncertainty = 1.0 - abs(room_prob - 0.5) * 2.0
        score += uncertainty * 30.0
        
        # Check if this room is adjacent to other interesting rooms
        adjacent_rooms = self._get_adjacent_rooms(room_name, game_state)
        for adj_room in adjacent_rooms:
            if adj_room not in self.visited_rooms:
                adj_prob = self.model.get_card_probability('rooms', adj_room)
                score += (1.0 - adj_prob) * 10.0
        
        return score
    
    def _score_corridor_destination(self, corridor: str, 
                                  current_position: Union[str, Room],
                                  game_state: Any) -> float:
        """
        Calculate a score for moving to a corridor.
        
        Args:
            corridor: The corridor to score (should be a string like 'C1', 'C2', etc.)
            current_position: Current position of the AI player (can be a Room object or corridor string)
            game_state: Current game state object
            
        Returns:
            float: Score for this corridor (higher is better)
        """
        score = 0.0
        
        # Base score for any corridor
        score += 30.0
        
        # Handle case where current_position is a Room object
        current_pos_str = current_position.name if hasattr(current_position, 'name') else str(current_position)
        
        # Check adjacent rooms to this corridor
        adjacent_rooms = self._get_adjacent_rooms(corridor, game_state)
        
        # Score based on adjacent rooms
        for room in adjacent_rooms:
            if room not in self.visited_rooms:
                room_prob = self.model.get_card_probability('rooms', room)
                # Higher score for corridors near uncertain rooms
                score += (1.0 - room_prob) * 15.0
        
        # Slight preference for corridors near the center of the board
        if corridor in ['C6', 'C7', 'C8']:
            score += 5.0
            
        return score
    
    def _get_adjacent_rooms(self, position: str, game_state: Any) -> List[str]:
        """
        Get rooms adjacent to a given position.
        
        Args:
            position: Current position (room or corridor)
            game_state: Current game state object
            
        Returns:
            List of adjacent room names
        """
        try:
            if hasattr(game_state, 'mansion') and hasattr(game_state.mansion, 'get_adjacent_rooms'):
                return game_state.mansion.get_adjacent_rooms(position)
            elif hasattr(game_state, 'board') and hasattr(game_state.board, 'get_adjacent_rooms'):
                return game_state.board.get_adjacent_rooms(position)
            elif hasattr(game_state, 'get_adjacent_rooms'):
                return game_state.get_adjacent_rooms(position)
        except Exception:
            pass
            
        # Fallback if we can't determine adjacency
        return []
    
    def record_room_visit(self, room: str):
        """
        Record that a room has been visited.
        
        Args:
            room: Name of the room that was visited
        """
        self.visited_rooms.add(room)
        
        # Keep only the most recent 3 rooms
        if len(self.visited_rooms) > 3:
            # Convert to list, keep last 3, convert back to set
            self.visited_rooms = set(list(self.visited_rooms)[-3:])
