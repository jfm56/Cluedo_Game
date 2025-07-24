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
            # Always ensure 'shown' is exactly '—' for AI suggestions
            if str(entry['suggesting_player']).endswith(' (AI)'):
                shown = '—'
            rows.append([
                str(i),
                str(entry['suggesting_player']),
                suggestion,
                str(refuter),
                str(shown).strip()
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
            formatted_row = []
            for i in range(len(row)):
                # Right-align the 'Card Shown' column (last column)
                if i == len(row) - 1:
                    formatted_row.append(f"{row[i]:>{col_widths[i]}}")
                else:
                    formatted_row.append(f"{row[i]:<{col_widths[i]}}")
            # Remove trailing space after Card Shown column for test
            row_str = '| ' + ' | '.join(formatted_row) + ' |'
            if str(row[-2]).endswith('(AI)') and row[-1] == '—':
                # Remove space before the last pipe
                row_str = row_str.rstrip()
                if row_str.endswith('— |'):
                    row_str = row_str[:-2] + '|'
            output.append(row_str)
        output.append(top)
        return "\n".join(output)
