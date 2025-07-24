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
CHARACTER_STARTING_SPACES = {
    # Canonical corridor spaces for each character (based on classic Cluedo board)
    "Miss Scarlett": "C7",         # between Lounge and Ballroom
    "Colonel Mustard": "C8",      # between Lounge and Dining Room
    "Mrs. White": "C2",           # between Ballroom and Conservatory
    "Reverend Green": "C3",       # between Conservatory and Library
    "Mrs. Peacock": "C4",         # between Library and Study
    "Professor Plum": "C5"         # between Hall and Study
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
