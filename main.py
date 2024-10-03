import pygame
import os
import random
import math
from pygame import mixer

# Initialize Pygame
pygame.init()

# CREATE screen
screen = pygame.display.set_mode((800, 600))

# TITLE AND ICON
pygame.display.set_caption('Space Invasion')
icon = pygame.image.load('/Users/alvarogonzalez/Documents/ITC/1_Primer_Semestre/JuegoUdemy/Python-Total-Course/Decimo Dia/ovni.png')
pygame.display.set_icon(icon)
background = pygame.image.load('/Users/alvarogonzalez/Documents/ITC/1_Primer_Semestre/JuegoUdemy/Python-Total-Course/Decimo Dia/fondo.jpg')

# ADD BACKGROUND MUSIC
mixer.music.load('/Users/alvarogonzalez/Documents/ITC/1_Primer_Semestre/JuegoUdemy/Python-Total-Course/Decimo Dia/MusicaFondo.mp3')
mixer.music.play(-1)  # -1 means it repeats every time it ends

# PLAYER VARIABLES
player_img = pygame.image.load('/Users/alvarogonzalez/Documents/ITC/1_Primer_Semestre/JuegoUdemy/Python-Total-Course/Decimo Dia/cohete.png')
player_x = 368
player_y = 500
player_x_change = 0

# ENEMY VARIABLES
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 8

for e in range(num_of_enemies):
    enemy_img.append(pygame.image.load('/Users/alvarogonzalez/Documents/ITC/1_Primer_Semestre/JuegoUdemy/Python-Total-Course/Decimo Dia/enemigo.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(0.3)
    enemy_y_change.append(50)

# BULLET VARIABLES
bullet_img = pygame.image.load('/Users/alvarogonzalez/Documents/ITC/1_Primer_Semestre/JuegoUdemy/Python-Total-Course/Decimo Dia/bala.png')
bullet_x = 0
bullet_y = 500
bullet_x_change = 0
bullet_y_change = 0.6
bullet_visible = False

# SCORE
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)  # FONT TYPE
text_x = 10
text_y = 10

# GAME OVER TEXT
game_over_font = pygame.font.Font('freesansbold.ttf', 40)

def game_over_text():
    my_game_over_font = game_over_font.render('Game Over', True, (255, 255, 255))
    screen.blit(my_game_over_font, (250, 250))

# FUNCTION TO DISPLAY SCORE
def show_score(x, y):
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (x, y))

# PLAYER FUNCTION
def player(x, y):
    screen.blit(player_img, (x, y))  # DRAW THE PLAYER

# ENEMY FUNCTION
def enemy(x, y, ene):
    screen.blit(enemy_img[ene], (x, y))  # DRAW THE ENEMY

# FUNCTION TO SHOOT BULLET
def shoot_bullet(x, y):
    global bullet_visible
    bullet_visible = True
    screen.blit(bullet_img, (x + 16, y + 10))

# FUNCTION TO DETECT COLLISION
def is_collision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y2 - y1, 2))
    if distance < 27:
        return True
    else:
        return False

# NEW FUNCTION
ship_crash = False

# FUNCTION TO DETECT SPACESHIP COLLISION
def space_ship_collision(x1, y1, x2, y2):
    global ship_crash
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y2 - y1, 2))

    if distance < 50:
        ship_crash = True
    
    if ship_crash:
        return True
    else:
        return False

# GAME LOOP
running = True
while running:

    # BACKGROUND IMAGE
    screen.blit(background, (0, 0))

    # EVENT ITERATION
    for event in pygame.event.get():

        # EVENT TO CLOSE WINDOW
        if event.type == pygame.QUIT:  # When pressing close button
            running = False

        # EVENT TO PRESS KEYS
        if event.type == pygame.KEYDOWN:  # A key was pressed
            if event.key == pygame.K_LEFT:
                player_x_change = -0.5
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.5
            if event.key == pygame.K_SPACE:
                if not bullet_visible:
                    bullet_sound = mixer.Sound('/Users/alvarogonzalez/Documents/ITC/1_Primer_Semestre/JuegoUdemy/Python-Total-Course/Decimo Dia/disparo.mp3')
                    bullet_sound.play()
                    bullet_x = player_x
                    shoot_bullet(bullet_x, bullet_y)

        # EVENT TO RELEASE KEYS
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # UPDATE PLAYER POSITION
    player_x += player_x_change

    # KEEP PLAYER WITHIN SCREEN BORDERS
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # BULLET MOVEMENT
    if bullet_y <= -64:
        bullet_y = 500
        bullet_visible = False

    if bullet_visible:
        shoot_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # UPDATE ENEMY MOVEMENT
    for e in range(num_of_enemies):
        ship_crash = space_ship_collision(enemy_x[e], enemy_y[e], player_x, player_y)

        # END GAME
        if enemy_y[e] > 436 and ship_crash:
            for k in range(num_of_enemies):
                enemy_y[k] = 1000
            game_over_text()
            break

        enemy_x[e] += enemy_x_change[e]

        # KEEP ENEMY WITHIN SCREEN BORDERS
        if enemy_x[e] <= 0:
            enemy_x_change[e] = 0.3
            enemy_y[e] += enemy_y_change[e]
        elif enemy_x[e] >= 736:
            enemy_x_change[e] = -0.3
            enemy_y[e] += enemy_y_change[e]

        # COLLISION DETECTION
        collision = is_collision(enemy_x[e], enemy_y[e], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound('/Users/alvarogonzalez/Documents/ITC/1_Primer_Semestre/JuegoUdemy/Python-Total-Course/Decimo Dia/golpe.mp3')
            collision_sound.play()
            bullet_y = 500
            bullet_visible = False
            score += 1
            enemy_x[e] = random.randint(0, 736)
            enemy_y[e] = random.randint(50, 200)

        enemy(enemy_x[e], enemy_y[e], e)

    player(player_x, player_y)

    show_score(text_x, text_y)
    
    # UPDATE SCREEN
    pygame.display.update()
