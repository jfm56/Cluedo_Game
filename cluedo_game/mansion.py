"""
Representation of the mansion layout for the Cluedo game.
Contains different rooms such as kitchen, library, ballroom, etc.
"""

class Mansion:
    def __init__(self):
        # List of rooms in the mansion
        self.rooms = [
            "Kitchen",
            "Ballroom",
            "Conservatory",
            "Dining Room",
            "Billiard Room",
            "Library",
            "Lounge",
            "Hall",
            "Study"
        ]
        # Optional: adjacency map for movement logic
        self.adjacency = {
            "Kitchen": ["Ballroom", "Dining Room"],
            "Ballroom": ["Kitchen", "Conservatory", "Billiard Room"],
            "Conservatory": ["Ballroom", "Library"],
            "Dining Room": ["Kitchen", "Billiard Room", "Lounge"],
            "Billiard Room": ["Dining Room", "Ballroom", "Library", "Hall"],
            "Library": ["Conservatory", "Billiard Room", "Study"],
            "Lounge": ["Dining Room", "Hall"],
            "Hall": ["Lounge", "Billiard Room", "Study"],
            "Study": ["Hall", "Library"]
        }

    def get_rooms(self):
        """Return a list of all rooms."""
        return self.rooms

    def get_adjacent_rooms(self, room):
        """Return a list of rooms adjacent to the given room."""
        return self.adjacency.get(room, [])
