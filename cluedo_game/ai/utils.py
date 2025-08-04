"""
Utility functions and constants for the Nash AI player.

This module contains shared functionality used across multiple AI components.
"""

import math
from typing import Dict, List, Any, Set, Optional, Tuple, Union

from cluedo_game.cards import Card, SuspectCard, WeaponCard, RoomCard

# Constants for game rules
MAX_PLAYERS = 6
CARDS_PER_PLAYER = {
    3: 6,  # 3 players: 6 cards each
    4: 4,  # 4 players: 4 cards each
    5: 3,  # 5 players: 3 cards each
    6: 3,  # 6 players: 3 cards each
}

def normalize_probabilities(prob_dict: Dict[Any, float]) -> Dict[Any, float]:
    """
    Normalize a dictionary of probabilities to sum to 1.0.
    
    Args:
        prob_dict: Dictionary mapping items to probabilities
        
    Returns:
        Dict with normalized probabilities
    """
    total = sum(prob_dict.values())
    if total > 0:
        return {k: v / total for k, v in prob_dict.items()}
    # If all probabilities are zero, return uniform distribution
    n = len(prob_dict)
    return {k: 1.0 / n for k in prob_dict.keys()}

def calculate_entropy(prob_dict: Dict[Any, float]) -> float:
    """
    Calculate the entropy of a probability distribution.
    
    Args:
        prob_dict: Dictionary mapping items to probabilities
        
    Returns:
        float: Entropy in bits
    """
    entropy = 0.0
    for p in prob_dict.values():
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy

def get_unknown_cards(seen_cards: Set[str], all_cards: List[Card]) -> List[Card]:
    """
    Filter a list of cards to only those not in the seen set.
    
    Args:
        seen_cards: Set of card names that have been seen
        all_cards: List of all card objects to filter
        
    Returns:
        List of card objects that haven't been seen
    """
    return [card for card in all_cards 
            if (card.name if hasattr(card, 'name') else str(card)) not in seen_cards]

def get_card_type(card: Union[Card, str]) -> str:
    """
    Determine the type of a card.
    
    Args:
        card: The card to check (object or string)
        
    Returns:
        str: 'suspects', 'weapons', or 'rooms'
    """
    if isinstance(card, SuspectCard) or (hasattr(card, 'is_suspect') and card.is_suspect):
        return 'suspects'
    elif isinstance(card, WeaponCard) or (hasattr(card, 'is_weapon') and card.is_weapon):
        return 'weapons'
    elif isinstance(card, RoomCard) or (hasattr(card, 'is_room') and card.is_room):
        return 'rooms'
    else:
        # Try to infer from string representation
        card_str = str(card).lower()
        from cluedo_game.cards import get_rooms, get_weapons
        
        if any(room.lower() in card_str for room in get_rooms()):
            return 'rooms'
        elif any(weapon.name.lower() in card_str for weapon in get_weapons()):
            return 'weapons'
        else:
            return 'suspects'  # Default to suspect if unknown

def format_suggestion(suggestion: Dict[str, Any]) -> str:
    """
    Format a suggestion as a human-readable string.
    
    Args:
        suggestion: Dictionary with 'character', 'weapon', 'room' keys
        
    Returns:
        Formatted string
    """
    char = suggestion['character']
    weapon = suggestion['weapon']
    room = suggestion['room']
    
    char_name = char.name if hasattr(char, 'name') else str(char)
    weapon_name = weapon.name if hasattr(weapon, 'name') else str(weapon)
    room_name = room.name if hasattr(room, 'name') else str(room)
    
    return f"{char_name} with the {weapon_name} in the {room_name}"
