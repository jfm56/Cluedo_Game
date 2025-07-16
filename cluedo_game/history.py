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
        # Prepare all data rows first
        rows = []
        for i, entry in enumerate(self.records, 1):
            suggestion = f"{entry['suggested_character']} / {entry['suggested_weapon']} / {entry['suggested_room']}"
            refuter = entry['refuting_player'] if entry['refuting_player'] else 'None'
            # Only show the card if the suggester is the human (does not end with ' (AI)')
            if entry['refuting_player'] and not str(entry['suggesting_player']).endswith(' (AI)'):
                shown = entry['shown_card'] if entry['shown_card'] else '—'
            else:
                shown = '—'
            rows.append([
                str(i),
                str(entry['suggesting_player']),
                suggestion,
                str(refuter),
                str(shown)
            ])
        # Determine max width for each column
        headers = ["Turn", "Suggester", "Suggestion", "Refuter", "Card Shown"]
        cols = list(zip(*([headers] + rows)))
        col_widths = [max(len(str(item)) for item in col) for col in cols]
        # Build border
        def border(char_left, char_mid, char_right, char_fill):
            return char_left + char_mid.join(char_fill * w for w in col_widths) + char_right
        top = border('+', '+', '+', '-')
        sep = border('+', '+', '+', '=')
        # Build header row
        header_row = '| ' + ' | '.join(f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers))) + ' |'
        output = [top, header_row, sep]
        # Build data rows
        for row in rows:
            output.append('| ' + ' | '.join(f"{row[i]:<{col_widths[i]}}" for i in range(len(row))) + ' |')
        output.append(top)
        return "\n".join(output)
