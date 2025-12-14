import pygame
from constants import *

class Pieces:
    def __init__(self, Square, image, color, type, row, col):
        self.Square = Square
        self.image = image
        self.color = color
        self.row = row
        self.col = col
        self.type = type
        self.x = 0
        self.y = 0
        self.availables_moves = []
        self.first_move = True if type == "pion" else False
        self.calc_pos()

    def piece_move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def calc_pos(self):
        self.x = self.col * self.Square
        self.y = self.row * self.Square

    def clear_available_moves(self):
        self.availables_moves = []

    def get_availables_moves(self, row, col, Plateau):
        return self.availables_moves

# ===================== PIÈCES ===================== #

class Pion(Pieces):
    def __init__(self, Square, image, color, type, row, col):
        super().__init__(Square,image,color,type,row,col)

    def get_availables_moves(self, row, col, Plateau):
        self.clear_available_moves()
        direction = -1 if self.color == blanc else 1
        # Avancer
        if 0 <= row+direction < 8 and Plateau[row+direction][col] == 0:
            self.availables_moves.append((row+direction, col))
            # premier double pas
            if self.first_move and 0 <= row+2*direction < 8 and Plateau[row+2*direction][col] == 0:
                self.availables_moves.append((row+2*direction, col))
        # Diagonales
        for dc in [-1,1]:
            if 0 <= col+dc < 8 and 0 <= row+direction < 8 and Plateau[row+direction][col+dc] != 0:
                piece = Plateau[row+direction][col+dc]
                if piece.color != self.color:
                    self.availables_moves.append((row+direction, col+dc))
        return self.availables_moves

class tour(Pieces):
    def get_availables_moves(self, row, col, Plateau):
        self.clear_available_moves()
        # Haut/Bas
        for r in range(row-1,-1,-1):
            if Plateau[r][col] == 0:
                self.availables_moves.append((r,col))
            else:
                if Plateau[r][col].color != self.color:
                    self.availables_moves.append((r,col))
                break
        for r in range(row+1,8):
            if Plateau[r][col] == 0:
                self.availables_moves.append((r,col))
            else:
                if Plateau[r][col].color != self.color:
                    self.availables_moves.append((r,col))
                break
        # Gauche/Droite
        for c in range(col-1,-1,-1):
            if Plateau[row][c] == 0:
                self.availables_moves.append((row,c))
            else:
                if Plateau[row][c].color != self.color:
                    self.availables_moves.append((row,c))
                break
        for c in range(col+1,8):
            if Plateau[row][c] == 0:
                self.availables_moves.append((row,c))
            else:
                if Plateau[row][c].color != self.color:
                    self.availables_moves.append((row,c))
                break
        return self.availables_moves

class fou(Pieces):
    def get_availables_moves(self, row, col, Plateau):
        self.clear_available_moves()
        for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
            r, c = row+dr, col+dc
            while 0<=r<8 and 0<=c<8:
                if Plateau[r][c] == 0:
                    self.availables_moves.append((r,c))
                else:
                    if Plateau[r][c].color != self.color:
                        self.availables_moves.append((r,c))
                    break
                r += dr
                c += dc
        return self.availables_moves

class cavalier(Pieces):
    def get_availables_moves(self, row, col, Plateau):
        self.clear_available_moves()
        moves = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
        for dr, dc in moves:
            r, c = row+dr, col+dc
            if 0<=r<8 and 0<=c<8:
                if Plateau[r][c] == 0 or Plateau[r][c].color != self.color:
                    self.availables_moves.append((r,c))
        return self.availables_moves

class reine(Pieces):
    def get_availables_moves(self, row, col, Plateau):
        self.clear_available_moves()
        # Combine tour + fou
        self.availables_moves = tour.get_availables_moves(self, row, col, Plateau) + fou.get_availables_moves(self, row, col, Plateau)
        return self.availables_moves

class roi(Pieces):
    def get_availables_moves(self, row, col, Plateau):
        self.clear_available_moves()
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr==0 and dc==0:
                    continue
                r, c = row+dr, col+dc
                if 0<=r<8 and 0<=c<8:
                    if Plateau[r][c] == 0 or Plateau[r][c].color != self.color:
                        self.availables_moves.append((r,c))
        return self.availables_moves
