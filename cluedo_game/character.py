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

# List of classic Cluedo character names
CHARACTER_NAMES = [
    "Miss Scarlett",
    "Colonel Mustard",
    "Mrs. White",
    "Reverend Green",
    "Mrs. Peacock",
    "Professor Plum"
]

def get_characters(rooms=None):
    """
    Return a list of Character instances, each with a random starting position.
    If rooms is provided, assign each character a unique random room if possible.
    Otherwise, assign random positions (possibly with repeats).
    """
    if rooms is None:
        # Fallback: use default rooms
        rooms = [
            "Lounge", "Dining Room", "Kitchen", "Conservatory", "Library", "Study"
        ]
    assigned_rooms = random.sample(rooms, k=min(len(CHARACTER_NAMES), len(rooms)))
    # If more characters than rooms, allow repeats
    while len(assigned_rooms) < len(CHARACTER_NAMES):
        assigned_rooms.append(random.choice(rooms))
    random.shuffle(assigned_rooms)
    return [Character(name, assigned_rooms[i]) for i, name in enumerate(CHARACTER_NAMES)]

def get_character_by_name(name):
    """Return a character instance by name, or None if not found."""
    for character in get_characters():
        if character.name == name:
            return character
    return None
