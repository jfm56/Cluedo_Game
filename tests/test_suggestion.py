import pytest
from cluedo_game.suggestion import Suggestion

class DummyPlayer(str):
    pass

def test_repr_no_refutation():
    s = Suggestion('Player1', 'Miss Scarlett', 'Candlestick', 'Lounge')
    assert repr(s) == 'Player1 suggested Miss Scarlett with Candlestick in Lounge; no one refuted'

def test_repr_refuted_by_human():
    s = Suggestion('Player1', 'Miss Scarlett', 'Candlestick', 'Lounge', refuting_player='Player2', shown_card='Candlestick')
    assert repr(s) == 'Player1 suggested Miss Scarlett with Candlestick in Lounge; refuted by Player2 (card: Candlestick)'

def test_repr_refuted_by_ai():
    s = Suggestion('Player1 (AI)', 'Miss Scarlett', 'Candlestick', 'Lounge', refuting_player='Player2', shown_card='Candlestick')
    assert repr(s) == 'Player1 (AI) suggested Miss Scarlett with Candlestick in Lounge; refuted by Player2'

def test_repr_handles_nonstring():
    s = Suggestion(DummyPlayer('PlayerX'), 'Miss Scarlett', 'Candlestick', 'Lounge', refuting_player=DummyPlayer('PlayerY'), shown_card=42)
    # Should not error and should show card as 42
    assert 'card: 42' in repr(s)
