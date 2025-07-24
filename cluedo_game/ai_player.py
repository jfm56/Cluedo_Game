import random
from cluedo_game.player import Player
from cluedo_game.weapon import get_weapons
from cluedo_game.character import get_characters

class AIPlayer(Player):
    """
    Represents a computer-controlled player that can take turns and make suggestions.
    """
    def __init__(self, character):
        super().__init__(character, is_human=False)
        self.seen_cards = set()  # Cards the AI has seen (in hand or shown)

    @property
    def name(self):
        base = self.character.name
        if base.endswith(" (AI)"):
            return base
        return base + " (AI)"

    def take_turn(self, game):
        """
        Take a full turn: move, make suggestion, and check for win.
        """
        # Move to a random adjacent room
        adjacent_rooms = game.mansion.get_adjacent_rooms(self.position)
        if adjacent_rooms:
            self.position = random.choice(adjacent_rooms)
        # Make a suggestion (randomly for now)
        suggestion = self.make_suggestion(game)
        # Handle refutation
        refuting_player, shown_card = game.handle_refutation(
            suggestion['character'], suggestion['weapon'], suggestion['room']
        )
        # Track seen cards
        if shown_card:
            self.seen_cards.add(shown_card)
        # Log suggestion
        game.suggestion_history.add(
            self.name, suggestion['character'].name, suggestion['weapon'].name, suggestion['room'], refuting_player, shown_card
        )
        # Output suggestion and refutation (always output, even if not a win)
        game.output(f"{self.name} (AI) suggests {suggestion['character'].name} with the {suggestion['weapon'].name} in the {suggestion['room']}. Refuted by {refuting_player} with {shown_card or '—'}.")
        # Check for win
        if (game.solution.character.name == suggestion['character'].name and
            game.solution.weapon.name == suggestion['weapon'].name and
            game.solution.room == suggestion['room']):
            game.output(f"\n{self.name} (AI) wins!")
            game.output(f"The solution was: {game.solution.character.name} with the {game.solution.weapon.name} in the {game.solution.room}.")
            return True
        return False

    def make_suggestion(self, game):
        """
        Pick a random suggestion (could be improved with deduction logic).
        """
        all_characters = get_characters()
        all_weapons = get_weapons()
        room = self.position
        character = random.choice(all_characters)
        weapon = random.choice(all_weapons)
        return {'character': character, 'weapon': weapon, 'room': room}
