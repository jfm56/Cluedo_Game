"""
Character definitions for Cluedo game.
Defines each character and their starting positions in the mansion.
"""

class Character:
    def __init__(self, name, starting_position):
        self.name = name
        self.position = starting_position

    def __repr__(self):
        return f"Character(name={self.name}, position={self.position})"

# List of classic Cluedo characters and their starting positions
# Positions correspond to rooms or mansion locations
CHARACTERS = [
    Character("Miss Scarlett", "Lounge"),
    Character("Colonel Mustard", "Dining Room"),
    Character("Mrs. White", "Kitchen"),
    Character("Reverend Green", "Conservatory"),
    Character("Mrs. Peacock", "Library"),
    Character("Professor Plum", "Study")
]

def get_characters():
    """Return a list of all character instances."""
    return CHARACTERS

def get_character_by_name(name):
    """Return a character instance by name, or None if not found."""
    for character in CHARACTERS:
        if character.name == name:
            return character
    return None
