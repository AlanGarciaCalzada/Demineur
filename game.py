"""
Fichier contenant la classe "Game".
"""

# Import
# from case import Case
import json
import random
import time
import pygame
from pygame.locals import *
from plateau import Plateau
import basic_functions

class Game:
    """
    Classe gérant une partie de démineur.
    """

    def __init__(self, width_plateau, height_plateau, bombs_no, difficulty):

        self.difficulty = difficulty

        self.game_settings = dict()

        self.game_settings["width_plateau"] = width_plateau
        self.game_settings["height_plateau"] = height_plateau
        self.game_settings["bombs_no"] = bombs_no
        self.game_settings["done"] = False
        self.game_settings["began"] = False

        with open("config.json","r") as file:
            config_str = file.read()

        self.game_settings["config"] =  json.loads(config_str)

        self.game_settings["pygame"] = dict()
        self.game_settings["sprites"] = dict()

        pygame.init()
        pygame.font.init()

        self.game_settings["pygame"]["pygame_font"] = pygame.font.SysFont(
            self.game_settings["config"]["FONT"]["NAME"],
            self.game_settings["config"]["FONT"]["SIZE"]
        )

        self.game_settings["sprites"]["cases_sprites"] = basic_functions.get_colors(
                                                self.game_settings["config"]["WIDTH_CELL"],
                                                self.game_settings["config"]["HEIGHT_CELL"]
                                              )

        pygame.display.set_icon(self.game_settings["sprites"]["cases_sprites"]["B"])

        self.game_settings["window"] = dict()

        self.game_settings["window"]["corners"] = {
            "corner_size" : (
                                (self.game_settings["config"]["WIDTH_CELL"]*6)//16,
                                (self.game_settings["config"]["HEIGHT_CELL"]*6)//16
                            ),
            "edge_v" :  (
                            (self.game_settings["config"]["WIDTH_CELL"],
                            (self.game_settings["config"]["HEIGHT_CELL"]*6)//16)
                        ),
            "edge_h" : (
                        (self.game_settings["config"]["WIDTH_CELL"]*6)//16,
                        self.game_settings["config"]["HEIGHT_CELL"]
                       )
        }

        self.game_settings["window"]["size"] = [
            self.game_settings["width_plateau"]
            * (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"])
            + self.game_settings["window"]["corners"]["corner_size"][0] * 2,
            self.game_settings["height_plateau"]
            * (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"])
            + self.game_settings["window"]["corners"]["corner_size"][1] * 2
        ]

        self.game_settings["sprites"]["corners"] = {
            "up_left" : pygame.transform.scale(
                    pygame.image.load("./img/Haut_Gauche.png"),
                    self.game_settings["window"]["corners"]["corner_size"]
                ),
            "up_right" : pygame.transform.scale(
                    pygame.image.load("./img/Haut_Droite.png"),
                    self.game_settings["window"]["corners"]["corner_size"]
                ),
            "down_right" : pygame.transform.scale(
                    pygame.image.load("./img/Bas_Droite.png"),
                    self.game_settings["window"]["corners"]["corner_size"]
                ),
            "down_left" : pygame.transform.scale(
                    pygame.image.load("./img/Bas_Gauche.png"),
                    self.game_settings["window"]["corners"]["corner_size"]
                )
        }

        self.game_settings["sprites"]["edges"] = {
            "vertical" : pygame.transform.scale(
                    pygame.image.load("./img/Haut.png"),
                    self.game_settings["window"]["corners"]["edge_v"]
                ),
            "horizontal" : pygame.transform.scale(
                    pygame.image.load("./img/Gauche.png"),
                    self.game_settings["window"]["corners"]["edge_h"]
                )
        }

        self.game_settings["pygame"]["clock"] = pygame.time.Clock()

        self.plateau = None

    def is_plateau_set(self):
        """
        Renvoie True si le self.plateau a été créé, False si non.
        """
        return self.game_settings["began"]

    def start(self):
        """
        Permet de lancer la partie.
        """

        black = (0, 0, 0)
        # GREY = (128,128,128)
        # WHITE = (255, 255, 255)
        # RED = (255, 0, 0)
        # GREEN = (0, 255, 0)
        # BLUE = (0, 0, 255)

        screen = pygame.display.set_mode(self.game_settings["window"]["size"])
        display = pygame.Surface(self.game_settings["window"]["size"])

        pygame.display.set_caption("Minesweeper - In Game")

        self.game_settings["began"] = False

        render_offset = [0, 0]

        while not self.game_settings["began"] and not self.game_settings["done"]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_settings["done"] = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pos[0] < self.game_settings["window"]["corners"]["corner_size"][0] or pos[1] < self.game_settings["window"]["corners"]["corner_size"][1] or pos[0] > self.game_settings["window"]["size"][0] - self.game_settings["window"]["corners"]["corner_size"][0] or pos[1] > self.game_settings["window"]["size"][1] - self.game_settings["window"]["corners"]["corner_size"][1]:
                        continue
                    row = (pos[0] - self.game_settings["window"]["corners"]["corner_size"][0]) // (self.game_settings["config"]["WIDTH_CELL"] + self.game_settings["config"]["MARGIN"])
                    column = (pos[1] - self.game_settings["window"]["corners"]["corner_size"][1]) // (self.game_settings["config"]["HEIGHT_CELL"] + self.game_settings["config"]["MARGIN"])
                    self.game_settings["began"] = True
                    self.plateau = Plateau(self.game_settings["width_plateau"], self.game_settings["height_plateau"], self.game_settings["bombs_no"], (row, column), self.difficulty)
                    self.plateau.activate(row, column, True)
                    print(self.plateau.print_plateau_debug())
                    print("Click ", pos, "Grid coordinates: ", row, column)
            
            display.blit(self.game_settings["sprites"]["corners"]["up_left"], (0, 0))
            for j in range(self.game_settings["width_plateau"]):
                display.blit(self.game_settings["sprites"]["edges"]["vertical"], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * j + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], 0))
            display.blit(self.game_settings["sprites"]["corners"]["up_right"], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * self.game_settings["width_plateau"] + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], 0))
            for i in range(self.game_settings["height_plateau"]):
                display.blit(self.game_settings["sprites"]["edges"]["horizontal"], (0, (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * i + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))
                for j in range(self.game_settings["width_plateau"]):
                    display.blit(self.game_settings["sprites"]["cases_sprites"]["I"], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * j + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * i + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))
                display.blit(self.game_settings["sprites"]["edges"]["horizontal"], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * self.game_settings["width_plateau"] + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * i + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))
            display.blit(self.game_settings["sprites"]["corners"]["down_left"], (0, (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * self.game_settings["height_plateau"] + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))
            for j in range(self.game_settings["width_plateau"]):
                display.blit(self.game_settings["sprites"]["edges"]["vertical"], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * j + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * self.game_settings["height_plateau"] + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))
            display.blit(self.game_settings["sprites"]["corners"]["down_right"], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * self.game_settings["width_plateau"] + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * self.game_settings["height_plateau"] + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))

            pygame.display.update()
            screen.blit(pygame.transform.scale(display, self.game_settings["window"]["size"]),render_offset) 

            self.game_settings["pygame"]["clock"].tick(60)
        
        for i in range(len(self.plateau.matrice)):
            for j in range(len(self.plateau.matrice[i])):
                case = self.plateau.matrice[i][j]
                if case.is_activated:
                    display.blit(self.game_settings["sprites"]["cases_sprites"][str(case.bombs_around)], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * j + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * i + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))
                else:
                    display.blit(self.game_settings["sprites"]["cases_sprites"]["I"], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * j + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * i + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))

        pygame.display.update()
        screen.blit(pygame.transform.scale(display, self.game_settings["window"]["size"]),render_offset) 

        while not self.game_settings["done"]:
            if self.plateau.has_failed:
                screen_shake = 60
                text = self.game_settings["pygame"]["pygame_font"].render('Perdu !', False, black)
                text_rect = text.get_rect(center=(self.game_settings["window"]["size"][0]/2, self.game_settings["window"]["size"][1]/2))
                for i in range(len(self.plateau.matrice)):
                    for j in range(len(self.plateau.matrice[i])):
                        case = self.plateau.matrice[i][j]
                        if not case.has_bomb:
                            display.blit(self.game_settings["sprites"]["cases_sprites"][str(case.bombs_around)], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * j + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * i + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))
                        else:
                            screen_shake = 30
                            display.blit(self.game_settings["sprites"]["cases_sprites"]["B"], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * j + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * i + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))
                
                while screen_shake:
                    render_offset[0] = random.randint(0, 8) - 4
                    render_offset[1] = random.randint(0, 8) - 4
                    display.blit(text, text_rect)
                    pygame.display.update()
                    screen.blit(pygame.transform.scale(display, self.game_settings["window"]["size"]),render_offset)
                    screen_shake -= 1
                    self.game_settings["pygame"]["clock"].tick(60)
                
                time.sleep(3)
                print("Tu as perdu !")
                break
            if self.plateau.has_win():
                text = self.game_settings["pygame"]["pygame_font"].render('Gagné !', False, black)
                text_rect = text.get_rect(center=(self.game_settings["window"]["size"][0]/2, self.game_settings["window"]["size"][1]/2))
                for i in range(len(self.plateau.matrice)):
                    for j in range(len(self.plateau.matrice[i])):
                        case = self.plateau.matrice[i][j]
                        if not case.has_bomb:
                            display.blit(self.game_settings["sprites"]["cases_sprites"][str(case.bombs_around)], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * j + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * i + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))
                        else:
                            screen_shake = 30
                            display.blit(self.game_settings["sprites"]["cases_sprites"]["B"], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * j + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * i + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))
                
                display.blit(text, text_rect)
                pygame.display.update()
                screen.blit(pygame.transform.scale(display, self.game_settings["window"]["size"]),render_offset)
                self.game_settings["pygame"]["clock"].tick(60)
                time.sleep(3)
                print("Tu as gagné !")
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_settings["done"] = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if pos[0] < self.game_settings["window"]["corners"]["corner_size"][0] or pos[1] < self.game_settings["window"]["corners"]["corner_size"][1] or pos[0] > self.game_settings["window"]["size"][0] - self.game_settings["window"]["corners"]["corner_size"][0] or pos[1] > self.game_settings["window"]["size"][1] - self.game_settings["window"]["corners"]["corner_size"][1]:
                            continue
                        row = (pos[0] - self.game_settings["window"]["corners"]["corner_size"][0]) // (self.game_settings["config"]["WIDTH_CELL"] + self.game_settings["config"]["MARGIN"])
                        column = (pos[1] - self.game_settings["window"]["corners"]["corner_size"][1]) // (self.game_settings["config"]["HEIGHT_CELL"] + self.game_settings["config"]["MARGIN"])
                        self.plateau.activate(row, column)
                        print("Click ", pos, "Grid coordinates: ", row, column)
                    elif event.button == 3:
                        pos = pygame.mouse.get_pos()
                        if pos[0] < self.game_settings["window"]["corners"]["corner_size"][0] or pos[1] < self.game_settings["window"]["corners"]["corner_size"][1] or pos[0] > self.game_settings["window"]["size"][0] - self.game_settings["window"]["corners"]["corner_size"][0] or pos[1] > self.game_settings["window"]["size"][1] - self.game_settings["window"]["corners"]["corner_size"][1]:
                            continue
                        row = (pos[0] - self.game_settings["window"]["corners"]["corner_size"][0]) // (self.game_settings["config"]["WIDTH_CELL"] + self.game_settings["config"]["MARGIN"])
                        column = (pos[1] - self.game_settings["window"]["corners"]["corner_size"][1]) // (self.game_settings["config"]["HEIGHT_CELL"] + self.game_settings["config"]["MARGIN"])
                        self.plateau.switch_flag(row, column)
                        print("Click ", pos, "Grid coordinates: ", row, column)
        
            for i in range(len(self.plateau.matrice)):
                for j in range(len(self.plateau.matrice[i])):
                    case = self.plateau.matrice[i][j]
                    if case.is_activated and not case.has_bomb:
                        display.blit(self.game_settings["sprites"]["cases_sprites"][str(case.bombs_around)], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * j + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * i + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))
                    elif case.is_flagged:
                        display.blit(self.game_settings["sprites"]["cases_sprites"]["F"], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * j + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * i + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))
                    elif case.is_activated and case.has_bomb:
                        display.blit(self.game_settings["sprites"]["cases_sprites"]["B"], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * j + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * i + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))
                    else:
                        display.blit(self.game_settings["sprites"]["cases_sprites"]["I"], ((self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["WIDTH_CELL"]) * j + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][0], (self.game_settings["config"]["MARGIN"] + self.game_settings["config"]["HEIGHT_CELL"]) * i + self.game_settings["config"]["MARGIN"] + self.game_settings["window"]["corners"]["corner_size"][1]))

            pygame.display.update()
            screen.blit(pygame.transform.scale(display, self.game_settings["window"]["size"]),render_offset)

            self.game_settings["pygame"]["clock"].tick(60)
    
        pygame.quit()