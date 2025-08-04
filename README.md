# Cluedo Game

## Introduction

**Cluedo** (known as "Clue" in North America) is a classic murder mystery board game where players take on the roles of suspects in a mansion. The objective is to deduce who committed the crime, with what weapon, and in which room. Players move from room to room, making suggestions and using logic and deduction to eliminate possibilities. The first player to correctly solve the mystery wins the game!

This project is a command-line implementation of Cluedo in Python. You can play it using Docker or directly with Python.

---

## Features
- Player movement between rooms
- Make suggestions (character, weapon, room)
- Simple deduction gameplay
- Tracks all suggestions and refutations in-game
- View suggestion/refute history at any prompt with `history`
- Make decisions based on gathered information
- **Play against AI opponents**: Computer players take their own turns, move, make suggestions, and can win the game!
- **Privacy/Fairness**: In the Suggestion/Refute History, the 'Card Shown' is only visible for suggestions made by the human player. For AI suggestions, the card is always hidden for fairness.

---

## How to Play

1. **Character Selection:** At the start, select your character from the list of classic Cluedo suspects. Each character starts in a specific room.
2. **Moving Between Rooms:** On each turn, your current room and its adjacent rooms are displayed. Enter the number corresponding to the room you want to move to, or 0 to quit.
3. **Making Suggestions:** After entering a room, you can choose to make a suggestion (character, weapon, and room). The game will display your suggestion.
4. **AI Opponents:** After your turn, each computer-controlled opponent (AI) will take their own turn: they move, make suggestions, and can win the game by solving the mystery before you!
5. **Winning the Game:** If your suggestion matches the randomly selected solution (character, weapon, and room), you win! Otherwise, you’ll be told how many guesses remain. You have a maximum of 6 guesses per game.
6. **Quitting:** You can quit at any time by entering 0 when prompted for a room.

**Tips:**
- Use deduction to narrow down the possibilities!
- Type `history` at any prompt to view all suggestions and refutes made so far.
- The solution is different every game.
- The AI players are currently random but can be made smarter!
- **Note:** For fairness, the 'Card Shown' column in the suggestion/refute history is only filled in for suggestions made by you (the human player). For AI suggestions, the card is always hidden.

---

## Installation & Running

### Using Docker (Recommended)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/jfm56/Cluedo_Game.git
   cd Cluedo_Game
   ```
2. **Build the Docker Image**
   ```bash
   docker build -t cluedo_game .
   ```

3. **Play the Game with AI Opponents (human vs. computers who take turns):**
   ```bash
   docker run --rm -it cluedo_game game
   ```

4. **Run Tests:**
   ```bash
   docker run --rm -it cluedo_game test
   ```

5. **Run Linting:**
   ```bash
   docker run --rm -it cluedo_game lint
   ```

> **Note:** You do NOT need to install Python or pip on your computer. All gameplay is done inside Docker.

---

## Running Without Docker

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Play the game with AI opponents:**
   ```bash
   python play_with_ai.py
   ```
   or
   ```bash
   python -m cluedo_game.game
   ```

3. **Run tests:**
   ```bash
   pytest
   ```

4. **Run linting:**
   ```bash
   pylint cluedo_game
   ```

### Test Coverage

- The test suite covers AI player logic, game flow, suggestion/refute history, and table formatting.
- All tests are passing as of July 2025, including robust checks for AI output and suggestion history formatting.
- To add new tests, see files in `tests/` for examples using `unittest` and `pytest`.

> 
> **Troubleshooting:** If you see no output after running the 'ai' command, make sure your terminal is interactive and your Docker image is up to date. Try rebuilding with `docker build -t cluedo_game .` if needed.
> 
> **Important:** The command `python -m cluedo_game.game_with_ai` only works outside Docker. Inside Docker, always use `ai` as shown above.

### Without Docker

1. **Ensure you have Python 3.8+ installed.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the classic game:**
   ```bash
   python play_cluedo.py
   ```
4. **Run the AI opponents game:**
   ```bash
   python -m cluedo_game.game_with_ai
   ```

---

## AI Player Feature

- The new AI player system means all computer-controlled opponents now move, make suggestions, and can win the game.
- To play against these AI opponents, use the `game_with_ai` module as described above.
- The AI logic is currently random, but the system is extensible for smarter strategies.

---

## Game Design and Algorithms

### 1. Board Representation and Movement
- **Graph-based Board**: The game board is represented as a graph where each node is a room or corridor space, and edges represent valid moves between them. This allows for efficient pathfinding and movement validation.
- **Chess-like Coordinate System**: Implements an A1-J10 coordinate system for intuitive position tracking and movement calculations.
- **Pathfinding**: Uses breadth-first search (BFS) to calculate valid moves and shortest paths between locations, ensuring players can only move to adjacent spaces.

### 2. Card Dealing and Solution Generation
- **Fair Distribution**: Cards are dealt using a Fisher-Yates shuffle algorithm to ensure random but fair distribution among players.
- **Solution Generation**: The solution (character, weapon, room) is selected at random at the start of each game, with the selected cards removed from the deck before dealing to players.
- **No Duplicate Cards**: The dealing mechanism ensures no player receives a card that's part of the solution, maintaining game integrity.

### 3. AI Opponents
- **Random Move Selection**: AI players use weighted random selection for movement, with preferences for moving toward rooms when making suggestions.
- **Suggestion Strategy**: AI players track known information and make suggestions based on their current room and remaining possibilities.
- **Deduction**: AI players maintain a knowledge base of seen cards and use process of elimination to make educated guesses.

### 4. Game State Management
- **Turn Management**: Implements a circular queue for turn order, supporting both human and AI players seamlessly.
- **Suggestion Resolution**: Efficiently resolves suggestions by checking all players' hands in turn order until a refutation is found.
- **Win Condition Checking**: Validates accusations against the solution with O(1) complexity for quick resolution.

### 5. Data Structures
- **Sets for Efficient Lookups**: Uses Python sets for O(1) membership testing of cards in player hands and solution sets.
- **Dictionaries for State Tracking**: Maintains game state using dictionaries for quick access to player positions, cards, and game history.
- **Immutable Data**: Uses tuples and frozen sets where appropriate to ensure data consistency and prevent accidental modifications.

### 6. Input Validation
- **Type Checking**: Validates all user inputs to ensure they match expected types and formats.
- **Range Validation**: Ensures all numerical inputs are within valid ranges for the current game state.
- **Command Parsing**: Implements a flexible command parser that supports both menu-based and natural language inputs.

### 7. Performance Considerations
- **Lazy Evaluation**: Defers expensive calculations until necessary, such as pathfinding only when a player moves.
- **Memoization**: Caches results of expensive operations like path calculations to improve performance.
- **Efficient Updates**: Uses incremental updates to the game state rather than recalculating from scratch when possible.

## Contributing

Enjoy playing Cluedo! If you have suggestions or want to contribute, feel free to open an issue or pull request.
