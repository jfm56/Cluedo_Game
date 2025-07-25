"""
Weapon definitions for the Cluedo game.
Defines each weapon used in the game.
"""

from cluedo_game.cards import WeaponCard

# List of classic Cluedo weapons
WEAPONS = [
    WeaponCard("Candlestick"),
    WeaponCard("Dagger"),
    WeaponCard("Lead Pipe"),
    WeaponCard("Revolver"),
    WeaponCard("Rope"),
    WeaponCard("Wrench")
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
