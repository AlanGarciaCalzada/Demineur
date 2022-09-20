"""
Fichier contenant tout les fonctions du projet.
"""

import pygame

def get_colors(width_cell, height_cell):
    """
    Renvoie un dictionnaire des sprites des cases.
    """

    colors = dict()

    colors["0"] = pygame.transform.scale(
                    pygame.image.load("./img/Empty.png"), (width_cell, height_cell)
                  )
    colors["1"] = pygame.transform.scale(
                    pygame.image.load("./img/1.png"), (width_cell, height_cell)
                  )
    colors["2"] = pygame.transform.scale(
                    pygame.image.load("./img/2.png"), (width_cell, height_cell)
                  )
    colors["3"] = pygame.transform.scale(
                    pygame.image.load("./img/3.png"), (width_cell, height_cell)
                  )
    colors["4"] = pygame.transform.scale(
                    pygame.image.load("./img/4.png"), (width_cell, height_cell)
                  )
    colors["5"] = pygame.transform.scale(
                    pygame.image.load("./img/5.png"), (width_cell, height_cell)
                  )
    colors["6"] = pygame.transform.scale(
                    pygame.image.load("./img/6.png"), (width_cell, height_cell)
                  )
    colors["7"] = pygame.transform.scale(
                    pygame.image.load("./img/7.png"), (width_cell, height_cell)
                  )
    colors["8"] = pygame.transform.scale(
                    pygame.image.load("./img/8.png"), (width_cell, height_cell)
                  )
    colors["B"] = pygame.transform.scale(
                    pygame.image.load("./img/Bomb.png"), (width_cell, height_cell)
                  )
    colors["F"] = pygame.transform.scale(
                    pygame.image.load("./img/Flagged.png"), (width_cell, height_cell)
                  )
    colors["I"] = pygame.transform.scale(
                    pygame.image.load("./img/Inactivated.png"), (width_cell, height_cell)
                  )

    return colors
