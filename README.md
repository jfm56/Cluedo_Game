# Cluedo_Game

A Python implementation of the classic Cluedo game, featuring player movement, suggestions, and automated tests.

## Features
- Player movement between rooms
- Make suggestions (character, weapon, room)
- Automated testing with pytest and coverage
- Linting with pylint
- Ready for GitHub Actions CI

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/jfm56/Cluedo_Game.git
```

### 2. Navigate to the Project Directory
```bash
cd Cluedo_Game
```

### 3. (Optional) Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Game
```bash
python play_cluedo.py
```

## How to Play

1. **Character Selection**: At the start, you select your character from the list of classic Cluedo suspects. Each character starts in a specific room.

2. **Moving Between Rooms**: On each turn, your current room and its adjacent rooms are displayed. Enter the number corresponding to the room you want to move to, or 0 to quit.

3. **Making Suggestions**:
   - After entering a room, you can choose to make a suggestion.
   - If you do, you'll select a character, a weapon, **and any room** from the lists shown (not limited to your current location).
   - The game will display your suggestion.
4. **Winning the Game**:
   - If your suggestion matches the randomly selected solution (character, weapon, and room), you win! The solution is revealed.
   - If your suggestion is incorrect, you'll be told how many guesses remain and can continue playing.
   - You have a maximum of 6 guesses per game. If you run out, the solution is revealed and the game ends.

5. **Quitting**: You can quit at any time by entering 0 when prompted for a room.

**Tips:**
- Use deduction to narrow down the possibilities!
- The solution is different every game.

## Running Tests
To run all tests and check coverage:
```bash
pytest --cov=cluedo_game --cov-report=term-missing
```

---

Enjoy playing Cluedo! If you have suggestions or want to contribute, feel free to open an issue or pull request.
