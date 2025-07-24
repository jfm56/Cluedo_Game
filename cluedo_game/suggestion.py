class Suggestion:
    def __init__(self, suggesting_player, character, weapon, room, refuting_player=None, shown_card=None):
        self.suggesting_player = suggesting_player
        self.character = character
        self.weapon = weapon
        self.room = room
        self.refuting_player = refuting_player
        self.shown_card = shown_card

    def __repr__(self):
        base = f"{self.suggesting_player} suggested {self.character} with {self.weapon} in {self.room}"
        if self.refuting_player:
            # If AI made the suggestion, do not show the card
            try:
                is_ai = self.suggesting_player.endswith(" (AI)")
            except AttributeError:
                is_ai = str(self.suggesting_player).endswith(" (AI)")
            if is_ai:
                return f"{base}; refuted by {self.refuting_player}"
            else:
                try:
                    shown = self.shown_card
                except AttributeError:
                    shown = str(self.shown_card)
                return f"{base}; refuted by {self.refuting_player} (card: {shown})"
        return f"{base}; no one refuted"
