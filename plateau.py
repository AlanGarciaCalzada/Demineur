"""
Fichier contenant la classe "Plateau".
"""

# Import
from random import randint
from case import Case
import board


class Plateau:
    """
    Permet de faire un plateau de démineur.
    Ce plateau possède des dimensions passé en paramètre et un nombre de bombes.
    Ce plateau sait aussi si la partie est perdue.
    Il place lui même ses bombes de manière aléatoire.
    Il peut activer et mettre un drapeau sur une de ses cases.
    """

    def __init__(self, size_x, size_y, bombs_no, first_clic, difficulty):
        """
        Initilisation du plateau.
        """
        self.size_x = size_x
        self.size_y = size_y
        self.difficulty = difficulty

        # Nombre de bombes
        self.bombs_no = bombs_no

        # Permet de savoir si la partie est perdue.
        self.has_failed = False

        # Création d'une matrice ayant pour dimension size_x/size_y
        self.matrice = [[Case(False) for j in range(size_x)] for i in range(size_y)]

        # On place de manière aléatoire les bombes dans la matrice
        for _ in range(bombs_no):
            bomb_x = randint(0, size_x-1)
            bomb_y = randint(0, size_y-1)
            while self.matrice[bomb_y][bomb_x].has_bomb \
            or (((first_clic[1] + 1 >= bomb_y >= first_clic[1] - 1) \
            and (first_clic[0] + 1 >= bomb_x >= first_clic[0] - 1))):
                bomb_x = randint(0, size_x-1)
                bomb_y = randint(0, size_y-1)
            self.placebomb(bomb_x, bomb_y)

    def inject_board(self, user_view, bomb_view):

        flagged = set()

        for y in range(self.size_y):
            for x in range(self.size_x):

                if self.matrice[y][x].is_flagged:
                    flagged.add((x, y))

        self.matrice = [[Case(False) for j in range(self.size_x)] for i in range(self.size_y)]

        for y in range(self.size_y):
            for x in range(self.size_x):

                if bomb_view[y][x] == board.Tile.BOMB:
                    self.placebomb(x, y)
                
                if user_view[y][x] != board.Tile.INACTIVATED:
                    self.matrice[y][x].activate()
                
                if (x, y) in flagged:
                    self.matrice[y][x].switch_flag()

    def placebomb(self, coord_x, coord_y):
        """
        Permet de placer une bombe aux coordonnées renseignées dans la matrice,
        elle incrémente aussi la variable notant le nombres de bombes autour
        d'une case à la dite case.
        """

        if coord_y > self.size_y or coord_x > self.size_x or coord_x < 0 or coord_y < 0:
            return False

        if coord_x > 0 and coord_y > 0:
            self.matrice[coord_y-1][coord_x-1].add_bomb_around()
            self.matrice[coord_y][coord_x-1].add_bomb_around()
            self.matrice[coord_y-1][coord_x].add_bomb_around()
        elif coord_y > 0:
            self.matrice[coord_y-1][coord_x].add_bomb_around()
        elif coord_x > 0:
            self.matrice[coord_y][coord_x-1].add_bomb_around()

        if coord_x < self.size_x - 1 and coord_y < self.size_y - 1:
            self.matrice[coord_y+1][coord_x+1].add_bomb_around()
            self.matrice[coord_y][coord_x+1].add_bomb_around()
            self.matrice[coord_y+1][coord_x].add_bomb_around()
        elif coord_y < self.size_y - 1:
            self.matrice[coord_y+1][coord_x].add_bomb_around()
        elif coord_x < self.size_x - 1:
            self.matrice[coord_y][coord_x+1].add_bomb_around()

        if coord_x > 0 and coord_y < self.size_y - 1:
            self.matrice[coord_y+1][coord_x-1].add_bomb_around()

        if coord_x < self.size_x - 1 and coord_y > 0:
            self.matrice[coord_y-1][coord_x+1].add_bomb_around()

        self.matrice[coord_y][coord_x] = Case(True)
        return True

    def print_plateau_debug(self):
        """
        Permet d'afficher dans la console le plateau sans problèmes.
        """
        to_print = ""
        for line in self.matrice:
            to_print += ""
            for case in line:
                if case.has_bomb:
                    to_print += "B "
                    continue
                to_print += str(case.bombs_around) + " "
            to_print += "\n\n"
        
        to_user_view = "user_view = ["
        to_bomb_view = "bomb_view = ["

        for line in self.matrice:
            to_user_view += "\n    ["
            to_bomb_view += "\n    ["
            for case in line:
                if case.is_activated:
                    to_user_view += str(case.bombs_around) + ", "
                    to_bomb_view += "None, "
                else:
                    to_user_view += "None, "
                    to_bomb_view += "False, "
                
            to_user_view = to_user_view[:len(to_user_view)-2]
            to_bomb_view = to_bomb_view[:len(to_bomb_view)-2]

            to_user_view += "],"
            to_bomb_view += "],"

        to_user_view = to_user_view[:len(to_user_view)-1] + "\n]"
        to_bomb_view = to_bomb_view[:len(to_bomb_view)-1] + "\n]"

        print("\n" + to_user_view + "\n\n" + to_bomb_view, "\n")

        return to_print

    def activate(self, coord_x, coord_y, pass_check=False):
        """
        Active la case aux coordonnées x et y renseignées.
        """
        if coord_y > self.size_y or coord_x > self.size_x or coord_x < 0 or coord_y < 0:
            pass
        else:

            if not pass_check:
            
                if self.difficulty == "e":

                    test_board = board.create_board_from(self)
                    test_board.bomb_view[coord_y][coord_x] = board.Tile.FORBIDDEN

                    solve_result = board.solve(test_board, self.bombs_no)

                    if solve_result is None:

                        self.matrice[coord_y][coord_x].activate()
                        self.has_failed = True
                        return
                    
                    else:

                        board.pretty_grid(solve_result.user_view, solve_result.bomb_view)

                        self.inject_board(solve_result.user_view, solve_result.bomb_view)
                        self.activate_zero(coord_x, coord_y)


                elif self.matrice[coord_y][coord_x].has_bomb:

                    self.matrice[coord_y][coord_x].activate()
                    self.has_failed = True
                    return
                
                elif self.difficulty == "d":

                    test_board = board.create_board_from(self)
                    print("")
                    temp_res = test_board.place_bombe(coord_x, coord_y)
                    if not temp_res:
                        self.activate_zero(coord_x, coord_y)
                        return

                    solve_result = board.solve(test_board, self.bombs_no - 1)

                    if solve_result is None:

                        self.activate_zero(coord_x, coord_y)
                        return
                    
                    else:

                        board.pretty_grid(solve_result.user_view, solve_result.bomb_view)
                        self.inject_board(solve_result.user_view, solve_result.bomb_view)
                        self.matrice[coord_y][coord_x].activate()
                        self.has_failed = True

            self.activate_zero(coord_x, coord_y)

    def activate_zero(self, coord_x, coord_y):

        self.matrice[coord_y][coord_x].activate()

        if self.matrice[coord_y][coord_x].bombs_around == 0:

            for i in range(-1,2):
                for j in range(-1,2):

                    if not (0 <= coord_y+i < len(self.matrice) and 0 <= coord_x+j < len(self.matrice[coord_y+i])) or (i,j) == (0,0) or self.matrice[coord_y+i][coord_x+j].is_activated:
                        continue

                    self.activate_zero(coord_x+j, coord_y + i)

    def switch_flag(self, coord_x, coord_y):
        """
        Permet de mettre un drapeau a la case aux coordonnées x et y renseignées.
        """
        if coord_y > self.size_y or coord_x > self.size_x or coord_x < 0 or coord_y < 0:
            pass
        else:
            self.matrice[coord_y][coord_x].switch_flag()

    def has_win(self):
        """
        Renvoie vrai si la partie est considérée comme gagnée.
        (toutes les cases activées sauf les bombes)
        """
        for line in self.matrice:
            for column in line:
                if column.has_bomb:
                    continue
                if not column.is_activated:
                    return False
        return True

    def trade(self, coord_a, coord_b):
        """
        ***FONCTION A TESTER***
        Permet de déplacer une case de coordonnées coord_a avec une autre de coordonnées coord_b.
        """
        if (coord_a[1] > self.size_y or coord_a[0] > self.size_x \
        or coord_a[0] < 0 or coord_a[1] < 0):
            if (coord_b[1] > self.size_y or coord_b[0] > self.size_x \
            or coord_b[0] < 0 or coord_b[1] < 0):
                pass
            else:
                tmp_case = self.matrice[coord_a[1]][coord_a[0]]
                self.matrice[coord_a[1]][coord_a[0]] = self.matrice[coord_b[1]][coord_b[0]]
                self.matrice[coord_b[1]][coord_b[0]] = tmp_case

    def get_bombs(self):
        """
        Renvoie la liste des bombes présentes dans le plateau.
        """

        result = []

        for coord_y in range(self.size_y):
            for coord_x in range(self.size_x):
                case = self.matrice[coord_y][coord_x]
                if case.has_bomb:
                    result.append(
                        {
                            "x": coord_x,
                            "y": coord_y,
                            "case": case
                        }
                    )

        return result

    def get_activated(self):
        """
        Renvoie une copie de la matrice avec seulement les cases activées.
        """

        result = []

        for coord_y in range(self.size_y):
            result.append([])
            for coord_x in range(self.size_x):
                case = self.matrice[coord_y][coord_x]
                if case.is_activated:
                    result[coord_y].append(case)
                else:
                    result[coord_y].append(None)

        return result

    def get_null_activated(self):
        """
        Renvoie une copie de la matrice avec seulement les cases et n'ayant pas de bombes autour.
        """

        result = []

        for coord_y in range(self.size_y):
            result.append([])
            for coord_x in range(self.size_x):
                case = self.matrice[coord_y][coord_x]
                if case.is_activated and case.bombs_around == 0:
                    result[coord_y].append(case)
                else:
                    result[coord_y].append(None)

        return result
