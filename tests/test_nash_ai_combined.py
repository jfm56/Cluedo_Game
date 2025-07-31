"""
Tests for the Nash AI Player functionality.
This file consolidates tests from:
- test_nash_ai_player.py (core AI functionality)
- test_nash_ai_advanced.py (advanced AI features)
- test_nash_ai_coverage.py (coverage-focused tests)
- test_nash_ai_strategy.py (strategic decision making)
- test_nash_integration.py (game integration)

Aims to achieve comprehensive test coverage of NashAIPlayer."""

import pytest
import logging
import math
from unittest.mock import MagicMock, patch, call

from cluedo_game.game import CluedoGame
from cluedo_game.mansion import Mansion, Room
from cluedo_game.solution import Solution
from cluedo_game.history import SuggestionHistory
from cluedo_game.cards import SuspectCard, WeaponCard, RoomCard, get_suspects, get_weapons, get_rooms
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
def mock_game(mock_input, mock_output, mock_logger):
    """Create a mock game instance for AI player testing."""
    with patch('logging.config.fileConfig'), \
         patch('logging.getLogger', return_value=mock_logger):
        game = CluedoGame(input_func=mock_input, output_func=mock_output)
    
    # Setup basic game state
    game.characters = [
        Character("Miss Scarlett", "C1"),
        Character("Colonel Mustard", "C2"),
        Character("Mrs. White", "C3"),
        Character("Professor Plum", "C6"),
        Character("Mrs. Peacock", "C5"),
        Character("Reverend Green", "C4")
    ]
    
    # Setup solution
    character_card = SuspectCard("Colonel Mustard")
    weapon_card = WeaponCard("Revolver")
    room_card = RoomCard("Kitchen")
    game.solution = Solution(character_card, weapon_card, room_card)
    
    # Setup history
    game.suggestion_history = SuggestionHistory()
    
    return game

@pytest.fixture
def all_cards():
    """Return a list of all cards in the game."""
    suspects = get_suspects()
    weapons = get_weapons()
    rooms = [RoomCard(room) for room in get_rooms()]
    return suspects + weapons + rooms

@pytest.fixture
def nash_ai(mock_game):
    """Create a basic Nash AI player instance."""
    player = Character("Professor Plum", "C6")
    nash_ai = NashAIPlayer(player, mock_game)
    return nash_ai

@pytest.fixture
def nash_ai_with_cards(mock_game, all_cards):
    """Create a Nash AI player with cards in hand."""
    player = Character("Professor Plum", "C6")
    nash_ai = NashAIPlayer(player, mock_game)
    
    # Add some cards to the AI's hand
    nash_ai.hand = [
        SuspectCard("Miss Scarlett"),
        WeaponCard("Candlestick"),
        RoomCard("Ballroom")
    ]
    
    return nash_ai

@pytest.fixture
def nash_ai_with_belief_state(nash_ai_with_cards):
    """Create a Nash AI player with initialized belief state."""
    nash_ai = nash_ai_with_cards
    # Initialize belief state
    nash_ai._init_belief_state()
    return nash_ai

