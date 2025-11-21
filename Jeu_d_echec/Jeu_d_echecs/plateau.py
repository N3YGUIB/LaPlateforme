import pygame
from pieces import *
from constants import *

class nvplateau:
    def __init__(self, Width, Height, Rows, Cols, Square, Win):
        self.Width = Width
        self.Height = Height
        self.Square = Square
        self.Win = Win
        self.Rows = Rows
        self.Cols = Cols
        self.plateau = []
        self.creer_Plateau()

    def creer_Plateau(self):
        self.plateau = [[0 for _ in range(self.Cols)] for _ in range(self.Rows)]
        for row in range(self.Rows):
            for col in range(self.Cols):
                # Pions
                if row == 1:
                    self.plateau[row][col] = Pion(self.Square, Pion_noir, noir, "pion", row, col)
                elif row == 6:
                    self.plateau[row][col] = Pion(self.Square, Pion_blanc, blanc, "pion", row, col)
                # Autres pièces
                if row == 0:
                    if col in [0,7]:
                        self.plateau[row][col] = tour(self.Square, Tour_noir, noir, "tour", row, col)
                    elif col in [1,6]:
                        self.plateau[row][col] = cavalier(self.Square, Cavalier_noir, noir, "cavalier", row, col)
                    elif col in [2,5]:
                        self.plateau[row][col] = fou(self.Square, Fou_noir, noir, "fou", row, col)
                    elif col == 3:
                        self.plateau[row][col] = reine(self.Square, Reine_noir, noir, "reine", row, col)
                    elif col == 4:
                        self.plateau[row][col] = roi(self.Square, Roi_noir, noir, "roi", row, col)
                elif row == 7:
                    if col in [0,7]:
                        self.plateau[row][col] = tour(self.Square, Tour_blanc, blanc, "tour", row, col)
                    elif col in [1,6]:
                        self.plateau[row][col] = cavalier(self.Square, Cavalier_blanc, blanc, "cavalier", row, col)
                    elif col in [2,5]:
                        self.plateau[row][col] = fou(self.Square, Fou_blanc, blanc, "fou", row, col)
                    elif col == 3:
                        self.plateau[row][col] = reine(self.Square, Reine_blanc, blanc, "reine", row, col)
                    elif col == 4:
                        self.plateau[row][col] = roi(self.Square, Roi_blanc, blanc, "roi", row, col)

    def get_piece(self, row, col):
        return self.plateau[row][col]

    def move(self, piece, row, col):
        self.plateau[piece.row][piece.col] = 0
        self.plateau[row][col] = piece
        piece.piece_move(row, col)
        if piece.type == "pion" and piece.first_move:
            piece.first_move = False

    def dessiner_Plateau(self):
        self.Win.fill(bleu)
        for row in range(Rows):
            for col in range(row%2, Cols, 2):
                pygame.draw.rect(self.Win, bg, (Square*col, Square*row, Square, Square))

    def dessiner_piece(self, piece):
        self.Win.blit(piece.image, (piece.x, piece.y))

    def dessiner_pieces(self):
        for row in self.plateau:
            for piece in row:
                if piece != 0:
                    self.dessiner_piece(piece)
