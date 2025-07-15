# cludo_game.py
# Main module for the Cluedo game logic

from cluedo_game.mansion import Mansion
from cluedo_game.character import get_characters
from cluedo_game.history import SuggestionHistory


def main():
    try:
        print("Welcome to Cluedo!\n")
        mansion = Mansion()
        characters = get_characters()

        # Let player select a character
        print("Select your character:")
        for idx, char in enumerate(characters):
            print(f"  {idx + 1}. {char.name} (starts in {char.position})")
        while True:
            try:
                choice = int(input("Enter number: "))
                if 1 <= choice <= len(characters):
                    player = characters[choice - 1]
                    break
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")

        print(f"\nYou are {player.name}, starting in the {player.position}.")

        # Game loop: allow movement between rooms
        from cluedo_game.weapon import get_weapons
        from cluedo_game.solution import select_solution
        import random
        solution = select_solution()

        # Prepare cards for dealing
        all_characters = get_characters()
        all_weapons = get_weapons()
        all_rooms = mansion.get_rooms()

        # Remove solution cards from the deck
        deal_characters = [c for c in all_characters if c.name != solution["character"].name]
        deal_weapons = [w for w in all_weapons if w.name != solution["weapon"].name]
        deal_rooms = [r for r in all_rooms if r != solution["room"]]

        # Prepare deck and shuffle
        deck = deal_characters + deal_weapons + deal_rooms
        random.shuffle(deck)

        # Deal cards to all players (characters)
        for idx, card in enumerate(deck):
            characters[idx % len(characters)].add_card(card)

        guesses_left = 6
        suggestion_history = SuggestionHistory()  # Track all suggestions and refutes
        while guesses_left > 0:
            print(f"\nCurrent room: {player.position}")
            # Suggestion opportunity
            while True:
                make_suggestion = input("Would you like to make a suggestion? (y/n or 'history'): ").strip().lower()
                if make_suggestion == 'history':
                    print("\n--- Suggestion/Refute History ---")
                    print(suggestion_history if str(suggestion_history) else "No suggestions made yet.")
                elif make_suggestion in ['y', 'n']:
                    break
                else:
                    print("Please enter 'y', 'n', or 'history'.")
            if make_suggestion == 'y':
                # Select a character for the suggestion
                print("Select a character to suggest:")
                for idx, char in enumerate(characters):
                    print(f"  {idx + 1}. {char.name}")
                while True:
                    char_choice = input("Enter number (or 'history'): ").strip().lower()
                    if char_choice == 'history':
                        print("\n--- Suggestion/Refute History ---")
                        print(suggestion_history if str(suggestion_history) else "No suggestions made yet.")
                        continue
                    try:
                        char_choice = int(char_choice)
                        if 1 <= char_choice <= len(characters):
                            suggested_character = characters[char_choice - 1]
                            break
                        else:
                            print("Invalid selection.")
                    except ValueError:
                        print("Please enter a valid number or 'history'.")
                # Select a weapon for the suggestion
                weapons = get_weapons()
                print("Select a weapon to suggest:")
                for idx, weapon in enumerate(weapons):
                    print(f"  {idx + 1}. {weapon.name}")
                while True:
                    weapon_choice = input("Enter number (or 'history'): ").strip().lower()
                    if weapon_choice == 'history':
                        print("\n--- Suggestion/Refute History ---")
                        print(suggestion_history if str(suggestion_history) else "No suggestions made yet.")
                        continue
                    try:
                        weapon_choice = int(weapon_choice)
                        if 1 <= weapon_choice <= len(weapons):
                            suggested_weapon = weapons[weapon_choice - 1]
                            break
                        else:
                            print("Invalid selection.")
                    except ValueError:
                        print("Please enter a valid number or 'history'.")
                # Select a room for the suggestion
                all_rooms = mansion.get_rooms()
                print("Select a room to suggest:")
                for idx, room in enumerate(all_rooms):
                    print(f"  {idx + 1}. {room}")
                while True:
                    room_choice = input("Enter number (or 'history'): ").strip().lower()
                    if room_choice == 'history':
                        print("\n--- Suggestion/Refute History ---")
                        print(suggestion_history if str(suggestion_history) else "No suggestions made yet.")
                        continue
                    try:
                        room_choice = int(room_choice)
                        if 1 <= room_choice <= len(all_rooms):
                            suggested_room = all_rooms[room_choice - 1]
                            break
                        else:
                            print("Invalid selection.")
                    except ValueError:
                        print("Please enter a valid number or 'history'.")
                print(f"\nYour suggestion: {suggested_character.name} with the {suggested_weapon.name} in the {suggested_room}.")

                # Suggestion disproving logic
                found_disprover = False
                # Start with the next player after the suggesting player
                player_idx = characters.index(player)
                refuting_player = None
                shown_card_name = None
                for offset in range(1, len(characters)):
                    other = characters[(player_idx + offset) % len(characters)]
                    # Check if this player can disprove
                    matching_cards = []
                    for card in other.hand:
                        if (
                            (hasattr(card, 'name') and card.name == suggested_character.name) or
                            (hasattr(card, 'name') and card.name == suggested_weapon.name) or
                            (isinstance(card, str) and card == suggested_room)
                        ):
                            matching_cards.append(card)
                    if matching_cards:
                        found_disprover = True
                        refuting_player = other.name
                        # If more than one matching card, allow the refuting player to choose which to show (AI: random)
                        if len(matching_cards) > 1:
                            # In future, prompt human refuter for choice
                            shown_card = random.choice(matching_cards)
                        else:
                            shown_card = matching_cards[0]
                        shown_card_name = shown_card.name if hasattr(shown_card, 'name') else shown_card
                        print(f"{other.name} can disprove your suggestion and secretly shows you the card: {shown_card_name}")
                        break
                if not found_disprover:
                    print("No one can disprove your suggestion!")
                    # Optionally, allow player to make an accusation here
                    refuting_player = None
                    shown_card_name = None

                # Log the suggestion and refute
                suggestion_history.add(
                    player.name,
                    suggested_character.name,
                    suggested_weapon.name,
                    suggested_room,
                    refuting_player,
                    shown_card_name
                )

                # Check if suggestion matches the solution
                if (
                    suggested_character.name == solution["character"].name and
                    suggested_weapon.name == solution["weapon"].name and
                    suggested_room == solution["room"]
                ):
                    print("\nCongratulations! You Win!")
                    print(f"The solution was: {solution['character'].name} with the {solution['weapon'].name} in the {solution['room']}.")
                    return
                else:
                    guesses_left -= 1
                    print(f"Guesses left: {guesses_left}")
                    # Continue to room selection

            adjacent = mansion.get_adjacent_rooms(player.position)
            print("Adjacent rooms:")
            for idx, room in enumerate(adjacent):
                print(f"  {idx + 1}. {room}")
            print("  0. Quit")
            try:
                move = int(input("Move to which room? (number): "))
                if move == 0:
                    print("Thanks for playing!")
                    break
                elif 1 <= move <= len(adjacent):
                    player.position = adjacent[move - 1]
                    print(f"Moved to {player.position}.")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")
        # If loop exits without a win
        print("\nOut of guesses!")
        print(f"The solution was: {solution['character'].name} with the {solution['weapon'].name} in the {solution['room']}.")

    except (EOFError, KeyboardInterrupt):
        print("\nGame exited. Goodbye!")
        exit(0)


if __name__ == "__main__":
    main()
