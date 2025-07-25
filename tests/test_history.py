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
        try:
            self.assertEqual(len(all_entries), 2)
            self.assertEqual(all_entries[0]['suggesting_player'], 'Player1')
            self.assertIsNone(all_entries[0]['refuting_player'])
            self.assertEqual(all_entries[1]['refuting_player'], 'Player3')
            self.assertEqual(all_entries[1]['shown_card'], 'Dagger')
        except Exception as e:
            self.fail(f"SuggestionHistory add/get_all check failed: {e}")

    def test_str_representation(self):
        history = SuggestionHistory()
        history.add('Player1', 'Miss Scarlett', 'Rope', 'Lounge', None, None)
        history.add('Player2', 'Colonel Mustard', 'Dagger', 'Kitchen', 'Player3', 'Dagger')
        s = str(history)
        try:
            self.assertIn('Player1', s)
            self.assertIn('Miss Scarlett / Rope / Lounge', s)
            self.assertIn('Player2', s)
            self.assertIn('Colonel Mustard / Dagger / Kitchen', s)
            self.assertIn('Player3', s)
            self.assertIn('Dagger', s)
        except Exception as e:
            self.fail(f"SuggestionHistory str representation check failed: {e}")

    def test_history_str(self):
        hist = SuggestionHistory()
        # Human suggestion (should show card)
        hist.add("Miss Scarlett", "Colonel Mustard", "Candlestick", "Kitchen", "Mrs. White", "Kitchen")
        # AI suggestion (should NOT show card)
        hist.add("Colonel Mustard (AI)", "Miss Scarlett", "Rope", "Ballroom", "Mrs. Peacock", "Ballroom")
        s = str(hist)
        # Human suggestion row shows card
        try:
            self.assertRegex(s, r"Miss Scarlett.*Kitchen.*Kitchen")
            # AI suggestion row does not show card, only '—'
            for line in s.splitlines():
                if "Colonel Mustard (AI)" in line:
                    # Accept table output ending with '— |'
                    self.assertTrue(line.rstrip().endswith("— |"))
        except Exception as e:
            self.fail(f"SuggestionHistory history str check failed: {e}")

if __name__ == '__main__':
    unittest.main()
