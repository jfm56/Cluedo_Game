from cluedo_game.game import CluedoGame

def main():
    try:
        game = CluedoGame()
        game.play()
    except (EOFError, KeyboardInterrupt):
        print("\nGame exited. Goodbye!")
        exit(0)

if __name__ == "__main__":
    main()
