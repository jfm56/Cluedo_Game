import unittest
from cluedo_game.history import SuggestionHistory

class TestSuggestionHistory(unittest.TestCase):
    def test_add_and_get_all(self):
        history = SuggestionHistory()
        # Add a suggestion with no refute
        history.add('Player1', 'Miss Scarlett', 'Rope', 'Lounge', None, None)
        # Add a suggestion with a refute
        history.add('Player2', 'Colonel Mustard', 'Dagger', 'Kitchen', 'Player3', 'Dagger')
        all_entries = history.get_all()
        self.assertEqual(len(all_entries), 2)
        self.assertEqual(all_entries[0]['suggesting_player'], 'Player1')
        self.assertIsNone(all_entries[0]['refuting_player'])
        self.assertEqual(all_entries[1]['refuting_player'], 'Player3')
        self.assertEqual(all_entries[1]['shown_card'], 'Dagger')

    def test_str_representation(self):
        history = SuggestionHistory()
        history.add('Player1', 'Miss Scarlett', 'Rope', 'Lounge', None, None)
        history.add('Player2', 'Colonel Mustard', 'Dagger', 'Kitchen', 'Player3', 'Dagger')
        s = str(history)
        self.assertIn('Player1 suggested Miss Scarlett with the Rope in the Lounge; no one refuted', s)
        self.assertIn('Player2 suggested Colonel Mustard with the Dagger in the Kitchen; refuted by Player3 (card: Dagger)', s)

if __name__ == '__main__':
    unittest.main()
