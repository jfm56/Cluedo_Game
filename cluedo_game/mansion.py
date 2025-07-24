"""
Representation of the mansion layout for the Cluedo game.
Contains different rooms such as kitchen, library, ballroom, etc.
"""

class Room:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Room({self.name})"
    def __eq__(self, other):
        if isinstance(other, Room):
            return self.name == other.name
        return False
    def __hash__(self):
        return hash(self.name)

class Mansion:
    def __init__(self):
        # List of rooms in the mansion (as Room objects)
        self.rooms = [
            Room("Kitchen"),
            Room("Ballroom"),
            Room("Conservatory"),
            Room("Dining Room"),
            Room("Billiard Room"),
            Room("Library"),
            Room("Lounge"),
            Room("Hall"),
            Room("Study")
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
        # Helper: room lookup by name
        self.room_lookup = {room.name: room for room in self.rooms}
        self.adjacency = {
            # Corridors (outer edge, starting positions)
            "C1": [self.room_lookup["Lounge"], "C7"],                  # Miss Scarlett start
            "C2": [self.room_lookup["Dining Room"], "C8"],            # Colonel Mustard start
            "C3": [self.room_lookup["Kitchen"], "C9"],                # Mrs. White start
            "C4": [self.room_lookup["Ballroom"], "C10"],              # Reverend Green start
            "C5": [self.room_lookup["Conservatory"], "C11"],          # Mrs. Peacock start
            "C6": [self.room_lookup["Study"], "C12"],                 # Professor Plum start
            # Corridors (inner/intersection)
            "C7": ["C1", self.room_lookup["Hall"], "C8"],
            "C8": ["C2", self.room_lookup["Dining Room"], "C7", "C9"],
            "C9": ["C3", self.room_lookup["Kitchen"], "C8", "C10"],
            "C10": ["C4", self.room_lookup["Ballroom"], "C9", "C11"],
            "C11": ["C5", self.room_lookup["Conservatory"], "C10", "C12"],
            "C12": ["C6", self.room_lookup["Study"], "C11", self.room_lookup["Hall"]],
            # Room to corridor connections
            self.room_lookup["Lounge"]: ["C1", "C7"],
            self.room_lookup["Dining Room"]: ["C2", "C8"],
            self.room_lookup["Kitchen"]: ["C3", "C9"],
            self.room_lookup["Ballroom"]: ["C4", "C10"],
            self.room_lookup["Conservatory"]: ["C5", "C11"],
            self.room_lookup["Study"]: ["C6", "C12"],
            self.room_lookup["Hall"]: ["C7", "C12"],
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
