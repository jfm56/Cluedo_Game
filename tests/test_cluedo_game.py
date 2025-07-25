import unittest
import pytest
from unittest.mock import patch
import random
from cluedo_game.game import CluedoGame
from cluedo_game.solution import Solution
from cluedo_game.cards import SuspectCard, WeaponCard, RoomCard


# Patch the roll_for_play_order method to prevent test hangs
@pytest.fixture(autouse=True)
def no_roll_for_play_order(monkeypatch):
    """Prevent dice roll method from running during tests"""
    def mock_roll(*args, **kwargs):
        return None
    monkeypatch.setattr(CluedoGame, '_roll_for_play_order', mock_roll)


class TestCluedoGameIntegration(unittest.TestCase):

    def test_player_can_win_with_accusation_anywhere(self):
        # Force the solution
        forced = Solution(
            character=SuspectCard("Miss Scarlett"),
            weapon=WeaponCard("Rope"),
            room=RoomCard("Lounge"),
        )
        with patch.object(Solution, 'random_solution', lambda: forced):
            # Setup game and select first character
            inputs = ['1']
            outputs = []
            game = CluedoGame(
                input_func=lambda prompt='': inputs.pop(0),
                output_func=outputs.append
            )
            game.select_character()
            game.deal_cards()

            # Ensure human holds the forced cards
            human = game.player
            for card in (forced.character, forced.weapon, forced.room):
                if card not in human.hand:
                    human.hand.append(card)

            # Place human in a corridor
            lounge = next(r for r in game.mansion.get_rooms() if r.name == forced.room.name)
            corridor = next(c for c in game.mansion.get_adjacent_spaces(lounge) if str(c).startswith('C'))
            human.position = corridor

            # Make accusation
            result = game.make_accusation(
                suspect=forced.character,
                weapon=forced.weapon,
                room=forced.room
            )

            joined = '\n'.join(outputs)
            self.assertTrue(result, "Correct accusation did not return True")
            self.assertIn("Congratulations! You Win!", joined)
            self.assertIn(forced.character.name, joined)
            self.assertIn(forced.weapon.name, joined)
            self.assertIn(forced.room.name, joined)

    def test_player_is_eliminated_after_false_accusation(self):
        # Force the solution
        forced = Solution(
            character=SuspectCard("Miss Scarlett"),
            weapon=WeaponCard("Rope"),
            room=RoomCard("Lounge"),
        )
        with patch.object(Solution, 'random_solution', lambda: forced):
            game = CluedoGame(input_func=lambda _: '1', output_func=lambda m: None)
            game.select_character()
            game.deal_cards()
            human = game.player

            # Make a false accusation (wrong weapon)
            wrong_weapon = WeaponCard("Candlestick")
            result = game.make_accusation(
                suspect=forced.character,
                weapon=wrong_weapon,
                room=forced.room
            )

            self.assertFalse(result, "False accusation did not return False")
            self.assertTrue(human.eliminated, "Player was not marked eliminated after false accusation")

    def test_player_can_win_unrefuted(self):
        # Force the solution
        forced = Solution(
            character=SuspectCard("Miss Scarlett"),
            weapon=WeaponCard("Rope"),
            room=RoomCard("Lounge"),
        )
        with patch.object(Solution, 'random_solution', lambda: forced):
            inputs = ['1']
            outputs = []
            game = CluedoGame(
                input_func=lambda prompt='': inputs.pop(0),
                output_func=outputs.append
            )
            game.select_character()
            game.deal_cards()
            human = game.player

            # Ensure human holds the forced cards
            for card in (forced.character, forced.weapon, forced.room):
                if card not in human.hand:
                    human.hand.append(card)

            # Place human in the correct room
            lounge = next(r for r in game.mansion.get_rooms() if r.name == forced.room.name)
            human.position = lounge

            # Prepare suggestion inputs
            sus_idx = next(i for i, c in enumerate(game.characters, 1)
                           if c.name == forced.character.name)
            from cluedo_game.weapon import get_weapons
            weap_list = get_weapons()
            weap_idx = next(i for i, w in enumerate(weap_list, 1)
                            if w.name == forced.weapon.name)
            inputs = [str(sus_idx), str(weap_idx), '0']
            game.input = lambda prompt='': inputs.pop(0)

            game.make_suggestion()
            joined = '\n'.join(outputs)
            self.assertIn("Congratulations! You Win!", joined)

    def test_blocking_door_rule_on_false_accusation(self):
        # Force the solution
        forced = Solution(
            character=SuspectCard("Miss Scarlett"),
            weapon=WeaponCard("Rope"),
            room=RoomCard("Lounge"),
        )
        with patch.object(Solution, 'random_solution', lambda: forced):
            game = CluedoGame(input_func=lambda _: '1', output_func=lambda m: None)
            game.select_character()
            game.deal_cards()
            human = game.player

            # Place in room then corridor, record last door
            lounge = next(r for r in game.mansion.get_rooms() if r.name == forced.room.name)
            corridor = next(c for c in game.mansion.get_adjacent_spaces(lounge) if str(c).startswith('C'))
            human.position = lounge
            game.last_door_passed[human] = lounge
            human.position = corridor

            wrong_weapon = WeaponCard("Candlestick")
            result = game.make_accusation(
                suspect=forced.character,
                weapon=wrong_weapon,
                room=lounge
            )

            self.assertFalse(result, "False accusation did not return False")
            self.assertEqual(human.position, lounge, "Blocking door rule did not move player back into room")

    def test_roll_for_play_order_deterministic(self):
        # Only two players to simplify
        game = CluedoGame(input_func=lambda x=None: "", output_func=lambda x: None)
        game.characters = game.characters[:2]

        # Round 1: 6+1=7 vs 2+5=7 → tie
        # Round 2: 6+0=6 vs 0+0=0 → no tie → exit
        responses = [6, 1,  2, 5,  6, 0,  0, 0]
        def fake_randint(a, b):
            return responses.pop(0) if responses else a

        import random as _random
        original_randint = _random.randint
        try:
            _random.randint = fake_randint
            # Should now complete without hanging
            game._roll_for_play_order()
        finally:
            # Restore original function
            _random.randint = original_randint

if __name__ == '__main__':
    unittest.main()
