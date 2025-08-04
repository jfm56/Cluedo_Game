"""
Suggestion engine for the Nash AI player.

This module handles generating optimal suggestions based on the current game state
and the AI's belief model.
"""

import random
from typing import Dict, List, Optional, Any, Tuple

from cluedo_game.cards import SuspectCard, WeaponCard, RoomCard, Card
from .bayesian_model import BayesianModel


class SuggestionEngine:
    """
    Handles suggestion generation and evaluation for the Nash AI player.
    
    This class is responsible for:
    - Generating optimal suggestions based on current knowledge
    - Evaluating the quality of potential suggestions
    - Tracking suggestion history
    """
    
    def __init__(self, model: BayesianModel):
        """
        Initialize the suggestion engine with a reference to the Bayesian model.
        
        Args:
            model: The BayesianModel instance to use for probability calculations
        """
        self.model = model
        self.suggestion_history = []
        
    def make_suggestion(self, current_room: str, game_state: Any) -> Dict[str, Any]:
        """
        Generate an optimal suggestion based on current knowledge.
        
        Args:
            current_room: The room where the suggestion is being made
            game_state: The current game state object
            
        Returns:
            Dictionary with 'character', 'weapon', and 'room' keys
        """
        # Get all possible suspects and weapons
        from cluedo_game.cards import get_suspects, get_weapons
        all_suspects = get_suspects()
        all_weapons = get_weapons()
        
        # Calculate solution confidence
        solution_confidence = self._calculate_solution_confidence()
        
        # If we're confident in our solution, suggest those cards
        if solution_confidence > 0.8:
            solution = self.model.get_most_likely_solution()
            return {
                'character': next(s for s in all_suspects if s.name == solution['character']),
                'weapon': next(w for w in all_weapons if w.name == solution['weapon']),
                'room': current_room
            }
        
        # Otherwise, make an information-gathering suggestion
        best_score = float('-inf')
        best_suggestion = None
        
        for suspect in all_suspects:
            for weapon in all_weapons:
                # Skip combinations we've already seen
                if (suspect.name in self.model.seen_cards and 
                    weapon.name in self.model.seen_cards):
                    continue
                
                # Calculate score based on information value and probability
                info_score = self._calculate_information_value(suspect, weapon, current_room)
                prob_score = self._calculate_probability_score(suspect, weapon, current_room)
                
                # Weight information value higher when less confident
                w1 = solution_confidence  # Weight for probability
                w2 = 1.0 - solution_confidence  # Weight for information
                
                total_score = (w1 * prob_score) + (w2 * info_score)
                
                # Add bonus for cards we've never seen before
                if suspect.name not in self.model.seen_cards:
                    total_score += 0.2
                if weapon.name not in self.model.seen_cards:
                    total_score += 0.2
                
                if total_score > best_score:
                    best_score = total_score
                    best_suggestion = {
                        'character': suspect,
                        'weapon': weapon,
                        'room': current_room
                    }
        
        # Fallback to random suggestion if no good one found
        if not best_suggestion:
            best_suggestion = {
                'character': random.choice(all_suspects),
                'weapon': random.choice(all_weapons),
                'room': current_room
            }
        
        return best_suggestion
    
    def evaluate_suggestion_quality(self, suggestion: Dict[str, Any]) -> float:
        """
        Evaluate how good a potential suggestion is.
        
        Args:
            suggestion: Dictionary with 'character', 'weapon', 'room' keys
            
        Returns:
            float: Score representing the quality of the suggestion (higher is better)
        """
        score = 0.0
        
        # Check character
        char_prob = self.model.get_card_probability('suspects', suggestion['character'].name)
        score += (1.0 - char_prob) * 0.4  # Higher score for lower probability
        
        # Check weapon
        weapon_prob = self.model.get_card_probability('weapons', suggestion['weapon'].name)
        score += (1.0 - weapon_prob) * 0.4
        
        # Check room
        room_prob = self.model.get_card_probability('rooms', suggestion['room'])
        score += (1.0 - room_prob) * 0.2
        
        return score
    
    def record_suggestion(self, player: str, suggestion: Dict[str, Any], 
                         refuting_player: Optional[str] = None, 
                         shown_card: Optional[Card] = None):
        """
        Record a suggestion and its outcome in the history.
        
        Args:
            player: Name of the player who made the suggestion
            suggestion: The suggestion that was made
            refuting_player: Name of the player who refuted, if any
            shown_card: The card that was shown, if any
        """
        self.suggestion_history.append({
            'player': player,
            'suggestion': suggestion,
            'refuting_player': refuting_player,
            'shown_card': shown_card
        })
    
    def _calculate_information_value(self, suspect, weapon, room) -> float:
        """
        Calculate the information value of a potential suggestion.
        
        Args:
            suspect: Suspect card being suggested
            weapon: Weapon card being suggested
            room: Room where the suggestion is being made
            
        Returns:
            float: Information value score
        """
        info_value = 0.0
        
        # Calculate information value for suspect
        if suspect.name not in self.model.seen_cards:
            # Higher value for suspects we know less about
            info_value += 0.5 * (1.0 - self.model.get_card_probability('suspects', suspect.name))
        
        # Calculate information value for weapon
        if weapon.name not in self.model.seen_cards:
            info_value += 0.5 * (1.0 - self.model.get_card_probability('weapons', weapon.name))
        
        return info_value
    
    def _calculate_probability_score(self, suspect, weapon, room) -> float:
        """
        Calculate a score based on how likely the suggestion is to be correct.
        
        Args:
            suspect: Suspect card being suggested
            weapon: Weapon card being suggested
            room: Room where the suggestion is being made
            
        Returns:
            float: Probability score
        """
        # Calculate joint probability of this being the solution
        suspect_prob = self.model.get_card_probability('suspects', suspect.name)
        weapon_prob = self.model.get_card_probability('weapons', weapon.name)
        room_prob = self.model.get_card_probability('rooms', room)
        
        # Combine probabilities (naive Bayes assumption)
        return suspect_prob * weapon_prob * room_prob
    
    def _calculate_solution_confidence(self) -> float:
        """
        Calculate how confident we are in our current solution.
        
        Returns:
            float: Confidence score between 0 and 1
        """
        # Get the most likely solution
        solution = self.model.get_most_likely_solution()
        
        # Calculate confidence as product of probabilities
        confidence = 1.0
        confidence *= self.model.get_card_probability('suspects', solution['character'])
        confidence *= self.model.get_card_probability('weapons', solution['weapon'])
        confidence *= self.model.get_card_probability('rooms', solution['room'])
        
        return confidence ** (1/3)  # Geometric mean
