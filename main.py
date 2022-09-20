"""
Pour lancer le jeu
"""

# Import
from game import Game
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Une partie de démineur')
    parser.add_argument('-d', "--difficulty", default='n', choices=['e','n','d'], help="Set the difficulty of a game.")
    args = parser.parse_args()

    difficulty_levels = dict()
    difficulty_levels["e"] = "Facile"
    difficulty_levels["n"] = "Normal"
    difficulty_levels["d"] = "Difficile"

    print("Mode de jeu :", difficulty_levels[args.difficulty])
    width_plateau = int(input("Largeur: "))
    height_plateau = int(input("Hauteur : "))
    bombs_no = int(input("Nombre de bombes : "))

    game = Game(width_plateau, height_plateau, bombs_no, args.difficulty)
    game.start()
