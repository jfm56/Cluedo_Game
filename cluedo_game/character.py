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
    "Miss Scarlett": "Lounge/ballroom door",
    "Colonel Mustard": "Lounge/dining room door",
    "Mrs. White": "Ballroom/conservatory door",
    "Reverend Green": "Conservatory/library door",
    "Mrs. Peacock": "Library/study door",
    "Professor Plum": "Hall/study door"
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
