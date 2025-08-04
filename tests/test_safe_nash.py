"""
Test-safe version of the Nash AI Player with simplified behavior for tests.
This module provides a test-compatible implementation that avoids infinite loops.
"""

from cluedo_game.ai import NashAIPlayer
import random

class TestSafeNashAI(NashAIPlayer):
    """A simplified Nash AI player designed specifically for test compatibility.
    This implementation reduces complexity and avoids operations that cause test hangs.
    """
    
    def update_belief_state(self, arg1, arg2=None):
        """Simplified belief state update that won't hang tests."""
        # Simply ensure belief state exists
        if not hasattr(self, 'belief_state') or not self.belief_state:
            self._init_belief_state()
        return
        
    def choose_destination(self, destinations, game):
        """Simplified destination choice for test compatibility."""
        # Just pick a random destination instead of complex calculations
        if destinations:
            return random.choice(list(destinations))
        return self.position
        
    def make_nash_suggestion(self, game, room):
        """Simplified suggestion for test compatibility."""
        from cluedo_game.cards import get_suspects
        from cluedo_game.weapon import get_weapons
        
        all_suspects = get_suspects()
        all_weapons = get_weapons()
        
        # Just return a random suggestion
        return {
            'character': random.choice(all_suspects),
            'weapon': random.choice(all_weapons),
            'room': room
        }
        
    def take_turn(self, game=None):
        """Simplified turn taking for test compatibility."""
        # No complex logic that might hang
        return False
        
    def should_make_accusation(self, game=None):
        """Simplified accusation decision for test compatibility."""
        # Never make accusations in tests
        return None
