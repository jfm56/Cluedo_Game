# cludo_game.py
# Main module for the Cluedo game logic

from cluedo_game.mansion import Mansion
from cluedo_game.character import get_characters


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
        solution = select_solution()
        guesses_left = 6
        while guesses_left > 0:
            print(f"\nCurrent room: {player.position}")
            # Suggestion opportunity
            make_suggestion = input("Would you like to make a suggestion? (y/n): ").strip().lower()
            if make_suggestion == 'y':
                # Select a character for the suggestion
                print("Select a character to suggest:")
                for idx, char in enumerate(characters):
                    print(f"  {idx + 1}. {char.name}")
                while True:
                    try:
                        char_choice = int(input("Enter number: "))
                        if 1 <= char_choice <= len(characters):
                            suggested_character = characters[char_choice - 1]
                            break
                        else:
                            print("Invalid selection.")
                    except ValueError:
                        print("Please enter a valid number.")
                # Select a weapon for the suggestion
                weapons = get_weapons()
                print("Select a weapon to suggest:")
                for idx, weapon in enumerate(weapons):
                    print(f"  {idx + 1}. {weapon.name}")
                while True:
                    try:
                        weapon_choice = int(input("Enter number: "))
                        if 1 <= weapon_choice <= len(weapons):
                            suggested_weapon = weapons[weapon_choice - 1]
                            break
                        else:
                            print("Invalid selection.")
                    except ValueError:
                        print("Please enter a valid number.")
                # Select a room for the suggestion
                all_rooms = mansion.get_rooms()
                print("Select a room to suggest:")
                for idx, room in enumerate(all_rooms):
                    print(f"  {idx + 1}. {room}")
                while True:
                    try:
                        room_choice = int(input("Enter number: "))
                        if 1 <= room_choice <= len(all_rooms):
                            suggested_room = all_rooms[room_choice - 1]
                            break
                        else:
                            print("Invalid selection.")
                    except ValueError:
                        print("Please enter a valid number.")
                print(f"\nYour suggestion: {suggested_character.name} with the {suggested_weapon.name} in the {suggested_room}.")
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
                    print(f"Sorry, that's not correct. Guesses left: {guesses_left}")
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
