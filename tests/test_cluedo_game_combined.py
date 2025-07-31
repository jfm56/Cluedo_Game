"""
Tests for the Cluedo Game functionality.
This file consolidates tests for:
- Core game functionality (test_game.py)
- Game display functionality (test_game_display.py)
- Game play logic (test_game_play.py)

Aims to achieve 90%+ code coverage.
"""
import pytest
import logging
from unittest.mock import MagicMock, patch, call

from cluedo_game.game import CluedoGame
from cluedo_game.mansion import Mansion, Room
from cluedo_game.solution import Solution
from cluedo_game.history import SuggestionHistory
from cluedo_game.movement import Movement
from cluedo_game.cards import SuspectCard, WeaponCard, RoomCard, get_suspects, CHARACTER_STARTING_SPACES
from cluedo_game.player import Player
from cluedo_game.nash_ai_player import NashAIPlayer
from cluedo_game.character import Character
from cluedo_game.weapon import Weapon

# -----------------------------------------------------------------------------
# Common Test Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def mock_input():
    """Mock input function for testing."""
    return MagicMock()

@pytest.fixture
def mock_output():
    """Mock output function for testing."""
    return MagicMock()

@pytest.fixture
def mock_logger():
    """Create a mock logger for testing."""
    logger_mock = MagicMock()
    return logger_mock

@pytest.fixture
def game(mock_input, mock_output, mock_logger):
    """Create a game instance with mocked I/O."""
    # Mock input to always return "1" for character selection
    mock_input.return_value = "1"
    
    # Mock logging configuration
    with patch('logging.config.fileConfig'), \
         patch('logging.getLogger', return_value=mock_logger):
        game = CluedoGame(input_func=mock_input, output_func=mock_output)
    return game

@pytest.fixture
def ai_game(mock_input, mock_output, mock_logger):
    """Create a game instance with AI players and mocked I/O."""
    # Mock input to always return "1" for character selection
    mock_input.return_value = "1"
    
    # Mock logging configuration
    with patch('logging.config.fileConfig'), \
         patch('logging.getLogger', return_value=mock_logger):
        game = CluedoGame(input_func=mock_input, output_func=mock_output, with_ai=True)
    return game

@pytest.fixture
def mock_game_display():
    """Create a mock game for testing display functions."""
    # Create mock input/output functions
    mock_output = MagicMock()
    mock_input = MagicMock()
    
    # Inject mocks through constructor
    game = CluedoGame(input_func=mock_input, output_func=mock_output, with_ai=False)
    
    # Set up basic game state
    game.characters = [
        Character("Miss Scarlett", "C1"),
        Character("Colonel Mustard", "C2"),
        Character("Mrs. White", "C3")
    ]
    # Set game.player to the first character
    game.player = game.characters[0]
    # Mock players list to include all characters
    game.players = game.characters
    
    return game

@pytest.fixture
def mock_game_play():
    """Create a mock game for testing play functions."""
    # Create mock input/output functions
    mock_output = MagicMock()
    mock_input = MagicMock()
    
    # Inject mocks through constructor
    game = CluedoGame(input_func=mock_input, output_func=mock_output, with_ai=False)
    
    # Set up basic game state
    game.characters = [
        Character("Miss Scarlett", "C1"),
        Character("Colonel Mustard", "C2"),
        Character("Mrs. White", "C3")
    ]
    
    # Set game.player to the first character
    game.player = game.characters[0]
    
    # Mock players list to include all characters
    game.players = game.characters
    
    # Mock solution
    game.solution = MagicMock()
    game.solution.character = "Professor Plum"
    game.solution.weapon = "Revolver"
    game.solution.room = "Kitchen"
    
    # Mock history and suggestion history
    game.suggestion_history = MagicMock()
    
    # Mock movement
    game.movement = MagicMock()
    
    # Initialize turn counter
    game.turn_counter = 0
    
    return game

