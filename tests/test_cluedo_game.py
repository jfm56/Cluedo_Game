import sys
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

# Import the module containing the main function
from cluedo_game.cluedo_game import main, CluedoGame


class TestCluedoGame:
    """Tests for the cluedo_game.py main module."""

    @patch('cluedo_game.cluedo_game.CluedoGame')
    def test_main_runs_game(self, mock_game_class):
        """Test that the main function creates and plays a game."""
        # Setup mock game instance
        mock_game_instance = MagicMock()
        mock_game_class.return_value = mock_game_instance

        # Call the main function
        with patch('sys.exit') as mock_exit:
            main()

        # Verify the game was instantiated and play was called
        mock_game_class.assert_called_once()
        mock_game_instance.play.assert_called_once()
        mock_exit.assert_not_called()  # Exit should not be called in normal flow

    def test_main_handles_keyboard_interrupt(self):
        """Test that KeyboardInterrupt is handled gracefully."""
        # Prepare mocks and patches
        with patch('cluedo_game.cluedo_game.CluedoGame') as mock_game_class, \
             patch('cluedo_game.cluedo_game.exit') as mock_exit, \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            
            # Setup mock game instance that raises KeyboardInterrupt
            mock_game_instance = MagicMock()
            mock_game_instance.play.side_effect = KeyboardInterrupt()
            mock_game_class.return_value = mock_game_instance
            
            # Call the main function
            main()
            
            # Verify exit was called and goodbye message was printed
            assert "Game exited. Goodbye!" in mock_stdout.getvalue()
            mock_exit.assert_called_once_with(0)

    def test_main_handles_eof_error(self):
        """Test that EOFError is handled gracefully."""
        # Prepare mocks and patches
        with patch('cluedo_game.cluedo_game.CluedoGame') as mock_game_class, \
             patch('cluedo_game.cluedo_game.exit') as mock_exit, \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            
            # Setup mock game instance that raises EOFError
            mock_game_instance = MagicMock()
            mock_game_instance.play.side_effect = EOFError()
            mock_game_class.return_value = mock_game_instance
            
            # Call the main function
            main()
            
            # Verify exit was called and goodbye message was printed
            assert "Game exited. Goodbye!" in mock_stdout.getvalue()
            mock_exit.assert_called_once_with(0)
