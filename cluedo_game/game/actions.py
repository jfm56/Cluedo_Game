"""
Player actions for the Cluedo game.

This module handles player actions like movement, suggestions, and accusations.
"""
from typing import Dict, List, Optional, Any, Tuple

from cluedo_game.player import Player
from cluedo_game.cards import Card, SuspectCard, WeaponCard, RoomCard

class ActionHandler:
    """Handles all player actions in the game."""
    
    def __init__(self, game):
        """
        Initialize the action handler.
        
        Args:
            game: Reference to the main game instance
        """
        self.game = game
    
    def handle_movement(self, player: Player, steps: int) -> None:
        """
        Handle player movement.
        
        Args:
            player: The player who is moving
            steps: Number of steps the player can move
        """
        if steps <= 0:
            self.game.output(f"{player.name} has no moves left this turn.")
            return
            
        current_pos = player.position
        
        # Get available moves
        destinations = self.game.movement.get_destinations_from(current_pos, steps)
        
        if not destinations:
            self.game.output(f"{player.name} has no valid moves from {current_pos}.")
            return
        
        # Let player choose destination
        if player.is_human:
            dest = self._get_human_destination_choice(destinations)
        else:
            # AI player chooses destination
            dest = self._get_ai_destination_choice(player, destinations)
        
        if dest:
            self._move_player(player, dest)
    
    def _get_human_destination_choice(self, destinations: List[str]) -> Optional[str]:
        """Get destination choice from human player."""
        self.game.output("\nAvailable destinations:")
        for i, dest in enumerate(destinations, 1):
            self.game.output(f"{i}. {dest}")
        
        while True:
            choice = self.game.input("Choose destination (or press Enter to skip): ").strip()
            if not choice:
                return None
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(destinations):
                    return destinations[idx]
                self.game.output(f"Please enter a number between 1 and {len(destinations)}.")
            except ValueError:
                self.game.output("Please enter a valid number.")
    
    def _get_ai_destination_choice(self, ai_player: Player, destinations: List[str]) -> Optional[str]:
        """Get destination choice from AI player."""
        # Simple AI: choose the first available destination
        # This can be enhanced with more sophisticated AI logic
        return destinations[0] if destinations else None
    
    def _move_player(self, player: Player, destination: str) -> None:
        """
        Move player to the specified destination and handle room entry.
        
        Args:
            player: The player to move
            destination: The destination position (room or corridor)
        """
        old_pos = player.position
        player.position = destination
        
        # Check if player passed through a door
        if not str(old_pos).startswith('C') and str(destination).startswith('C'):
            self.game.last_door_passed[player.name] = old_pos
        
        self.game.output(f"{player.name} moved from {old_pos} to {destination}")
        
        # We'll handle suggestions in the main turn flow, not here
        # This prevents duplicate suggestion prompts
    
    def _prompt_for_suggestion(self, player: Player, room: str) -> None:
        """
        Prompt the player to make a suggestion when entering a room.
        
        Args:
            player: The player making the suggestion
            room: The room the player entered
        """
        self.game.output(f"\nYou've entered the {room}. Would you like to make a suggestion?")
        make_suggestion = self._get_yes_no("Make a suggestion? (y/n): ")
        
        if make_suggestion:
            self.handle_suggestion(player)
    
    def _get_yes_no(self, prompt: str) -> bool:
        """
        Get a yes/no response from the player.
        
        Args:
            prompt: The prompt to display
            
        Returns:
            bool: True if the player answered 'y', False otherwise
        """
        while True:
            response = self.game.input(prompt).strip().lower()
            if response in ('y', 'yes'):
                return True
            elif response in ('n', 'no'):
                return False
            self.game.output("Please enter 'y' or 'n'.")
    
    def handle_suggestion(self, suggesting_player: Player) -> bool:
        """
        Handle a player making a suggestion.
        
        Args:
            suggesting_player: The player making the suggestion
            
        Returns:
            bool: True if the game should end (correct accusation), False otherwise
        """
        if suggesting_player.is_human:
            return self._handle_human_suggestion(suggesting_player)
        else:
            return self._handle_ai_suggestion(suggesting_player)
    
    def _handle_human_suggestion(self, player: Player) -> bool:
        """
        Handle a suggestion from a human player.
        
        Args:
            player: The player making the suggestion
            
        Returns:
            bool: True if the game should end (correct accusation), False otherwise
        """
        current_room = str(player.position)
        self.game.output(f"\n{player.name}, you're in the {current_room}. Make a suggestion:")
        
        # Get suspect choice
        suspects = [s.name for s in self.game.player_manager.characters]
        suspect = self._get_player_choice("Suspect", suspects)
        
        # Get weapon choice
        weapons = [w.name for w in self.game.weapons]
        weapon = self._get_player_choice("Weapon", weapons)
        
        # Move the suggested character to the room
        for character in self.game.player_manager.characters:
            if character.name == suspect:
                old_pos = character.position
                character.position = current_room
                self.game.output(f"Moved {character.name} from {old_pos} to {current_room}")
                break
        
        # The room is the current room
        room = current_room
        
        # Process the suggestion and set the flag
        result = self._process_suggestion(player, suspect, weapon, room)
        # Set the suggestion_made flag to prevent multiple suggestions per turn
        if hasattr(self.game, '_suggestion_made'):
            self.game._suggestion_made = True
        return result
    
    def _handle_ai_suggestion(self, ai_player: Player) -> bool:
        """
        Handle a suggestion from an AI player.
        
        Args:
            ai_player: The AI player making the suggestion
            
        Returns:
            bool: True if the game should end (correct accusation), False otherwise
        """
        # Simple AI: suggest a random combination
        # This can be enhanced with more sophisticated AI logic
        suspects = [s.name for s in self.game.player_manager.characters]
        weapons = [w.name for w in self.game.weapons]
        
        suspect = random.choice(suspects)
        weapon = random.choice(weapons)
        room = str(ai_player.position)
        
        # Move the suggested character to the room
        for character in self.game.player_manager.characters:
            if character.name == suspect:
                old_pos = character.position
                character.position = room
                self.game.output(f"Moved {character.name} from {old_pos} to {room}")
                break
        
        self.game.output(f"\n{ai_player.name} suggests: {suspect} with the {weapon} in the {room}")
        return self._process_suggestion(ai_player, suspect, weapon, room)
    
    def _process_suggestion(self, suggesting_player: Player, 
                          suspect: str, weapon: str, room: str) -> bool:
        """Process a suggestion and check for refutations."""
        # Check if this is actually an accusation
        is_accusation = self._is_accusation(suspect, weapon, room)
        
        if is_accusation:
            return self._handle_accusation(suggesting_player, suspect, weapon, room)
        
        # It's a regular suggestion
        self._handle_regular_suggestion(suggesting_player, suspect, weapon, room)
        return False
    
    def _is_accusation(self, suspect: str, weapon: str, room: str) -> bool:
        """Check if the suggestion is actually an accusation."""
        # In the standard game, a suggestion made in the room that matches the solution is an accusation
        # This logic can be adjusted based on your game's rules
        return False  # Default implementation - override as needed
    
    def _handle_accusation(self, player: Player, suspect: str, weapon: str, room: str) -> bool:
        """Handle a player making an accusation."""
        is_correct = (suspect == self.game.solution.character.name and
                     weapon == self.game.solution.weapon.name and
                     room == self.game.solution.room.name)
        
        if is_correct:
            self.game.output(f"\n{player.name} correctly accused {suspect} with the {weapon} in the {room}!")
            return True
        else:
            self.game.output(f"\n{player.name} made a false accusation! {player.name} is out of the game!")
            player.eliminated = True
            return False
    
    def _handle_regular_suggestion(self, suggesting_player: Player, 
                                 suspect: str, weapon: str, room: str) -> None:
        """Handle a regular suggestion (not an accusation)."""
        # Find the first player who can refute the suggestion
        refuting_player, shown_card = self._get_refutation(suggesting_player, suspect, weapon, room)
        
        # Record the suggestion in history
        self.game.suggestion_history.add(
            suggesting_player.name, suspect, weapon, room,
            refuting_player.name if refuting_player else None,
            shown_card.name if shown_card else None
        )
        
        # Show the suggestion result
        if refuting_player and shown_card:
            self.game.output(f"{refuting_player.name} shows a card to {suggesting_player.name}")
            if suggesting_player.is_human:
                self.game.output(f"You were shown: {shown_card.name}")
        else:
            self.game.output("No one could refute the suggestion.")
    
    def _get_refutation(self, suggesting_player: Player, 
                       suspect: str, weapon: str, room: str) -> Tuple[Optional[Player], Optional[Card]]:
        """
        Find a player who can refute the suggestion.
        
        Returns:
            Tuple of (refuting_player, shown_card) or (None, None) if no refutation
        """
        players = self._get_players_after(suggesting_player)
        
        for player in players:
            # Check if player has any of the suggested cards
            for card in player.hand:
                if (isinstance(card, SuspectCard) and card.name == suspect) or \
                   (isinstance(card, WeaponCard) and card.name == weapon) or \
                   (isinstance(card, RoomCard) and card.name == room):
                    return player, card
        
        return None, None
    
    def _get_players_after(self, current_player: Player) -> List[Player]:
        """Get all players who come after the current player in turn order."""
        all_players = self.game.game_loop._get_play_order()
        current_idx = all_players.index(current_player)
        return all_players[current_idx+1:] + all_players[:current_idx]
    
    def _get_player_choice(self, prompt: str, options: List[str]) -> str:
        """Helper method to get a choice from the player."""
        self.game.output(f"\n{prompt}s:")
        for i, option in enumerate(options, 1):
            self.game.output(f"{i}. {option}")
        
        while True:
            choice = self.game.input(f"Choose {prompt.lower()}: ").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    return options[idx]
                self.game.output(f"Please enter a number between 1 and {len(options)}.")
            except ValueError:
                self.game.output("Please enter a valid number.")
