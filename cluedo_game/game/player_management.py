"""
Player management for the Cluedo game.

This module handles player initialization, character selection, and card dealing.
"""
import random
from typing import List, Optional, Tuple, Dict, Any, Set, Union

from cluedo_game.cards import (
    get_suspects, get_weapons, get_rooms,
    SuspectCard, WeaponCard, RoomCard, Card,
    CHARACTER_STARTING_SPACES
)
from cluedo_game.player import Player
from cluedo_game.ai import NashAIPlayer

class PlayerManager:
    """Manages players, characters, and card distribution."""
    
    def __init__(self, game):
        """
        Initialize the player manager.
        
        Args:
            game: Reference to the main game instance
        """
        self.game = game
        self._characters: List[Player] = []
        self.player: Optional[Player] = None
        self.ai_players: List[NashAIPlayer] = []
        
        # Initialize characters from suspect cards
        self._initialize_characters()
        
    @property
    def characters(self) -> List[Player]:
        """Get the list of all characters."""
        return self._characters
        
    @characters.setter
    def characters(self, value: List[Player]) -> None:
        """Set the list of characters."""
        self._characters = value
    
    def get_all_active_players(self) -> List[Player]:
        """
        Get a list of all active (non-eliminated) players.
        
        Returns:
            List of all active Player objects
        """
        # First, make sure we have players initialized
        if not self._characters and not self.ai_players and not self.player:
            self._initialize_characters()
            
        # If we have a human player, include them
        all_players = []
        if self.player is not None:
            all_players.append(self.player)
            
        # Add AI players
        all_players.extend(self.ai_players)
        
        # If we still have no players, use the base characters
        if not all_players and self._characters:
            all_players = self._characters
            
        # Filter out eliminated players
        active_players = [p for p in all_players if not getattr(p, 'eliminated', False)]
        
        # Debug information
        self.game.logger.debug(f"Active players: {[p.name for p in active_players]}")
        return active_players
    
    def _initialize_characters(self) -> None:
        """Initialize all playable characters from suspect cards."""
        self._characters = []
        suspects = get_suspects()
        self.game.logger.debug(f"Initializing {len(suspects)} characters from suspect cards")
        
        for suspect_card in suspects:
            # Create both human and AI players with is_human flag
            player = Player(suspect_card, is_human=True)
            player.position = CHARACTER_STARTING_SPACES[suspect_card.name]
            player.eliminated = False
            self._characters.append(player)
            self.game.logger.debug(f"Created character: {player.name} at position {player.position}")
            
        self.game.logger.debug(f"Total characters initialized: {len(self._characters)}")
    
    def select_character(self) -> None:
        """Handle character selection for the human player."""
        if not self.characters:
            self._initialize_characters()
            
        self.game.ui.show_message("Select your character:")
        for idx, player in enumerate(self.characters):
            chess_coord = self.game.mansion.get_chess_coordinate(player.position)
            pos_str = player.position  # Just use the position code directly
            self.game.ui.show_message(f"  {idx + 1}. {player.name} (starts in {pos_str} [{chess_coord}])")
            
        while True:
            inp = self.game.input("Enter number: ").strip()
            try:
                choice = int(inp)
                if 1 <= choice <= len(self.characters):
                    self._process_character_selection(choice - 1)
                    break
                self.game.ui.show_message("Invalid selection.")
            except ValueError:
                self.game.ui.show_message("Please enter a valid number.")
    
    def _process_character_selection(self, selected_idx: int) -> None:
        """Process the selected character and set up AI players if needed."""
        # Set the human player
        self.player = self.characters[selected_idx]
        self.player.is_human = True
        
        # Update the game's player reference
        self.game.player = self.player
        
        # Update position to use corridor code if needed
        pos = self.player.position
        chess_coord = self.game.mansion.get_chess_coordinate(pos)
        
        # Show starting position with chess coordinate
        self.game.ui.show_message(f"\nYou are {self.player.name}, starting in {pos} [{chess_coord}].")
        
        # Initialize AI players if in AI mode
        if self.game.with_ai:
            self._setup_ai_players(selected_idx)
    
    def _setup_ai_players(self, selected_idx: int) -> None:
        """Set up AI players for the game."""
        self.ai_players = []
        for i, character in enumerate(self.characters):
            if i != selected_idx:  # All characters except the player's
                ai_player = NashAIPlayer(character.character)
                ai_player.position = character.position  # Preserve position
                ai_player.is_human = False
                self.ai_players.append(ai_player)
        
        self.game.ui.show_message(
            f"AI opponents: {', '.join(ai.name for ai in self.ai_players)}"
        )
    
    def setup_ai_only_players(self) -> None:
        """Set up AI players for an AI-only game."""
        self.game.with_ai = True
        all_indices = list(range(len(self.characters)))
        selected_indices = random.sample(all_indices, min(4, len(all_indices)))
        
        self.ai_players = []
        for idx in selected_indices:
            character = self.characters[idx]
            ai_player = NashAIPlayer(character.character)
            ai_player.position = character.position
            ai_player.is_human = False
            self.ai_players.append(ai_player)
        
        # Set the first AI player as the main player for compatibility
        if self.ai_players:
            self.player = self.ai_players[0]
    
    def deal_cards(self) -> None:
        """
        Deal cards to all players, ensuring solution cards are not dealt.
        
        This method follows the logic from the original game.py where solution cards
        are filtered out before dealing to ensure no player gets a solution card.
        """
        # Get all cards in the game
        all_cards = self._get_all_cards()
        
        # Get the solution cards to filter them out
        solution_cards = self._get_solution_cards()
        
        # Remove solution cards from the deck
        deck = [card for card in all_cards if not self._is_card_in_solution(card, solution_cards)]
        random.shuffle(deck)
        
        # Get all players (human + AI)
        players = self._get_all_active_players()
        if not players:
            self.game.ui.show_message("No players to deal cards to!")
            return
        
        # Distribute cards as evenly as possible
        num_cards = len(deck)
        num_players = len(players)
        
        # Calculate cards per player and remainder
        cards_per_player = num_cards // num_players
        remainder = num_cards % num_players
        
        # Deal cards to each player
        start = 0
        for i, player in enumerate(players):
            # Give an extra card to the first 'remainder' players
            end = start + cards_per_player + (1 if i < remainder else 0)
            player.hand = deck[start:end]
            start = end
            
            # Log the dealt cards for debugging
            if hasattr(self.game, 'logger'):
                card_names = [card.name for card in player.hand]
                self.game.logger.debug(f"Dealt to {player.name}: {', '.join(card_names)}")
    
    def _get_all_cards(self) -> List[Card]:
        """Get all cards in the game (suspects, weapons, rooms)."""
        cards = []
        
        # Add suspect cards
        cards.extend([SuspectCard(suspect.name) for suspect in get_suspects()])
        
        # Add weapon cards
        cards.extend([WeaponCard(weapon.name) for weapon in get_weapons()])
        
        # Add room cards
        cards.extend([RoomCard(room) for room in get_rooms()])
        
        return cards
    
    def _get_solution_cards(self) -> List[Card]:
        """Get the solution cards as a list of Card objects."""
        return [
            self.game.solution.character,
            self.game.solution.weapon,
            self.game.solution.room
        ]
    
    def _is_card_in_solution(self, card: Card, solution_cards: List[Card]) -> bool:
        """
        Check if a card is part of the solution.
        
        Args:
            card: The card to check
            solution_cards: List of cards in the solution
            
        Returns:
            bool: True if the card is in the solution, False otherwise
        """
        for solution_card in solution_cards:
            # Compare both name and type to ensure it's the exact card
            if (card.name == solution_card.name and 
                isinstance(card, type(solution_card))):
                return True
        return False
    
    def _get_all_active_players(self) -> List[Union[Player, NashAIPlayer]]:
        """
        Get all active (non-eliminated) players.
        
        Returns:
            List of active Player and NashAIPlayer objects
        """
        players = []
        
        # Add human player if exists and not eliminated
        if self.player is not None and not getattr(self.player, 'eliminated', False):
            players.append(self.player)
        
        # Add AI players that are not eliminated
        for ai_player in self.ai_players:
            if not getattr(ai_player, 'eliminated', False):
                players.append(ai_player)
        
        # If no players found (shouldn't happen in normal game flow)
        if not players and self.characters:
            # Fallback to all non-eliminated characters
            players = [p for p in self.characters if not getattr(p, 'eliminated', False)]
        
        return players
