"""
Randomly select the solution to the murder: one character, one weapon, and one room.
"""
import random
from cluedo_game.character import get_characters
from cluedo_game.weapon import get_weapons
from cluedo_game.mansion import Mansion

def select_solution():
    """Randomly select one character, one weapon, and one room."""
    character = random.choice(get_characters())
    weapon = random.choice(get_weapons())
    room = random.choice(Mansion().get_rooms())
    return {
        "character": character,
        "weapon": weapon,
        "room": room
    }
