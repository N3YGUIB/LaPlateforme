import pygame
from plateau import nvplateau
from constants import *
from copy import deepcopy


class Jeu:
    def __init__(self, Width, Height, Rows, Cols, Square, Win):
        self.Win = Win
        self.plateau = nvplateau(Width, Height, Rows, Cols, Square, Win)
        self.Square = Square
        self.selected = None
        self.turn = blanc
        self.valid_moves = []
        self.pieces_noir_droite = 16
        self.pieces_blanc_droite = 16
    
    def update_window(self):

        self.plateau.dessiner_Plateau()
        self.plateau.dessiner_pieces()
        self.dessine_available_moves()
        pygame.display.update()

    def reset(self):
        self.plateau = nvplateau(self, Width, Height, Rows, Cols, Square, Win)
        self.Square = Square
        self.selected = None

    def check_game(self):
        if self.pieces_noir_droite == 0:
            print("Les Blanc Gagne !")
            return True

        if self.pieces_blanc_droite == 0:
            print("Les Noirs gagne !")
            return True
        
        if self.echec_et_mat(self.plateau):
            if self.turn == blanc:
                print("Les Noirs gagne !")
                return True
            else:
                print("Les Blanc Gagne !")
                return True
    
    def enemies_moves(self, piece, plateau):
        enemies_moves = []
        for r in range(len(plateau)):
            for c in range(len(plateau[r])):
                if plateau[r][c] != 0:
                    if plateau[r][c].color != piece.color:
                        moves = plateau[r][c].get_availables_moves(r, c, plateau)
                        for move in moves:
                            enemies_moves.append(move)
        return enemies_moves
    
    def get_Roi_pos(self,plateau):
        for r in range(len(plateau)):
            for c in range(len(plateau[r])):
                if plateau[r][c] != 0:
                    if plateau[r][c].type == "roi" and plateau[r][c].color == self.turn:
                        return (r, c)

    def simulate_move(self, piece, row, col):
        piece_row, piece_col = piece.row, piece.col
        save_piece = self.plateau.plateau[row][col]

        if self.plateau.plateau[row][col] != 0:
            self.plateau.plateau[row][col] = 0

        self.plateau.plateau[piece.row][piece.col], self.plateau.plateau[row][col] = self.plateau.plateau[row][col], self.plateau.plateau[piece.row][piece.col]

        roi_Pos = self.get_Roi_pos(self.plateau.plateau)
        if roi_Pos in self.enemies_moves(piece, self.plateau.plateau):
            piece.row, piece.col = piece_row, piece_col
            self.plateau.plateau[piece_row][piece_col] = piece
            self.plateau.plateau[row][col] = save_piece
            return False
        
        piece.row, piece.col = piece_row, piece_col
        self.plateau.plateau[piece_row][piece_col] = piece
        self.plateau.plateau[row][col] = save_piece
        return True

    def possible_moves(self, Plateau):
        possible_moves = []
        for r in range(len(Plateau)):
            for c in range(len(Plateau[r])):
                if Plateau[r][c] != 0:
                    if Plateau[r][c].color == self.turn and Plateau[r][c].type != "roi":
                        moves =Plateau[r][c].get_availables_moves(r,c,Plateau)

                        for move in moves:
                            possible_moves.append(move)

        return possible_moves
    
    def echec_et_mat(self,plateau):
        roi_pos = self.get_Roi_pos(plateau.plateau)
        get_roi = plateau.get_piece(roi_pos[0], roi_pos[1])

        roi_availables_moves = set(get_roi.get_availables_moves(roi_pos[0], roi_pos[1], plateau.plateau))
        enemies_moves_set = set(self.enemies_moves(get_roi, plateau.plateau))
        roi_moves = roi_availables_moves - enemies_moves_set
        set1 = roi_availables_moves.intersection(enemies_moves_set)
        possible_moves_def = set1.intersection(self.possible_moves(plateau.plateau))

        if len(roi_moves)  == 0 and len(roi_availables_moves) != 0 and len(possible_moves_def) == 0:
            return True
    
        return False
    

    def change_turn(self):
        if self.turn == blanc:
            self.turn = noir
        else:
            self.turn = blanc

    def select(self, row, col):
        if self.selected:
            move = self._move(row, col)

            if not move:
                self.selected = None
                self.select(row, col)

        piece = self.plateau.get_piece(row, col)
        if piece != 0 and self.turn == piece.color:
            self.selected = piece

            self.valid_moves = piece.get_availables_moves(row, col, self.plateau.plateau)

    def _move(self,row, col):
        piece = self.plateau.get_piece(row,col)

        if self.selected and (row, col) in self.valid_moves:
            if piece == 0 or piece.color != self.selected.color:
                if self.simulate_move(self.selected, row, col):
                    
                    self.remove( self.plateau.plateau, piece, row, col)
                    self.plateau.move(self.selected, row, col)
                    self.change_turn()
                    self.valid_moves = []
                    self.selected = None
                    return True
                return False
        
        return False
    
    def remove(self, plateau, piece, row, col):
        if piece != 0:
            plateau[row][col] = 0
            if piece.color == blanc:
                self.pieces_blanc_droite -= 1
            else:
                self.pieces_noir_droite -= 1

    def dessine_available_moves(self):
        if len( self.valid_moves) >0:
            for pos in self.valid_moves:
                row, col = pos[0], pos[1]
                pygame.draw.circle(self.Win, gris, (col*self.Square + self.Square//2, row*self.Square + self.Square//2), self.Square//8)

    def get_plateau(self):
        return self.plateau
