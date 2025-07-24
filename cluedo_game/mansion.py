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
        # List of corridor spaces (C1–C12) matching the visual board layout
        # C1: left of Lounge (Miss Scarlett start)
        # C2: below Dining Room (Colonel Mustard start)
        # C3: above Kitchen (Mrs. White start)
        # C4: above Ballroom (Reverend Green start)
        # C5: above Conservatory (Mrs. Peacock start)
        # C6: right of Study (Professor Plum start)
        # C7–C12: other corridor/intersection spaces, mapped clockwise
        self.corridors = [f"C{i}" for i in range(1, 13)]
        # Adjacency map matching board image
        self.adjacency = {
            # Corridors (outer edge, starting positions)
            "C1": ["Lounge", "C7"],                  # Miss Scarlett start
            "C2": ["Dining Room", "C8"],            # Colonel Mustard start
            "C3": ["Kitchen", "C9"],                # Mrs. White start
            "C4": ["Ballroom", "C10"],              # Reverend Green start
            "C5": ["Conservatory", "C11"],          # Mrs. Peacock start
            "C6": ["Study", "C12"],                 # Professor Plum start
            # Corridors (inner/intersection)
            "C7": ["C1", "Hall", "C8"],
            "C8": ["C2", "Dining Room", "C7", "C9"],
            "C9": ["C3", "Kitchen", "C8", "C10"],
            "C10": ["C4", "Ballroom", "C9", "C11"],
            "C11": ["C5", "Conservatory", "C10", "C12"],
            "C12": ["C6", "Study", "C11", "Hall"],
            # Room to corridor connections
            "Lounge": ["C1", "C7"],
            "Dining Room": ["C2", "C8"],
            "Kitchen": ["C3", "C9"],
            "Ballroom": ["C4", "C10"],
            "Conservatory": ["C5", "C11"],
            "Study": ["C6", "C12"],
            "Hall": ["C7", "C12"],
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
