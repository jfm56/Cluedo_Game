import pytest
from cluedo_game.history import SuggestionHistory
from cluedo_game.cards import SuspectCard, WeaponCard, RoomCard


class TestSuggestionHistory:
    """Test suite for the SuggestionHistory class."""

    def test_init(self):
        """Test initialization of a SuggestionHistory object."""
        history = SuggestionHistory()
        assert history.records == []

    def test_add(self):
        """Test adding a suggestion to the history."""
        history = SuggestionHistory()
        
        # Test data
        suggesting_player = "Miss Scarlett"
        suggested_character = SuspectCard("Colonel Mustard")
        suggested_weapon = WeaponCard("Rope")
        suggested_room = RoomCard("Kitchen")
        refuting_player = "Professor Plum"
        shown_card = suggested_weapon
        
        # Add a suggestion
        history.add(suggesting_player, suggested_character, suggested_weapon, suggested_room, refuting_player, shown_card)
        
        # Verify the record was added correctly
        assert len(history.records) == 1
        record = history.records[0]
        assert record["suggesting_player"] == suggesting_player
        assert record["suggested_character"] == suggested_character
        assert record["suggested_weapon"] == suggested_weapon
        assert record["suggested_room"] == suggested_room
        assert record["refuting_player"] == refuting_player
        assert record["shown_card"] == shown_card

    def test_get_all(self):
        """Test get_all method returns all records."""
        history = SuggestionHistory()
        
        # Add two suggestions
        history.add("Miss Scarlett", SuspectCard("Colonel Mustard"), WeaponCard("Rope"), 
                   RoomCard("Kitchen"), "Professor Plum", WeaponCard("Rope"))
        
        history.add("Professor Plum", SuspectCard("Mrs. White"), WeaponCard("Candlestick"), 
                   RoomCard("Library"), "Miss Scarlett", SuspectCard("Mrs. White"))
        
        # Verify get_all returns all records
        records = history.get_all()
        assert len(records) == 2
        assert records[0]["suggesting_player"] == "Miss Scarlett"
        assert records[1]["suggesting_player"] == "Professor Plum"

    def test_str_empty_history(self):
        """Test string representation of an empty history."""
        history = SuggestionHistory()
        assert str(history) == "No suggestions yet."

    def test_str_with_records(self):
        """Test string representation with records."""
        history = SuggestionHistory()
        
        # Add a suggestion with refutation
        history.add("Miss Scarlett", SuspectCard("Colonel Mustard"), WeaponCard("Rope"), 
                   RoomCard("Kitchen"), "Professor Plum", WeaponCard("Rope"))
        
        # Verify string representation contains expected elements
        result = str(history)
        assert "Turn" in result
        assert "Suggester" in result
        assert "Suggestion" in result
        assert "Refuter" in result
        assert "Card Shown" in result
        assert "Miss Scarlett" in result
        assert "Colonel Mustard" in result
        assert "Rope" in result
        assert "Kitchen" in result
        assert "Professor Plum" in result

    def test_str_with_ai_suggester(self):
        """Test string representation with AI suggester."""
        history = SuggestionHistory()
        
        # Add a suggestion from an AI player
        history.add("Colonel Mustard (AI)", SuspectCard("Miss Scarlett"), WeaponCard("Revolver"), 
                   RoomCard("Ballroom"), "Professor Plum", WeaponCard("Revolver"))
        
        # Verify string representation hides the card shown for AI suggester
        result = str(history)
        assert "Colonel Mustard (AI)" in result
        assert "Professor Plum" in result
        # Card should be hidden with the dash character
        assert "—" in result

    def test_str_with_no_refutation(self):
        """Test string representation with no refutation."""
        history = SuggestionHistory()
        
        # Add a suggestion without refutation
        history.add("Miss Scarlett", SuspectCard("Colonel Mustard"), WeaponCard("Rope"), 
                   RoomCard("Kitchen"), None, None)
        
        # Verify string representation shows 'None' for refuter and '—' for card shown
        result = str(history)
        assert "None" in result
        assert "—" in result

    def test_str_with_complex_records(self):
        """Test string representation with various types of records."""
        history = SuggestionHistory()
        
        # Add various types of suggestions
        # 1. Normal suggestion with refutation
        history.add("Miss Scarlett", SuspectCard("Colonel Mustard"), WeaponCard("Rope"), 
                   RoomCard("Kitchen"), "Professor Plum", WeaponCard("Rope"))
        
        # 2. AI suggestion with refutation (card should be hidden)
        history.add("Colonel Mustard (AI)", SuspectCard("Miss Scarlett"), WeaponCard("Revolver"), 
                   RoomCard("Ballroom"), "Professor Plum", WeaponCard("Revolver"))
        
        # 3. Suggestion without refutation
        history.add("Mrs. White", SuspectCard("Professor Plum"), WeaponCard("Candlestick"), 
                   RoomCard("Conservatory"), None, None)
        
        # 4. Suggestion with missing shown card
        history.add("Reverend Green", SuspectCard("Mrs. Peacock"), WeaponCard("Lead Pipe"), 
                   RoomCard("Study"), "Miss Scarlett", None)
        
        # Verify string representation formats all records correctly
        result = str(history)
        
        # Check number of rows (header + separator + 4 records + borders)
        assert result.count("\n") >= 7
        
        # Check formatting
        assert "Turn" in result
        assert "1" in result
        assert "2" in result
        assert "3" in result
        assert "4" in result
        assert "None" in result
        assert "—" in result
