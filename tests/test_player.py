"""
Tests for the Player class in the Cluedo game.
Aims to achieve 90%+ code coverage.
"""
import pytest
from unittest.mock import MagicMock

from cluedo_game.player import Player
from cluedo_game.cards import SuspectCard


class TestPlayer:
    """Test suite for the Player class."""
    
    @pytest.fixture
    def mock_suspect(self):
        """Create a mock suspect card."""
        suspect = MagicMock(spec=SuspectCard)
        suspect.name = "Colonel Mustard"
        return suspect
    
    @pytest.fixture
    def player(self, mock_suspect):
        """Create a Player instance with a mock suspect card."""
        return Player(mock_suspect)
    
    def test_init(self, mock_suspect):
        """Test the initialization of the Player class."""
        player = Player(mock_suspect)
        
        assert player.character == mock_suspect
        assert player.name == mock_suspect.name
        assert player.position is None
        assert player.hand == []
        assert player.eliminated is False
        assert player.is_human is True
        
    def test_init_ai_player(self, mock_suspect):
        """Test the initialization of an AI Player."""
        player = Player(mock_suspect, is_human=False)
        
        assert player.character == mock_suspect
        assert player.is_human is False
    
    def test_add_card(self, player):
        """Test adding a card to the player's hand."""
        card = MagicMock()
        card.name = "Test Card"
        player.add_card(card)
        
        assert card in player.hand
        assert len(player.hand) == 1
    
    def test_position_property(self, player):
        """Test the position property getter and setter."""
        # Initial position should be None
        assert player.position is None
        
        # Set position to a new value
        test_position = "Kitchen"
        player.position = test_position
        
        # Check if position was updated
        assert player.position == test_position
    
    def test_repr(self, player, mock_suspect):
        """Test the string representation of a Player instance."""
        expected = f"Player({mock_suspect}, hand=[], is_human=True)"
        assert repr(player) == expected
        
        # Add a card and check the updated representation
        card = MagicMock()
        player.add_card(card)
        expected = f"Player({mock_suspect}, hand=[{card}], is_human=True)"
        assert repr(player) == expected
        

