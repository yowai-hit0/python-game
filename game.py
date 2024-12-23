import pygame
import random

# initialize the pygame
pygame.init()

screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption('galaxy war', ' the ')
pygame.display.get_allow_screensaver()

# icon
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
# enemy
enemyImg = pygame.image.load('yogurt.png')
enemyX = random.randint(0, 800)
enemyY = random.randint(20, 500)
enemyX_change = 0.1
enemyY_change = random.randrange(-20, 20)


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


# player


playerImg = pygame.image.load('spaceship.png')
playerX = 380
playerY = 501
playerX_change = 0
playerY_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# opengl loop

running = True

while running:
    screen.fill((25, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            if event.key == pygame.K_DOWN:
                playerY_change = 0.2
            if event.key == pygame.K_UP:
                playerY_change = -0.2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT == event.key or pygame.K_UP == event.key or pygame.K_DOWN == event.key:
                playerX_change = 0
                playerY_change = 0
    # player movements
    playerX += playerX_change
    playerY += playerY_change
    # boundaries for plater
    if playerX <= 0:
        playerX = 0
    if playerX >= 750:
        playerX = 750
    if playerY <= 10:
        playerY = 10
    if playerY >= 550:
        playerY = 550
    # enemy movements
    enemyX += enemyX_change
    enemyY_change = random.randrange(-50, 30)
    if enemyX <= 0:
        enemyX_change = 0.1

        enemyY += enemyY_change
    elif enemyX >= 750:
        enemyX_change = -0.1
        enemyY += enemyY_change
    # boundaries for enemy

    if enemyY <= 10:
        enemyY = 10
    if enemyY >= 550:
        enemyY = 550

    enemy(enemyX, enemyY)
    player(playerX, playerY)
    pygame.display.update()

pygame.quit()