# -----------------------------------------------------------------------------
# Core Nash AI Player Tests
# -----------------------------------------------------------------------------
class TestNashAIPlayer:
    """Test suite for the basic NashAIPlayer functionality."""
    
    def test_init(self, mock_game):
        """Test AI player initialization."""
        player = Character("Professor Plum", "C6")
        nash_ai = NashAIPlayer(player, mock_game)
        
        # Verify basic initialization
        assert nash_ai.character == player
        assert nash_ai.game == mock_game
        assert nash_ai.name == "Professor Plum"
        assert nash_ai.position == "C6"
        assert nash_ai.hand == []
        assert not nash_ai.is_eliminated
        
    def test_init_belief_state(self, nash_ai_with_cards):
        """Test belief state initialization."""
        nash_ai = nash_ai_with_cards
        nash_ai._init_belief_state()
        
        # Verify belief state structure
        assert hasattr(nash_ai, 'belief_state')
        assert isinstance(nash_ai.belief_state, dict)
        
        # Check that all card types are in the belief state
        assert 'suspects' in nash_ai.belief_state
        assert 'weapons' in nash_ai.belief_state
        assert 'rooms' in nash_ai.belief_state
        
        # Check that cards in hand have 0 probability
        for card in nash_ai.hand:
            if isinstance(card, SuspectCard):
                assert nash_ai.belief_state['suspects'][card.name] == 0
            elif isinstance(card, WeaponCard):
                assert nash_ai.belief_state['weapons'][card.name] == 0
            elif isinstance(card, RoomCard):
                assert nash_ai.belief_state['rooms'][card.name] == 0
    
    def test_calculate_player_uncertainty(self, nash_ai_with_belief_state):
        """Test player uncertainty calculation."""
        nash_ai = nash_ai_with_belief_state
        
        # Calculate uncertainty
        uncertainty = nash_ai._calculate_player_uncertainty()
        
        # Uncertainty should be a value between 0 and 1
        assert 0 <= uncertainty <= 1
    
    def test_calculate_total_confidence(self, nash_ai_with_belief_state):
        """Test total confidence calculation."""
        nash_ai = nash_ai_with_belief_state
        
        # Calculate total confidence
        confidence = nash_ai._calculate_total_confidence()
        
        # Total confidence should be a value between 0 and 1
        assert 0 <= confidence <= 1
    
    def test_learn_from_refutation(self, nash_ai_with_belief_state):
        """Test learning from card refutation."""
        nash_ai = nash_ai_with_belief_state
        
        # Set up a suggestion and refutation
        suggestion = {
            'character': 'Mrs. Peacock',
            'weapon': 'Rope',
            'room': 'Library'
        }
        refuting_player = Character("Mrs. White", "C3")
        refutation_card = SuspectCard('Mrs. Peacock')
        
        # Mock the belief state to have non-zero probabilities for all cards
        nash_ai.belief_state['suspects']['Mrs. Peacock'] = 0.2
        nash_ai.belief_state['weapons']['Rope'] = 0.2
        nash_ai.belief_state['rooms']['Library'] = 0.2
        
        # Learn from refutation
        nash_ai.learn_from_refutation(suggestion, refuting_player, refutation_card)
        
        # The refuted card should now have 0 probability in the belief state
        assert nash_ai.belief_state['suspects']['Mrs. Peacock'] == 0
    
    def test_update_belief_state_from_no_refutation(self, nash_ai_with_belief_state):
        """Test updating belief state when no player refutes a suggestion."""
        nash_ai = nash_ai_with_belief_state
        
        # Set up a suggestion
        suggestion = {
            'character': 'Mrs. Peacock',
            'weapon': 'Rope',
            'room': 'Library'
        }
        
        # Mock the belief state to have non-zero probabilities for all cards
        nash_ai.belief_state['suspects']['Mrs. Peacock'] = 0.2
        nash_ai.belief_state['weapons']['Rope'] = 0.2
        nash_ai.belief_state['rooms']['Library'] = 0.2
        
        other_player = Character("Mrs. White", "C3")
        
        # Update belief state when no one could refute
        nash_ai._update_probability_from_no_refutation(
            suggestion['character'],
            suggestion['weapon'],
            suggestion['room']
        )
        
        # The probabilities should be updated to reflect the knowledge gained
        # Since no one could refute, these cards are more likely to be in the solution
        # The implementation adds 0.1 to the current probability (capped at 1.0)
        assert nash_ai.belief_state['suspects']['Mrs. Peacock'] == pytest.approx(0.3)  # 0.2 + 0.1
        assert nash_ai.belief_state['weapons']['Rope'] == pytest.approx(0.3)  # 0.2 + 0.1
        assert nash_ai.belief_state['rooms']['Library'] == pytest.approx(0.3)  # 0.2 + 0.1

