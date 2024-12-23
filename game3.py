import pygame
import random
import serial

# Initialize pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption('Galaxy War')

# Icon
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Enemy
enemyImg = pygame.image.load('yogurt.png')
enemies = []

def spawn_enemy():
    enemyX = random.randint(0, 750)
    enemyY = random.randint(20, 500)
    enemyX_change = 0.1
    enemyY_change = random.randrange(-20, 20)
    enemies.append([enemyX, enemyY, enemyX_change, enemyY_change])

def draw_enemy(x, y):
    screen.blit(enemyImg, (x, y))

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 380
playerY = 501
playerX_change = 0
playerY_change = 0
score = 0

def draw_player(x, y):
    screen.blit(playerImg, (x, y))

def is_collision(playerX, playerY, enemyX, enemyY):
    distance = ((playerX - enemyX) ** 2 + (playerY - enemyY) ** 2) ** 0.5
    if distance < 27:
        return True
    return False

# Serial communication setup
ser = serial.Serial('COM13', 9600)  # Replace 'COM3' with the correct serial port and baud rate

# Game loop
running = True

while running:
    screen.fill((25, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read data from the serial port
    if ser.in_waiting:
        data = ser.readline().decode().strip()
        if data:
            print(f"Received data: {data}")  # Debug print
            try:
                # Split the received data into X and Y values
                x, y = map(int, data.split(','))
                playerX_change = x / 100.0  # Adjust the scaling factor as needed
                playerY_change = y / 100.0  # Adjust the scaling factor as needed
            except ValueError:
                print("Error: Invalid data format")

    # ... Rest of the opengl loop remains the same

# Game loop
running = True

while running:
    screen.fill((25, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read data from the serial port
    if ser.in_waiting:
        data = ser.readline().decode().strip()
        if data:
            # Split the received data into X and Y values
            x, y = map(int, data.split(','))
            playerX_change = x / 100.0  # Adjust the scaling factor as needed
            playerY_change = y / 100.0  # Adjust the scaling factor as needed

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
            enemy_info[2] = 0.1
        elif enemy_info[0] > 750:
            enemy_info[2] = -0.1

    # Remove enemies that go out of bounds
    enemies = [[x, y, x_change, y_change] for x, y, x_change, y_change in enemies if 10 <= y <= 550]

    # Collision detection
    for enemy_info in enemies:
        if is_collision(playerX, playerY, enemy_info[0], enemy_info[1]):
            score += 1
            enemies.remove(enemy_info)

    # Spawn new enemies up to a maximum of 10
    while len(enemies) < 10:
        spawn_enemy()

    # Draw enemies
    for enemy_info in enemies:
        draw_enemy(enemy_info[0], enemy_info[1])

    draw_player(playerX, playerY)
    pygame.display.update()

    if score >= 10:
        running = False

ser.close()  # Close the serial port when the opengl is finished

pygame.quit()
