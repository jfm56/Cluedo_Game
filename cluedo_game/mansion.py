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
        
        # Create a mapping of room names to Room objects for faster lookup
        self._room_map = {room.name: room for room in self.rooms}
        self.room_lookup = {room.name: room for room in self.rooms}
        
        # List of corridor spaces (C1–C12) matching the visual board layout
        # C1: left of Lounge (Miss Scarlett start)
        # C2: below Dining Room (Colonel Mustard start)
        # C3: above Kitchen (Mrs. White start)
        # C4: above Ballroom (Reverend Green start)
        # C5: above Conservatory (Mrs. Peacock start)
        # C6: right of Study (Professor Plum start)
        # C7–C12: other corridor/intersection spaces, mapped clockwise
        self.corridors = [f"C{i}" for i in range(1, 13)]
        
        # Chess-like coordinate system
        # Map each space (rooms and corridors) to a chess-like coordinate
        self.chess_coordinates = {
            # Rooms mapped to their approximate center points
            "Kitchen": "A1",
            "Dining Room": "C1",
            "Lounge": "E1",
            "Ballroom": "A3",
            "Billiard Room": "C3",
            "Hall": "E3",
            "Conservatory": "A5",
            "Library": "C5",
            "Study": "E5",
            
            # Corridors mapped to their locations
            "C1": "E2",  # Miss Scarlett start (left of Lounge)
            "C2": "C2",  # Colonel Mustard start (below Dining Room)
            "C3": "A2",  # Mrs. White start (above Kitchen)
            "C4": "A4",  # Reverend Green start (above Ballroom)
            "C5": "B5",  # Mrs. Peacock start (above Conservatory)
            "C6": "F5",  # Professor Plum start (right of Study)
            "C7": "D2",  # Corridor between Lounge and Hall
            "C8": "B2",  # Corridor near Dining Room and Kitchen
            "C9": "B3",  # Corridor near Kitchen and Ballroom
            "C10": "B4", # Corridor near Ballroom and Conservatory
            "C11": "C4", # Corridor near Conservatory and Library
            "C12": "D4"  # Corridor near Library and Study
        }
        
        # Reverse mapping from chess coordinates to spaces
        self.spaces_by_coordinates = {coord: space for space, coord in self.chess_coordinates.items()}
        
        # Secret passages connect specific rooms diagonally across the board
        self.secret_passages = {
            self.room_lookup["Kitchen"]: self.room_lookup["Study"],
            self.room_lookup["Study"]: self.room_lookup["Kitchen"],
            self.room_lookup["Conservatory"]: self.room_lookup["Lounge"],
            self.room_lookup["Lounge"]: self.room_lookup["Conservatory"]
        }
        
        # Adjacency map matching board image
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
            "C9": ["C3", self.room_lookup["Kitchen"], "C8", "C10", self.room_lookup["Billiard Room"]],
            "C10": ["C4", self.room_lookup["Ballroom"], "C9", "C11"],
            "C11": ["C5", self.room_lookup["Conservatory"], "C10", "C12", self.room_lookup["Billiard Room"], self.room_lookup["Library"]],
            "C12": ["C6", self.room_lookup["Study"], "C11", self.room_lookup["Hall"], self.room_lookup["Library"]],
            # Room to corridor connections
            self.room_lookup["Lounge"]: ["C1", "C7"],
            self.room_lookup["Dining Room"]: ["C2", "C8"],
            self.room_lookup["Kitchen"]: ["C3", "C9"],
            self.room_lookup["Ballroom"]: ["C4", "C10"],
            self.room_lookup["Billiard Room"]: ["C9", "C11"],  # Billiard Room connects to C9 and C11
            self.room_lookup["Library"]: ["C11", "C12"],  # Library connects to C11 and C12
            self.room_lookup["Conservatory"]: ["C5", "C11"],
            self.room_lookup["Study"]: ["C6", "C12"],
            self.room_lookup["Hall"]: ["C7", "C12"],
        }
        
    def get_room(self, position):
        """Get the Room object for a given position if it's a room.
        
        Args:
            position: The position to check (can be a Room object or room name)
            
        Returns:
            Room: The Room object if the position is a room, None otherwise
        """
        if position is None:
            return None
            
        # If position is already a Room object
        if isinstance(position, Room):
            return position if position.name in self._room_map else None
            
        # If position is a room name
        if isinstance(position, str):
            return self._room_map.get(position)
            
        return None


    def get_rooms(self):
        """Return a list of all rooms."""
        return self.rooms

    def get_corridors(self):
        """Return a list of all corridor spaces."""
        return self.corridors

    def get_all_spaces(self):
        """Return a list of all spaces (rooms + corridors)."""
        return self.rooms + self.corridors

    def get_adjacent_spaces(self, space, include_secret_passages=False):
        """
        Return a list of spaces adjacent to the given space (room or corridor).
        
        Args:
            space: The space (room or corridor) to get adjacent spaces for
            include_secret_passages: If True, includes secret passages in the result
                                    (default is False for normal movement)
        """
        # Get normal adjacency (corridors for rooms, rooms/corridors for corridors)
        adjacent = self.adjacency.get(space, []).copy()
        
        # Add secret passage if this room has one and they're enabled
        if include_secret_passages and space in self.secret_passages:
            adjacent.append(self.secret_passages[space])
            
        return adjacent

    def get_adjacent_rooms(self, space):
        """
        Return a list of adjacent rooms (not corridors) for the given space.
        
        Args:
            space: The space (room or corridor) to get adjacent rooms for
            
        Returns:
            List[Room]: List of adjacent rooms (empty list if none)
        """
        # For rooms, they should only be adjacent to corridors, not other rooms
        if space in self.rooms:
            return []
            
        # For corridors, return adjacent rooms (not other corridors)
        return [s for s in self.adjacency.get(space, []) if s in self.rooms]
        
    def get_chess_coordinate(self, space):
        """Convert a space name or Room object to its chess coordinate (e.g., A1, B2).
        
        Args:
            space: A Room object, room name (case-insensitive), or corridor name (case-insensitive)
            
        Returns:
            str: The chess coordinate (e.g., 'A1', 'E2') or the original space name if not found
        """
        if space is None:
            return None
            
        # If it's a Room object, get its name
        if hasattr(space, 'name'):
            space = space.name
            
        if not isinstance(space, str):
            return str(space)
            
        # Normalize input to handle case insensitivity
        space = space.strip()
        if not space:
            return ""
            
        # Check if it's a corridor (C followed by digits)
        if space.upper().startswith('C'):
            try:
                # Extract corridor number and normalize format (e.g., 'c1' -> 'C1')
                corridor_num = int(space[1:])
                if 1 <= corridor_num <= 12:
                    corridor = f"C{corridor_num}"
                    # Return the mapped coordinate for the corridor (e.g., 'C1' -> 'E2')
                    return self.chess_coordinates.get(corridor, corridor)
            except (ValueError, IndexError):
                pass  # Not a valid corridor number, continue with normal lookup
                
        # Try exact match first (case-sensitive)
        if space in self.chess_coordinates:
            return self.chess_coordinates[space]
            
        # Try case-insensitive match for room names
        space_lower = space.lower()
        for name, coord in self.chess_coordinates.items():
            if isinstance(name, str) and name.lower() == space_lower:
                return coord
                
        # If not found, return the original space
        return space
    
    def get_space_from_coordinate(self, coordinate):
        """Convert a chess coordinate (e.g., A1, B2) to its corresponding space name.
        
        Args:
            coordinate: A chess coordinate (e.g., 'A1', 'E2') or a space name to pass through
            
        Returns:
            str: The space name (room or corridor) or the original coordinate if not found
        """
        if coordinate is None:
            return None
            
        # If input is a Room object, return its name
        if hasattr(coordinate, 'name'):
            return coordinate.name
            
        if not isinstance(coordinate, str):
            return str(coordinate)
            
        # Normalize input
        coordinate = coordinate.strip()
        if not coordinate:
            return ""
            
        # First try exact match for coordinates (e.g., 'A1' -> 'Kitchen', 'E2' -> 'C1')
        if coordinate in self.spaces_by_coordinates:
            return self.spaces_by_coordinates[coordinate]
            
        # Try case-insensitive match for coordinates
        coordinate_upper = coordinate.upper()
        for coord, space in self.spaces_by_coordinates.items():
            if coord.upper() == coordinate_upper:
                return space
                
        # Check if it's a corridor name (C followed by digits)
        if coordinate.upper().startswith('C'):
            try:
                # Extract corridor number and normalize format (e.g., 'c1' -> 'C1')
                corridor_num = int(coordinate[1:])
                if 1 <= corridor_num <= 12:
                    return f"C{corridor_num}"  # Return normalized corridor name
            except (ValueError, IndexError):
                pass  # Not a valid corridor number, continue with normal lookup
                
        # Try exact match for coordinates (e.g., 'A1' -> 'Kitchen', 'E2' -> 'C1')
        if coordinate in self.spaces_by_coordinates:
            return self.spaces_by_coordinates[coordinate]
            
        # Try case-insensitive match for coordinates
        coordinate_upper = coordinate.upper()
        for coord, space in self.spaces_by_coordinates.items():
            if coord.upper() == coordinate_upper:
                return space
                
        # If not found, return the original coordinate
        return coordinate
    
    def display_with_chess_coordinates(self):
        """Return a string representation of the mansion with chess coordinates and secret passages."""
        output = []
        output.append("Mansion Layout with Chess Coordinates:")
        output.append("=" * 50)
        
        # Add rooms section
        output.append("\nRooms:")
        rooms_with_coords = [(room.name, self.chess_coordinates[room.name]) 
                           for room in self.rooms 
                           if room.name in self.chess_coordinates]
        
        # Sort by coordinate (A1, A3, A5, C1, etc.)
        rooms_with_coords.sort(key=lambda x: (x[1][1], x[1][0]))
        
        for name, coord in rooms_with_coords:
            room = self.room_lookup[name]
            secret_passage = self.secret_passages.get(room)
            passage_info = f" (Secret passage to {secret_passage.name})" if secret_passage else ""
            output.append(f"- {name}: {coord}{passage_info}")
        
        # Add corridors section
        output.append("\nCorridors:")
        corridors_with_coords = [(f"C{i}", self.chess_coordinates[f"C{i}"]) 
                               for i in range(1, 13) 
                               if f"C{i}" in self.chess_coordinates]
        
        # Sort by coordinate
        corridors_with_coords.sort(key=lambda x: (x[1][1], x[1][0]))
        
        for name, coord in corridors_with_coords:
            output.append(f"- {name}: {coord}")
            
        # Add secret passages legend
        output.append("\nSecret Passages:")
        output.append("Kitchen <-> Study")
        output.append("Conservatory <-> Lounge")
        
        return "\n".join(output)

    def display_chess_coordinates(self):
        """Display all rooms and corridors with their chess coordinates.
        
        The output will be in the format:
        Chess Coordinates:
        Rooms:
          Room Name (XY)
          ...
        Corridors:
          C1 (XY)
          ...
        """
        print("Chess Coordinates:")
        print("Rooms:")
        for room in sorted(self.rooms, key=lambda r: r.name):
            coord = self.get_chess_coordinate(room)
            print(f"  {room.name} ({coord})")
        
        print("\nCorridors:")
        for corridor in sorted(self.corridors):
            coord = self.get_chess_coordinate(corridor)
            print(f"  {corridor} ({coord})")
