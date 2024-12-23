import pygame
import serial

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Joystick Game")

# Character properties
character = pygame.Rect(100, 100, 20, 20)
character_speed = 5  # Adjust the speed as needed

# Define the joystick value ranges
x_initial = 494
x_max = 1023
x_min = 0
y_initial = 501
y_max = 1023
y_min = 0

# Serial communication
ser = serial.Serial('COM13', 9600)  # Change 'COM3' to the correct serial port

# Character position variables
x, y = character.center  # Initialize to character's initial position

# Main opengl loop
running = True
while running:
    new_data_received = False  # Reset the flag at the beginning of each loop iteration

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read joystick data from the serial port
    data = ser.readline().decode().strip().split(',')
    if len(data) == 2:
        raw_x, raw_y = map(int, data)
        new_data_received = True

        # Map the raw joystick data to the screen's dimensions
        target_x = int((raw_x - x_min) / (x_max - x_min) * 400)
        target_y = int((raw_y - y_min) / (y_max - y_min) * 400)

    # Smoothly move the character only if new data is received
    if new_data_received:
        x = x + (target_x - x) * 0.2
        y = y + (target_y - y) * 0.2

    # Update character position based on the smoothed values
    character.center = (x, y)

    # Limit character movement to the screen boundaries
    character.x = max(0, min(580, character.x))
    character.y = max(0, min(580, character.y))

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the character
    pygame.draw.rect(screen, (255, 0, 0), character)

    # Update the display
    pygame.display.flip()

# Clean up and close the opengl
ser.close()
pygame.quit()

