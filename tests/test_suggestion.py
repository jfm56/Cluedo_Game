import pytest
from cluedo_game.suggestion import Suggestion

class DummyPlayer(str):
    pass

def test_repr_no_refutation():
    s = Suggestion('Player1', 'Miss Scarlett', 'Candlestick', 'Lounge')
    try:
        assert repr(s) == 'Player1 suggested Miss Scarlett with Candlestick in Lounge; no one refuted'
    except Exception as e:
        pytest.fail(f"repr no refutation check failed: {e}")

def test_repr_refuted_by_human():
    s = Suggestion('Player1', 'Miss Scarlett', 'Candlestick', 'Lounge', refuting_player='Player2', shown_card='Candlestick')
    try:
        assert repr(s) == 'Player1 suggested Miss Scarlett with Candlestick in Lounge; refuted by Player2 (card: Candlestick)'
    except Exception as e:
        pytest.fail(f"repr refuted by human check failed: {e}")

def test_repr_refuted_by_ai():
    s = Suggestion('Player1 (AI)', 'Miss Scarlett', 'Candlestick', 'Lounge', refuting_player='Player2', shown_card='Candlestick')
    try:
        assert repr(s) == 'Player1 (AI) suggested Miss Scarlett with Candlestick in Lounge; refuted by Player2'
    except Exception as e:
        pytest.fail(f"repr refuted by AI check failed: {e}")

def test_repr_handles_nonstring():
    s = Suggestion(DummyPlayer('PlayerX'), 'Miss Scarlett', 'Candlestick', 'Lounge', refuting_player=DummyPlayer('PlayerY'), shown_card=42)
    # Should not error and should show card as 42
    try:
        assert 'card: 42' in repr(s)
    except Exception as e:
        pytest.fail(f"repr handles nonstring card check failed: {e}")