# -----------------------------------------------------------------------------
# Advanced Nash AI Features Tests
# -----------------------------------------------------------------------------
class TestNashAIAdvanced:
    """Test suite for advanced NashAIPlayer functionality."""
    
    def test_make_suggestion(self, nash_ai_with_belief_state, mock_game):
        """Test the make_suggestion method."""
        nash_ai = nash_ai_with_belief_state
        
        # Debug: Print initial state
        print(f"Initial position: {nash_ai.position}")
        print(f"Initial belief state: {nash_ai.belief_state}")
        print(f"Has seen_cards: {hasattr(nash_ai, 'seen_cards')}")
        if hasattr(nash_ai, 'seen_cards'):
            print(f"Seen cards: {nash_ai.seen_cards}")
        
        # Prepare the AI to make a suggestion
        nash_ai.position = "Kitchen"  # Set position to a room
        
        # Create expected suggestions based on belief state
        nash_ai.belief_state['suspects']['Mrs. Peacock'] = 0.8  # High probability
        nash_ai.belief_state['weapons']['Rope'] = 0.7  # High probability
        
        # Debug: Print state after setting up belief state
        print(f"Position after setup: {nash_ai.position}")
        print(f"Belief state after setup: {nash_ai.belief_state}")
        
        # Make suggestion
        print("Calling make_suggestion()...")
        try:
            suggestion = nash_ai.make_suggestion()
            print(f"Suggestion returned: {suggestion}")
        except Exception as e:
            print(f"Exception in make_suggestion: {e}")
            raise
        
        # Verify suggestion is not None
        assert suggestion is not None, "make_suggestion() returned None"
        
        # Verify suggestion format
        assert 'character' in suggestion, f"Suggestion missing 'character' key: {suggestion}"
        assert 'weapon' in suggestion, f"Suggestion missing 'weapon' key: {suggestion}"
        assert 'room' in suggestion, f"Suggestion missing 'room' key: {suggestion}"
        
        # Room should match current position
        assert suggestion['room'] == "Kitchen", f"Expected room 'Kitchen', got {suggestion['room']}"
        
        # Character and weapon should be selected based on highest probability in belief state
        # We set 'Mrs. Peacock' and 'Rope' as the most likely in the test setup
        assert suggestion['character'] == 'Mrs. Peacock', f"Expected 'Mrs. Peacock', got {suggestion['character']}"
        assert suggestion['weapon'] == 'Rope', f"Expected 'Rope', got {suggestion['weapon']}"
    
    def test_make_accusation(self, nash_ai_with_belief_state, mock_game):
        """Test the make_accusation method."""
        nash_ai = nash_ai_with_belief_state
        
        # Set high confidence for specific cards in belief state
        nash_ai.belief_state['suspects']['Colonel Mustard'] = 0.9  # Very high probability
        nash_ai.belief_state['weapons']['Revolver'] = 0.9  # Very high probability
        nash_ai.belief_state['rooms']['Kitchen'] = 0.9  # Very high probability
        
        # Mock game's check_accusation method
        mock_game.check_accusation = MagicMock(return_value=True)  # Correct accusation
        
        # Make accusation
        accusation, is_correct = nash_ai.make_accusation()
        
        # Verify accusation structure
        assert 'character' in accusation
        assert 'weapon' in accusation
        assert 'room' in accusation
        
        # Verify game interaction
        assert mock_game.check_accusation.call_count == 1
        assert is_correct is True  # Should match what mock_game.check_accusation returns
    
    def test_get_accusation(self, nash_ai_with_belief_state):
        """Test the get_accusation method which returns the most likely solution."""
        nash_ai = nash_ai_with_belief_state
        
        # Set different probabilities for cards
        nash_ai.belief_state['suspects']['Colonel Mustard'] = 0.8
        nash_ai.belief_state['suspects']['Mrs. Peacock'] = 0.2
        nash_ai.belief_state['weapons']['Revolver'] = 0.7
        nash_ai.belief_state['weapons']['Rope'] = 0.3
        nash_ai.belief_state['rooms']['Kitchen'] = 0.6
        nash_ai.belief_state['rooms']['Library'] = 0.4
        
        # Get accusation
        accusation = nash_ai.get_accusation()
        
        # Should return the cards with highest probability
        assert accusation['character'] == 'Colonel Mustard'
        assert accusation['weapon'] == 'Revolver'
        assert accusation['room'] == 'Kitchen'
    
    def test_should_make_accusation(self, nash_ai_with_belief_state):
        """Test the should_make_accusation method which decides if AI is confident enough."""
        nash_ai = nash_ai_with_belief_state
        
        # Test case 1: Not confident enough
        print("\n=== Test case 1: Not confident enough ===")
        # Set specific probabilities for test case 1
        nash_ai.belief_state = {
            'suspects': {
                'Miss Scarlett': 0.0,
                'Colonel Mustard': 0.5,  # Set to 0.5 (below threshold)
                'Mrs. White': 0.1,
                'Reverend Green': 0.1,
                'Mrs. Peacock': 0.1,
                'Professor Plum': 0.1
            },
            'weapons': {
                'Candlestick': 0.0,
                'Dagger': 0.1,
                'Lead Pipe': 0.1,
                'Revolver': 0.5,  # Set to 0.5 (below threshold)
                'Rope': 0.1,
                'Wrench': 0.1
            },
            'rooms': {
                'Kitchen': 0.5,  # Set to 0.5 (below threshold)
                'Ballroom': 0.0,
                'Conservatory': 0.1,
                'Dining Room': 0.1,
                'Billiard Room': 0.1,
                'Library': 0.1,
                'Lounge': 0.1,
                'Hall': 0.1,
                'Study': 0.1
            }
        }
        
        # Print the test case setup
        print("Test case 1 setup:")
        print(f"  Best suspect: Colonel Mustard (0.5)")
        print(f"  Best weapon: Revolver (0.5)")
        print(f"  Best room: Kitchen (0.5)")
        print("  Threshold: 0.8")
        
        # Call the method and check the result
        result1 = nash_ai.should_make_accusation(confidence_threshold=0.8)
        print(f"Test case 1 result: {result1} (expected: False)")
        assert result1 is False, "Test case 1 failed: should return False when confidences are below threshold"
    
        # Test case 2: Very confident
        print("\n=== Test case 2: Very confident ===")
        # Update the belief state for test case 2
        nash_ai.belief_state['suspects']['Colonel Mustard'] = 0.95  # Above threshold
        nash_ai.belief_state['weapons']['Revolver'] = 0.95          # Above threshold
        nash_ai.belief_state['rooms']['Kitchen'] = 0.95             # Above threshold
        
        # Print the test case setup
        print("Test case 2 setup:")
        print(f"  Best suspect: Colonel Mustard (0.95)")
        print(f"  Best weapon: Revolver (0.95)")
        print(f"  Best room: Kitchen (0.95)")
        print("  Threshold: 0.8")
        
        # Call the method and check the result
        result2 = nash_ai.should_make_accusation(confidence_threshold=0.8)
        print(f"Test case 2 result: {result2} (expected: True)")
        assert result2 is True, "Test case 2 failed: should return True when all confidences are above threshold"
        
        # Additional debug: Check if the method is being overridden
        print("\n=== Debug: Checking method resolution ===")
        print(f"Method resolution order: {nash_ai.__class__.__mro__}")
        print(f"Method in class: {nash_ai.__class__.__dict__.get('should_make_accusation', 'NOT FOUND')}")
        
        # Directly test the method with a minimal case
        print("\n=== Debug: Direct test with minimal case ===")
        test_ai = nash_ai_with_belief_state
        test_ai.belief_state = {
            'suspects': {'Test Suspect': 0.95},
            'weapons': {'Test Weapon': 0.95},
            'rooms': {'Test Room': 0.95}
        }
        direct_result = test_ai.should_make_accusation(confidence_threshold=0.9)
        print(f"Direct test result: {direct_result} (expected: True)")
        print(f"Direct test belief state: {test_ai.belief_state}")
    
    def test_calculate_suggestion_information_gain(self, nash_ai_with_belief_state):
        """Test calculating information gain for a potential suggestion."""
        nash_ai = nash_ai_with_belief_state
        
        # Create a potential suggestion
        suggestion = {
            'character': 'Mrs. Peacock',
            'weapon': 'Rope',
            'room': 'Library'
        }
        
        # Create other players
        other_players = [
            Character("Miss Scarlett", "C1"),
            Character("Mrs. White", "C3")
        ]
        
        # Calculate information gain
        info_gain = nash_ai._calculate_suggestion_information_gain(suggestion, other_players)
        
        # Information gain should be a non-negative value
        assert info_gain >= 0
        
    def test_calculate_room_information_gain(self, nash_ai_with_belief_state):
        """Test calculating information gain for visiting a room."""
        nash_ai = nash_ai_with_belief_state
        
        # Create a room
        room = "Library"
        
        # Create other players for testing
        other_players = [
            Character("Miss Scarlett", "C1"),
            Character("Mrs. White", "C3")
        ]
        
        # Calculate room information gain
        info_gain = nash_ai._calculate_room_information_gain(room, other_players)
        
        # Information gain should be a non-negative value
        assert info_gain >= 0