# -----------------------------------------------------------------------------
# Core Game Functionality Tests
# -----------------------------------------------------------------------------
class TestCluedoGame:
    """Test suite for the CluedoGame class."""

    def test_init(self, mock_input, mock_output):
        """Test game initialization."""
        game = CluedoGame(input_func=mock_input, output_func=mock_output)
        
        # Verify basic initialization
        assert game.input == mock_input
        assert game.output == mock_output
        assert game.with_ai is False
        assert game.logger is not None
        assert isinstance(game.mansion, Mansion)
        assert isinstance(game.movement, Movement)
        assert len(game.characters) > 0
        assert isinstance(game.suggestion_history, SuggestionHistory)
        assert isinstance(game.solution, Solution)
        assert game.last_door_passed == {}
        assert game.player is None
        assert game.ai_players == []

    def test_init_with_ai(self, mock_input, mock_output):
        """Test game initialization with AI mode enabled."""
        game = CluedoGame(input_func=mock_input, output_func=mock_output, with_ai=True)
        
        # Verify initialization with AI enabled
        assert game.with_ai is True
        assert game.ai_players == []  # AI players are initialized later during character selection

    def test_select_character(self, game):
        """Test character selection."""
        # Mock input is already set to return "1" in the fixture
        
        # Call method
        game.select_character()
        
        # Verify player selection
        assert game.player is not None
        assert game.player == game.characters[0]
        assert game.output.call_count > 0  # Should output character selection info

    def test_select_character_with_ai(self, ai_game):
        """Test character selection with AI mode."""
        # Call method
        ai_game.select_character()
        
        # Verify player selection and AI player creation
        assert ai_game.player is not None
        assert ai_game.player == ai_game.characters[0]
        assert len(ai_game.ai_players) > 0  # AI players should be created
        assert all(isinstance(ai, NashAIPlayer) for ai in ai_game.ai_players)
        assert ai_game.output.call_count > 0

    def test_is_ai_mode(self, game, ai_game):
        """Test is_ai_mode method."""
        # Standard game
        assert game.is_ai_mode() is False
        
        # AI game
        assert ai_game.is_ai_mode() is True

    def test_get_all_players(self, game, ai_game):
        """Test get_all_players method."""
        # Setup - select characters to initialize players
        game.select_character()
        ai_game.select_character()
        
        # Test standard game
        all_players = game.get_all_players()
        assert len(all_players) > 0
        assert all_players[0] == game.player  # First player should be human
        
        # Test AI game
        all_ai_players = ai_game.get_all_players()
        assert len(all_ai_players) > 0
        assert all_ai_players[0] == ai_game.player  # First player should be human
        assert len(all_ai_players) > len([ai_game.player])  # Should include AI players too
        

# -----------------------------------------------------------------------------
# Game Display Tests
# -----------------------------------------------------------------------------
class TestGameDisplay:
    """Test suite for game display functionality."""
    
    def test_display_board(self, mock_game_display):
        """Test the display_board method."""
        # Call the method
        mock_game_display.display_board()
        
        # Check that output was called the expected number of times
        # We expect at least 3 calls: header, rooms section, corridors section
        assert mock_game_display.output.call_count >= 3
        
        # Get all calls to mock_output
        output_calls = [call[0][0] for call in mock_game_display.output.call_args_list]
        
        # Check for expected headers
        assert any("--- Mansion Board with Chess Coordinates ---" in call for call in output_calls)
        assert any("Rooms:" in call for call in output_calls)
        assert any("Corridors:" in call for call in output_calls)
        
        # Reset the mock for other tests
        mock_game_display.output.reset_mock()
    
    def test_print_player_locations(self, mock_game_display):
        """Test the print_player_locations method with chess coordinates."""
        # Call the method
        mock_game_display.print_player_locations()
        
        # Get all calls to mock_output
        output_calls = [call[0][0] for call in mock_game_display.output.call_args_list]
        
        # Check for expected content in output
        assert any("--- Player Locations ---" in call for call in output_calls)
        
        # Check that at least one player location includes a chess coordinate (in brackets)
        chess_coordinate_displayed = any("[" in call and "]" in call for call in output_calls)
        assert chess_coordinate_displayed, "No chess coordinates found in player location output"
        
        # Reset the mock for other tests
        mock_game_display.output.reset_mock()
        
    def test_select_character_with_chess_coordinates(self, mock_game_display):
        """Test that select_character method displays chess coordinates."""
        # Prepare mock for input
        mock_game_display.input = MagicMock(return_value="1")  # Select the first character
        
        # Call the method
        mock_game_display.select_character()
        
        # Get all calls to mock_output
        output_calls = [call[0][0] for call in mock_game_display.output.call_args_list]
        
        # Check that character selection includes chess coordinates
        character_with_coord = any("[" in call and "]" in call and "starts in" in call for call in output_calls)
        assert character_with_coord, "No chess coordinates found in character selection output"
        
        # Check feedback message includes chess coordinates
        selection_feedback = [call for call in output_calls if "You are" in call]
        assert any("[" in msg and "]" in msg for msg in selection_feedback), "Chess coordinates missing in selection feedback"
        
    def test_suggestion_phase_with_board_option(self, mock_game_display):
        """Test that suggestion_phase accepts 'board' command to display the board."""
        # Set up mock to return 'board' then 'n'
        mock_game_display.input = MagicMock(side_effect=["board", "n"])
        
        # Call the method
        result = mock_game_display.suggestion_phase()
        
        # Check the result (should be True for 'n')
        assert result is True
        
        # Verify that display_board was called via output
        output_calls = [call[0][0] for call in mock_game_display.output.call_args_list]
        assert any("--- Mansion Board with Chess Coordinates ---" in call for call in output_calls)


