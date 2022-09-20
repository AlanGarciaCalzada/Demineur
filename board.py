# -*- coding: utf-8 -*-
import time
from random import randint
from enum import Enum
from typing import List

class Tile(Enum):
    ACTIVATED = 10     # only for bomb_view since user_view has numbers
    INACTIVATED = 20   # only for user_view when a tile is not activated
    NO_BOMB = 30       # only for bomb_view when there is no bomb
    BOMB = 40          # only for bomb_view when there is a bomb
    FORBIDDEN = 50     # only for bomb_view when it is forbidden to place a bomb

class Board:

    def __init__(self, user_view, bomb_view):
        self.user_view = user_view
        self.bomb_view = bomb_view
        #self.bombe_nb = bombe_nb

        self.cases_activated = 0
        self.cases_inactivated = len(self.user_view) * len(self.user_view[0])
        self.zero_nb = 0

        self.wall = set()

        for y in range(len(self.user_view)):
            for x in range(len(self.user_view[y])):

                if self.user_view[y][x] != Tile.INACTIVATED:
                    self.cases_activated += 1

                    if self.user_view[y][x] == 0:
                        self.zero_nb += 1

                    for i in range(-1,2):
                        for j in range(-1,2):

                            if not (0 <= y-i < len(self.bomb_view) and 0 <= x-j < len(self.bomb_view[y-i])) or (i,j) == (0,0):
                                continue
                            
                            if self.bomb_view[y-i][x-j] != Tile.ACTIVATED:
                                self.wall.add((x-j,y-i))

        self.cases_inactivated -= self.cases_activated



    def nb_case_non_zero(self):
        result = 0
        for y in range(len(self.user_view)):
            for x in range(len(self.user_view[y])):
                if self.user_view[y][x] != Tile.INACTIVATED and self.user_view[y][x] > 0:
                    result += 1
        return result

    def place_bombe(self, x, y):

        if self.bomb_view[y][x] == Tile.BOMB or self.bomb_view[y][x] == Tile.FORBIDDEN:
            return False

        result = True

        for i in range(-1,2):
            for j in range(-1,2):

                if not (0 <= y-i < len(self.user_view) and 0 <= x-j < len(self.user_view[y-i])) or (i,j) == (0,0):
                    continue

                if self.user_view[y-i][x-j] != Tile.INACTIVATED:
                    self.user_view[y-i][x-j] -= 1

                    if self.user_view[y-i][x-j] < 0:
                        result = False
        
        self.bomb_view[y][x] = Tile.BOMB

        return result


    def enleve_bombe(self, x, y):

        if self.bomb_view[y][x] == Tile.NO_BOMB or self.bomb_view[y][x] == Tile.FORBIDDEN:
            return False

        for i in range(-1,2):
            for j in range(-1,2):

                if not (0 <= y-i < len(self.user_view) and 0 <= x-j < len(self.user_view[y-i])) or (i,j) == (0,0):
                    continue

                if self.user_view[y-i][x-j] != Tile.INACTIVATED:
                    self.user_view[y-i][x-j] += 1
        
        self.bomb_view[y][x] = Tile.NO_BOMB

        return True

    def size_interieur(self):
        return self.cases_inactivated

    def liste_frontiere(self):
        return self.wall

    def is_bomb(self,x,y):
        if not (0 <= y < len(self.bomb_view) and 0 <= x < len(self.bomb_view[y])):
            return None

        return self.bomb_view[y][x] == Tile.BOMB
    
    def result(self):
        return user_view, bomb_view


def solve(board,nb_bombs):
    
    if nb_bombs==0:
       if board.nb_case_non_zero()==0:
           return board
       else:
           return None

    if board.nb_case_non_zero()==0:
        if nb_bombs<=board.size_interieur():

            for _ in range(nb_bombs):
                bomb_y = randint(0, len(board.user_view)-1)
                bomb_x = randint(0, len(board.user_view[bomb_y])-1)
                while board.bomb_view[bomb_y][bomb_x] == Tile.ACTIVATED or board.bomb_view[bomb_y][bomb_x] == Tile.BOMB or (bomb_x,bomb_y) in board.liste_frontiere():
                    bomb_y = randint(0, len(board.user_view)-1)
                    bomb_x = randint(0, len(board.user_view[bomb_y])-1)
                board.bomb_view[bomb_y][bomb_x] = Tile.BOMB

            return board
        else:
            return None

    for (x,y) in board.liste_frontiere():
        if board.is_bomb(x,y):
            continue
        res=board.place_bombe(x,y)
        if not res:
            board.enleve_bombe(x,y)
            continue
        res_solve=solve(board,nb_bombs-1)
        if res_solve is None:
            board.enleve_bombe(x,y)
            continue
        else:
            return board
    
    return None



