"""
Tests for the board layout, rooms, and movement functionality in the Cluedo game.
This file consolidates tests for:
- Room and Mansion classes
- Movement and path-finding capabilities
- Board structure and adjacencies

Aims to achieve 90%+ code coverage.
"""
import pytest
from unittest.mock import MagicMock, patch

from cluedo_game.mansion import Mansion, Room
from cluedo_game.movement import Movement

# -----------------------------------------------------------------------------
# Room Tests
# -----------------------------------------------------------------------------
class TestRoom:
    """Test suite for the Room class."""

    def test_room_init(self):
        """Test Room initialization."""
        name = "Kitchen"
        room = Room(name)
        assert room.name == name

    def test_room_repr(self):
        """Test Room __repr__ method."""
        room = Room("Kitchen")
        assert repr(room) == "Room(Kitchen)"

    def test_room_equality(self):
        """Test Room equality comparison."""
        room1 = Room("Kitchen")
        room2 = Room("Kitchen")
        room3 = Room("Ballroom")

        assert room1 == room2
        assert room1 != room3
        assert room1 != "Kitchen"  # Different types

    def test_room_hash(self):
        """Test Room hash functionality for dictionary use."""
        room1 = Room("Kitchen")
        room2 = Room("Kitchen")
        
        # Same name should produce same hash
        assert hash(room1) == hash(room2)
        
        # Hash should be based on name
        assert hash(room1) == hash(room1.name)
        
        # Room objects with same name should work as dictionary keys
        room_dict = {room1: "Test Value"}
        assert room_dict[room2] == "Test Value"