# -----------------------------------------------------------------------------
# Nash AI Strategy Tests
# -----------------------------------------------------------------------------
class TestNashAIStrategy:
    """Test suite for NashAIPlayer strategic decision making."""
    
    def test_choose_move_destination(self, nash_ai_with_belief_state, mock_game):
        """Test AI choosing a strategic move destination."""
        nash_ai = nash_ai_with_belief_state
        
        # Mock available destinations
        destinations = ["C1", "Kitchen", "Ballroom"]
        
        # Mock movement methods
        mock_game.movement.get_destinations_from = MagicMock(return_value=destinations)
        
        # Mock information gain calculations
        nash_ai._calculate_room_information_gain = MagicMock(side_effect=lambda room: {
            "C1": 0.1,
            "Kitchen": 0.8,  # Highest info gain
            "Ballroom": 0.3
        }.get(room, 0))
        
        # Set other players
        mock_game.get_all_players = MagicMock(return_value=[
            nash_ai.character,  # The AI itself
            Character("Miss Scarlett", "C1"),
            Character("Mrs. White", "C3")
        ])
        
        # Choose move
        destination = nash_ai.choose_move_destination()
        
        # Should choose the destination with highest information gain
        assert destination == "Kitchen"
    
    def test_plan_suggestion_strategy(self, nash_ai_with_belief_state):
        """Test AI planning a suggestion for maximum information gain."""
        nash_ai = nash_ai_with_belief_state
        
        # Set current position to a room
        nash_ai.position = "Library"
        
        # Mock information gain calculations
        original_calc_method = nash_ai._calculate_suggestion_information_gain
        nash_ai._calculate_suggestion_information_gain = MagicMock()
        nash_ai._calculate_suggestion_information_gain.side_effect = lambda s, p: {
            # Return high value for a specific character+weapon combo
            'Mrs. Peacock' + 'Rope': 0.9,
            'Miss Scarlett' + 'Candlestick': 0.2,
        }.get(s['character'] + s['weapon'], 0.1)
        
        # Create other players for testing
        other_players = [
            Character("Miss Scarlett", "C1"),
            Character("Mrs. White", "C3")
        ]
        nash_ai.game.get_all_players = MagicMock(return_value=[nash_ai.character] + other_players)
        
        # Call the method that uses suggestion strategy
        suggestion = nash_ai.make_suggestion()
        
        # Verify suggestion includes the room the AI is currently in
        assert suggestion['room'] == "Library"
        
        # Restore original method
        nash_ai._calculate_suggestion_information_gain = original_calc_method
    
    def test_bayesian_update(self, nash_ai_with_belief_state):
        """Test Bayesian probability update in the belief state."""
        nash_ai = nash_ai_with_belief_state
        
        # Record initial probabilities
        initial_suspect_prob = nash_ai.belief_state['suspects']['Mrs. Peacock']
        initial_weapon_prob = nash_ai.belief_state['weapons']['Rope']
        
        # Set up a suggestion with these cards
        suggestion = {
            'character': 'Mrs. Peacock',
            'weapon': 'Rope',
            'room': 'Library'
        }
        
        # Create a refutation scenario
        refuting_player = Character("Mrs. White", "C3")
        
        # Update belief state based on no refutation
        nash_ai._update_probability_from_unknown_refutation(suggestion, refuting_player)
        
        # Probabilities should be updated using Bayes' rule
        # Verify probabilities have changed (specific values will depend on implementation)
        assert nash_ai.belief_state['suspects']['Mrs. Peacock'] != initial_suspect_prob
        assert nash_ai.belief_state['weapons']['Rope'] != initial_weapon_prob

