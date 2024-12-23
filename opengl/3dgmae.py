from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import serial
import json

ser = serial.Serial('COM13', 9600)  # Replace 'COM3' with your Arduino port

def draw_cube():
    glutWireCube(1)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    try:
        data = ser.readline().decode().strip()
        if data:
            joystick_data = json.loads(data)
            joyX1, joyY1, joyX2, joyY2 = (
                joystick_data.get("joyX1", 0),
                joystick_data.get("joyY1", 0),
                joystick_data.get("joyX2", 0),
                joystick_data.get("joyY2", 0),
            )
            # Adjust your game logic here based on joystick input
            glTranslatef(joyX1 / 1024 - 0.5, joyY1 / 1024 - 0.5, -(joyX2 / 1024 - 0.5))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    draw_cube()
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutCreateWindow(b"Joystick Control Tutorial")
glutReshapeWindow(800, 600)
glutDisplayFunc(display)
glutIdleFunc(display)
glutMainLoop()