# -----------------------------------------------------------------------------
# Mansion Tests
# -----------------------------------------------------------------------------
class TestMansion:
    """Test suite for the Mansion class."""

    @pytest.fixture
    def mansion(self):
        """Create a Mansion instance for testing."""
        return Mansion()

    def test_mansion_init(self, mansion):
        """Test Mansion initialization and board structure."""
        # Check rooms were created
        assert len(mansion.rooms) == 9
        assert all(isinstance(room, Room) for room in mansion.rooms)
        
        # Check room names
        room_names = [room.name for room in mansion.rooms]
        expected_rooms = [
            "Kitchen", "Ballroom", "Conservatory", "Dining Room", 
            "Billiard Room", "Library", "Lounge", "Hall", "Study"
        ]
        for expected in expected_rooms:
            assert expected in room_names
        
        # Check corridors
        assert len(mansion.corridors) == 12
        for i in range(1, 13):
            corridor = f"C{i}"
            assert corridor in mansion.corridors
            # Verify corridor is in adjacency map
            assert corridor in mansion.adjacency or any(corridor in adj for adj in mansion.adjacency.values())
        
        # Check room lookup
        assert len(mansion.room_lookup) == 9
        for room in mansion.rooms:
            assert mansion.room_lookup[room.name] == room
        
        # Check adjacency map
        assert len(mansion.adjacency) > 0
        
        # Check a few key adjacencies (based on the board layout)
        kitchen = mansion.room_lookup["Kitchen"]
        assert "C3" in mansion.adjacency[kitchen]
        assert "C9" in mansion.adjacency[kitchen]
        
        ballroom = mansion.room_lookup["Ballroom"]
        assert "C4" in mansion.adjacency[ballroom]
        assert "C10" in mansion.adjacency[ballroom]
        
        # Verify that rooms are only connected to corridors, not directly to other rooms
        for room in mansion.rooms:
            for adjacent in mansion.adjacency[room]:
                assert adjacent.startswith("C"), f"Room {room.name} is directly connected to non-corridor {adjacent}"

    def test_get_rooms(self, mansion):
        """Test get_rooms method."""
        rooms = mansion.get_rooms()
        assert len(rooms) == 9
        assert all(isinstance(room, Room) for room in rooms)
        assert rooms == mansion.rooms

    def test_get_corridors(self, mansion):
        """Test get_corridors method."""
        corridors = mansion.get_corridors()
        assert len(corridors) == 12
        assert all(isinstance(corridor, str) for corridor in corridors)
        assert all(corridor.startswith("C") for corridor in corridors)
        assert corridors == mansion.corridors

    def test_get_all_spaces(self, mansion):
        """Test get_all_spaces method."""
        all_spaces = mansion.get_all_spaces()
        assert len(all_spaces) == 21  # 9 rooms + 12 corridors
        assert all(space in all_spaces for space in mansion.rooms)
        assert all(space in all_spaces for space in mansion.corridors)

    def test_get_adjacent_spaces(self, mansion):
        """Test get_adjacent_spaces method with various space types."""
        # Test room adjacency (Kitchen)
        kitchen = mansion.room_lookup["Kitchen"]
        kitchen_adjacent = mansion.get_adjacent_spaces(kitchen)
        assert "C3" in kitchen_adjacent, "Kitchen should be adjacent to C3"
        assert "C9" in kitchen_adjacent, "Kitchen should be adjacent to C9"
        assert len(kitchen_adjacent) == 2, "Kitchen should have exactly 2 adjacent spaces"
        
        # Test starting corridor (C1 - Miss Scarlett's start)
        c1_adjacent = mansion.get_adjacent_spaces("C1")
        assert mansion.room_lookup["Lounge"] in c1_adjacent, "C1 should be adjacent to Lounge"
        assert "C7" in c1_adjacent, "C1 should be adjacent to C7"
        assert len(c1_adjacent) == 2, "C1 should have exactly 2 adjacent spaces"
        
        # Test intersection corridor (C8 - near Dining Room)
        c8_adjacent = mansion.get_adjacent_spaces("C8")
        assert "C2" in c8_adjacent, "C8 should be adjacent to C2"
        assert mansion.room_lookup["Dining Room"] in c8_adjacent, "C8 should be adjacent to Dining Room"
        assert "C7" in c8_adjacent, "C8 should be adjacent to C7"
        assert "C9" in c8_adjacent, "C8 should be adjacent to C9"
        assert len(c8_adjacent) == 4, "C8 should have exactly 4 adjacent spaces"
        
        # Test edge corridor (C6 - Professor Plum's start)
        c6_adjacent = mansion.get_adjacent_spaces("C6")
        assert mansion.room_lookup["Study"] in c6_adjacent, "C6 should be adjacent to Study"
        assert "C12" in c6_adjacent, "C6 should be adjacent to C12"
        assert len(c6_adjacent) == 2, "C6 should have exactly 2 adjacent spaces"
        
        # Test with invalid space (should return empty list or handle gracefully)
        invalid_adjacent = mansion.get_adjacent_spaces("InvalidSpace123")
        assert isinstance(invalid_adjacent, list), "Should return a list even for invalid spaces"
        assert len(invalid_adjacent) == 0, "Invalid space should have no adjacent spaces"
        
        # Test non-existent space
        assert mansion.get_adjacent_spaces("NonExistent") == []

    def test_get_adjacent_rooms(self, mansion):
        """Test get_adjacent_rooms method with various space types."""
        # From a corridor, should return adjacent rooms
        c1_adjacent_rooms = mansion.get_adjacent_rooms("C1")
        assert len(c1_adjacent_rooms) == 1, "C1 should be adjacent to 1 room (Lounge)"
        assert mansion.room_lookup["Lounge"] in c1_adjacent_rooms, "C1 should be adjacent to Lounge"
        
        # From an intersection corridor, should return adjacent rooms
        c8_adjacent_rooms = mansion.get_adjacent_rooms("C8")
        assert len(c8_adjacent_rooms) == 1, "C8 should be adjacent to 1 room (Dining Room)"
        assert mansion.room_lookup["Dining Room"] in c8_adjacent_rooms, "C8 should be adjacent to Dining Room"
        
        # From a room, should return empty list (rooms are only connected to corridors)
        kitchen = mansion.room_lookup["Kitchen"]
        kitchen_adjacent_rooms = mansion.get_adjacent_rooms(kitchen)
        assert len(kitchen_adjacent_rooms) == 0, "Rooms should not be directly connected to other rooms"
        
        # Test with invalid space (should return empty list)
        invalid_adjacent_rooms = mansion.get_adjacent_rooms("InvalidSpace123")
        assert isinstance(invalid_adjacent_rooms, list), "Should return a list even for invalid spaces"
        assert len(invalid_adjacent_rooms) == 0, "Invalid space should have no adjacent rooms"
        
        # Test with a room that has multiple corridor connections (should still return empty list)
        study = mansion.room_lookup["Study"]
        study_adjacent_rooms = mansion.get_adjacent_rooms(study)
        assert len(study_adjacent_rooms) == 0, "Rooms should never have adjacent rooms, only corridors"
        
        # Test intersection corridor with adjacent rooms
        c8_adjacent_rooms = mansion.get_adjacent_rooms("C8")
        assert len(c8_adjacent_rooms) == 1
        assert mansion.room_lookup["Dining Room"] in c8_adjacent_rooms


