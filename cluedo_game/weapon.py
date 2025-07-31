"""
Weapon definitions for the Cluedo game.
Defines each weapon used in the game and corresponding cards.
"""

from cluedo_game.cards import WeaponCard

class Weapon:
    """Represents a physical weapon in the mansion."""
    
    def __init__(self, name):
        """
        Initialize a weapon.
        
        Args:
            name (str): The name of the weapon
        """
        self.name = name
    
    def __repr__(self):
        return f"Weapon({self.name})"
    
    def __eq__(self, other):
        if isinstance(other, Weapon):
            return self.name == other.name
        return False

# List of physical weapons in the mansion
WEAPONS = [
    Weapon("Candlestick"),
    Weapon("Dagger"),
    Weapon("Lead Pipe"),
    Weapon("Revolver"),
    Weapon("Rope"),
    Weapon("Wrench")
]

# Weapon cards corresponding to physical weapons
WEAPON_CARDS = [
    WeaponCard(weapon.name) for weapon in WEAPONS
]

def get_weapons():
    """Return a list of all weapon instances."""
    return WEAPONS

def get_weapon_by_name(name):
    """Return a weapon instance by name, or None if not found."""
    for weapon in WEAPONS:
        if weapon.name == name:
            return weapon
    return None
