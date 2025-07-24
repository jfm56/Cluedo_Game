from cluedo_game.player import Player
from cluedo_game.solution import Solution


def make_accusation(game, player, suspect, weapon, room):
    """
    Handle a player's accusation. If correct, returns True (win). If incorrect, marks player eliminated and returns False.
    Prints outcome via game's output_func.
    """
    # Compare by name for suspect/weapon, by object identity for room
    is_correct = (
        game.solution.character.name == suspect.name and
        game.solution.weapon.name == weapon.name and
        game.solution.room == room
    )
    if is_correct:
        game.output("\nCongratulations! You Win!")
        game.output(f"The solution was: {game.solution.character.name} with the {game.solution.weapon.name} in the {game.solution.room.name}.")
        return True
    else:
        player.eliminated = True
        game.output("Incorrect accusation. You are eliminated and may not move, suggest, or accuse for the rest of the game.")
        return False
