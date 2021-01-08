import pygame
import random
import math

# initializing the pygame
pygame.init()

# creating a screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("background.png")

# making title
pygame.display.set_caption("first game")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("space_invader.png")
playerx = 350
playerx_change = 0
playery = 480

# enemy
enemyImg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_enemies = 6
for i in range(num_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyx.append(random.randint(0, 735))
    enemyx_change.append(6)
    enemyy.append(random.randint(20, 80))
    enemyy_change.append(80)

# bullet
# here we need a bullet state to check if it fires on press of space bar
bulletImg = pygame.image.load("bullet.png")
bulletx = 0
bulletx_change = 3
bullety = 480
bullety_change = 10
bullet_state = "ready"
# score counter
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textx = 10
texty = 10

over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over():
    game_over_text = over_font.render("Game Over :)", True, (255, 255, 255))
    screen.blit(game_over_text, (280, 250))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 5))


def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow((enemyx - bulletx), 2) + math.pow((enemyy - bullety), 2))
    if distance < 32:
        return True


# making a game loop
running = True
while running:
    # RGB values 0- 255 it is written first so that all other stuff is above the background color
    screen.fill((23, 34, 56))
    # background img const
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # to check if the keyboard arrow key is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -3.5
            if event.key == pygame.K_RIGHT:
                playerx_change = 3.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # checking for player boundaries
    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    # enemy for player boundaries
    for i in range(num_enemies):
        if enemyy[i] > 430:
            for j in range(num_enemies):
                enemyy[j] = 1000
            game_over()
            break
        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 6
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -6
            enemyy[i] += enemyy_change[i]
        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision == True:
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(20, 80)
        # calling the enemy method for enemy to be always be visible on screen
        enemy(enemyx[i], enemyy[i], i)
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    # calling the player method for player to be always be visible on screen
    player(playerx, playery)
    # displaying the score on screen
    show_score(textx, texty)
    # always update screen to view effects
    pygame.display.update()
