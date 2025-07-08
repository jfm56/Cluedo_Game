# Cluedo Game

A command-line Cluedo (Clue) game implemented in Python, designed for **full Docker usage**. No need to install Python or dependencies locally—everything runs in an isolated container.

## Features
- Player movement between rooms
- Make suggestions (character, weapon, room)
- Automated testing with pytest and coverage
- Linting with pylint
- Ready for GitHub Actions CI

## Quick Start (Docker Only)

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
4. **Run Tests**
   ```bash
   docker run --rm cluedo_game test
   ```
5. **Lint the Code**
   ```bash
   docker run --rm cluedo_game lint
   ```

> **Note:** You do NOT need to install Python or pip on your computer. All development, testing, and gameplay are done inside Docker. Local virtual environments are not needed.

## Running with Docker

You can use Docker to run the game, tests, lint, or code-server for development. First, build the image:

```bash
docker build -t cluedo_game .
```

- **Play the Game:**
  ```bash
  docker run --rm -it cluedo_game game
  ```
- **Run Tests:**
  ```bash
  docker run --rm cluedo_game test
  ```
- **Run Lint:**
  ```bash
  docker run --rm cluedo_game lint
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
