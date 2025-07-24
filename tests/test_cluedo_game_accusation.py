import unittest
from unittest.mock import patch

from cluedo_game.game     import CluedoGame
from cluedo_game.solution   import Solution
from cluedo_game.weapon import Weapon
from cluedo_game.mansion import Room
from cluedo_game.character import Character  # Use Character as Suspect if needed
from cluedo_game.weapon   import get_weapons

class TestCluedoGameIntegration(unittest.TestCase):

    def test_player_can_win_with_accusation_anywhere(self):
        # Force the solution
        forced = Solution(
            character=Character('Miss Scarlett', 'C1'),
            weapon=Weapon('Rope'),
            room=Room('Lounge'),
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
            corridor = next(sp for sp in game.mansion.get_corridors())
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
            character=Character('Miss Scarlett', 'C1'),
            weapon=Weapon('Rope'),
            room=Room('Lounge'),
        )
        with patch.object(Solution, 'random_solution', lambda: forced):
            game = CluedoGame(input_func=lambda _: '1', output_func=lambda m: None)
            game.select_character()
            game.deal_cards()
            human = game.player

            # Make a false accusation (wrong weapon)
            wrong_weapon = Weapon('Candlestick')
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
            character=Character('Miss Scarlett', 'C1'),
            weapon=Weapon('Rope'),
            room=Room('Lounge'),
        )
        with patch.object(Solution, 'random_solution', lambda: forced):
            # Setup game
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

            # Prepare suggestion inputs: suspect index, weapon index, then quit
            try:
                sus_idx = next(i for i, c in enumerate(game.characters, 1) if getattr(c, 'name', c) == forced.character.name)
            except StopIteration:
                raise AssertionError(f"Suspect '{forced.character.name}' not found in game.characters: {[getattr(c, 'name', c) for c in game.characters]}")
            weap_list = get_weapons()
            try:
                weap_idx = next(i for i, w in enumerate(weap_list, 1) if getattr(w, 'name', w) == forced.weapon.name)
            except StopIteration:
                raise AssertionError(f"Weapon '{forced.weapon.name}' not found in weap_list: {[getattr(w, 'name', w) for w in weap_list]}")
            inputs = [str(sus_idx), str(weap_idx), '0']
            game.input = lambda prompt='': inputs.pop(0)

            game.make_suggestion()
            joined = '\n'.join(outputs)
            self.assertIn("Congratulations! You Win!", joined)

    def test_blocking_door_rule_on_false_accusation(self):
        # Force the solution
        forced = Solution(
            character=Character('Miss Scarlett', 'C1'),
            weapon=Weapon('Rope'),
            room=Room('Lounge'),
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

            # False accusation
            wrong_weapon = Weapon('Candlestick')
            result = game.make_accusation(
                suspect=forced.character,
                weapon=wrong_weapon,
                room=lounge
            )

            self.assertFalse(result, "False accusation did not return False")
            self.assertEqual(human.position, lounge, "Blocking door rule did not move player back into room")

if __name__ == '__main__':
    unittest.main()