# -----------------------------------------------------------------------------
# Nash AI Coverage Tests
# -----------------------------------------------------------------------------
class TestNashAICoverage:
    """Test suite focusing on coverage of NashAIPlayer edge cases."""
    
    def test_empty_belief_state(self, nash_ai):
        """Test behavior with an empty belief state."""
        # Call init_belief_state but don't initialize any probabilities
        nash_ai._init_belief_state()
        
        # Make sure we can get an accusation without errors
        accusation = nash_ai.get_accusation()
        
        # Should return a valid accusation structure even with empty state
        assert 'character' in accusation
        assert 'weapon' in accusation
        assert 'room' in accusation
    
    def test_all_zero_probabilities(self, nash_ai_with_belief_state):
        """Test behavior when all probabilities are zero."""
        nash_ai = nash_ai_with_belief_state
        
        # Set all probabilities to zero
        for category in nash_ai.belief_state.values():
            for card in category:
                category[card] = 0
        
        # Should still calculate uncertainty without division by zero errors
        uncertainty = nash_ai._calculate_player_uncertainty()
        assert uncertainty >= 0
        
        # Should still calculate total confidence without errors
        confidence = nash_ai._calculate_total_confidence()
        assert 0 <= confidence <= 1
    
    def test_learn_with_unknown_card(self, nash_ai_with_belief_state):
        """Test learning from an unknown card refutation."""
        nash_ai = nash_ai_with_belief_state
        
        # Set up a suggestion
        suggestion = {
            'character': 'Mrs. Peacock',
            'weapon': 'Rope',
            'room': 'Library'
        }
        
        # Create a refutation with a card not in the suggestion
        refuting_player = Character("Mrs. White", "C3")
        refutation_card = WeaponCard("Candlestick")  # Not in the suggestion
        
        # Learn from this odd refutation - should not crash
        nash_ai.learn_from_refutation(suggestion, refuting_player, refutation_card)
    
    def test_position_not_in_room(self, nash_ai_with_belief_state):
        """Test make_suggestion when AI is not in a room."""
        nash_ai = nash_ai_with_belief_state
        
        # Set position to a corridor
        nash_ai.position = "C1"
        
        # This should not raise an exception, but should handle the case appropriately
        suggestion = nash_ai.make_suggestion()
        
        # Either returns None or a valid suggestion with the nearest room
        if suggestion is not None:
            assert 'character' in suggestion
            assert 'weapon' in suggestion
            assert 'room' in suggestion

