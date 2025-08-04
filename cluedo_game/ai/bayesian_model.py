"""
Bayesian model for the Nash AI player.

This module handles all probability calculations and belief state management
for the Nash equilibrium-based Cluedo AI player.
"""

import math
import random
from typing import Dict, List, Set, Tuple, Optional, Any, DefaultDict
from collections import defaultdict
from dataclasses import dataclass, field

from cluedo_game.cards import SuspectCard, WeaponCard, RoomCard, Card
from cluedo_game.character import Character


@dataclass
class BayesianModel:
    """
    Manages the Bayesian probability model for the Nash AI player.
    
    This class handles:
    - Maintaining prior and posterior probability distributions
    - Updating beliefs based on evidence
    - Calculating probabilities for decision making
    """
    
    # Prior probability distributions
    priors: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        'suspects': {},
        'weapons': {},
        'rooms': {}
    })
    
    # Posterior probability distributions
    posteriors: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        'suspects': {},
        'weapons': {},
        'rooms': {}
    })
    
    # Track which cards have been seen
    seen_cards: Set[str] = field(default_factory=set)
    
    # Track player card probabilities
    player_card_probabilities: DefaultDict[str, Dict[str, float]] = field(
        default_factory=lambda: defaultdict(dict)
    )
    
    # Track known card assignments
    player_cards: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))
    player_not_cards: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))
    
    def __post_init__(self):
        """Initialize the model with uniform priors."""
        self._init_priors()
        self._init_posteriors()
    
    def _init_priors(self):
        """Initialize uniform prior probabilities for all cards."""
        from cluedo_game.cards import get_suspects, get_weapons, get_rooms
        
        # Initialize suspect priors
        suspects = get_suspects()
        suspect_count = len(suspects)
        for suspect in suspects:
            self.priors['suspects'][suspect.name] = 1.0 / suspect_count
        
        # Initialize weapon priors
        weapons = get_weapons()
        weapon_count = len(weapons)
        for weapon in weapons:
            self.priors['weapons'][weapon.name] = 1.0 / weapon_count
        
        # Initialize room priors
        rooms = get_rooms()
        room_count = len(rooms)
        for room in rooms:
            self.priors['rooms'][room] = 1.0 / room_count
    
    def _init_posteriors(self):
        """Initialize posteriors to match priors."""
        for card_type in self.priors:
            self.posteriors[card_type] = self.priors[card_type].copy()
    
    def update_from_card_reveal(self, card: Card, player_name: str):
        """
        Update the model when a card is revealed to the AI.
        
        Args:
            card: The card that was revealed
            player_name: Name of the player who showed the card
        """
        card_name = card.name if hasattr(card, 'name') else str(card)
        card_type = self._get_card_type(card)
        
        # Add to seen cards
        self.seen_cards.add(card_name)
        
        # Update player-card assignments
        if player_name not in self.player_cards:
            self.player_cards[player_name] = set()
        self.player_cards[player_name].add(card_name)
        
        # Update probabilities
        self._update_probabilities()
    
    def update_from_no_refutation(self, suggestion: Dict[str, Any], game):
        """
        Update the model when no one can refute a suggestion.
        
        Args:
            suggestion: Dictionary with 'character', 'weapon', 'room' keys
            game: The game object for context
        """
        # Get all players who could have refuted but didn't
        players_without_cards = set()
        for player in game.players:
            if player != self and player != suggestion['character']:
                players_without_cards.add(player.name)
        
        # Update probabilities for each card in the suggestion
        for card_type in ['character', 'weapon', 'room']:
            card = suggestion[card_type]
            card_name = card.name if hasattr(card, 'name') else str(card)
            
            # If we haven't seen this card yet
            if card_name not in self.seen_cards:
                # For players who couldn't refute, they don't have these cards
                for player_name in players_without_cards:
                    if player_name not in self.player_not_cards:
                        self.player_not_cards[player_name] = set()
                    self.player_not_cards[player_name].add(card_name)
        
        # Recalculate probabilities
        self._update_probabilities()
    
    def get_card_probability(self, card_type: str, card_name: str) -> float:
        """
        Get the current probability that a card is in the solution.
        
        Args:
            card_type: Type of card ('suspects', 'weapons', 'rooms')
            card_name: Name of the card
            
        Returns:
            float: Probability between 0 and 1
        """
        return self.posteriors[card_type].get(card_name, 0.0)
    
    def get_most_likely_solution(self) -> Dict[str, str]:
        """
        Get the current most likely solution based on posteriors.
        
        Returns:
            Dict with 'character', 'weapon', 'room' keys and the most likely values
        """
        solution = {}
        
        # Find most likely suspect
        if self.posteriors['suspects']:
            solution['character'] = max(
                self.posteriors['suspects'].items(), 
                key=lambda x: x[1]
            )[0]
        
        # Find most likely weapon
        if self.posteriors['weapons']:
            solution['weapon'] = max(
                self.posteriors['weapons'].items(),
                key=lambda x: x[1]
            )[0]
        
        # Find most likely room
        if self.posteriors['rooms']:
            solution['room'] = max(
                self.posteriors['rooms'].items(),
                key=lambda x: x[1]
            )[0]
        
        return solution
    
    def _update_probabilities(self):
        """Update all probability distributions based on current evidence."""
        # Update posteriors based on priors and evidence
        # This is a simplified version - in practice, you'd use Bayesian updating
        # with the actual evidence from the game
        
        # For now, just copy priors to posteriors
        # In a real implementation, this would update based on evidence
        for card_type in self.priors:
            for card_name in self.priors[card_type]:
                # If we've seen the card, it's not in the solution
                if card_name in self.seen_cards:
                    self.posteriors[card_type][card_name] = 0.0
                else:
                    # Otherwise, use the prior (will be normalized)
                    self.posteriors[card_type][card_name] = self.priors[card_type][card_name]
        
        # Normalize probabilities for each card type
        for card_type in self.posteriors:
            self._normalize_probabilities(card_type)
    
    def _normalize_probabilities(self, card_type: str):
        """Normalize probabilities for a card type to sum to 1."""
        total = sum(self.posteriors[card_type].values())
        if total > 0:
            for card_name in self.posteriors[card_type]:
                self.posteriors[card_type][card_name] /= total
    
    @staticmethod
    def _get_card_type(card) -> str:
        """Determine the type of a card."""
        if isinstance(card, SuspectCard) or (hasattr(card, 'is_suspect') and card.is_suspect):
            return 'suspects'
        elif isinstance(card, WeaponCard) or (hasattr(card, 'is_weapon') and card.is_weapon):
            return 'weapons'
        elif isinstance(card, RoomCard) or (hasattr(card, 'is_room') and card.is_room):
            return 'rooms'
        else:
            # Try to infer from string representation
            card_str = str(card).lower()
            if any(room.lower() in card_str for room in get_rooms()):
                return 'rooms'
            elif any(weapon.lower() in card_str for weapon in [w.name.lower() for w in get_weapons()]):
                return 'weapons'
            else:
                return 'suspects'  # Default to suspect if unknown