# -----------------------------------------------------------------------------
# Movement Tests
# -----------------------------------------------------------------------------
class TestMovement:
    """Test suite for the Movement class and its methods."""
    
    @pytest.fixture
    def mock_mansion(self):
        """Create a mock mansion with predefined rooms, corridors, and adjacency."""
        mansion = MagicMock(spec=Mansion)
        
        # Mock rooms and corridors
        mansion.rooms = [
            Room("Kitchen"), Room("Ballroom"), Room("Conservatory"), 
            Room("Dining Room"), Room("Billiard Room"), Room("Library"),
            Room("Lounge"), Room("Hall"), Room("Study")
        ]
        mansion.corridors = [f"C{i}" for i in range(1, 13)]
        
        # Create room lookup
        mansion.room_lookup = {room.name: room for room in mansion.rooms}
        
        # Mock chess coordinates
        mansion.chess_coordinates = {
            # Rooms
            "Kitchen": "A1", "Dining Room": "C1", "Lounge": "E1",
            "Ballroom": "A3", "Billiard Room": "C3", "Hall": "E3",
            "Conservatory": "A5", "Library": "C5", "Study": "E5",
            # Corridors
            "C1": "E2", "C2": "C2", "C3": "A2", "C4": "A4", "C5": "B5",
            "C6": "F5", "C7": "D2", "C8": "B2", "C9": "B3", "C10": "B4",
            "C11": "C4", "C12": "D4"
        }
        
        # Reverse mapping
        mansion.spaces_by_coordinates = {v: k for k, v in mansion.chess_coordinates.items()}
        
        # Create adjacency map matching the actual game board
        mansion.adjacency = {
            # Corridors (outer edge, starting positions)
            "C1": [mansion.room_lookup["Lounge"], "C7"],
            "C2": [mansion.room_lookup["Dining Room"], "C8"],
            "C3": [mansion.room_lookup["Kitchen"], "C9"],
            "C4": [mansion.room_lookup["Ballroom"], "C10"],
            "C5": [mansion.room_lookup["Conservatory"], "C11"],
            "C6": [mansion.room_lookup["Study"], "C12"],
            # Corridors (inner/intersection)
            "C7": ["C1", mansion.room_lookup["Hall"], "C8"],
            "C8": ["C2", mansion.room_lookup["Dining Room"], "C7", "C9"],
            "C9": ["C3", mansion.room_lookup["Kitchen"], "C8", "C10"],
            "C10": ["C4", mansion.room_lookup["Ballroom"], "C9", "C11"],
            "C11": ["C5", mansion.room_lookup["Conservatory"], "C10", "C12"],
            "C12": ["C6", mansion.room_lookup["Study"], "C11", mansion.room_lookup["Hall"]],
            # Rooms
            mansion.room_lookup["Lounge"]: ["C1", "C7"],
            mansion.room_lookup["Dining Room"]: ["C2", "C8"],
            mansion.room_lookup["Kitchen"]: ["C3", "C9"],
            mansion.room_lookup["Ballroom"]: ["C4", "C10"],
            mansion.room_lookup["Conservatory"]: ["C5", "C11"],
            mansion.room_lookup["Study"]: ["C6", "C12"],
            mansion.room_lookup["Hall"]: ["C7", "C12"],
            mansion.room_lookup["Billiard Room"]: ["C3"],
            mansion.room_lookup["Library"]: ["C5"]
        }
        
        # Mock get_adjacent_spaces to use our adjacency map
        def get_adjacent_spaces(space):
            if space is None:
                return []
                
            # Handle both string and Room object lookups
            if isinstance(space, Room):
                space = space.name
            
            # Special case for Room objects in the adjacency map
            for key, value in mansion.adjacency.items():
                if isinstance(key, Room) and key.name == space:
                    return value
                    
            # Default case for string lookups
            return mansion.adjacency.get(space, [])
            
        mansion.get_adjacent_spaces.side_effect = get_adjacent_spaces
        
        # Mock get_chess_coordinate
        def get_chess_coordinate(space):
            if isinstance(space, Room):
                space = space.name
            return mansion.chess_coordinates.get(space, space)
            
        mansion.get_chess_coordinate.side_effect = get_chess_coordinate
        
        # Mock get_space_from_coordinate
        def get_space_from_coordinate(coord):
            return mansion.spaces_by_coordinates.get(coord, coord)
            
        mansion.get_space_from_coordinate.side_effect = get_space_from_coordinate
        
        return mansion
    
    @pytest.fixture
    def movement(self, mock_mansion):
        """Create a Movement instance with the mock mansion."""
        return Movement(mock_mansion)
    
    def test_display_board(self, movement, capsys):
        """Test displaying the board with chess coordinates and verify all spaces are included."""
        movement.display_board()
        captured = capsys.readouterr()
        output = captured.out
        
        # Check all rooms are displayed with their chess coordinates
        room_coords = {
            "Kitchen (A1)", "Ballroom (A3)", "Conservatory (A5)",
            "Dining Room (C1)", "Billiard Room (C3)", "Library (C5)",
            "Lounge (E1)", "Hall (E3)", "Study (E5)"
        }
        
        # Check all corridors are displayed with their chess coordinates
        corridor_coords = {
            "C1 (E2)", "C2 (C2)", "C3 (A2)", "C4 (A4)", "C5 (B5)",
            "C6 (F5)", "C7 (D2)", "C8 (B2)", "C9 (B3)", "C10 (B4)",
            "C11 (C4)", "C12 (D4)"
        }
        
        # Verify all rooms are in the output
        for room in room_coords:
            assert room in output, f"{room} should be displayed in the board output"
        
        # Verify all corridors are in the output
        for corridor in corridor_coords:
            assert corridor in output, f"{corridor} should be displayed in the board output"
        
        # Verify the output is formatted nicely (basic check)
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        assert len(lines) > 15, "Board output should have multiple lines"
        
        # Check for section headers
        assert "Rooms:" in output, "Should have a 'Rooms:' section header"
        assert "Corridors:" in output, "Should have a 'Corridors:' section header"
        
        # Check that coordinates are in the correct format (letter followed by number)
        import re
        coord_pattern = r'[A-Za-z]\d+'
        for line in lines:
            if '(' in line and ')' in line:
                # Extract content between parentheses
                match = re.search(r'\((.*?)\)', line)
                if match:
                    coord = match.group(1)
                    assert re.fullmatch(coord_pattern, coord), f"Invalid coordinate format: {coord}"

    def test_init(self, mock_mansion):
        """Test the initialization of the Movement class."""
        movement = Movement(mock_mansion)
        assert movement.mansion == mock_mansion
    
    def test_get_destinations_from_with_zero_steps(self, movement, mock_mansion):
        """Test getting destinations with zero steps (should return empty list)."""
        # Test with room as starting point
        destinations = movement.get_destinations_from("Kitchen", 0)
        assert destinations == [], "With 0 steps, should return empty list"
        
        # Test with corridor as starting point
        destinations = movement.get_destinations_from("C1", 0)
        assert destinations == [], "With 0 steps, should return empty list"
        
        # Test with Room object as starting point
        kitchen = mock_mansion.room_lookup["Kitchen"]
        destinations = movement.get_destinations_from(kitchen, 0)
        assert destinations == [], "With 0 steps, should return empty list even with Room object"
    
    def test_get_destinations_from_with_one_step(self, movement, mock_mansion):
        """Test getting destinations with one step."""
        # Mock the mansion's get_adjacent_spaces to return expected values
        def mock_get_adjacent_spaces(space):
            if space == "Kitchen" or (hasattr(space, 'name') and space.name == "Kitchen"):
                return ["C3", "C9"]
            elif space == "C1":
                return ["Lounge", "C7"]
            elif space == "C8":
                return ["C2", "Dining Room", "C7", "C9"]
            return []
            
        mock_mansion.get_adjacent_spaces.side_effect = mock_get_adjacent_spaces
        
        # From a room, should get adjacent corridors
        kitchen_destinations = movement.get_destinations_from("Kitchen", 1)
        assert set(kitchen_destinations) == {"C3", "C9"}, "From Kitchen with 1 step, should reach C3 and C9"
        
        # From a corridor, should get adjacent rooms and corridors
        c1_destinations = movement.get_destinations_from("C1", 1)
        assert set(c1_destinations) == {"Lounge", "C7"}, "From C1 with 1 step, should reach Lounge and C7"
        
        # From an intersection corridor
        c8_destinations = movement.get_destinations_from("C8", 1)
        expected_destinations = {"C2", "Dining Room", "C7", "C9"}
        assert set(c8_destinations) == expected_destinations, f"From C8 with 1 step, should reach {expected_destinations}"
        
        # Test with Room object as starting point
        kitchen = mock_mansion.room_lookup["Kitchen"]
        kitchen_destinations = movement.get_destinations_from(kitchen, 1)
        assert set(kitchen_destinations) == {"C3", "C9"}, "Should work with Room objects as starting point"
    
    def test_get_destinations_from_with_room_name_string(self, movement, mock_mansion):
        """Test getting destinations with a room name as string."""
        # Mock the mansion's get_adjacent_spaces to return expected values
        def mock_get_adjacent_spaces(space):
            if space == "Kitchen" or (hasattr(space, 'name') and space.name == "Kitchen"):
                return ["C3", "C9"]
            elif space == "Dining Room" or (hasattr(space, 'name') and space.name == "Dining Room"):
                return ["C2", "C8"]
            return []
            
        mock_mansion.get_adjacent_spaces.side_effect = mock_get_adjacent_spaces
        
        # Should work the same as with Room object
        kitchen_destinations = movement.get_destinations_from("Kitchen", 1)
        assert set(kitchen_destinations) == {"C3", "C9"}, "Should work with room name as string"
        
        # Test with room that has a space in the name
        dining_room_destinations = movement.get_destinations_from("Dining Room", 1)
        assert set(dining_room_destinations) == {"C2", "C8"}, "Should work with room names containing spaces"
        
        # Test with invalid room name (should return empty list)
        invalid_destinations = movement.get_destinations_from("Nonexistent Room", 1)
        assert invalid_destinations == [], "Should return empty list for invalid room names"
        
        # Test with empty string (should return empty list)
        empty_destinations = movement.get_destinations_from("", 1)
        assert empty_destinations == [], "Should return empty list for empty string"
    
    def test_get_destinations_from_with_multiple_steps(self, movement, mock_mansion):
        """Test getting destinations with multiple steps."""
        # From Kitchen, 2 steps
        destinations = movement.get_destinations_from("Kitchen", 2)
        # Should include:
        # - C3's adjacents: Kitchen (already at start, excluded), C9
        # - C9's adjacents: Kitchen (already at start, excluded), C3, C8, C10
        # So with 2 steps from Kitchen, we can reach:
        # - C3 (1 step)
        # - C9 (1 step)
        # - C8 (via C9)
        # - C10 (via C9)
        expected = {"C3", "C9", "C8", "C10"}
        assert set(destinations) == expected, f"From Kitchen with 2 steps, should reach {expected}"
        
        # From C1 (Lounge's corridor), 3 steps
        destinations = movement.get_destinations_from("C1", 3)
        # Should be able to reach:
        # - 1 step: Lounge, C7
        # - 2 steps: From C7: Hall, C8
        # - 3 steps: From C8: C2, Dining Room, C9; From Hall: C12
        expected = {"Lounge", "C7", "Hall", "C8", "C2", "Dining Room", "C9", "C12"}
        assert set(destinations) == expected, f"From C1 with 3 steps, should reach {expected}"
        
        # Test with 2 steps from Kitchen
        destinations = movement.get_destinations_from('Kitchen', 2)
        
        # Convert any Room objects to strings for easier assertion
        dest_names = [getattr(d, 'name', d) for d in destinations]
        
        # Should include all spaces reachable in 2 steps (but not starting point)
        # From Kitchen (0 steps)
        # 1 step: C3, C9
        # 2 steps: From C3: Kitchen (excluded), C9 (already at 1 step)
        #          From C9: C3 (already at 1 step), C8, C10
        expected_destinations = ['C3', 'C9', 'C8', 'C10']
        for expected in expected_destinations:
            assert expected in dest_names, f"Expected {expected} in destinations but got {dest_names}"
        assert 'Kitchen' not in dest_names, "Starting point should not be included"
        assert len(dest_names) == len(expected_destinations), f"Expected {len(expected_destinations)} destinations but got {len(dest_names)}: {dest_names}"
    
    def test_get_destinations_from_corridor(self, movement, mock_mansion):
        """Test getting destinations starting from a corridor."""
        # Setup adjacency map
        adjacency_map = {
            'C1': ['Kitchen', 'C2'],
            'C2': ['C1', 'Ballroom', 'C4'],
            'Kitchen': ['C1'],
            'Ballroom': ['C2'],
            'C4': ['C2', 'Billiard Room'],
            'Billiard Room': ['C4']
        }
        
        # Mock get_adjacent_spaces for each space
        mock_mansion.get_adjacent_spaces.side_effect = lambda space: adjacency_map.get(getattr(space, 'name', space), [])
        
        # Test with 2 steps from corridor C1
        destinations = movement.get_destinations_from('C1', 2)
        
        # Convert any Room objects to strings for easier assertion
        dest_names = [getattr(d, 'name', d) for d in destinations]
        
        # Should include Kitchen, C2, Ballroom, C4 (all reachable in 2 steps)
        expected_destinations = ['Kitchen', 'C2', 'Ballroom', 'C4']
        for expected in expected_destinations:
            assert expected in dest_names
        assert 'C1' not in dest_names  # Starting point
        assert 'Billiard Room' not in dest_names  # 3 steps away
    
    def test_get_optimal_path_same_position(self, movement):
        """Test finding an optimal path when start and end are the same."""
        path = movement.get_optimal_path('Kitchen', 'Kitchen')
        
        # Path to self should be empty
        assert len(path) == 0
    
    def test_get_optimal_path_adjacent(self, movement, mock_mansion):
        """Test finding an optimal path when start and end are adjacent."""
        # Setup adjacency
        adjacency_map = {
            'Kitchen': ['C1'],
            'C1': ['Kitchen']
        }
        
        mock_mansion.get_adjacent_spaces.side_effect = lambda space: adjacency_map.get(getattr(space, 'name', space), [])
        
        # Get path from Kitchen to adjacent corridor C1
        path = movement.get_optimal_path('Kitchen', 'C1')
        
        # Path should just be [C1]
        assert len(path) == 1
        assert path[0] == 'C1'
        
        # Test reverse direction too
        path = movement.get_optimal_path('C1', 'Kitchen')
        assert len(path) == 1
        assert path[0] == 'Kitchen'
    
    def test_get_optimal_path_multiple_steps(self, movement, mock_mansion):
        """Test finding an optimal path requiring multiple steps."""
        # Setup a more complex adjacency map
        adjacency_map = {
            'Kitchen': ['C1'],
            'C1': ['Kitchen', 'C2'],
            'C2': ['C1', 'C3', 'Ballroom'],
            'C3': ['C2', 'C4'],
            'C4': ['C3', 'Conservatory'],
            'Ballroom': ['C2'],
            'Conservatory': ['C4']
        }
        
        mock_mansion.get_adjacent_spaces.side_effect = lambda space: adjacency_map.get(getattr(space, 'name', space), [])
        
        # Test Kitchen to Conservatory (requires multiple steps)
        path = movement.get_optimal_path('Kitchen', 'Conservatory')
        
        # The optimal path should be Kitchen -> C1 -> C2 -> C3 -> C4 -> Conservatory
        expected_path = ['C1', 'C2', 'C3', 'C4', 'Conservatory']
        assert path == expected_path
        
        # Test Kitchen to Ballroom (shorter path)
        path = movement.get_optimal_path('Kitchen', 'Ballroom')
        
        # The optimal path should be Kitchen -> C1 -> C2 -> Ballroom
        expected_path = ['C1', 'C2', 'Ballroom']
        assert path == expected_path
        
        # Test a path that doesn't exist
        mock_mansion.get_adjacent_spaces.return_value = []
        path = movement.get_optimal_path('Kitchen', 'NonExistentRoom')
        assert path == []
    
    def test_get_optimal_path_unreachable(self, movement, mock_mansion):
        """Test finding an optimal path when the destination is unreachable."""
        # Setup disjoint graph - no path exists
        mock_mansion.get_adjacent_spaces.return_value = []
        
        # Try to get path between disconnected locations
        path = movement.get_optimal_path('Kitchen', 'Ballroom')
        
        # Should return empty list (no path)
        assert path == []
    
    def test_get_optimal_path_limited_steps(self, movement, mock_mansion):
        """Test finding an optimal path with limited steps."""
        # Setup a linear path requiring 4 steps
        adjacency_map = {
            'Kitchen': ['C1'],
            'C1': ['Kitchen', 'C2'],
            'C2': ['C1', 'C3'],
            'C3': ['C2', 'C4'],
            'C4': ['C3', 'Ballroom'],
            'Ballroom': ['C4']
        }
        
        mock_mansion.get_adjacent_spaces.side_effect = lambda space: adjacency_map.get(getattr(space, 'name', space), [])
        
        # Test with exactly enough steps
        path = movement.get_optimal_path('Kitchen', 'Ballroom', max_steps=5)
        expected_path = ['C1', 'C2', 'C3', 'C4', 'Ballroom']
        assert path == expected_path
        
        # Test with more than enough steps
        path = movement.get_optimal_path('Kitchen', 'Ballroom', max_steps=10)
        assert path == expected_path  # Same result, still optimal
        
        # Test with not enough steps
        path = movement.get_optimal_path('Kitchen', 'Ballroom', max_steps=4)
        assert path == []  # Can't reach it in 4 steps
        
        # Test with 0 steps
        path = movement.get_optimal_path('Kitchen', 'Ballroom', max_steps=0)
        assert path == []
    
    def test_is_path_possible(self, movement, mock_mansion):
        """Test if a path is possible within given steps."""
        # Setup multi-step path
        adjacency_map = {
            'Kitchen': ['C1'],
            'C1': ['Kitchen', 'C2'],
            'C2': ['C1', 'Ballroom'],
            'Ballroom': ['C2']
        }
        
        mock_mansion.get_adjacent_spaces.side_effect = lambda space: adjacency_map.get(getattr(space, 'name', space), [])
        
        # Test with enough steps
        assert movement.is_path_possible('Kitchen', 'Ballroom', 3) is True
        
        # Test with too few steps
        assert movement.is_path_possible('Kitchen', 'Ballroom', 1) is False
    
    def test_get_neighboring_rooms(self, movement, mock_mansion):
        """Test getting neighboring rooms from a position."""
        # Setup mock method
        mock_mansion.get_adjacent_rooms.return_value = [mock_mansion.rooms[1], mock_mansion.rooms[3]]  # Ballroom and Billiard Room
        
        # Test without include_corridors flag
        neighboring_rooms = movement.get_neighboring_rooms('Kitchen')
        assert neighboring_rooms == [mock_mansion.rooms[1], mock_mansion.rooms[3]]
        mock_mansion.get_adjacent_rooms.assert_called_once_with('Kitchen')
        
    def test_get_neighboring_rooms_with_corridors(self, movement, mock_mansion):
        """Test getting neighboring rooms including corridors."""
        # Setup adjacent spaces to match what get_adjacent_spaces returns for Kitchen
        # According to the board layout, Kitchen is connected to C3 and C9
        mock_mansion.get_adjacent_spaces.return_value = ['C3', 'C9']
        
        # Test with include_corridors flag
        neighboring_spaces = movement.get_neighboring_rooms('Kitchen', include_corridors=True)
        
        # The actual implementation returns corridors only, not rooms
        assert set(neighboring_spaces) == set(['C3', 'C9']), \
            f"Expected neighboring corridors to be ['C3', 'C9'] but got {neighboring_spaces}"
        mock_mansion.get_adjacent_spaces.assert_called_once_with('Kitchen')
        
    def test_find_closest_room(self, movement, mock_mansion):
        """Test finding the closest room from a position."""
        # Setup mocks
        kitchen_room = mock_mansion.rooms[0]  # Kitchen
        ballroom_room = mock_mansion.rooms[1]  # Ballroom
        conservatory_room = mock_mansion.rooms[2]  # Conservatory
        billiard_room = mock_mansion.rooms[3]  # Billiard Room
        
        all_rooms = [kitchen_room, ballroom_room, conservatory_room, billiard_room]
        mock_mansion.get_rooms.return_value = all_rooms
        
        # Set up the BFS traversal simulation
        adjacency_map = {
            'C1': [kitchen_room, 'C2'],
            'C2': ['C1', ballroom_room],
            kitchen_room: ['C1'],
            ballroom_room: ['C2'],
            conservatory_room: ['C3'],
            billiard_room: ['C4']
        }
                
        mock_mansion.get_adjacent_spaces.side_effect = lambda space: adjacency_map.get(space, [])
        
        # Test finding closest room without filter
        result, distance = movement.find_closest_room('C1')
        assert result == kitchen_room  # Kitchen should be found first
        assert distance == 1
        
        # Test finding with filter (only Ballroom)
        room_filter = lambda r: r == ballroom_room
        result, distance = movement.find_closest_room('C1', room_filter=room_filter)
        assert result == ballroom_room
        assert distance == 2
        
    def test_find_closest_room_no_match(self, movement, mock_mansion):
        """Test finding the closest room when none match the filter."""
        # Setup no matching rooms
        all_rooms = [mock_mansion.rooms[0], mock_mansion.rooms[1]]  # Kitchen, Ballroom
        mock_mansion.get_rooms.return_value = all_rooms
        
        # Empty adjacency - no paths to any rooms
        mock_mansion.get_adjacent_spaces.return_value = []
        
        # Test with a filter that no room can satisfy
        room_filter = lambda r: False
        result, distance = movement.find_closest_room('C1', room_filter=room_filter)
        assert result is None
        assert distance == float('inf')
