"""
Encapsulate the solution to the murder: one character, one weapon, and one room.
"""
import random
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
        character = random.choice(get_characters())
        weapon = random.choice(get_weapons())
        room = random.choice(Mansion().get_rooms())
        return Solution(character, weapon, room)

    def matches(self, character, weapon, room):
        return (self.character.name == character.name and
                self.weapon.name == weapon.name and
                self.room == room)

    def __repr__(self):
        return (f"Solution: {self.character.name} with the {self.weapon.name} in the {self.room}")
