"""
Tests for the chess coordinate functionality in the Mansion class.
"""
import pytest
from unittest.mock import MagicMock, patch

from cluedo_game.mansion import Mansion, Room


class TestChessCoordinates:
    """Test suite for chess coordinate functionality."""
    
    @pytest.fixture
    def mansion(self):
        """Create a Mansion instance for testing."""
        return Mansion()
    
    def test_chess_coordinate_mapping_exists(self, mansion):
        """Test that chess coordinate mapping exists and has expected structure."""
        assert hasattr(mansion, 'chess_coordinates'), "Mansion should have chess_coordinates attribute"
        assert isinstance(mansion.chess_coordinates, dict), "chess_coordinates should be a dictionary"
        
        # Check all rooms have valid coordinates
        room_names = [room.name for room in mansion.rooms]
        for room in room_names:
            assert room in mansion.chess_coordinates, f"{room} is missing from chess_coordinates"
            coord = mansion.chess_coordinates[room]
            assert isinstance(coord, str), f"Coordinate for {room} should be a string"
            assert 2 <= len(coord) <= 3, f"Coordinate {coord} for {room} should be 2-3 characters"
            
            # Verify coordinate format (letter followed by number)
            assert coord[0].isalpha(), f"First character of {coord} should be a letter"
            assert coord[1:].isdigit(), f"Remaining characters of {coord} should be digits"
            
        # Check all corridors have valid coordinates
        for i in range(1, 13):
            corridor = f"C{i}"
            assert corridor in mansion.chess_coordinates, f"{corridor} is missing from chess_coordinates"
            coord = mansion.chess_coordinates[corridor]
            assert isinstance(coord, str), f"Coordinate for {corridor} should be a string"
            assert 2 <= len(coord) <= 3, f"Coordinate {coord} for {corridor} should be 2-3 characters"
            
            # Verify coordinate format (letter followed by number)
            assert coord[0].isalpha(), f"First character of {coord} should be a letter"
            assert coord[1:].isdigit(), f"Remaining characters of {coord} should be digits"
    
    def test_reverse_mapping_exists(self, mansion):
        """Test that reverse mapping exists and is consistent with forward mapping."""
        assert hasattr(mansion, 'spaces_by_coordinates'), "Mansion should have spaces_by_coordinates attribute"
        assert isinstance(mansion.spaces_by_coordinates, dict), "spaces_by_coordinates should be a dictionary"
        
        # Verify the reverse mapping is consistent with forward mapping
        for space, coord in mansion.chess_coordinates.items():
            assert coord in mansion.spaces_by_coordinates, f"Coordinate {coord} is missing from spaces_by_coordinates"
            assert mansion.spaces_by_coordinates[coord] == space, f"Reverse mapping for {coord} should be {space}"
        
        # Verify no duplicate coordinates exist
        all_coords = list(mansion.chess_coordinates.values())
        unique_coords = set(all_coords)
        assert len(all_coords) == len(unique_coords), "Duplicate coordinates found in chess_coordinates"
        
    def test_get_chess_coordinate_for_room_object(self, mansion):
        """Test getting chess coordinate for Room objects."""
        # Test all rooms have valid coordinates
        room_coords = {
            "Kitchen": "A1",
            "Dining Room": "C1",
            "Lounge": "E1",
            "Ballroom": "A3",
            "Billiard Room": "C3",
            "Hall": "E3",
            "Conservatory": "A5",
            "Library": "C5",
            "Study": "E5"
        }
        
        for room in mansion.rooms:
            coord = mansion.get_chess_coordinate(room)
            assert coord == room_coords[room.name], f"{room.name} should have coordinate {room_coords[room.name]}, got {coord}"
        
        # Test with a mock room object (not in mansion.rooms)
        mock_room = MagicMock(spec=Room)
        mock_room.name = "Secret Room"
        coord = mansion.get_chess_coordinate(mock_room)
        assert coord == "Secret Room", "Should return the room name for unknown rooms"
        
    def test_get_chess_coordinate_for_room_name(self, mansion):
        """Test getting chess coordinate for room names with various formats."""
        # Test all rooms with different name formats
        room_tests = [
            ("Kitchen", "A1"),
            ("Dining Room", "C1"),
            ("Lounge", "E1"),
            ("Ballroom", "A3"),
            ("Billiard Room", "C3"),
            ("Hall", "E3"),
            ("Conservatory", "A5"),
            ("Library", "C5"),
            ("Study", "E5"),
            # Test case variations
            ("KITCHEN", "A1"),
            ("dining room", "C1"),
            ("BiLlIaRd RoOm", "C3")
        ]
        
        for room_name, expected_coord in room_tests:
            coord = mansion.get_chess_coordinate(room_name)
            assert coord == expected_coord, f"{room_name} should map to {expected_coord}, got {coord}"
        
        # Test with unknown room name
        assert mansion.get_chess_coordinate("Nonexistent Room") == "Nonexistent Room", "Should return input for unknown rooms"
        assert mansion.get_chess_coordinate("") == "", "Should handle empty string"
        assert mansion.get_chess_coordinate(None) is None, "Should handle None input"
        
    def test_get_chess_coordinate_for_corridor(self, mansion):
        """Test getting chess coordinate for all corridors."""
        # Test all corridors have the correct coordinates
        corridor_tests = {
            "C1": "E2", "C2": "C2", "C3": "A2", "C4": "A4", "C5": "B5",
            "C6": "F5", "C7": "D2", "C8": "B2", "C9": "B3", "C10": "B4",
            "C11": "C4", "C12": "D4"
        }
        
        for corridor, expected_coord in corridor_tests.items():
            coord = mansion.get_chess_coordinate(corridor)
            assert coord == expected_coord, f"{corridor} should map to {expected_coord}, got {coord}"
        
        # Test with invalid corridor names
        assert mansion.get_chess_coordinate("C0") == "C0", "Should return input for C0"
        assert mansion.get_chess_coordinate("C13") == "C13", "Should return input for C13"
        assert mansion.get_chess_coordinate("X1") == "X1", "Should return input for invalid corridor format"
        
    def test_get_chess_coordinate_case_insensitive(self, mansion):
        """Test that get_chess_coordinate is case-insensitive for all spaces."""
        # Test room names with different cases
        test_cases = [
            ("KITCHEN", "A1"),
            ("kitchen", "A1"),
            ("KiTcHeN", "A1"),
            ("DINING ROOM", "C1"),
            ("dining room", "C1"),
            ("DiNiNg RoOm", "C1"),
            # Corridors
            ("c1", "E2"),
            ("C1", "E2"),
            ("c12", "D4"),
            ("C12", "D4")
        ]
        
        for input_str, expected_coord in test_cases:
            coord = mansion.get_chess_coordinate(input_str)
            assert coord == expected_coord, f"{input_str} should map to {expected_coord}, got {coord}"
        
    def test_get_space_from_coordinate(self, mansion):
        """Test getting space name from chess coordinates with various inputs."""
        # Test all room coordinates
        room_tests = {
            "A1": "Kitchen",
            "C1": "Dining Room",
            "E1": "Lounge",
            "A3": "Ballroom",
            "C3": "Billiard Room",
            "E3": "Hall",
            "A5": "Conservatory",
            "C5": "Library",
            "E5": "Study"
        }
        
        for coord, expected_space in room_tests.items():
            space = mansion.get_space_from_coordinate(coord)
            assert space == expected_space, f"{coord} should map to {expected_space}, got {space}"
        
        # Test corridor coordinates
        corridor_tests = {
            "E2": "C1", "C2": "C2", "A2": "C3", "A4": "C4", "B5": "C5",
            "F5": "C6", "D2": "C7", "B2": "C8", "B3": "C9", "B4": "C10",
            "C4": "C11", "D4": "C12"
        }
        
        for coord, expected_space in corridor_tests.items():
            space = mansion.get_space_from_coordinate(coord)
            assert space == expected_space, f"{coord} should map to {expected_space}, got {space}"
        
        # Test with invalid coordinates
        assert mansion.get_space_from_coordinate("Z99") == "Z99", "Should return input for unknown coordinates"
        assert mansion.get_space_from_coordinate("") == "", "Should handle empty string"
        assert mansion.get_space_from_coordinate(None) is None, "Should handle None input"
        
        # Test with space names (should pass through if not a coordinate)
        assert mansion.get_space_from_coordinate("Kitchen") == "Kitchen", "Should pass through space names"
        # C1 is a valid coordinate that maps to Dining Room, so it should not pass through
        assert mansion.get_space_from_coordinate("C1") == "Dining Room", "C1 should map to Dining Room"
        
        # Test with room coordinate in the middle of the board
        space = mansion.get_space_from_coordinate("C3")
        assert space == "Billiard Room", "C3 should map to Billiard Room"
        
    def test_unknown_coordinates(self, mansion):
        """Test behavior with unknown coordinates or spaces."""
        # Unknown space returns original input
        coord = mansion.get_chess_coordinate("Unknown Room")
        assert coord == "Unknown Room"
        
        # Empty string returns empty string
        coord = mansion.get_chess_coordinate("")
        assert coord == ""
        
        # None returns None
        coord = mansion.get_chess_coordinate(None)
        assert coord is None
        
        # Unknown coordinate returns original input
        space = mansion.get_space_from_coordinate("Z9")
        assert space == "Z9"
        
        # Invalid coordinate format returns as-is
        space = mansion.get_space_from_coordinate("Invalid123")
        assert space == "Invalid123"
        
        # Empty string returns empty string
        space = mansion.get_space_from_coordinate("")
        assert space == ""
        
        # None returns None
        space = mansion.get_space_from_coordinate(None)
        assert space is None
        
    def test_display_chess_coordinates(self, mansion, capsys):
        """Test displaying chess coordinates with proper formatting and completeness."""
        # Call the display method
        mansion.display_chess_coordinates()
        captured = capsys.readouterr()
        output = captured.out
        
        # Check that all rooms are displayed with their coordinates
        room_coords = [
            "Kitchen (A1)", "Ballroom (A3)", "Conservatory (A5)",
            "Dining Room (C1)", "Billiard Room (C3)", "Library (C5)",
            "Lounge (E1)", "Hall (E3)", "Study (E5)"
        ]
        
        # Check that all corridors are displayed with their coordinates
        corridor_coords = [
            "C1 (E2)", "C2 (C2)", "C3 (A2)", "C4 (A4)", "C5 (B5)",
            "C6 (F5)", "C7 (D2)", "C8 (B2)", "C9 (B3)", "C10 (B4)",
            "C11 (C4)", "C12 (D4)"
        ]
        
        # Verify all rooms are in the output
        for room in room_coords:
            assert room in output, f"{room} should be displayed in the output"
        
        # Verify all corridors are in the output
        for corridor in corridor_coords:
            assert corridor in output, f"{corridor} should be displayed in the output"
        
        # Verify the output is formatted nicely (basic check)
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        assert len(lines) > 10, "Output should have multiple lines"
        
        # Check for section headers
        assert "Chess Coordinates:" in output, "Should have a 'Chess Coordinates:' header"
        assert "Rooms:" in output, "Should have a 'Rooms:' section header"
        assert "Corridors:" in output, "Should have a 'Corridors:' section header"
        
        # Check that each line has the format "Name (XY)" where X is a letter and Y is a digit
        import re
        coord_pattern = re.compile(r'^[\w\s]+ \([A-Za-z]\d+\)$')
        
        for line in lines:
            # Skip section headers and empty lines
            if line.endswith(':') or not line.strip():
                continue
                
            assert coord_pattern.match(line), f"Line '{line}' doesn't match expected format 'Name (XY)'"
