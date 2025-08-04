"""
Script to start a new Cluedo game with AI players.
"""
from cluedo_game.game import CluedoGame

def main():
    # Create a new game with AI players enabled
    game = CluedoGame(with_ai=True)
    
    # Start the game
    game.play()

if __name__ == "__main__":
    main()
