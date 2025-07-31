"""
Tests for the cards, weapons, and character components in the Cluedo game.
Merged from separate component test files to reduce test file count.
"""
import pytest

from cluedo_game.cards import (
    Card, SuspectCard, WeaponCard, RoomCard,
    get_suspects, get_suspect_by_name,
    CHARACTER_STARTING_SPACES as CARD_STARTING_SPACES,  # Renamed to avoid conflict
    SUSPECTS
)

from cluedo_game.weapon import (
    Weapon,
    WEAPONS,
    WEAPON_CARDS,
    get_weapons,
    get_weapon_by_name
)

from cluedo_game.character import (
    Character,
    CHARACTER_NAMES,
    CHARACTER_STARTING_SPACES,
    get_characters,
    get_character_by_name
)

#------------------------------------------------------------------------------
# Card Tests
#------------------------------------------------------------------------------
class TestCards:
    """Test suite for the cards module."""
    
    def test_card_init(self):
        """Test the initialization of the base Card class."""
        card = Card("Test Card")
        assert card.name == "Test Card"
    
    def test_card_equality(self):
        """Test that cards with the same name are considered equal."""
        card1 = Card("Test Card")
        card2 = Card("Test Card")
        card3 = Card("Different Card")
        
        assert card1 == card2
        assert card1 != card3
    
    def test_card_str_representation(self):
        """Test the string representation of a Card instance."""
        card = Card("Test Card")
        assert str(card) == "Card(name=Test Card)"
    
    def test_suspect_card_init(self):
        """Test the initialization of the SuspectCard class."""
        suspect = SuspectCard("Colonel Mustard")
        assert suspect.name == "Colonel Mustard"
        assert isinstance(suspect, Card)
    
    def test_weapon_card_init(self):
        """Test the initialization of the WeaponCard class."""
        weapon = WeaponCard("Candlestick")
        assert weapon.name == "Candlestick"
        assert isinstance(weapon, Card)
    
    def test_room_card_init(self):
        """Test the initialization of the RoomCard class."""
        room = RoomCard("Library")
        assert room.name == "Library"
        assert isinstance(room, Card)
    
    def test_get_suspects(self):
        """Test the get_suspects function returns the correct suspects."""
        suspects = get_suspects()
        
        # Check we have the expected number of suspects
        assert len(suspects) == 6
        
        # Check all suspects are SuspectCard instances
        for suspect in suspects:
            assert isinstance(suspect, SuspectCard)
        
        # Check all expected suspect names are present
        suspect_names = [suspect.name for suspect in suspects]
        expected_names = ["Colonel Mustard", "Professor Plum", "Reverend Green", 
                          "Mrs. Peacock", "Miss Scarlett", "Mrs. White"]
        
        for name in expected_names:
            assert name in suspect_names
            
    def test_get_suspect_by_name(self):
        """Test the get_suspect_by_name function."""
        # Test finding an existing suspect
        suspect = get_suspect_by_name("Colonel Mustard")
        assert suspect is not None
        assert suspect.name == "Colonel Mustard"
        assert isinstance(suspect, SuspectCard)
        
        # Test finding a non-existent suspect
        suspect = get_suspect_by_name("Non-existent Character")
        assert suspect is None
    
    # No get_weapons() function exists, so we'll test the WeaponCard class directly
    def test_weapon_card(self):
        """Test the WeaponCard class."""
        weapon = WeaponCard("Candlestick")
        assert weapon.name == "Candlestick"
        assert isinstance(weapon, Card)
    
    # No get_rooms() function exists, so we'll test the RoomCard class directly
    def test_room_card(self):
        """Test the RoomCard class."""
        room = RoomCard("Kitchen")
        assert room.name == "Kitchen"
        assert isinstance(room, Card)
    
    def test_character_starting_spaces(self):
        """Test that CHARACTER_STARTING_SPACES has the correct mappings."""
        # Check all suspects have a starting position
        for suspect in get_suspects():
            assert suspect.name in CARD_STARTING_SPACES
        
        # Check specific starting positions (add more as needed)
        assert CARD_STARTING_SPACES["Colonel Mustard"] == "C2"
        
        # Check all starting positions are valid
        valid_positions = ["C" + str(i) for i in range(1, 13)]  # C1 to C12
        for position in CARD_STARTING_SPACES.values():
            assert position in valid_positions

