import random
from cluedo_game.mansion import Mansion
from cluedo_game.history import SuggestionHistory
from cluedo_game.solution import Solution
from cluedo_game.weapon import get_weapons
from cluedo_game.cards import SuspectCard, WeaponCard, RoomCard, get_suspects, CHARACTER_STARTING_SPACES

class CluedoGame:
    def __init__(self, input_func=input, output_func=print):
        self.input = input_func
        self.output = output_func
        self.mansion = Mansion()
        self.characters = []
        for suspect_card in get_suspects():
            from cluedo_game.player import Player
            player = Player(suspect_card)
            player.position = CHARACTER_STARTING_SPACES[suspect_card.name]
            player.eliminated = False
            self.characters.append(player)
        self.suggestion_history = SuggestionHistory()
        self.solution = Solution.random_solution()
        self.last_door_passed = {}          # track last room exited via door per player
        self.player = None

    def select_character(self):
        self.output("Select your character:")
        for idx, player in enumerate(self.characters):
            self.output(f"  {idx + 1}. {player.name} (starts in {player.position})")
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
        self._roll_for_play_order()
        self.deal_cards()
        self.show_hand()

        turn_index = 0
        while True:
            self.print_player_locations()
            current = self.characters[turn_index]
            # skip eliminated characters
            if current.eliminated:
                if current is self.player:
                    self.output(f"{current.name} has been eliminated. Game over.")
                    return
            else:
                self.player = current
                # free-form accusation at start of turn
                if self.prompt_accusation():
                    return
                # movement & suggestion
                if not self.move_phase():
                    return
                # default win if one active remains
                active = [p for p in self.characters if not p.eliminated]
                if len(active) == 1:
                    self.winner = active[0]
                    self.output(f"{self.winner.name} wins by default!")
                    return
            turn_index = (turn_index + 1) % len(self.characters)

    def print_player_locations(self):
        self.output("\n--- Player Locations ---")
        for player in self.characters:
            if player.eliminated:
                status = "(eliminated)"
            else:
                status = ""
            pos = getattr(player, 'position', None)
            if hasattr(pos, 'name'):
                pos_str = pos.name
            else:
                pos_str = str(pos)
            self.output(f"{player.name}: {pos_str} {status}")
        self.output("------------------------\n")

    def _roll_for_play_order(self):
        rolls = {}
        self.output("\nRolling dice to determine play order...")
        original_order = list(self.characters)
        contenders = list(self.characters)
        while True:
            rolls.clear()
            for char in contenders:
                roll = random.randint(1,6) + random.randint(1,6)
                rolls.setdefault(roll, []).append(char)
                self.output(f"{char.name} rolls a {roll}")
            max_roll = max(rolls.keys())
            if len(rolls[max_roll]) == 1:
                break
            tie = rolls[max_roll]
            names = ', '.join(c.name for c in tie)
            self.output(f"Tie for highest roll ({max_roll}) between: {names}. Re-rolling...")
            contenders = tie
        winner = rolls[max_roll][0]
        # Rotate the full original_order so winner is first, others follow in original order
        idx = original_order.index(winner)
        self.characters = original_order[idx:] + original_order[:idx]
        order_names = ', '.join(c.name for c in self.characters)
        self.output(f"\nPlay order: {order_names}")

    def deal_cards(self):
        # build deck excluding the three solution cards
        sol = self.solution
        all_chars = get_suspects()
        all_weaps = get_weapons()
        all_rooms = [RoomCard(room.name) for room in self.mansion.get_rooms()]
        deck = [c for c in all_chars if c != sol.character]
        deck += [w for w in all_weaps if w != sol.weapon]
        deck += [r for r in all_rooms if r != sol.room]
        random.shuffle(deck)
        # deal round-robin
        for idx, card in enumerate(deck):
            player = self.characters[idx % len(self.characters)]
            player.add_card(card)

    def show_hand(self):
        hand = getattr(self.player, 'hand', [])
        if hand:
            self.output("\nYour cards:")
            for card in hand:
                name = getattr(card, 'name', str(card))
                self.output(f"  - {name}")
        else:
            self.output("\nYou have no cards.")

    def move_phase(self):
        # roll for movement
        dice = random.randint(1,6) + random.randint(1,6)
        self.output(f"You rolled a {dice} for movement.")
        # preview reachable spaces
        def reachable_spaces(start, steps):
            from collections import deque
            rooms = set(self.mansion.get_rooms())
            visited = set()
            queue = deque([(start,0)])
            reachable = set()
            while queue:
                pos, dist = queue.popleft()
                if (pos,dist) in visited or dist>steps:
                    continue
                visited.add((pos,dist))
                if dist>0:
                    reachable.add(pos)
                if pos in rooms:
                    continue
                for adj in self.mansion.get_adjacent_spaces(pos):
                    queue.append((adj,dist+1))
            return sorted(reachable, key=lambda s: getattr(s,'name',str(s)))

        preview = reachable_spaces(self.player.position, dice)
        if preview:
            self.output("\nWith your roll, you could reach:")
            for space in preview:
                self.output(f"  - {space}")
            self.output("(Entering a room ends your movement.)")
        else:
            self.output("No spaces reachable!")

        moves = dice
        entered_room = False
        while moves>0:
            current = self.player.position
            adjacent = self.mansion.get_adjacent_spaces(current)
            self.output(f"\nCurrent position: {current}")
            self.output(f"Moves left: {moves}")
            self.output("Adjacent spaces:")
            for idx, sp in enumerate(adjacent):
                self.output(f"  {idx+1}. {sp}")
            self.output("  0. Quit")
            inp = self.input("Move to which space? ").strip().lower()
            if inp=='hand':
                self.show_hand()
                continue
            try:
                choice = int(inp)
                if choice==0:
                    self.output("Thanks for playing!")
                    return False
                if 1<=choice<=len(adjacent):
                    nxt = adjacent[choice-1]
                    # record door crossing
                    if (current in self.mansion.get_rooms() and str(nxt).startswith('C')) or \
                       (str(current).startswith('C') and nxt in self.mansion.get_rooms()):
                        self.last_door_passed[self.player] = current
                    self.player.position = nxt
                    self.output(f"Moved to {nxt}.")
                    moves -= 1
                    if nxt in self.mansion.get_rooms():
                        self.output(f"You have entered the {nxt}. Movement ends.")
                        entered_room = True
                        break
                else:
                    self.output("Invalid selection.")
            except ValueError:
                self.output("Please enter a valid number or 'hand'.")

        # allow accusation after movement
        if self.prompt_accusation():
            return False
        # suggestion if entered a room
        if entered_room:
            return self.make_suggestion()
        return True

    def make_suggestion(self):
        current_room = self.player.position
        if current_room not in self.mansion.get_rooms():
            self.output("You must be in a room to make a suggestion.")
            return True
        self.output(f"\nYou may make a suggestion. You are in the {current_room}.")
        suspect = self.select_from_list("suspect", self.characters)
        weapons = get_weapons()
        weapon  = self.select_from_list("weapon", weapons)
        room    = current_room
        self.output(f"\nYou suggest: {suspect.name}, in the {room.name}, with the {weapon.name}.")
        # move tokens
        for c in self.characters:
            if c.name==suspect.name:
                c.position = room
        for w in weapons:
            if w.name==weapon.name:
                w.position = room
        refuter, shown = self.handle_refutation(suspect, weapon, room)
        self.suggestion_history.add(self.player.name, suspect.name, weapon.name, room, refuter, shown)
        if (suspect.name==self.solution.character.name and
            weapon.name==self.solution.weapon.name and
            room.name==self.solution.room.name):
            self.output("\nCongratulations! You Win!")
            self.output(f"The solution was: {suspect.name} with the {weapon.name} in the {room.name}.")
            return False
        return True

    def handle_refutation(self, suspect, weapon, room):
        for other in self.characters:
            if other is self.player:
                continue
            matches = []
            for card in other.hand:
                if card == suspect or card == weapon or card == room:
                    matches.append(card)
            if matches:
                shown = random.choice(matches)
                name = getattr(shown,'name',str(shown))
                self.output(f"{other.name} can disprove your suggestion and shows you the card: {name}")
                return other.name, name
        self.output("No one can disprove your suggestion!")
        return None, None

    def make_accusation(self, suspect, weapon, room):
        if (suspect.name==self.solution.character.name and
            weapon.name==self.solution.weapon.name and
            room.name==self.solution.room.name):
            self.output("\nCongratulations! You Win!")
            self.output(f"The solution was: {suspect.name} with the {weapon.name} in the {room.name}.")
            self.winner = self.player
            return True
        self.output("\nIncorrect accusation—sorry, that’s not the solution.")
        self.player.eliminated = True
        # blocking door rule
        last = self.last_door_passed.get(self.player)
        if last:
            self.player.position = last
            self.output("Blocking door rule: you move back into that room.")
        return False

    def prompt_accusation(self):
        self.output("\nDo you want to make an accusation? (y/n)")
        resp = self.input().strip().lower()
        if resp!='y':
            return False
        suspect = self.select_from_list("suspect", self.characters)
        weapon  = self.select_from_list("weapon", get_weapons())
        room    = self.select_from_list("room", self.mansion.get_rooms())
        return self.make_accusation(suspect, weapon, room)

    def select_from_list(self, prompt, options):
        self.output(f"Select {prompt}:")
        for idx,item in enumerate(options):
            name = getattr(item,'name',str(item))
            self.output(f"  {idx+1}. {name}")
        while True:
            inp = self.input(f"Enter number for {prompt}: ").strip()
            try:
                i = int(inp)
                if 1<=i<=len(options):
                    return options[i-1]
            except ValueError:
                pass
            self.output("Invalid selection.")

    def check_win(self):
        return False

    def print_history(self):
        self.output("\n--- Suggestion/Refute History ---")
        self.output(str(self.suggestion_history) if str(self.suggestion_history) else "No suggestions made yet.")


def main():
    """Command-line entry point for Cluedo game."""
    game = CluedoGame()
    game.play()

if __name__ == "__main__":
    main()