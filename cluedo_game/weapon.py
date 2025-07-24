"""
Weapon definitions for the Cluedo game.
Defines each weapon used in the game.
"""

class Weapon:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Weapon(name={self.name})"

# List of classic Cluedo weapons
WEAPONS = [
    Weapon("Candlestick"),
    Weapon("Dagger"),
    Weapon("Lead Pipe"),
    Weapon("Revolver"),
    Weapon("Rope"),
    Weapon("Wrench")
]

def get_weapons():
    """Return a list of all weapon instances."""
    return WEAPONS

def get_weapon_by_name(name):
    """Return a weapon instance by name, or None if not found."""
    for weapon in WEAPONS:
        try:
            if weapon.name == name:
                return weapon
        except AttributeError:
            continue
    return None
