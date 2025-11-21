import pygame
import os 
from pathlib import Path

# Taille de la fenetre 
Width, Height =760,760
Rows, Cols = 8,8
Square = Width//Rows

# Couleurs
bg = (220,220,220)
bleu = (145,152,255)
noir = (0,0,0)
blanc = (255,255,255)
gris = (128,128,128)

# Chemin de mes images.
chemin_image = Path.home() / "Desktop\Projet_GitHub\Jeu_d_echec\Jeu_d_echecs\echec_images"

# Pièces noirs
Cavalier_noir = pygame.transform.scale(pygame.image.load(os.path.join(chemin_image, "CN.png")),(Square, Square))
Roi_noir = pygame.transform.scale(pygame.image.load(os.path.join(chemin_image, "RoiN.png")),(Square, Square))
Reine_noir = pygame.transform.scale(pygame.image.load(os.path.join(chemin_image, "RN.png")),(Square, Square))
Fou_noir = pygame.transform.scale(pygame.image.load(os.path.join(chemin_image, "FN.png")),(Square, Square))
Tour_noir = pygame.transform.scale(pygame.image.load(os.path.join(chemin_image, "TN.png")),(Square, Square))
Pion_noir = pygame.transform.scale(pygame.image.load(os.path.join(chemin_image, "PN.png")),(Square, Square))

# Pièces Blanches
Cavalier_blanc = pygame.transform.scale(pygame.image.load(os.path.join(chemin_image, "CB.png")),(Square, Square))
Roi_blanc = pygame.transform.scale(pygame.image.load(os.path.join(chemin_image, "RoiB.png")),(Square, Square))
Reine_blanc = pygame.transform.scale(pygame.image.load(os.path.join(chemin_image, "RB.png")),(Square, Square))
Fou_blanc = pygame.transform.scale(pygame.image.load(os.path.join(chemin_image, "FB.png")),(Square, Square))
Tour_blanc = pygame.transform.scale(pygame.image.load(os.path.join(chemin_image, "TB.png")),(Square, Square))
Pion_blanc = pygame.transform.scale(pygame.image.load(os.path.join(chemin_image, "PB.png")),(Square, Square))
