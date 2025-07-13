# Cluedo Game

## Introduction

**Cluedo** (known as "Clue" in North America) is a classic murder mystery board game where players take on the roles of suspects in a mansion. The objective is to deduce who committed the crime, with what weapon, and in which room. Players move from room to room, making suggestions and using logic and deduction to eliminate possibilities. The first player to correctly solve the mystery wins the game!

This project is a command-line implementation of Cluedo in Python. You can play it using Docker or directly with Python.

---

## Features
- Player movement between rooms
- Make suggestions (character, weapon, room)
- Simple deduction gameplay

---

## How to Play

1. **Character Selection:** At the start, select your character from the list of classic Cluedo suspects. Each character starts in a specific room.
2. **Moving Between Rooms:** On each turn, your current room and its adjacent rooms are displayed. Enter the number corresponding to the room you want to move to, or 0 to quit.
3. **Making Suggestions:** After entering a room, you can choose to make a suggestion (character, weapon, and room). The game will display your suggestion.
4. **Winning the Game:** If your suggestion matches the randomly selected solution (character, weapon, and room), you win! Otherwise, you’ll be told how many guesses remain. You have a maximum of 6 guesses per game.
5. **Quitting:** You can quit at any time by entering 0 when prompted for a room.

**Tips:**
- Use deduction to narrow down the possibilities!
- The solution is different every game.

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
3. **Play the Game**
   ```bash
   docker run --rm -it cluedo_game game
   ```

> **Note:** You do NOT need to install Python or pip on your computer. All gameplay is done inside Docker.

### Without Docker

1. **Ensure you have Python 3.8+ installed.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the game:**
   ```bash
   python play_cluedo.py
   ```

---

## Contributing

Enjoy playing Cluedo! If you have suggestions or want to contribute, feel free to open an issue or pull request.
