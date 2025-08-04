"""
Learning module for the Nash AI player.

This module handles learning from game events and updating the AI's knowledge
based on observations of other players' actions.
"""

from typing import Dict, List, Optional, Any, Set
from collections import defaultdict

from cluedo_game.cards import Card, SuspectCard, WeaponCard, RoomCard
from .bayesian_model import BayesianModel


class LearningModule:
    """
    Handles learning from game events and updating the Bayesian model.
    
    This class is responsible for:
    - Processing refutations and updating beliefs
    - Learning from other players' suggestions
    - Updating card probabilities based on observations
    """
    
    def __init__(self, model: BayesianModel):
        """
        Initialize the learning module with a reference to the Bayesian model.
        
        Args:
            model: The BayesianModel instance to update
        """
        self.model = model
        self.known_refutations = defaultdict(set)  # player -> set of card names they've shown
    
    def process_refutation(self, player_name: str, suggestion: Dict[str, Any], 
                         shown_card: Optional[Card] = None):
        """
        Process a refutation of a suggestion.
        
        Args:
            player_name: Name of the player who refuted
            suggestion: The suggestion that was refuted
            shown_card: The card that was shown, if any
        """
        if shown_card:
            # Record that this player has this card
            self.known_refutations[player_name].add(shown_card.name)
            
            # Update the model with this information
            self.model.update_from_card_reveal(shown_card, player_name)
    
    def process_no_refutation(self, suggestion: Dict[str, Any], game_state: Any):
        """
        Process the case where no one could refute a suggestion.
        
        Args:
            suggestion: The suggestion that wasn't refuted
            game_state: Current game state for context
        """
        self.model.update_from_no_refutation(suggestion, game_state)
    
    def learn_from_suggestion(self, player_name: str, suggestion: Dict[str, Any], 
                            refuting_player: Optional[str] = None,
                            shown_card: Optional[Card] = None):
        """
        Learn from another player's suggestion.
        
        Args:
            player_name: Name of the player who made the suggestion
            suggestion: The suggestion that was made
            refuting_player: Name of the player who refuted, if any
            shown_card: The card that was shown, if any
        """
        if refuting_player and shown_card:
            # A card was shown - record this information
            self.process_refutation(refuting_player, suggestion, shown_card)
        elif refuting_player:
            # The player refuted but didn't show a card (shouldn't happen)
            pass
        else:
            # No one could refute - update our model accordingly
            self.model.update_from_no_refutation(suggestion, None)
    
    def update_from_accusation(self, player_name: str, accusation: Dict[str, Any], 
                             is_correct: bool, game_state: Any):
        """
        Update our model based on an accusation made by a player.
        
        Args:
            player_name: Name of the player who made the accusation
            accusation: The accusation that was made
            is_correct: Whether the accusation was correct
            game_state: Current game state for context
        """
        if is_correct:
            # Game over - update our model with the solution
            self.model.update_from_card_reveal(accusation['character'], 'solution')
            self.model.update_from_card_reveal(accusation['weapon'], 'solution')
            self.model.update_from_card_reveal(accusation['room'], 'solution')
        else:
            # The player made an incorrect accusation - they must not have all these cards
            # This is a strong signal that these cards are not in their hand
            for card_type in ['character', 'weapon', 'room']:
                card = accusation[card_type]
                card_name = card.name if hasattr(card, 'name') else str(card)
                
                # Add to player's known not-cards
                if player_name not in self.model.player_not_cards:
                    self.model.player_not_cards[player_name] = set()
                self.model.player_not_cards[player_name].add(card_name)
            
            # Update the model
            self.model._update_probabilities()
    
    def learn_from_card_reveal(self, player_name: str, card: Card):
        """
        Learn from a card being revealed to us.
        
        Args:
            player_name: Name of the player who showed the card
            card: The card that was shown
        """
        # Record that we've seen this card
        self.model.seen_cards.add(card.name if hasattr(card, 'name') else str(card))
        
        # Update the model
        self.model.update_from_card_reveal(card, player_name)
    
    def update_belief_state(self, game_state: Any):
        """
        Update the AI's belief state based on the current game state.
        
        This method is called at the start of each AI's turn to update its
        internal model with the latest game information.
        
        Args:
            game_state: The current CluedoGame instance
        """
        try:
            # Update based on all players' known cards
            for player in game_state.get_all_players():
                if hasattr(player, 'hand') and player.hand:
                    for card in player.hand:
                        self.model.update_from_card_reveal(card, player.name)
            
            # Update from the suggestion history
            if hasattr(game_state, 'suggestion_history'):
                # Use get_all() if available, otherwise access records directly
                history_entries = getattr(game_state.suggestion_history, 'get_all', 
                                       lambda: getattr(game_state.suggestion_history, 'records', []))()
                
                for entry in history_entries:
                    refuting_player = entry.get('refuting_player')
                    if refuting_player:
                        # Create a suggestion dictionary in the expected format
                        suggestion = {
                            'character': entry.get('suggested_character'),
                            'weapon': entry.get('suggested_weapon'),
                            'room': entry.get('suggested_room')
                        }
                        self.process_refutation(
                            refuting_player,
                            suggestion,
                            entry.get('shown_card')
                        )
            
            # Update the model's probabilities
            self.model._update_probabilities()
            
        except Exception as e:
            # Log any errors but don't crash the game
            import logging
            logging.error(f"Error updating belief state: {e}", exc_info=True)
    
    def update_from_game_state(self, game_state: Any):
        """
        Update our model based on the current game state.
        
        Args:
            game_state: Current game state object
        """
        # For backward compatibility, just call update_belief_state
        self.update_belief_state(game_state)
