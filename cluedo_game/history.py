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
        if not self.records:
            return "No suggestions yet."
        header = f"{'Turn':<5} {'Suggester':<12} {'Suggestion':<40} {'Refuter':<12} {'Card Shown':<15}"
        sep = '-' * len(header)
        output = [header, sep]
        for i, entry in enumerate(self.records, 1):
            suggestion = f"{entry['suggested_character']} / {entry['suggested_weapon']} / {entry['suggested_room']}"
            refuter = entry['refuting_player'] if entry['refuting_player'] else 'None'
            # Only show the card if the suggester is the human (does not end with ' (AI)')
            if entry['refuting_player'] and not str(entry['suggesting_player']).endswith(' (AI)'):
                shown = entry['shown_card'] if entry['shown_card'] else '—'
            else:
                shown = '—'
            row = f"{i:<5} {entry['suggesting_player']:<12} {suggestion:<40} {refuter:<12} {shown:<15}"
            output.append(row)
        return "\n".join(output)
