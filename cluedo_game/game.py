import random
from cluedo_game.mansion import Mansion
from cluedo_game.character import get_characters
from cluedo_game.history import SuggestionHistory
from cluedo_game.solution import Solution
from cluedo_game.weapon import get_weapons

class CluedoGame:
    def __init__(self, input_func=input, output_func=print):
        self.input = input_func
        self.output = output_func
        self.mansion = Mansion()
        self.characters = get_characters(rooms=self.mansion.get_rooms())
        self.suggestion_history = SuggestionHistory()
        self.solution = Solution.random_solution()

        self.player = None

    def select_character(self):
        self.output("Select your character:")
        for idx, char in enumerate(self.characters):
            self.output(f"  {idx + 1}. {char.name} (starts in {char.position})")
        while True:
            inp = self.input("Enter number: ").strip()
            try:
                choice = int(inp)
                if 1 <= choice <= len(self.characters):
                    self.player = self.characters[choice - 1]
                    pos = self.player.position
                    if str(pos).startswith('C'):
                        self.output(f"\nYou are {self.player.name}, starting at corridor space {pos}.")
                    else:
                        self.output(f"\nYou are {self.player.name}, starting in the {pos}.")
                    break
                else:
                    self.output("Invalid selection.")
            except ValueError:
                self.output("Please enter a valid number.")

    def play(self):
        self.output("Welcome to Cluedo!\n")
        self.select_character()
        # Dice roll phase
        rolls = {}
        self.output("\nRolling dice to determine play order...")
        while True:
            rolls.clear()
            for char in self.characters:
                roll = random.randint(1, 6) + random.randint(1, 6)
                rolls.setdefault(roll, []).append(char)
                self.output(f"{char.name} rolls a {roll}")
            max_roll = max(rolls.keys())
            if len(rolls[max_roll]) == 1:
                break  # Unique highest roll
            self.output(f"Tie for highest roll ({max_roll}) between: {', '.join(c.name for c in rolls[max_roll])}. Re-rolling...")
            self.characters = rolls[max_roll]  # Only tied players roll again
        # Set play order: winner first, then others in original order after
        winner = rolls[max_roll][0]
        idx = self.characters.index(winner)
        self.characters = self.characters[idx:] + self.characters[:idx]
        self.output(f"\nPlay order: {', '.join(c.name for c in self.characters)}")
        # Ensure self.player is set correctly in new order
        for char in self.characters:
            if char.name == self.player.name:
                self.player = char
                break
        self.deal_cards()
        self.show_hand()
        while True:
            self.output(f"\nCurrent location: {self.player.position}")
            if not self.suggestion_phase():
                break  # Player quit
            if self.check_win():
                return
            if not self.move_phase():
                break  # Player quit

    def show_hand(self):
        hand = getattr(self.player, 'hand', [])
        if hand:
            card_names = []
            for card in hand:
                try:
                    card_names.append(card.name)
                except AttributeError:
                    card_names.append(str(card))
            self.output("\nYour cards:")
            for c in card_names:
                self.output(f"  - {c}")
        else:
            self.output("\nYou have no cards.")

    def deal_cards(self):
        # Remove solution cards from the deck
        all_characters = get_characters()
        all_weapons = get_weapons()
        all_rooms = self.mansion.get_rooms()
        sol = self.solution
        deal_characters = [c for c in all_characters if c.name != sol.character.name]
        deal_weapons = [w for w in all_weapons if w.name != sol.weapon.name]
        deal_rooms = [r for r in all_rooms if r != sol.room]
        deck = deal_characters + deal_weapons + deal_rooms
        random.shuffle(deck)
        for idx, card in enumerate(deck):
            self.characters[idx % len(self.characters)].add_card(card)

    def suggestion_phase(self):
        while True:
            inp = self.input("Would you like to make a suggestion? (y/n, 'history', or 'hand'): ").strip().lower()
            if inp == 'history':
                self.print_history()
                continue
            elif inp == 'hand':
                self.show_hand()
                continue
            elif inp == 'n':
                return True
            elif inp == 'y':
                return self.make_suggestion()
            elif inp == 'quit':
                self.output("Thanks for playing!")
                return False
            else:
                self.output("Please enter 'y', 'n', 'history', 'hand', or 'quit'.")

    def make_suggestion(self):
        # Select suspect
        suspects = [c for c in get_characters()]
        suspect = self.select_from_list("Suspect", suspects)
        # Select weapon
        weapons = get_weapons()
        weapon = self.select_from_list("Weapon", weapons)
        # Room is current room
        room = self.player.position
        # Refutation
        refuting_player, shown_card = self.handle_refutation(suspect, weapon, room)
        # Log
        self.suggestion_history.add(
            self.player.name, suspect.name, weapon.name, room, refuting_player, shown_card)
        # Check win
        if self.solution.character.name == suspect.name and \
           self.solution.weapon.name == weapon.name and \
           self.solution.room == room:
            self.output("\nCongratulations! You Win!")
            self.output(f"The solution was: {self.solution.character.name} with the {self.solution.weapon.name} in the {self.solution.room}.")
            return False
        else:
            return True

    def handle_refutation(self, suspect, weapon, room):
        for other in self.characters:
            if other == self.player:
                continue
            matching_cards = []
            for card in other.hand:
                try:
                    if card.name == suspect.name or card.name == weapon.name:
                        matching_cards.append(card)
                except AttributeError:
                    try:
                        if card == room:
                            matching_cards.append(card)
                    except Exception:
                        pass
            if matching_cards:
                shown_card = random.choice(matching_cards)
                try:
                    shown_card_name = shown_card.name
                except AttributeError:
                    shown_card_name = shown_card
                self.output(f"{other.name} can disprove your suggestion and secretly shows you the card: {shown_card_name}")
                return other.name, shown_card_name
        self.output("No one can disprove your suggestion!")
        return None, None

    def move_phase(self):
        # Roll dice for movement
        dice = random.randint(1, 6) + random.randint(1, 6)
        self.output(f"You rolled a {dice} for movement.")
        moves_left = dice
        while moves_left > 0:
            current = self.player.position
            adjacent = self.mansion.get_adjacent_spaces(current)
            self.output(f"\nCurrent position: {current}")
            self.output(f"Moves left: {moves_left}")
            self.output("Adjacent spaces:")
            for idx, space in enumerate(adjacent):
                self.output(f"  {idx + 1}. {space}")
            self.output("  0. Quit")
            inp = self.input("Move to which space? (number or 'hand'): ").strip().lower()
            if inp == 'hand':
                self.show_hand()
                continue
            try:
                move = int(inp)
                if move == 0:
                    self.output("Thanks for playing!")
                    return False
                elif 1 <= move <= len(adjacent):
                    next_space = adjacent[move - 1]
                    self.player.position = next_space
                    self.output(f"Moved to {next_space}.")
                    moves_left -= 1
                    if next_space in self.mansion.get_rooms():
                        self.output(f"You have entered the {next_space}. Movement ends.")
                        break
                else:
                    self.output("Invalid selection.")
            except ValueError:
                self.output("Please enter a valid number or 'hand'.")
        return True

    def select_from_list(self, prompt, options):
        self.output(f"Select {prompt}:")
        for idx, item in enumerate(options):
            try:
                item_name = item.name
            except AttributeError:
                item_name = str(item)
            self.output(f"  {idx + 1}. {item_name}")
        while True:
            inp = self.input(f"Enter number for {prompt}: ").strip()
            try:
                choice = int(inp)
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                else:
                    self.output("Invalid selection.")
            except ValueError:
                self.output("Please enter a valid number.")

    def check_win(self):
        # This is now handled in make_suggestion; kept for extensibility
        return False

    def out_of_guesses(self):
        self.output("\nOut of guesses!")
        self.output(f"The solution was: {self.solution.character.name} with the {self.solution.weapon.name} in the {self.solution.room}.")

    def print_history(self):
        self.output("\n--- Suggestion/Refute History ---")
        self.output(str(self.suggestion_history) if str(self.suggestion_history) else "No suggestions made yet.")

