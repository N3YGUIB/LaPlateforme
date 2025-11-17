
import pygame
from pygame.locals import *

# Initialiser pygame
pygame.init()
pygame.mixer.init()

# Gestion de la fenêtre
LARGEUR, HAUTEUR = 1080,720 # Taille de la fenetre
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Pokémon Blue Sky") # Titre afficher sur la fenetre

# IMAGES
# Charger l'image background de la fenêtre
fond_intro= pygame.image.load(r"C:\Users\Neygu\Desktop\Jeu_Pokemon\Images\Pokemon.webp") #dimension de l'image 1080x720
fond_intro= pygame.transform.scale(fond_intro,(LARGEUR, HAUTEUR))

fond_menu = pygame.image.load(r"C:\Users\Neygu\Desktop\Jeu_Pokemon\Images\Menu.png").convert()
fond_menu = pygame.transform.scale(fond_menu,(LARGEUR, HAUTEUR))

# Charger l'image secondaire "logo pokemon"
titrepng=pygame.image.load(r"C:\Users\Neygu\Desktop\Jeu_Pokemon\Images\Titre.png").convert_alpha() # Dimension de l'image 2560x940

# Fond du jeu
fond_Jeu1= pygame.image.load(r"C:\Users\Neygu\Desktop\Jeu_Pokemon\Images\Jeu1.png").convert()
fond_Jeu1= pygame.transform.scale(fond_Jeu1,(LARGEUR, HAUTEUR))

# Charger les sons
pygame.mixer.music.load(r"C:\Users\Neygu\Desktop\Jeu_Pokemon\Sons\EcranTitreOST.mp3")
pygame.mixer.music.play(-1)
son_Lugia= pygame.mixer.Sound(r"C:\Users\Neygu\Desktop\Jeu_Pokemon\Sons\Cri_Lugia.mp3")
son_Clic= pygame.mixer.Sound(r"C:\Users\Neygu\Desktop\Jeu_Pokemon\Sons\Clic.mp3")

# Police
police = pygame.font.Font(None,40)

# Bouton "Press Start"
start_texte= police.render("APPUYER SUR ESPACE", True, (130,130,130))
texte_rect= start_texte.get_rect(center=(LARGEUR // 2, HAUTEUR - 150))

# Bouton Ecran Titre
    #si aucune donnée n'a été créée
boutons_1 =[
    pygame.image.load(r"C:\Users\Neygu\Desktop\Jeu_Pokemon\Images\Bouton_NouvellePartie1.png").convert_alpha(),
    pygame.image.load(r"C:\Users\Neygu\Desktop\Jeu_Pokemon\Images\Bouton_Options1.png").convert_alpha()
]
    # Si des données sont deja créer
boutons_2 =[
    pygame.image.load(r"C:\Users\Neygu\Desktop\Jeu_Pokemon\Images\Bouton_Continuer.png").convert_alpha(),
    pygame.image.load(r"C:\Users\Neygu\Desktop\Jeu_Pokemon\Images\Bouton_NouvellePartie2.png").convert_alpha(),
    pygame.image.load(r"C:\Users\Neygu\Desktop\Jeu_Pokemon\Images\Bouton_Options2.png").convert_alpha()

]
# positions des boutons 
positions = [
    (LARGEUR // 1000 - 0),  # bouton du haut
    (LARGEUR // 1000 - 0)    # bouton du bas
]

# Redimension des boutons a la taille de la fenetre
boutons_1 = [pygame.transform.scale(img, (LARGEUR,HAUTEUR))for img in boutons_1]

#======== clignotement du bouton "PRESS START" ========
clignote = True
temps = pygame.time.get_ticks()
intervalle = 450

#======== Etats du jeu ========
etat = "intro"
menu = True
continuer = True
selectioner = 0

horloge = pygame.time.Clock()

#======== Boucle principale ======== 
while continuer :
    for event in pygame.event.get():
        if event.type == QUIT : 
            continuer = False

        #======== Ecran intro ========
        if etat == "intro":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                son_Lugia.play()
                etat = "menu"
        
        #======== Navigation dans le menu ========
        elif etat == "menu":
            if event.type == KEYDOWN:
                if event.key == K_z: # Z pour aller en haut
                    selectioner = (selectioner - 1) % len(boutons_1)
                    son_Clic.play()
                elif event.key == K_s: # S pour aller en bas
                    selectioner = (selectioner + 1) % len(boutons_1)
                    son_Clic.play()
                elif event.key == K_SPACE: # Espace pour valider le choix
                    son_Clic.play()
                    if selectioner == 0:
                        etat = "jeu"
                    elif selectioner == 1:
                        print("options selectionné")
        #======== Jeu ========
        elif etat == "jeu":
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                etat = "menu"

            # Conditions pour le Clignotement du bouton "PRESS START"
            temps_actuel = pygame.time.get_ticks()
            if temps_actuel - temps > intervalle:
                clignote = not clignote
                temps = temps_actuel

    # Affichage dans la fenetre
        if etat == "intro":
            fenetre.blit(fond_intro,(0,0)) # Affiche le Background
            fenetre.blit(titrepng, (0,0)) # Affiche le logo "Pokémon"
            if clignote:
                fenetre.blit(start_texte,texte_rect) # Affiche "PRESS START"

        elif etat == "menu":
            fenetre.blit(fond_menu,(0,0)) # Si clic sur le bouton changement de "page"
        
            # Surbrillance des boutons  
            for i, boutons in enumerate (boutons_1):
                pos = positions[i]
                fenetre.blit(boutons, (pos))    
                
                if i == selectioner:
                    surbrillance = pygame.Surface((400, 100),pygame.SRCALPHA)
                    surbrillance.fill((0,0,0,100))
                    fenetre.blit(surbrillance, (pos))

        elif etat == "jeu":
            fenetre.blit(fond_Jeu1,(0,0))

    pygame.display.flip()
    horloge.tick(30)
pygame.mixer.music.stop() # Stop la musique si la fenetre se ferme
pygame.quit()