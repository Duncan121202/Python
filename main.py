import pygame
pygame.font.init()
pygame.mixer.init()

LARGEUR , HAUTEUR = 900 , 500                               #   Définition de la taille de la fenêtre
VEL = 5                                                     #   Rapidité du déplacement
BALLES_VEL = 7                                              #   Rapidité des projectiles
MAX_BALLES = 3                                              #   Nombres de balles sur l'écran maximals pour chaque joueur

WINDOWS = pygame.display.set_mode((LARGEUR,HAUTEUR))        #   Création de la fenêtre
WHITE = ( 255 , 255 , 255 )                                 #   Couleur blanche
BLACK = ( 0, 0 , 0)                                         #   Couleur noire
COULEUR_BARRIERE = (181, 230, 215)                          #   Couleur de la barrière
RED = ( 255 , 0, 0)                                         #   Couleur rouge
YELLOW = ( 255 , 255 , 0)                                   #   Couleur jaune
FPS = 60                                                    #   Image par secondes du jeu

SON_BALLE_TOUCHE =pygame.mixer.Sound('Son2.mp3')            #   Importation des sons
SON_BALLE_TIREE = pygame.mixer.Sound('Son1.mp3')

BARRIERE = pygame.Rect(LARGEUR // 2 -5 ,0,10,HAUTEUR)       #   Création de la barrière

VAISSEAU_LONGUEUR,VAISSEAU_HAUTEUR = 55,40                  #   Dimension du vaisseau

SANTE_POLICE = pygame.font.SysFont('comicsans',40)          #   Police de "Score"
GAGNANT_POLICE = pygame.font.SysFont('comicsans',100)       #   Police de l'affichage gagnant

JAUNE_HIT = pygame.USEREVENT + 1                            #Création des évènements
ROUGE_HIT = pygame.USEREVENT + 2



#Rotation et redimension des deux vaisseaux :

VAISSEAU_JAUNE = pygame.transform.rotate(
        pygame.transform.scale(
        pygame.image.load('spaceship_yellow.png'),(VAISSEAU_LONGUEUR,VAISSEAU_HAUTEUR)),90)
VAISSEAU_ROUGE = pygame.transform.rotate(
    pygame.transform.scale(
        pygame.image.load('spaceship_red.png'),(VAISSEAU_LONGUEUR,VAISSEAU_HAUTEUR)),270)


# Importation de l'image en fond

ESPACE = pygame.transform.scale(pygame.image.load('fond-de-hotte-la-terre-vue-de-l-espace.jpg'),(LARGEUR,HAUTEUR))

#Nom de la fenêtre d'affichage
pygame.display.set_caption("Fenêtre")

def draw_window(rouge,jaune,balles_rouge,balles_jaune, rouge_sante , jaune_sante): #Fonction affichant à l'écran
    WINDOWS.blit(ESPACE,(0,0))                              #Affichage du fond d'écran
    pygame.draw.rect(WINDOWS,COULEUR_BARRIERE,BARRIERE)     #Affichage de la barrière

    rouge_sante_texte = SANTE_POLICE.render("Sante : " + str(rouge_sante), 1 , WHITE)
    jaune_sante_texte = SANTE_POLICE.render("Sante : " + str(jaune_sante), 1 , WHITE)

    WINDOWS.blit(rouge_sante_texte,(LARGEUR - rouge_sante_texte.get_width() - 10 , 10)) #Affichage de la santé des 2 joueurs
    WINDOWS.blit(jaune_sante_texte,(10,10))

    WINDOWS.blit(VAISSEAU_JAUNE,(jaune.x,jaune.y))  # Affichage des 2 vaisseaux
    WINDOWS.blit(VAISSEAU_ROUGE,(rouge.x,rouge.y))



    for bullet in balles_rouge:
        pygame.draw.rect(WINDOWS,RED,bullet)        #Affichage des balles
    for bullet in balles_jaune :
        pygame.draw.rect(WINDOWS,YELLOW,bullet)

    pygame.display.update()     #Update de l'écran

def jaune_mouvement(keys_pressed,jaune):
    if keys_pressed[pygame.K_q] and jaune.x - VEL > 0:  # TOUCHE GAUCHE
        jaune.x -= VEL
    if keys_pressed[pygame.K_d] and jaune.x + VEL + jaune.width < BARRIERE.x :  # TOUCHE DROITE
        jaune.x += VEL
    if keys_pressed[pygame.K_z] and jaune.y - VEL > 0:  # TOUCHE HAUT
        jaune.y -= VEL
    if keys_pressed[pygame.K_s] and jaune.y + VEL + jaune.height < HAUTEUR - 15 :  # TOUCHE BAS
        jaune.y += VEL

def rouge_mouvement(keys_pressed,rouge):
    if keys_pressed[pygame.K_LEFT] and rouge.x - VEL > BARRIERE.x + BARRIERE.width:  # TOUCHE GAUCHE
        rouge.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and rouge.x + VEL + rouge.width < LARGEUR :  # TOUCHE DROITE
        rouge.x += VEL
    if keys_pressed[pygame.K_UP] and rouge.y - VEL > 0 :  # TOUCHE HAUT
        rouge.y -= VEL
    if keys_pressed[pygame.K_DOWN] and rouge.y + VEL + rouge.height < HAUTEUR - 15 :  # TOUCHE BAS
        rouge.y += VEL

def handle_balles(jaune_balles, rouge_balles , jaune ,rouge):
    for bullet in jaune_balles :
        bullet.x += BALLES_VEL                                  # Déplacement de la balle
        if rouge.colliderect(bullet):                           # Évènement de collision entre la balle et le joueur
            pygame.event.post(pygame.event.Event(ROUGE_HIT))
            jaune_balles.remove(bullet)
        elif bullet.x > LARGEUR :                               # Fait disparaitre la balle lorsqu'elle sort de l'écran
            jaune_balles.remove(bullet)

    for bullet in rouge_balles :
        bullet.x -= BALLES_VEL                                  # Déplacement de la balle
        if jaune.colliderect(bullet):                           # Évènement de collision entre la balle et le joueur
            pygame.event.post(pygame.event.Event(JAUNE_HIT))
            rouge_balles.remove(bullet)
        elif bullet.x < 0 :
            rouge_balles.remove(bullet)                         # Fait disparaitre la balle lorsqu'elle sort de l'écran

def draw_winner(texte):                                         # Affichage du texte vainqueur
    draw_texte = GAGNANT_POLICE.render(texte,1,WHITE)
    WINDOWS.blit(draw_texte,(LARGEUR/2 - draw_texte.get_width()/2 , HAUTEUR/2 - draw_texte.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)                                     # Délai entre l'affichage de fin de partie et la fermeture de la fenêtre


def main():
    rouge = pygame.Rect(700,300,VAISSEAU_LONGUEUR,VAISSEAU_HAUTEUR)             #Rectange autour des sprites ( Sorte de Hitbox )
    jaune = pygame.Rect(100, 300, VAISSEAU_LONGUEUR, VAISSEAU_HAUTEUR)

    rouge_balles=[]                                                             #Liste contenant les informations des balles tirées
    jaune_balles=[]

    rouge_sante = 10            #Santé des deux joueurs
    jaune_sante = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)                     # Fréquence de rafraichissement de la fenêtre
        for event in pygame.event.get():
            if event.type == pygame.QUIT :  # Evènement pour quitter la fenêtre , ( Click sur la croix )
                run = False
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LCTRL and len(jaune_balles)<MAX_BALLES: # Evenement Touche de Tir appuyé
                    balle = pygame.Rect(jaune.x + jaune.width//2 , jaune.y + jaune.height//2 + 4,10,5)  #Dimension du projectile
                    jaune_balles.append(balle)
                    SON_BALLE_TIREE.play()

                if event.key == pygame.K_RCTRL and len(rouge_balles)<MAX_BALLES:    # Evenement Touche de Tir appuyé
                    balle = pygame.Rect(rouge.x, rouge.y + rouge.height // 2 + 4, 10,5)  # Dimension du projectile
                    rouge_balles.append(balle)
                    SON_BALLE_TIREE.play()

            if event.type == ROUGE_HIT :    # Conséquence de l'évènement Joueur Touché
                rouge_sante -= 1
                SON_BALLE_TOUCHE.play()

            if event.type == JAUNE_HIT :    # Conséquence de l'évènement Joueur Touché
                jaune_sante -= 1
                SON_BALLE_TOUCHE.play()

        gagnant_text = ""
        if rouge_sante <= 0:                            # Affichage des textes du joueur gagnant
            gagnant_text = " Le Jaune a Gagné ! "
        if jaune_sante <= 0:
            gagnant_text = " Le Rouge a Gagné ! "

        if gagnant_text != "":
            draw_winner(gagnant_text)
            break

        keys_pressed = pygame.key.get_pressed()
        jaune_mouvement(keys_pressed,jaune)
        rouge_mouvement(keys_pressed,rouge)

        handle_balles(jaune_balles,rouge_balles , jaune , rouge)

        draw_window(rouge,jaune, rouge_balles , jaune_balles , rouge_sante, jaune_sante)

    pygame.quit()

if __name__=="__main__":
    main()