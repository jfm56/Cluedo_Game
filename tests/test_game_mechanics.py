"""
Tests for the game mechanics in the Cluedo game.
This file consolidates tests for:
- Accusation functionality
- Solution management
- Suggestion mechanics

Aims to achieve 90%+ code coverage.
"""
import pytest
from unittest.mock import MagicMock, patch, call

from cluedo_game.accusation import make_accusation
from cluedo_game.solution import Solution
from cluedo_game.suggestion import Suggestion
from cluedo_game.cards import SuspectCard, WeaponCard, RoomCard
from cluedo_game.player import Player
from cluedo_game.character import Character, get_characters
from cluedo_game.weapon import Weapon, get_weapons
from cluedo_game.mansion import Mansion


# -----------------------------------------------------------------------------
# Accusation Tests
# -----------------------------------------------------------------------------
class TestAccusation:
    """Test suite for accusation functionality."""
    
    @pytest.fixture
    def mock_game(self):
        """Fixture for creating a mock game object."""
        game = MagicMock()
        game.output = MagicMock()  # Mock the output function
        return game
    
    @pytest.fixture
    def mock_player(self):
        """Fixture for creating a mock player object."""
        player = MagicMock(spec=Player)
        player.eliminated = False
        return player
    
    @pytest.fixture
    def mock_suspect(self):
        """Fixture for creating a mock suspect card."""
        suspect = MagicMock(spec=SuspectCard)
        suspect.name = "Colonel Mustard"
        return suspect
    
    @pytest.fixture
    def mock_weapon(self):
        """Fixture for creating a mock weapon card."""
        weapon = MagicMock(spec=WeaponCard)
        weapon.name = "Candlestick"
        return weapon
    
    @pytest.fixture
    def mock_room(self):
        """Fixture for creating a mock room card."""
        room = MagicMock(spec=RoomCard)
        room.name = "Library"
        return room
    
    def test_correct_accusation(self, mock_game, mock_player, mock_suspect, mock_weapon, mock_room):
        """Test that a correct accusation results in a win."""
        # Set up the game solution to match the accusation
        mock_game.solution = Solution(mock_suspect, mock_weapon, mock_room)
        
        # Make the accusation
        result = make_accusation(mock_game, mock_player, mock_suspect, mock_weapon, mock_room)
        
        # Verify the result and output
        assert result is True
        mock_game.output.assert_has_calls([
            call("\nCongratulations! You Win!"),
            call(f"The solution was: {mock_suspect.name} with the {mock_weapon.name} in the {mock_room.name}.")
        ])
        assert mock_player.eliminated is False  # Player should not be eliminated
    
    def test_incorrect_accusation_wrong_suspect(self, mock_game, mock_player, mock_suspect, mock_weapon, mock_room):
        """Test that an accusation with the wrong suspect results in elimination."""
        # Create a different suspect for the solution
        different_suspect = MagicMock(spec=SuspectCard)
        different_suspect.name = "Professor Plum"
        
        # Set up the game solution with a different suspect
        mock_game.solution = Solution(different_suspect, mock_weapon, mock_room)
        
        # Make the accusation
        result = make_accusation(mock_game, mock_player, mock_suspect, mock_weapon, mock_room)
        
        # Verify the result and output
        assert result is False
        mock_game.output.assert_called_with("Incorrect accusation. You are eliminated and may not move, suggest, or accuse for the rest of the game.")
        assert mock_player.eliminated is True  # Player should be eliminated
    
    def test_incorrect_accusation_wrong_weapon(self, mock_game, mock_player, mock_suspect, mock_weapon, mock_room):
        """Test that an accusation with the wrong weapon results in elimination."""
        # Create a different weapon for the solution
        different_weapon = MagicMock(spec=WeaponCard)
        different_weapon.name = "Rope"
        
        # Set up the game solution with a different weapon
        mock_game.solution = Solution(mock_suspect, different_weapon, mock_room)
        
        # Make the accusation
        result = make_accusation(mock_game, mock_player, mock_suspect, mock_weapon, mock_room)
        
        # Verify the result and output
        assert result is False
        mock_game.output.assert_called_with("Incorrect accusation. You are eliminated and may not move, suggest, or accuse for the rest of the game.")
        assert mock_player.eliminated is True  # Player should be eliminated
    
    def test_incorrect_accusation_wrong_room(self, mock_game, mock_player, mock_suspect, mock_weapon, mock_room):
        """Test that an accusation with the wrong room results in elimination."""
        # Create a different room for the solution
        different_room = MagicMock(spec=RoomCard)
        different_room.name = "Kitchen"
        
        # Set up the game solution with a different room
        mock_game.solution = Solution(mock_suspect, mock_weapon, different_room)
        
        # Make the accusation
        result = make_accusation(mock_game, mock_player, mock_suspect, mock_weapon, mock_room)
        
        # Verify the result and output
        assert result is False
        mock_game.output.assert_called_with("Incorrect accusation. You are eliminated and may not move, suggest, or accuse for the rest of the game.")
        assert mock_player.eliminated is True  # Player should be eliminated
    
    def test_incorrect_accusation_all_wrong(self, mock_game, mock_player, mock_suspect, mock_weapon, mock_room):
        """Test that an accusation with all wrong components results in elimination."""
        # Create different cards for the solution
        different_suspect = MagicMock(spec=SuspectCard)
        different_suspect.name = "Mrs. White"
        
        different_weapon = MagicMock(spec=WeaponCard)
        different_weapon.name = "Revolver"
        
        different_room = MagicMock(spec=RoomCard)
        different_room.name = "Billiard Room"
        
        # Set up the game solution with all different components
        mock_game.solution = Solution(different_suspect, different_weapon, different_room)
        
        # Make the accusation
        result = make_accusation(mock_game, mock_player, mock_suspect, mock_weapon, mock_room)
        
        # Verify the result and output
        assert result is False
        mock_game.output.assert_called_with("Incorrect accusation. You are eliminated and may not move, suggest, or accuse for the rest of the game.")
        assert mock_player.eliminated is True  # Player should be eliminated