# -----------------------------------------------------------------------------
# Nash AI Integration Tests
# -----------------------------------------------------------------------------
class TestNashAIIntegration:
    """Test suite for NashAIPlayer integration with the game."""
    
    def test_ai_full_turn(self, mock_game):
        """Test AI player taking a full turn in the game."""
        # Create an AI player
        player = Character("Professor Plum", "C6")
        nash_ai = NashAIPlayer(player, mock_game)
        nash_ai.hand = [SuspectCard("Miss Scarlett"), WeaponCard("Candlestick")]
        
        # Initialize the AI's belief state
        nash_ai._init_belief_state()
        
        # Mock necessary game methods
        mock_game.movement = MagicMock()
        mock_game.movement.get_destinations_from = MagicMock(return_value=["C1", "Kitchen"])
        mock_game.move_player = MagicMock()
        mock_game.process_suggestion = MagicMock(return_value=None)
        mock_game.suggestion_history = MagicMock()
        mock_game.get_all_players = MagicMock(return_value=[nash_ai.character])
        mock_game.check_accusation = MagicMock(return_value=False)
        
        # Force movement in test mode
        nash_ai._force_move = True
        
        # Take a turn
        result = nash_ai.take_turn()
        
        # Verify turn flow
        assert mock_game.move_player.call_count == 1  # Move should have happened
        
        # Turn should complete without errors
        assert result is not None
    
    def test_ai_take_turn_make_accusation(self, mock_game):
        """Test AI player making an accusation during its turn."""
        # Create an AI player with high confidence
        player = Character("Professor Plum", "C6")
        nash_ai = NashAIPlayer(player, mock_game)
        nash_ai.hand = [SuspectCard("Miss Scarlett"), WeaponCard("Candlestick")]
        
        # Initialize the AI's belief state with very high confidence
        nash_ai._init_belief_state()
        nash_ai.belief_state['suspects']['Colonel Mustard'] = 0.99
        nash_ai.belief_state['weapons']['Revolver'] = 0.99
        nash_ai.belief_state['rooms']['Kitchen'] = 0.99
        
        # Mock should_make_accusation to return True (ready to accuse)
        original_should_accuse = nash_ai.should_make_accusation
        nash_ai.should_make_accusation = MagicMock(side_effect=original_should_accuse)
        
        # Create expected accusation components
        suspect = Character("Colonel Mustard", "C2")
        weapon = Weapon("Revolver")
        room = Room("Kitchen")
        
        # Mock get_accusation to return the expected accusation
        nash_ai.get_accusation = MagicMock(return_value={
            'character': suspect,
            'weapon': weapon,
            'room': room
        })
        
        # Mock necessary game methods
        mock_game.movement = MagicMock()
        mock_game.movement.get_destinations_from = MagicMock(return_value=["C1", "Kitchen"])
        mock_game.move_player = MagicMock()
        mock_game.process_suggestion = MagicMock()
        mock_game.suggestion_history = MagicMock()
        mock_game.get_all_players = MagicMock(return_value=[nash_ai.character])
        mock_game.make_accusation = MagicMock(return_value=True)  # Correct accusation
        
        # Set IN_TEST_MODE to False to prevent take_turn from returning early
        import cluedo_game.nash_ai_player as nash_ai_module
        original_test_mode = nash_ai_module.IN_TEST_MODE
        nash_ai_module.IN_TEST_MODE = False
        
        try:
            # Take a turn with accusation
            result = nash_ai.take_turn()
        finally:
            # Restore the original IN_TEST_MODE value
            nash_ai_module.IN_TEST_MODE = original_test_mode
        
        # Verify accusation was made with the correct parameters
        assert mock_game.make_accusation.call_count == 1, \
            f"Expected make_accusation to be called once, but it was called {mock_game.make_accusation.call_count} times"
            
        mock_game.make_accusation.assert_called_once_with(
            nash_ai, suspect, weapon, room
        )
        assert result is True, f"Expected take_turn to return True (game won), but got {result}"
    
    def test_ai_response_to_suggestion(self, mock_game):
        """Test AI player responding to another player's suggestion."""
        # Create an AI player with cards in hand
        player = Character("Professor Plum", "C6")
        nash_ai = NashAIPlayer(player, mock_game)
        
        # Give AI specific cards
        mrs_peacock_card = SuspectCard("Mrs. Peacock")
        candlestick_card = WeaponCard("Candlestick")
        library_card = RoomCard("Library")
        nash_ai.hand = [mrs_peacock_card, candlestick_card, library_card]
        
        # Test case 1: Suggestion contains one of AI's cards
        suggestion1 = {
            'character': 'Mrs. Peacock',  # AI has this card
            'weapon': 'Rope',
            'room': 'Kitchen'
        }
        
        card1 = nash_ai.respond_to_suggestion(suggestion1)
        assert card1 == mrs_peacock_card  # Should show the card it has
        
        # Test case 2: Suggestion contains multiple of AI's cards
        suggestion2 = {
            'character': 'Mrs. Peacock',
            'weapon': 'Candlestick',
            'room': 'Library'
        }
        
        card2 = nash_ai.respond_to_suggestion(suggestion2)
        # Should return one of the cards (which one depends on implementation)
        assert card2 in [mrs_peacock_card, candlestick_card, library_card]
        
        # Test case 3: Suggestion contains none of AI's cards
        suggestion3 = {
            'character': 'Miss Scarlett',
            'weapon': 'Rope',
            'room': 'Kitchen'
        }
        
        card3 = nash_ai.respond_to_suggestion(suggestion3)
        assert card3 is None  # Should not be able to refute
    
    def test_multiple_ai_players_interaction(self, mock_game):
        """Test interactions between multiple AI players."""
        # Create three AI players
        player1 = Character("Professor Plum", "C6")
        player2 = Character("Mrs. Peacock", "C5")
        player3 = Character("Reverend Green", "C4")
        
        ai1 = NashAIPlayer(player1, mock_game)
        ai2 = NashAIPlayer(player2, mock_game)
        ai3 = NashAIPlayer(player3, mock_game)
        
        # Set up their hands
        ai1.hand = [SuspectCard("Miss Scarlett"), WeaponCard("Candlestick")]
        ai2.hand = [SuspectCard("Colonel Mustard"), WeaponCard("Rope")]
        ai3.hand = [RoomCard("Library"), RoomCard("Ballroom")]
        
        # Initialize belief states
        ai1._init_belief_state()
        ai2._init_belief_state()
        ai3._init_belief_state()
        
        # Mock game to return all AIs as players
        mock_game.get_all_players = MagicMock(return_value=[ai1.character, ai2.character, ai3.character])
        
        # Set up a suggestion that will be refuted by ai2
        suggestion = {
            'character': 'Colonel Mustard',  # AI2 has this
            'weapon': 'Knife',
            'room': 'Kitchen'
        }
        
        # Create a suggestion history entry
        mock_game.suggestion_history.add_suggestion = MagicMock()
        mock_game.suggestion_history.get_all_suggestions = MagicMock(return_value=[{
            'suggester': player1.name,
            'suggestion': suggestion,
            'refuter': player2.name,
            'card': 'Unknown'  # Other AIs don't know which card was shown
        }])
        
        # Let AI1 learn from this history
        for history_entry in mock_game.suggestion_history.get_all_suggestions():
            if history_entry['suggester'] != ai1.name:
                # AI learns that player2 has one of these cards
                ai1.update_belief_state(history_entry['suggestion'],
                                       [p for p in [ai1.character, ai2.character, ai3.character] 
                                        if p.name == history_entry['refuter']][0])
        
        # AI1's belief about Colonel Mustard should be updated
        assert ai1.belief_state['suspects']['Colonel Mustard'] < 1.0 / len(ai1.belief_state['suspects'])
