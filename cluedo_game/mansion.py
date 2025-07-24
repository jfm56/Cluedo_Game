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
        # List of corridor spaces (simplified, e.g., C1-C12)
        self.corridors = [f"C{i}" for i in range(1, 13)]
        # Unified adjacency map: rooms and corridors
        # (This is a simplified example; adjust to match the real Cluedo board layout as needed)
        self.adjacency = {
            # Corridors between rooms (simplified linear/circular for now)
            "C1": ["Kitchen", "Ballroom", "C2"],
            "C2": ["C1", "Ballroom", "C3"],
            "C3": ["C2", "Conservatory", "C4"],
            "C4": ["C3", "Library", "C5"],
            "C5": ["C4", "Study", "C6"],
            "C6": ["C5", "Hall", "C7"],
            "C7": ["C6", "Lounge", "C8"],
            "C8": ["C7", "Dining Room", "C9"],
            "C9": ["C8", "Kitchen", "C10"],
            "C10": ["C9", "Billiard Room", "C11"],
            "C11": ["C10", "Ballroom", "C12"],
            "C12": ["C11", "Dining Room", "C1"],
            # Room to corridor connections (examples)
            "Kitchen": ["C1", "C9"],
            "Ballroom": ["C1", "C2", "C11"],
            "Conservatory": ["C3"],
            "Library": ["C4"],
            "Study": ["C5"],
            "Hall": ["C6"],
            "Lounge": ["C7"],
            "Dining Room": ["C8", "C12"],
            "Billiard Room": ["C10"]
        }

    def get_rooms(self):
        """Return a list of all rooms."""
        return self.rooms

    def get_corridors(self):
        """Return a list of all corridor spaces."""
        return self.corridors

    def get_all_spaces(self):
        """Return a list of all spaces (rooms + corridors)."""
        return self.rooms + self.corridors

    def get_adjacent_spaces(self, space):
        """Return a list of spaces adjacent to the given space (room or corridor)."""
        return self.adjacency.get(space, [])

    def get_adjacent_rooms(self, space):
        """Return a list of adjacent rooms (not corridors) for compatibility with legacy code/tests."""
        return [s for s in self.get_adjacent_spaces(space) if s in self.rooms]
