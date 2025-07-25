from cluedo_game.cards import SuspectCard

class Player:
    """
    Represents a player (human or AI) in the Cluedo game.
    Tracks hand, position, and elimination status.
    """
    def __init__(self, character: SuspectCard, is_human=True):
        self.character = character
        self.is_human = is_human
        self.hand = []
        self.eliminated = False  # True if player made a false accusation
        self._position = None  # Store position directly in Player

    @property
    def name(self):
        return self.character.name

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def add_card(self, card):
        self.hand.append(card)

    def __repr__(self):
        return f"Player({self.character}, hand={self.hand}, is_human={self.is_human})"
