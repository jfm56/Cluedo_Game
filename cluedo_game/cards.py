"""
Card classes for Cluedo game: Suspect, Weapon, Room.
"""

class Card:
    """Base class for all cards in Cluedo."""
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Card) and self.name == other.name and type(self) == type(other)

    def __hash__(self):
        return hash((self.name, type(self)))

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name})"

class SuspectCard(Card):
    pass

class WeaponCard(Card):
    pass

class RoomCard(Card):
    pass

# List of classic Cluedo suspects
SUSPECTS = [
    SuspectCard("Miss Scarlett"),
    SuspectCard("Colonel Mustard"),
    SuspectCard("Mrs. White"),
    SuspectCard("Reverend Green"),
    SuspectCard("Mrs. Peacock"),
    SuspectCard("Professor Plum")
]

# Mapping of character names to starting positions
CHARACTER_STARTING_SPACES = {
    "Miss Scarlett": "C1",         # bottom left, left of Lounge
    "Colonel Mustard": "C2",      # left middle, below Dining Room
    "Mrs. White": "C3",           # top left, above Kitchen
    "Reverend Green": "C4",       # top middle, above Ballroom
    "Mrs. Peacock": "C5",         # top right, above Conservatory
    "Professor Plum": "C6"        # right middle, right of Study
}

def get_suspects():
    """Return a list of all suspect card instances."""
    return SUSPECTS

def get_suspect_by_name(name):
    """Return a suspect card instance by name, or None if not found."""
    for suspect in SUSPECTS:
        if suspect.name == name:
            return suspect
    return None
