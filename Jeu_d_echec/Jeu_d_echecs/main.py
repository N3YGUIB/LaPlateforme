import sys
import os

# Ajoute le dossier courant au sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


import pygame

from pieces import *
from plateau import nvplateau
from jeu import Jeu
from constants import *

pygame.init()
Win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Échecs")

jeu = Jeu(Width, Height, Rows, Cols, Square, Win)
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(60)
    jeu.update_window()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row = y // Square
            col = x // Square
            jeu.select(row, col)

pygame.quit()