# -----------------------------------------------------------------------------
# Solution Tests
# -----------------------------------------------------------------------------
class TestSolution:
    """Test suite for the Solution class and its methods."""
    
    @pytest.fixture
    def mock_suspect(self):
        """Create a mock suspect card."""
        suspect = MagicMock(spec=SuspectCard)
        suspect.name = "Colonel Mustard"
        return suspect
    
    @pytest.fixture
    def mock_weapon(self):
        """Create a mock weapon card."""
        weapon = MagicMock(spec=WeaponCard)
        weapon.name = "Candlestick"
        return weapon
        
    @pytest.fixture
    def mock_character(self):
        """Create a mock character."""
        character = MagicMock(spec=Character)
        character.name = "Colonel Mustard"
        return character
        
    @pytest.fixture
    def mock_physical_weapon(self):
        """Create a mock physical weapon."""
        weapon = MagicMock(spec=Weapon)
        weapon.name = "Candlestick"
        return weapon
    
    @pytest.fixture
    def mock_room(self):
        """Create a mock room card."""
        room = MagicMock(spec=RoomCard)
        room.name = "Library"
        return room
    
    @pytest.fixture
    def solution(self, mock_suspect, mock_weapon, mock_room):
        """Create a Solution instance with mock cards."""
        return Solution(mock_suspect, mock_weapon, mock_room)
    
    def test_init(self, mock_suspect, mock_weapon, mock_room):
        """Test the initialization of the Solution class."""
        solution = Solution(mock_suspect, mock_weapon, mock_room)
        
        assert solution.character == mock_suspect
        assert solution.weapon == mock_weapon
        assert solution.room == mock_room
    
    def test_repr_representation(self, solution, mock_suspect, mock_weapon, mock_room):
        """Test the string representation of a Solution instance."""
        expected_string = f"Solution: {mock_suspect.name} with the {mock_weapon.name} in the {mock_room}"
        assert repr(solution) == expected_string
    
    def test_random_solution(self):
        """Test the random_solution factory method."""
        with patch('cluedo_game.solution.random') as mock_random:
            with patch('cluedo_game.solution.get_characters') as mock_get_characters:
                with patch('cluedo_game.solution.get_weapons') as mock_get_weapons:
                    with patch('cluedo_game.solution.Mansion') as mock_mansion_class:
                        # Set up mock return values
                        mock_character = MagicMock(spec=Character)
                        mock_character.name = "Miss Scarlett"
                        
                        mock_weapon = MagicMock(spec=Weapon)
                        mock_weapon.name = "Rope"
                        
                        mock_mansion = MagicMock(spec=Mansion)
                        mock_mansion.get_rooms.return_value = ["Kitchen"]
                        mock_mansion_class.return_value = mock_mansion
                        
                        mock_get_characters.return_value = [mock_character]
                        mock_get_weapons.return_value = [mock_weapon]
                        
                        # Set up random.choice to return our mocks
                        mock_random.choice.side_effect = lambda x: x[0]
                        
                        # Create a random solution
                        solution = Solution.random_solution()
                        
                        # Verify the solution
                        assert solution.character.name == "Miss Scarlett"
                        assert solution.weapon.name == "Rope"
                        assert solution.room.name == "Kitchen"
                        
                        # Verify calls to random.choice
                        assert mock_random.choice.call_count == 3
    
    def test_matches(self, solution, mock_suspect, mock_weapon, mock_room):
        """Test checking if a solution matches specific cards."""
        # Test with the same cards
        assert solution.matches(mock_suspect, mock_weapon, mock_room) is True
        
        # Test with a different suspect
        different_suspect = MagicMock(spec=SuspectCard)
        different_suspect.name = "Mrs. White"
        assert solution.matches(different_suspect, mock_weapon, mock_room) is False
        
        # Test with a different weapon
        different_weapon = MagicMock(spec=WeaponCard)
        different_weapon.name = "Rope"
        assert solution.matches(mock_suspect, different_weapon, mock_room) is False
        
        # Test with a different room
        different_room = MagicMock(spec=RoomCard)
        different_room.name = "Kitchen"
        assert solution.matches(mock_suspect, mock_weapon, different_room) is False


