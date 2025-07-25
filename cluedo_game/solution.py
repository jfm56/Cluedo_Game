"""
Encapsulate the solution to the murder: one character, one weapon, and one room.
"""
import random
from cluedo_game.cards import SuspectCard, WeaponCard, RoomCard
from cluedo_game.character import get_characters
from cluedo_game.weapon import get_weapons
from cluedo_game.mansion import Mansion

class Solution:
    def __init__(self, character, weapon, room):
        self.character = character
        self.weapon = weapon
        self.room = room

    @staticmethod
    def random_solution():
        character = SuspectCard(random.choice(get_characters()).name)
        weapon = WeaponCard(random.choice(get_weapons()).name)
        room = RoomCard(random.choice(Mansion().get_rooms()).name)
        return Solution(character, weapon, room)

    def matches(self, character, weapon, room):
        return (self.character == character and
                self.weapon == weapon and
                self.room == room)

    def __repr__(self):
        return (f"Solution: {self.character.name} with the {self.weapon.name} in the {self.room}")
