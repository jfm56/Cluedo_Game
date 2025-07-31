"""
Tests for the chess coordinate functionality in the Mansion class.
"""
import pytest
from unittest.mock import MagicMock

from cluedo_game.mansion import Mansion, Room


class TestChessCoordinates:
    """Test suite for chess coordinate functionality."""
    
    @pytest.fixture
    def mansion(self):
        """Create a Mansion instance for testing."""
        return Mansion()
    
    def test_chess_coordinate_mapping_exists(self, mansion):
        """Test that chess coordinate mapping exists."""
        assert hasattr(mansion, 'chess_coordinates')
        assert isinstance(mansion.chess_coordinates, dict)
        assert len(mansion.chess_coordinates) > 0
    
    def test_reverse_mapping_exists(self, mansion):
        """Test that reverse mapping exists."""
        assert hasattr(mansion, 'spaces_by_coordinates')
        assert isinstance(mansion.spaces_by_coordinates, dict)
        assert len(mansion.spaces_by_coordinates) > 0
        
    def test_get_chess_coordinate_for_room_object(self, mansion):
        """Test getting chess coordinate for a Room object."""
        kitchen = mansion.rooms[0]  # Kitchen
        coord = mansion.get_chess_coordinate(kitchen)
        assert coord == "A1"
        
    def test_get_chess_coordinate_for_room_name(self, mansion):
        """Test getting chess coordinate for a room name."""
        coord = mansion.get_chess_coordinate("Kitchen")
        assert coord == "A1"
        
        coord = mansion.get_chess_coordinate("Study")
        assert coord == "E5"
        
    def test_get_chess_coordinate_for_corridor(self, mansion):
        """Test getting chess coordinate for a corridor."""
        coord = mansion.get_chess_coordinate("C1")
        assert coord == "E2"
        
        coord = mansion.get_chess_coordinate("C5")
        assert coord == "B5"
        
    def test_get_space_from_coordinate(self, mansion):
        """Test getting space name from a chess coordinate."""
        space = mansion.get_space_from_coordinate("A1")
        assert space == "Kitchen"
        
        space = mansion.get_space_from_coordinate("E2")
        assert space == "C1"
        
    def test_unknown_coordinates(self, mansion):
        """Test behavior with unknown coordinates."""
        # Unknown space returns original input
        coord = mansion.get_chess_coordinate("Unknown Room")
        assert coord == "Unknown Room"
        
        # Unknown coordinate returns original input
        space = mansion.get_space_from_coordinate("Z9")
        assert space == "Z9"
        
    def test_display_with_chess_coordinates(self, mansion):
        """Test the display_with_chess_coordinates method."""
        display = mansion.display_with_chess_coordinates()
        
        # Check that the output is a string with expected content
        assert isinstance(display, str)
        assert "Mansion Board with Chess Coordinates:" in display
        assert "Rooms:" in display
        assert "Corridors:" in display
        assert "Kitchen: A1" in display
        assert "C1: E2" in display
