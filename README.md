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
   docker build -t project2_sourcecode .
   ```
3. **Play the Classic Game (human vs. only refuting computers):**
   ```bash
   docker run --rm -it project2_sourcecode game
   ```
4. **Play the AI Opponents Game (human vs. computers who take turns):**
   ```bash
   docker run --rm -it project2_sourcecode ai
   ```

> **Note:** You do NOT need to install Python or pip on your computer. All gameplay is done inside Docker.
> 
> **Troubleshooting:** If you see no output after running the 'ai' command, make sure your terminal is interactive and your Docker image is up to date. Try rebuilding with `docker build -t project2_sourcecode .` if needed.
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

## Contributing

Enjoy playing Cluedo! If you have suggestions or want to contribute, feel free to open an issue or pull request.
