"""
Encapsulate the solution to the murder: one character, one weapon, and one room.
"""
from dataclasses import dataclass
import random
from typing import Optional

from cluedo_game.cards import SuspectCard, WeaponCard, RoomCard
from cluedo_game.character import get_characters
from cluedo_game.weapon import get_weapons
from cluedo_game.mansion import Mansion

@dataclass
class Solution:
    """Represents the solution to the Cluedo game."""
    character: SuspectCard
    weapon: WeaponCard
    room: str

    @staticmethod
    def random_solution():
        # Get physical entities first
        character_obj = random.choice(get_characters())
        weapon_obj = random.choice(get_weapons())
        room_name = random.choice(Mansion().get_rooms())
        
        # Create cards from those entities
        character = SuspectCard(character_obj.name)
        weapon = WeaponCard(weapon_obj.name)
        room = RoomCard(room_name)
        
        return Solution(character, weapon, room)

    def matches(self, character, weapon, room):
        return (self.character == character and
                self.weapon == weapon and
                self.room == room)

    def __repr__(self):
        # Handle both RoomCard objects and room name strings
        room_name = self.room.name if hasattr(self.room, 'name') else str(self.room)
        return f"Solution: {self.character.name} with the {self.weapon.name} in the {room_name}"

def create_solution() -> Solution:
    """Create a random solution for the game."""
    return Solution.random_solution()
