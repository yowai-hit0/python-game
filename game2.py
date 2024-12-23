import pygame
import random
import serial
import time
from pygame import mixer
# Initialize pygame
pygame.init()

game_state = "opengl is playing"
time_limit = 30
# Record the start time of the opengl
start_time = time.time()

clock = pygame.time.Clock()
# Set up the screen
screen = pygame.display.set_mode([800, 590])
pygame.display.set_caption('Galaxy War')
# background
background = pygame.image.load('img_1.png')
# Icon
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Enemy
enemyImg = pygame.image.load('oil.png')
enemies = []
#serial
# ser = serial.Serial('COM13',9600)
def spawn_enemy():
    enemyX = random.randint(0, 750)
    enemyY = random.randint(20, 500)
    enemyX_change = random.randrange(-20, 20)
    enemyY_change = random.randrange(-20, 20)
    enemies.append([enemyX, enemyY, enemyX_change, enemyY_change])

def draw_enemy(x, y):
    screen.blit(enemyImg, (x, y))

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 380
playerY = 501
playerX_change = 0
X_min = 0
Y_min = 0
X_max = 1000
Y_max = 1000
playerY_change = 0
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textx = 10
texty = 10
gameover = pygame.font.Font('freesansbold.ttf',64)
loses = pygame.font.Font('freesansbold.ttf',64)
def gameOver():
    gameOve = gameover.render("YOU WIN", True, (255,255,255))
    screen.blit(gameOve, (200,200))
def youLose():
    youlose = loses.render("YOU LOSE", True, (255,255,255))
    screen.blit(youlose, (200,200))
def showScore(x,y):
    scor_val = font.render("Score : "+ str(score),True, (255,255,255))
    screen.blit(scor_val, (x, y))
def draw_player(x, y):
    screen.blit(playerImg, (x, y))

def is_collision(playerX, playerY, enemyX, enemyY):
    distance = ((playerX - enemyX) ** 2 + (playerY - enemyY) ** 2) ** 0.5
    if distance < 27:
        return True
    return False
# music
mixer.music.load('fight.wav')
mixer.music.play(1)

# Game loop
running = True

while running:
    new_data_received = False
    # screen.fill((25, 20, 20))
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    elapsed_time = time.time() - start_time
    if elapsed_time >= time_limit:
        game_state = "opengl over"

    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_DOWN:
                playerY_change = 5
            if event.key == pygame.K_UP:
                playerY_change = -5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerX_change = 0
                    playerY_change = 0
    #
    # # Read joystick data from the serial port
    # # data = ser.readline().decode().strip().split(',')
    # if len(data) == 2:
    #     raw_x, raw_y = map(int, data)
    #     new_data_received = True
    #
    #     # Map the raw joystick data to the screen's dimensions
    #     target_x = int((raw_x - X_min) / (X_max - X_min) * 800)
    #     target_y = int((raw_y - Y_min) / (Y_max - Y_min) * 900)
    #
    # # Smoothly move the character only if new data is received
    # if new_data_received:
    #     playerX = playerX + (target_x - playerX) * 0.09
    #     playerY = playerY + (target_y - playerY) * 0.09


    # Player movements
    playerX += playerX_change
    playerY += playerY_change

    # Boundaries for player
    if playerX < 0:
        playerX = 0
    if playerX > 750:
        playerX = 750
    if playerY < 10:
        playerY = 10
    if playerY > 550:
        playerY = 550

    # Enemy movements
    for enemy_info in enemies:
        enemy_info[0] += enemy_info[2]
        enemy_info[3] = random.randrange(-50, 30)
        if enemy_info[0] < 0:
            enemy_info[2] = 10
        elif enemy_info[0] > 750:
            enemy_info[2] = -10

    # Remove enemies that go out of bounds
    enemies = [[x, y, x_change, y_change] for x, y, x_change, y_change in enemies if 10 <= y <= 550]

    # Collision detection
    for enemy_info in enemies:
        if is_collision(playerX, playerY, enemy_info[0], enemy_info[1]):
            score += 1
            enemies.remove(enemy_info)
            eat_sound = mixer.Sound('eat.wav')
            eat_sound.play()

    # Spawn new enemies up to a maximum of 10
    while len(enemies) < 5:
        spawn_enemy()
    # Draw enemies
    for enemy_info in enemies:
        draw_enemy(enemy_info[0], enemy_info[1])
    showScore(textx, texty)
    draw_player(playerX, playerY)
    if game_state == "opengl over":
        youLose()
        lose_sound = mixer.Sound('lose.wav')
        lose_sound.play(1)
    if score >= 5:
        gameOver()
        win_sound = mixer.Sound('win.wav')
        win_sound.play()
        win_sound.set_volume(100)
    clock.tick(60)
    pygame.display.update()
pygame.quit()