def generate_grid():
    """user_view = [
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, 3, 2, 1],
        [None, None, 2, 0, 0],
        [None, None, 2, 0, 0]
    ]

    bomb_view = [
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, None, None, None],
        [False, False, None, None, None],
        [False, False, None, None, None],
    ]

    bombe_nb = 10"""

    """user_view = [
        [0, 1, None, None],
        [0, 1, None, None],
        [0, 0, 1, 1]
    ]

    bomb_view = [
        [None, None, False, False],
        [None, None, False, False],
        [None, None, None, None]
    ]

    bombe_nb = 3"""

    """user_view = [
        [0, 1, None, None, None],
        [0, 1, 2, None, None],
        [0, 0, 1, 2, 2],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    bomb_view = [
        [None, None, False, False, False],
        [None, None, None, False, False],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None]
    ]

    bombe_nb = 3"""

    """user_view = [
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, 3, 2, 1, 2, None],
        [None, 2, 0, 0, 1, None],
        [None, 3, 2, 1, 1, None],
        [None, None, None, None, None, None]
    ]

    bomb_view = [
        [False, False, False, False, False, False],
        [False, False, False, False, False, False],
        [False, None, None, None, None, False],
        [False, None, None, None, None, False],
        [False, None, None, None, None, False],
        [False, False, False, False, False, False]
    ]

    bombe_nb = 10"""

    user_view = [
        [Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED],
        [Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED],
        [Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED],
        [Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED],
        [Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, 2, 2, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED],
        [Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, 1, 0, 0, 1, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED],
        [Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, 2, 0, 0, 0, 1, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED],
        [Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, 1, 1, 1, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED],
        [Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED],
        [Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED],
        [Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED, Tile.INACTIVATED]
    ]

    bomb_view = [
        [Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB],
        [Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB],
        [Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB],
        [Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB],
        [Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.ACTIVATED, Tile.ACTIVATED, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB],
        [Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.ACTIVATED, Tile.ACTIVATED, Tile.ACTIVATED, Tile.ACTIVATED, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB],
        [Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.ACTIVATED, Tile.ACTIVATED, Tile.ACTIVATED, Tile.ACTIVATED, Tile.ACTIVATED, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB],
        [Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.ACTIVATED, Tile.ACTIVATED, Tile.ACTIVATED, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB],
        [Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB],
        [Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB],
        [Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB, Tile.NO_BOMB]
    ]

    bombe_nb = 31

    return user_view, bomb_view, bombe_nb


def create_board_from(plateau):

    user_view = []
    bomb_view = []

    for y in range(len(plateau.matrice)):

        user_line = []
        bomb_line = []

        for x in range(len(plateau.matrice[y])):

            case = plateau.matrice[y][x]

            if case.is_activated:
                user_line.append(case.bombs_around)
                bomb_line.append(Tile.ACTIVATED)
            else:
                user_line.append(Tile.INACTIVATED)
                bomb_line.append(Tile.NO_BOMB)
        
        user_view.append(user_line)
        bomb_view.append(bomb_line)
    
    pretty_grid(user_view, bomb_view)
    
    board_result = Board(user_view, bomb_view)

    return board_result

trad = "0️⃣ ,1️⃣ ,2️⃣ ,3️⃣ ,4️⃣ ,5️⃣ ,6️⃣ ,7️⃣ ,8️⃣ ".split(",")

def pretty_grid(user_view, bomb_view):
    print("USER VIEW")
    for line in user_view:

        to_print = ""

        for case in line:

            if case == Tile.INACTIVATED:
                to_print += "⬛ "
            else:
                to_print +=  trad[case] + " "
        
        print(to_print)


    print("BOMBES VIEW")
    for line in bomb_view:

        to_print = ""

        for case in line:

            if case == Tile.ACTIVATED:
                to_print += "⬛ "

            elif case == Tile.NO_BOMB:
                to_print += "0️⃣  "

            elif case == Tile.BOMB:
                to_print += "1️⃣  "
        
        print(to_print)

def pretty_matrix(matrix):
    for lines in matrix:
        print(lines)

if __name__ == "__main__":
    user_view, bomb_view, bombe_nb = generate_grid()
    board = Board(user_view, bomb_view)
    # User Action, Click on 2,1
    #bomb_view[1][2] = True
    pretty_grid(user_view, bomb_view)
    print("\nAprès ... \n")
    start = time.time()
    pretty_grid(board.user_view,board.bomb_view)
    print("\nCases activés : ", board.cases_activated)
    print("\nCases non activés : ", board.cases_inactivated)
    print("\nWall : ", board.wall)
    print("\nNombre de 0 :", board.zero_nb)
    print("\nNombre de non 0 :", board.nb_case_non_zero())
    print("\nCensé être False :", board.is_bomb(1,1))
    results = solve(board, bombe_nb)
    end = time.time()
    if not results:
        print("ça marche pas")
    else:
        user_view, bomb_view = results.result()
        pretty_grid(user_view, bomb_view)
        print("\n\n")
    print("\n\n", end - start)