# -----------------------------------------------------------------------------
# Suggestion Tests
# -----------------------------------------------------------------------------
class TestSuggestion:
    """Test suite for the Suggestion class."""

    def test_suggestion_init(self):
        """Test initialization of a Suggestion object."""
        # Create test data
        suggesting_player = "Miss Scarlett"
        character = SuspectCard("Colonel Mustard")
        weapon = WeaponCard("Candlestick")
        room = RoomCard("Kitchen")
        
        # Create the suggestion
        suggestion = Suggestion(suggesting_player, character, weapon, room)
        
        # Verify attributes
        assert suggestion.suggesting_player == suggesting_player
        assert suggestion.character == character
        assert suggestion.weapon == weapon
        assert suggestion.room == room
        assert suggestion.refuting_player is None
        assert suggestion.shown_card is None
    
    def test_suggestion_init_with_refutation(self):
        """Test initialization of a Suggestion object with refutation."""
        # Create test data
        suggesting_player = "Miss Scarlett"
        character = SuspectCard("Colonel Mustard")
        weapon = WeaponCard("Candlestick")
        room = RoomCard("Kitchen")
        refuting_player = "Professor Plum"
        shown_card = weapon
        
        # Create the suggestion
        suggestion = Suggestion(suggesting_player, character, weapon, room, refuting_player, shown_card)
        
        # Verify attributes
        assert suggestion.suggesting_player == suggesting_player
        assert suggestion.character == character
        assert suggestion.weapon == weapon
        assert suggestion.room == room
        assert suggestion.refuting_player == refuting_player
        assert suggestion.shown_card == shown_card
    
    def test_repr_no_refutation(self):
        """Test string representation of a suggestion with no refutation."""
        # Create test data
        suggesting_player = "Miss Scarlett"
        character = SuspectCard("Colonel Mustard")
        weapon = WeaponCard("Candlestick")
        room = RoomCard("Kitchen")
        
        # Create the suggestion
        suggestion = Suggestion(suggesting_player, character, weapon, room)
        
        # Verify string representation
        expected = f"{suggesting_player} suggested {character} with {weapon} in {room}; no one refuted"
        assert str(suggestion) == expected
    
    def test_repr_with_refutation_human_player(self):
        """Test string representation of a suggestion with refutation for a human player."""
        # Create test data
        suggesting_player = "Miss Scarlett"
        character = SuspectCard("Colonel Mustard")
        weapon = WeaponCard("Candlestick")
        room = RoomCard("Kitchen")
        refuting_player = "Professor Plum"
        shown_card = weapon
        
        # Create the suggestion
        suggestion = Suggestion(suggesting_player, character, weapon, room, refuting_player, shown_card)
        
        # Verify string representation
        expected = f"{suggesting_player} suggested {character} with {weapon} in {room}; refuted by {refuting_player} (card: {shown_card})"
        assert str(suggestion) == expected

    def test_repr_with_refutation_ai_player(self):
        """Test string representation of a suggestion with refutation for an AI player."""
        # Create test data
        suggesting_player = "Miss Scarlett (AI)"
        character = SuspectCard("Colonel Mustard")
        weapon = WeaponCard("Candlestick")
        room = RoomCard("Kitchen")
        refuting_player = "Professor Plum"
        shown_card = weapon
        
        # Create the suggestion
        suggestion = Suggestion(suggesting_player, character, weapon, room, refuting_player, shown_card)
        
        # Verify string representation
        expected = f"{suggesting_player} suggested {character} with {weapon} in {room}; refuted by {refuting_player}"
        assert str(suggestion) == expected
    
    def test_repr_with_refutation_object_player(self):
        """Test string representation of a suggestion with refutation using player objects."""
        # Create test data using mock objects
        suggesting_player = MagicMock()
        suggesting_player.__str__.return_value = "Miss Scarlett"
        
        character = SuspectCard("Colonel Mustard")
        weapon = WeaponCard("Candlestick")
        room = RoomCard("Kitchen")
        refuting_player = "Professor Plum"
        
        # Mock shown_card that raises AttributeError in try-except block inside __repr__
        shown_card = MagicMock()
        shown_card.__str__.return_value = "Mock Card"
        
        # Create the suggestion
        suggestion = Suggestion(suggesting_player, character, weapon, room, refuting_player, shown_card)
        
        # Verify string representation - the expected output doesn't contain the card
        # because the suggesting_player mock doesn't properly handle the endswith check
        expected = f"Miss Scarlett suggested {character} with {weapon} in {room}; refuted by {refuting_player}"
        assert str(suggestion) == expected
    
    def test_repr_with_refutation_ai_object_player(self):
        """Test string representation with AI player as an object."""
        # Create test data using mock objects for AI player
        suggesting_player = MagicMock()
        suggesting_player.__str__.return_value = "Miss Scarlett (AI)"
        suggesting_player.endswith.side_effect = AttributeError("No endswith method")
        
        character = SuspectCard("Colonel Mustard")
        weapon = WeaponCard("Candlestick")
        room = RoomCard("Kitchen")
        refuting_player = "Professor Plum"
        shown_card = weapon
        
        # Create the suggestion
        suggestion = Suggestion(suggesting_player, character, weapon, room, refuting_player, shown_card)
        
        # Verify string representation
        expected = f"Miss Scarlett (AI) suggested {character} with {weapon} in {room}; refuted by {refuting_player}"
        assert str(suggestion) == expected
