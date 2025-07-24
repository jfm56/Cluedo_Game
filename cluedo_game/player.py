from cluedo_game.character import Character

class Player:
    """
    Represents a player (human or AI) in the Cluedo game.
    Tracks hand, position, and elimination status.
    """
    def __init__(self, character: 'Character', is_human=True):
        self.character = character
        self.is_human = is_human
        self.hand = []
        self.eliminated = False  # True if player made a false accusation

    def __init__(self, character: Character, is_human=True):
        self.character = character
        self.is_human = is_human
        self.hand = []

    @property
    def name(self):
        return self.character.name

    @property
    def position(self):
        return self.character.position

    @position.setter
    def position(self, value):
        self.character.position = value

    def add_card(self, card):
        self.hand.append(card)

    def __repr__(self):
        return f"Player({self.character}, hand={self.hand}, is_human={self.is_human})"
