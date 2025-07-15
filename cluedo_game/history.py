class SuggestionHistory:
    def __init__(self):
        self.records = []

    def add(self, suggesting_player, suggested_character, suggested_weapon, suggested_room, refuting_player, shown_card):
        self.records.append({
            "suggesting_player": suggesting_player,
            "suggested_character": suggested_character,
            "suggested_weapon": suggested_weapon,
            "suggested_room": suggested_room,
            "refuting_player": refuting_player,
            "shown_card": shown_card
        })

    def get_all(self):
        return self.records

    def __str__(self):
        output = []
        for entry in self.records:
            s = f"{entry['suggesting_player']} suggested {entry['suggested_character']} with the {entry['suggested_weapon']} in the {entry['suggested_room']}"
            if entry['refuting_player']:
                s += f"; refuted by {entry['refuting_player']} (card: {entry['shown_card']})"
            else:
                s += "; no one refuted"
            output.append(s)
        return "\n".join(output)
