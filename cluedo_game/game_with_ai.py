import random
from cluedo_game.mansion import Mansion
from cluedo_game.character import get_characters
from cluedo_game.history import SuggestionHistory
from cluedo_game.solution import Solution
from cluedo_game.weapon import get_weapons
from cluedo_game.ai_player import AIPlayer
from cluedo_game.player import Player

class CluedoGameWithAI:
    def __init__(self, input_func=input, output_func=print):
        self.input = input_func
        self.output = output_func
        self.mansion = Mansion()
        self.characters = get_characters(rooms=self.mansion.get_rooms())
        self.suggestion_history = SuggestionHistory()
        self.solution = Solution.random_solution()
        self.guesses_left = 6
        self.player = None
        self.ai_players = []

    def select_character(self):
        self.output("Select your character:")
        for idx, char in enumerate(self.characters):
            self.output(f"  {idx + 1}. {char.name} (starts in {char.position})")
        while True:
            inp = self.input("Enter number: ").strip()
            try:
                choice = int(inp)
                if 1 <= choice <= len(self.characters):
                    self.player = Player(self.characters[choice - 1], is_human=True)
                    # All other characters are AI
                    self.ai_players = [AIPlayer(c) for i, c in enumerate(self.characters) if i != (choice - 1)]
                    break
                else:
                    self.output("Invalid selection.")
            except ValueError:
                self.output("Please enter a valid number.")

    def play(self):
        self.output("Welcome to Cluedo!\n")
        self.select_character()
        self.deal_cards()
        while self.guesses_left > 0:
            self.output(f"\nCurrent room: {self.player.position}")
            if not self.suggestion_phase():
                break  # Player quit
            if self.check_win():
                return
            if not self.move_phase():
                break  # Player quit
            # AI TURNS
            for ai in self.ai_players:
                self.output(f"\n{ai.name} (AI) is taking their turn...")
                ai_win = ai.take_turn(self)
                if ai_win:
                    return
        else:
            self.out_of_guesses()

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
        all_players = [self.player] + self.ai_players
        for idx, card in enumerate(deck):
            all_players[idx % len(all_players)].add_card(card)

    def suggestion_phase(self):
        while True:
            inp = self.input("Would you like to make a suggestion? (y/n or 'history'): ").strip().lower()
            if inp == 'history':
                self.print_history()
                continue
            elif inp == 'n':
                return True
            elif inp == 'y':
                return self.make_suggestion()
            elif inp == 'quit':
                self.output("Thanks for playing!")
                return False
            else:
                self.output("Please enter 'y', 'n', 'history', or 'quit'.")

    def make_suggestion(self):
        suspects = [c for c in get_characters()]
        suspect = self.select_from_list("Suspect", suspects)
        weapons = get_weapons()
        weapon = self.select_from_list("Weapon", weapons)
        room = self.player.position
        refuting_player, shown_card = self.handle_refutation(suspect, weapon, room)
        # Always use self.player.name so AI/human is correctly labeled
        suggester_name = getattr(self.player, 'name', str(self.player))
        self.suggestion_history.add(
            suggester_name, suspect.name, weapon.name, room, refuting_player, shown_card)
        if self.solution.character.name == suspect.name and \
           self.solution.weapon.name == weapon.name and \
           self.solution.room == room:
            self.output("\nCongratulations! You Win!")
            self.output(f"The solution was: {self.solution.character.name} with the {self.solution.weapon.name} in the {self.solution.room}.")
            return False
        else:
            self.guesses_left -= 1
            self.output(f"Guesses left: {self.guesses_left}")
            return True

    def handle_refutation(self, suspect, weapon, room):
        # AI and human refutation
        all_players = [self.player] + self.ai_players
        for other in all_players:
            if other == self.player:
                continue
            matching_cards = []
            for card in other.hand:
                if (hasattr(card, 'name') and (card.name == suspect.name or card.name == weapon.name)) or (isinstance(card, str) and card == room):
                    matching_cards.append(card)
            if matching_cards:
                shown_card = random.choice(matching_cards)
                shown_card_name = shown_card.name if hasattr(shown_card, 'name') else shown_card
                self.output(f"{other.name} can disprove your suggestion and secretly shows you the card: {shown_card_name}")
                return other.name, shown_card_name
        self.output("No one can disprove your suggestion!")
        return None, None

    def move_phase(self):
        adjacent = self.mansion.get_adjacent_rooms(self.player.position)
        self.output("Adjacent rooms:")
        for idx, room in enumerate(adjacent):
            self.output(f"  {idx + 1}. {room}")
        self.output("  0. Quit")
        try:
            move = int(self.input("Move to which room? (number): "))
            if move == 0:
                self.output("Thanks for playing!")
                return False
            elif 1 <= move <= len(adjacent):
                self.player.position = adjacent[move - 1]
                self.output(f"Moved to {self.player.position}.")
                return True
            else:
                self.output("Invalid selection.")
                return self.move_phase()
        except ValueError:
            self.output("Please enter a valid number.")
            return self.move_phase()

    def select_from_list(self, prompt, options):
        self.output(f"Select {prompt}:")
        for idx, item in enumerate(options):
            self.output(f"  {idx + 1}. {item.name if hasattr(item, 'name') else str(item)}")
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

if __name__ == "__main__":
    game = CluedoGameWithAI()
    game.play()
