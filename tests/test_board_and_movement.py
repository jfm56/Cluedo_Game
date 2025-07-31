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
        """Test Mansion initialization."""
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
            assert f"C{i}" in mansion.corridors
        
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
        """Test get_adjacent_spaces method."""
        # Test room adjacency
        kitchen = mansion.room_lookup["Kitchen"]
        kitchen_adjacent = mansion.get_adjacent_spaces(kitchen)
        assert "C3" in kitchen_adjacent
        assert "C9" in kitchen_adjacent
        assert len(kitchen_adjacent) == 2
        
        # Test corridor adjacency
        c1_adjacent = mansion.get_adjacent_spaces("C1")
        assert mansion.room_lookup["Lounge"] in c1_adjacent
        assert "C7" in c1_adjacent
        assert len(c1_adjacent) == 2
        
        # Test intersection corridor
        c8_adjacent = mansion.get_adjacent_spaces("C8")
        assert "C2" in c8_adjacent
        assert mansion.room_lookup["Dining Room"] in c8_adjacent
        assert "C7" in c8_adjacent
        assert "C9" in c8_adjacent
        assert len(c8_adjacent) == 4
        
        # Test non-existent space
        assert mansion.get_adjacent_spaces("NonExistent") == []

    def test_get_adjacent_rooms(self, mansion):
        """Test get_adjacent_rooms method."""
        # Test corridor with adjacent rooms
        c1_adjacent_rooms = mansion.get_adjacent_rooms("C1")
        assert len(c1_adjacent_rooms) == 1
        assert mansion.room_lookup["Lounge"] in c1_adjacent_rooms
        
        # Test room with no adjacent rooms
        kitchen = mansion.room_lookup["Kitchen"]
        kitchen_adjacent_rooms = mansion.get_adjacent_rooms(kitchen)
        assert len(kitchen_adjacent_rooms) == 0
        
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
        mansion.get_rooms.return_value = ['Kitchen', 'Ballroom', 'Conservatory', 'Billiard Room']
        mansion.get_corridors.return_value = ['C1', 'C2', 'C3', 'C4', 'C5']
        
        # Mock rooms and corridors as actual rooms, not just strings
        rooms = ['Kitchen', 'Ballroom', 'Conservatory', 'Billiard Room']
        mansion.rooms = [MagicMock(name=room) for room in rooms]
        for mock_room, room_name in zip(mansion.rooms, rooms):
            mock_room.name = room_name
        
        # Mock adjacency map for strings (for testing)
        adjacency_map = {
            'Kitchen': ['C1', 'C5'],
            'Ballroom': ['C2', 'C3'],
            'Conservatory': ['C3'],
            'Billiard Room': ['C4', 'C5'],
            'C1': ['Kitchen', 'C2'],
            'C2': ['C1', 'Ballroom', 'C4'],
            'C3': ['Ballroom', 'Conservatory'],
            'C4': ['C2', 'Billiard Room'],
            'C5': ['Kitchen', 'Billiard Room']
        }
        
        # Mock the get_adjacent_spaces method
        mansion.get_adjacent_spaces.side_effect = lambda space: [
            next((r for r in mansion.rooms if r.name == adj), adj) 
            for adj in adjacency_map.get(getattr(space, 'name', space), [])
        ]
        
        return mansion
    
    @pytest.fixture
    def movement(self, mock_mansion):
        """Create a Movement instance with the mock mansion."""
        return Movement(mock_mansion)
    
    def test_init(self, mock_mansion):
        """Test the initialization of the Movement class."""
        movement = Movement(mock_mansion)
        assert movement.mansion == mock_mansion
    
    def test_get_destinations_from_with_zero_steps(self, movement):
        """Test getting destinations with zero steps (should return empty list)."""
        start_position = 'Kitchen'
        destinations = movement.get_destinations_from(start_position, 0)
        
        assert len(destinations) == 0
    
    def test_get_destinations_from_with_one_step(self, movement, mock_mansion):
        """Test getting destinations with one step."""
        # Setup expected adjacency
        start_position = 'Kitchen'
        mock_mansion.get_adjacent_spaces.side_effect = lambda space: ['C1', 'C5'] if getattr(space, 'name', space) == start_position else []
        mock_mansion.get_rooms.return_value = ['Kitchen']
    
        destinations = movement.get_destinations_from(start_position, 1)
    
        # Convert any Room objects to strings for easier assertion
        dest_names = [getattr(d, 'name', d) for d in destinations]
    
        # Should only include adjacent spaces (NOT starting position, per implementation)
        assert len(dest_names) == 2  # C1, C5
        assert 'C1' in dest_names
        assert 'C5' in dest_names
        
    def test_get_destinations_from_with_room_name_string(self, movement, mock_mansion):
        """Test getting destinations with a room name as string."""
        # Setup the test to convert a string room name to a Room object
        kitchen_room = mock_mansion.rooms[0]  # Kitchen room object
        mock_mansion.get_adjacent_spaces.side_effect = lambda space: ['C1', 'C5'] if space == kitchen_room else []
        
        # Call with string name instead of room object
        destinations = movement.get_destinations_from('Kitchen', 1)
        
        # Verify it correctly converted the string to a Room object
        assert len(destinations) == 2
        assert 'C1' in destinations
        assert 'C5' in destinations
    
    def test_get_destinations_from_with_multiple_steps(self, movement, mock_mansion):
        """Test getting destinations with multiple steps."""
        # Setup adjacency map for BFS traversal
        adjacency_map = {
            'Kitchen': ['C1', 'C5'],
            'C1': ['Kitchen', 'C2'],
            'C2': ['C1', 'Ballroom', 'C4'],
            'Ballroom': ['C2', 'C3'],
            'C3': ['Ballroom', 'Conservatory'],
            'Conservatory': ['C3'],
            'C4': ['C2', 'Billiard Room'],
            'Billiard Room': ['C4', 'C5'],
            'C5': ['Kitchen', 'Billiard Room']
        }
        
        # Mock get_adjacent_spaces for each space
        mock_mansion.get_adjacent_spaces.side_effect = lambda space: adjacency_map.get(getattr(space, 'name', space), [])
        
        # Test with 2 steps from Kitchen
        destinations = movement.get_destinations_from('Kitchen', 2)
        
        # Convert any Room objects to strings for easier assertion
        dest_names = [getattr(d, 'name', d) for d in destinations]
        
        # Should include all spaces reachable in 2 steps (but not starting point)
        expected_destinations = ['C1', 'C5', 'C2', 'Billiard Room']
        for expected in expected_destinations:
            assert expected in dest_names
        assert 'Kitchen' not in dest_names  # Starting point shouldn't be included
        assert 'Ballroom' not in dest_names  # 3 steps away, not reachable
    
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
        # Setup adjacent spaces to match what get_adjacent_spaces returns
        mock_mansion.get_adjacent_spaces.return_value = ['C1', 'C5']
        
        # Test with include_corridors flag
        neighboring_spaces = movement.get_neighboring_rooms('Kitchen', include_corridors=True)
        
        # The actual implementation returns corridors only, not rooms
        assert set(neighboring_spaces) == set(['C1', 'C5'])
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
