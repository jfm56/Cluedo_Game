"""
User interface for the Cluedo game.

This module handles all user input and output.
"""
from typing import Callable, List, Optional, Any, Dict

class GameUI:
    """Handles all user interface interactions for the game."""
    
    def __init__(self, input_func: Callable = input, output_func: Callable = print):
        """
        Initialize the game UI.
        
        Args:
            input_func: Function to use for input (default: built-in input)
            output_func: Function to use for output (default: built-in print)
        """
        self.input = input_func
        self.output = output_func
    
    def show_welcome(self) -> None:
        """Display the welcome message."""
        self.output("=" * 50)
        self.output("CLUEDO: THE CLASSIC MYSTERY GAME")
        self.output("=" * 50)
        self.output("\nA murder has been committed in the mansion!")
        self.output("Can you solve the mystery before the other players?\n")
    
    def show_game_over(self, winner: Optional[str] = None) -> None:
        """
        Display the game over message.
        
        Args:
            winner: Name of the winning player, if any
        """
        self.output("\n" + "=" * 50)
        self.output("GAME OVER")
        if winner:
            self.output(f"{winner} wins!")
        self.output("=" * 50)
    
    def show_player_turn(self, player_name: str) -> None:
        """
        Display whose turn it is.
        
        Args:
            player_name: Name of the current player
        """
        self.output(f"\n--- {player_name}'s turn ---")
    
    def show_dice_roll(self, player_name: str, roll: int) -> None:
        """
        Display the result of a dice roll.
        
        Args:
            player_name: Name of the player who rolled
            roll: The result of the dice roll
        """
        self.output(f"{player_name} rolled a {roll}")
    
    def show_movement(self, player_name: str, start_pos: str, end_pos: str) -> None:
        """
        Display a player's movement.
        
        Args:
            player_name: Name of the moving player
            start_pos: Starting position
            end_pos: Destination position
        """
        self.output(f"{player_name} moved from {start_pos} to {end_pos}")
    
    def show_suggestion(self, player_name: str, suspect: str, weapon: str, room: str) -> None:
        """
        Display a player's suggestion.
        
        Args:
            player_name: Name of the player making the suggestion
            suspect: Suspect being suggested
            weapon: Weapon being suggested
            room: Room being suggested
        """
        self.output(f"\n{player_name} suggests: {suspect} with the {weapon} in the {room}")
    
    def show_accusation(self, player_name: str, suspect: str, weapon: str, room: str, is_correct: bool) -> None:
        """
        Display a player's accusation and its result.
        
        Args:
            player_name: Name of the player making the accusation
            suspect: Suspect being accused
            weapon: Weapon being accused
            room: Room being accused
            is_correct: Whether the accusation was correct
        """
        self.output(f"\n{player_name} accuses: {suspect} with the {weapon} in the {room}")
        if is_correct:
            self.output(f"{player_name} is correct! The mystery is solved!")
        else:
            self.output(f"{player_name} is wrong! {player_name} is out of the game!")
    
    def show_refutation(self, refuting_player: str, showing_to: str, card: Optional[str] = None) -> None:
        """
        Display that a player is refuting a suggestion.
        
        Args:
            refuting_player: Name of the player refuting
            showing_to: Name of the player being shown a card
            card: Name of the card being shown, if any
        """
        if card:
            self.output(f"{refuting_player} shows a card to {showing_to}")
            if showing_to == "You":
                self.output(f"You see: {card}")
        else:
            self.output(f"{refuting_player} cannot refute the suggestion.")
    
    def show_no_refutation(self) -> None:
        """Display that no one could refute a suggestion."""
        self.output("No one could refute the suggestion.")
    
    def get_player_choice(self, prompt: str, options: List[str]) -> str:
        """
        Get a choice from the player.
        
        Args:
            prompt: The prompt to display
            options: List of available options
            
        Returns:
            The player's chosen option
        """
        self.output(f"\n{prompt}:")
        for i, option in enumerate(options, 1):
            self.output(f"{i}. {option}")
        
        while True:
            choice = self.input("Enter your choice: ").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    return options[idx]
                self.output(f"Please enter a number between 1 and {len(options)}.")
            except ValueError:
                self.output("Please enter a valid number.")
    
    def get_yes_no(self, prompt: str, default: Optional[bool] = None) -> bool:
        """
        Get a yes/no response from the player.
        
        Args:
            prompt: The prompt to display
            default: Default value if user just presses Enter
            
        Returns:
            True for yes, False for no
        """
        if default is not None:
            default_str = 'Y/n' if default else 'y/N'
        else:
            default_str = 'y/n'
            
        while True:
            response = self.input(f"{prompt} [{default_str}]: ").strip().lower()
            if not response and default is not None:
                return default
            if response in ('y', 'yes'):
                return True
            if response in ('n', 'no'):
                return False
            self.output("Please enter 'y' or 'n'.")
    
    def show_message(self, message: str) -> None:
        """
        Display a message to the player.
        
        Args:
            message: The message to display
        """
        self.output(message)
    
    def show_player_hand(self, player_name: str, cards: List[str]) -> None:
        """
        Display a player's hand.
        
        Args:
            player_name: Name of the player
            cards: List of card names in the player's hand
        """
        self.output(f"\n{player_name}'s hand:")
        if cards:
            for card in cards:
                self.output(f"- {card}")
        else:
            self.output("(No cards)")
    
    def show_player_locations(self, players: List[Dict[str, Any]]) -> None:
        """
        Display the current locations of all players with chess coordinates.
        
        Args:
            players: List of player dictionaries with 'name', 'position', and 'eliminated' keys
        """
        self.output("\nCurrent player locations:")
        for player in players:
            status = "(eliminated)" if player.get('eliminated', False) else ""
            pos = player['position']
            # Get chess coordinate for all positions
            if hasattr(self, 'game') and hasattr(self.game, 'mansion') and hasattr(self.game.mansion, 'get_chess_coordinate'):
                chess_coord = self.game.mansion.get_chess_coordinate(pos)
                pos_str = f"{pos} [{chess_coord}]"
            else:
                pos_str = str(pos)
                
            self.output(f"- {player['name']}: {pos_str} {status}".strip())
