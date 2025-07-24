"""
Character definitions for Cluedo game.
Defines each character and their starting positions in the mansion.
"""
import random

class Character:
    def __init__(self, name, starting_position):
        self.name = name
        self.position = starting_position
        self.hand = []  # List of cards dealt to this character

    def add_card(self, card):
        self.hand.append(card)

    def __repr__(self):
        return f"Character(name={self.name}, position={self.position}, hand={self.hand})"

# List of classic Cluedo character names and their canonical starting spaces
# CHARACTER_STARTING_SPACES is assigned to match the classic Cluedo board layout as in the provided image:
#
#   [C3]   [C4]   [C5]
#     |      |      |
# [C2]-Kitchen-Ballroom-Conservatory-[C6]
#     |      |      |
# [C1]-Lounge-Hall-Study-[C7]
#
# Character tokens:
#   Miss Scarlett: C1 (bottom left, left of Lounge)
#   Colonel Mustard: C2 (left middle, below Dining Room)
#   Mrs. White: C3 (top left, above Kitchen)
#   Reverend Green: C4 (top middle, above Ballroom)
#   Mrs. Peacock: C5 (top right, above Conservatory)
#   Professor Plum: C6 (right middle, right of Study)
CHARACTER_STARTING_SPACES = {
    "Miss Scarlett": "C1",         # bottom left, left of Lounge
    "Colonel Mustard": "C2",      # left middle, below Dining Room
    "Mrs. White": "C3",           # top left, above Kitchen
    "Reverend Green": "C4",       # top middle, above Ballroom
    "Mrs. Peacock": "C5",         # top right, above Conservatory
    "Professor Plum": "C6"         # right middle, right of Study
}
CHARACTER_NAMES = list(CHARACTER_STARTING_SPACES.keys())

def get_characters(rooms=None):
    """
    Return a list of Character instances, each with their canonical starting position (edge of board).
    """
    return [Character(name, CHARACTER_STARTING_SPACES[name]) for name in CHARACTER_NAMES]

def get_character_by_name(name):
    """Return a character instance by name, or None if not found."""
    for character in get_characters():
        try:
            if character.name == name:
                return character
        except AttributeError:
            continue
    return None