#------------------------------------------------------------------------------
# Weapon Tests
#------------------------------------------------------------------------------
class TestWeapon:
    """Test suite for the Weapon class and related functions."""

    def test_weapon_init(self):
        """Test initialization of a Weapon object."""
        name = "Candlestick"
        weapon = Weapon(name)
        
        assert weapon.name == name

    def test_weapon_repr(self):
        """Test the string representation of a Weapon object."""
        weapon = Weapon("Candlestick")
        
        assert repr(weapon) == "Weapon(Candlestick)"

    def test_weapon_equality_same_weapon(self):
        """Test equality comparison between identical weapons."""
        weapon1 = Weapon("Candlestick")
        weapon2 = Weapon("Candlestick")
        
        assert weapon1 == weapon2

    def test_weapon_equality_different_weapons(self):
        """Test equality comparison between different weapons."""
        weapon1 = Weapon("Candlestick")
        weapon2 = Weapon("Rope")
        
        assert weapon1 != weapon2

    def test_weapon_equality_non_weapon(self):
        """Test equality comparison with non-Weapon objects."""
        weapon = Weapon("Candlestick")
        
        assert weapon != "Candlestick"
        assert weapon != 42
        assert weapon != None
        assert weapon != {"name": "Candlestick"}

    def test_weapons_constant(self):
        """Test WEAPONS constant contains all expected weapons."""
        expected_names = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
        weapon_names = [weapon.name for weapon in WEAPONS]
        
        # Check all expected weapons are in WEAPONS
        for name in expected_names:
            assert name in weapon_names
        
        # Check WEAPONS doesn't have extra weapons
        assert len(WEAPONS) == len(expected_names)
        
        # Check each weapon is a Weapon instance
        for weapon in WEAPONS:
            assert isinstance(weapon, Weapon)

    def test_weapon_cards_constant(self):
        """Test WEAPON_CARDS constant contains cards for all weapons."""
        # Check we have the same number of cards as weapons
        assert len(WEAPON_CARDS) == len(WEAPONS)
        
        # Check each card is a WeaponCard instance
        for card in WEAPON_CARDS:
            assert isinstance(card, WeaponCard)
        
        # Check card names match weapon names
        weapon_names = [weapon.name for weapon in WEAPONS]
        card_names = [card.name for card in WEAPON_CARDS]
        
        assert sorted(weapon_names) == sorted(card_names)

    def test_get_weapons(self):
        """Test get_weapons returns the WEAPONS constant."""
        weapons = get_weapons()
        
        assert weapons is WEAPONS  # Check it returns the exact same object
        assert len(weapons) == len(WEAPONS)

    def test_get_weapon_by_name_valid(self):
        """Test get_weapon_by_name returns correct weapon for valid name."""
        for expected_weapon in WEAPONS:
            weapon = get_weapon_by_name(expected_weapon.name)
            assert weapon is not None
            assert weapon.name == expected_weapon.name
            # Should return the exact object from WEAPONS
            assert weapon is expected_weapon

    def test_get_weapon_by_name_invalid(self):
        """Test get_weapon_by_name returns None for invalid name."""
        weapon = get_weapon_by_name("Nonexistent Weapon")
        assert weapon is None

#------------------------------------------------------------------------------
# Character Tests
#------------------------------------------------------------------------------
class TestCharacter:
    """Test suite for the Character class and related functions."""

    def test_character_init(self):
        """Test initialization of a Character object."""
        name = "Miss Scarlett"
        position = "C1"
        character = Character(name, position)
        
        assert character.name == name
        assert character.position == position
        assert character.hand == []

    def test_character_add_card(self):
        """Test adding a card to a character's hand."""
        character = Character("Miss Scarlett", "C1")
        card = SuspectCard("Colonel Mustard")
        
        character.add_card(card)
        
        assert len(character.hand) == 1
        assert character.hand[0] == card

    def test_character_repr(self):
        """Test the string representation of a Character object."""
        character = Character("Miss Scarlett", "C1")
        
        # Test with empty hand
        assert repr(character) == "Character(name=Miss Scarlett, position=C1, hand=[])"
        
        # Add a card and test again
        card = SuspectCard("Colonel Mustard")
        character.add_card(card)
        assert repr(character) == f"Character(name=Miss Scarlett, position=C1, hand=[{repr(card)}])"

    def test_character_names_constant(self):
        """Test CHARACTER_NAMES constant contains all the expected names."""
        expected_names = [
            "Miss Scarlett", "Colonel Mustard", "Mrs. White", 
            "Reverend Green", "Mrs. Peacock", "Professor Plum"
        ]
        
        # Check all expected names are in CHARACTER_NAMES
        for name in expected_names:
            assert name in CHARACTER_NAMES
        
        # Check CHARACTER_NAMES doesn't have extra names
        assert len(CHARACTER_NAMES) == len(expected_names)

    def test_character_starting_spaces(self):
        """Test CHARACTER_STARTING_SPACES constant has correct mappings."""
        expected_mappings = {
            "Miss Scarlett": "C1",
            "Colonel Mustard": "C2",
            "Mrs. White": "C3",
            "Reverend Green": "C4",
            "Mrs. Peacock": "C5",
            "Professor Plum": "C6"
        }
        
        # Check all expected mappings are correct
        for name, position in expected_mappings.items():
            assert CHARACTER_STARTING_SPACES[name] == position
        
        # Check CHARACTER_STARTING_SPACES doesn't have extra mappings
        assert len(CHARACTER_STARTING_SPACES) == len(expected_mappings)

    def test_get_characters(self):
        """Test get_characters returns list of Character objects with correct properties."""
        characters = get_characters()
        
        # Check we got the expected number of characters
        assert len(characters) == len(CHARACTER_NAMES)
        
        # Check each character has correct name and position
        for character in characters:
            assert character.name in CHARACTER_NAMES
            assert character.position == CHARACTER_STARTING_SPACES[character.name]

    def test_get_character_by_name_valid(self):
        """Test get_character_by_name returns correct character for valid name."""
        # Test for each valid character name
        for name in CHARACTER_NAMES:
            character = get_character_by_name(name)
            assert character is not None
            assert character.name == name
            assert character.position == CHARACTER_STARTING_SPACES[name]

    def test_get_character_by_name_invalid(self):
        """Test get_character_by_name returns None for invalid name."""
        character = get_character_by_name("Nonexistent Character")
        assert character is None

    def test_get_character_by_name_handles_exceptions(self, monkeypatch):
        """Test get_character_by_name properly handles AttributeError exceptions."""
        # Create a mock list of "characters" where one item will raise AttributeError
        # when its name is accessed
        class MockCharacterWithoutName:
            @property
            def name(self):
                raise AttributeError("No name attribute")
        
        mock_character_list = [MockCharacterWithoutName()]
        
        # We need to patch get_characters to return our mock list
        monkeypatch.setattr('cluedo_game.character.get_characters', lambda: mock_character_list)
        
        # Test that the function handles the exception gracefully
        result = get_character_by_name("Some Name")
        assert result is None