# -----------------------------------------------------------------------------
# Game Play Tests
# -----------------------------------------------------------------------------
class TestGamePlay:
    """Test suite for game play functionality."""
    
    def test_process_human_turn_corridor(self, mock_game_play):
        """Test process_human_turn when player is in a corridor."""
        # Set up mocks for input and movement
        mock_game_play.input = MagicMock(side_effect=["1"])  # For destination selection
        mock_game_play.movement.get_destinations_from = MagicMock(return_value=["C1", "C2"])
        
        # Mock the player's position (in a corridor)
        mock_game_play.player = MagicMock()
        mock_game_play.player.position = "C1"
        mock_game_play.player.name = "TestPlayer"
        
        # Mock methods that will be called
        mock_game_play.suggestion_phase = MagicMock()
        mock_game_play.prompt_accusation = MagicMock(return_value=False)
        
        # Call the method
        result = mock_game_play.process_human_turn()
        
        # Check that methods were called correctly
        mock_game_play.movement.get_destinations_from.assert_called_once()
        mock_game_play.prompt_accusation.assert_called_once()
        
        # Suggestion phase should not be called when in corridor
        mock_game_play.suggestion_phase.assert_not_called()
        
        # Check the result
        assert isinstance(result, bool)  # Can be True (game over) or False (continue game)
    
    def test_process_human_turn_room(self, mock_game_play):
        """Test process_human_turn when player is in a room."""
        # Set up mocks for input and movement
        mock_game_play.input = MagicMock(side_effect=["1"])  # For destination selection
        mock_game_play.movement.get_destinations_from = MagicMock(return_value=["Kitchen"])
        
        # Mock the player's position (in a room)
        mock_game_play.player = MagicMock()
        mock_game_play.player.position = "Kitchen"
        mock_game_play.player.name = "TestPlayer"
        
        # Mock methods that will be called
        mock_game_play.suggestion_phase = MagicMock(return_value=False)
        mock_game_play.prompt_accusation = MagicMock(return_value=False)
        
        # Mock the output method to prevent print statements
        mock_game_play.output = MagicMock()
        
        # Call the method
        result = mock_game_play.process_human_turn()
        
        # Check that methods were called correctly
        mock_game_play.movement.get_destinations_from.assert_called_once()
        
        # In room, suggestion_phase should be called
        mock_game_play.suggestion_phase.assert_called_once()
        
        # Check the result
        assert isinstance(result, bool)  # Can be True (game over) or False (continue game)
    
    def test_move_phase(self, mock_game_play):
        """Test the move_phase method."""
        # Set up player with required attributes
        mock_player = MagicMock()
        mock_player.eliminated = False
        mock_player.position = "C1"
        mock_game_play.player = mock_player
        
        # Mock the get_destinations_from method to return some destinations
        mock_game_play.movement.get_destinations_from = MagicMock(return_value=["C1", "Kitchen"])
        
        # Mock input to select the first option
        mock_game_play.input = MagicMock(return_value="1")
        
        # Call the method
        result = mock_game_play.move_phase()
        
        # Verify that destinations were displayed
        assert mock_game_play.output.call_count > 0
        
        # Check the result is the first destination
        assert result == "C1"
    
    def test_suggestion_phase(self, mock_game_play):
        """Test the suggestion_phase method."""
        # Mock input to say 'y' to make a suggestion
        mock_game_play.input = MagicMock(return_value="y")
        mock_game_play.make_suggestion = MagicMock()
        
        # Call the method
        result = mock_game_play.suggestion_phase()
        
        # Verify make_suggestion was called
        mock_game_play.make_suggestion.assert_called_once()
        
        # Check the result
        assert result is False  # Should return False for 'y'
    
    def test_make_accusation(self, mock_game_play):
        """Test the make_accusation method."""
        # Setup test data
        test_player = Character("Test Player", "C1")
        test_suspect = SuspectCard("Miss Scarlett")
        test_weapon = WeaponCard("Knife")
        test_room = RoomCard("Kitchen")
        
        # Setup mock return values
        mock_game_play.solution = MagicMock()
        mock_game_play.solution.character = test_suspect
        mock_game_play.solution.weapon = test_weapon
        mock_game_play.solution.room = test_room
        
        # Test correct accusation
        result = mock_game_play.make_accusation(
            player=test_player,
            suspect=test_suspect,
            weapon=test_weapon,
            room=test_room
        )
        
        # Should return True for correct accusation
        assert result is True
        
        # Test incorrect accusation
        wrong_weapon = WeaponCard("Candlestick")
        result = mock_game_play.make_accusation(
            player=test_player,
            suspect=test_suspect,
            weapon=wrong_weapon,  # Incorrect weapon
            room=test_room
        )
        
        # Should return False for incorrect accusation
        assert result is False
        # Player should be marked as eliminated
        assert test_player.eliminated is True
    
    def test_deal_cards(self, mock_game_play):
        """Test the deal_cards method."""
        # Setup players with empty hands
        players = [
            Character("Miss Scarlett", "C1"),
            Character("Colonel Mustard", "C2"),
            Character("Mrs. White", "C3")
        ]
        
        # Setup some test cards
        all_cards = [
            SuspectCard("Miss Scarlett"),
            SuspectCard("Colonel Mustard"),
            SuspectCard("Mrs. White"),
            WeaponCard("Candlestick"),
            WeaponCard("Knife"),
            WeaponCard("Revolver"),
            RoomCard("Kitchen"),
            RoomCard("Ballroom"),
            RoomCard("Conservatory")
        ]
        
        # Mock the solution to exclude certain cards
        mock_game_play.solution.character = "Professor Plum"
        mock_game_play.solution.weapon = "Rope"
        mock_game_play.solution.room = Room("Study")
        
        # Mock get_all_players to return our test players
        mock_game_play.get_all_players = MagicMock(return_value=players)
        
        # Call the method
        mock_game_play.deal_cards(all_cards)
        
        # Verify that each player has cards
        for player in players:
            assert len(player.hand) > 0, f"Player {player.name} has no cards"
    
    def test_check_win_one_player_left(self, mock_game_play):
        """Test the check_win method when only one player is left."""
        # Setup only one active player
        test_player = Character("Miss Scarlett", "C1")
        test_player.eliminated = False
        
        # Mock get_all_players to return our test player
        mock_game_play.get_all_players = MagicMock(return_value=[test_player])
        
        # Call the method
        result = mock_game_play.check_win()
        
        # Should return True since only one player remains
        assert result is True
    
    def test_play_standard(self, mock_game_play):
        """Test the _play_standard method."""
        # Setup mocks for game phases
        mock_player = MagicMock()
        mock_player.eliminated = False
        mock_game_play.player = mock_player
        mock_game_play.players = [mock_player]
        
        # Set up the process_human_turn to return False first time, then True to end the game
        mock_game_play.process_human_turn = MagicMock(side_effect=[False, True])
        mock_game_play.get_all_players = MagicMock(return_value=[mock_player])
        mock_game_play.check_win = MagicMock(return_value=False)
        mock_game_play.turn_counter = 0
        mock_game_play.output = MagicMock()
        
        # Set up the player to be considered human
        mock_game_play.player = mock_player
        
        # Call the method with required parameters
        mock_game_play._play_standard(play_order=[mock_player], current_idx=0, max_turns=2)
        
        # Verify that process_human_turn was called
        assert mock_game_play.process_human_turn.called, "process_human_turn should be called"
        assert mock_game_play.check_win.called, "check_win should be called"
        
        # Verify that process_human_turn was called twice (once for each turn)
        assert mock_game_play.process_human_turn.call_count == 2, "process_human_turn should be called twice"
