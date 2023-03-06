""" PONG IN PYTHON
Author : Hugues Boisdon
"""

#imports
import pygame
from sys import exit
from lib import *


#initialisation
pygame.init()
SCREEN = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
pygame.display.set_caption('PongInPython')

clock = pygame.time.Clock()

#gameObjects

LEFT  = Object(position = Vector2D(-0.75 * DISPLAY_WIDTH/2,0), size = Vector2D(20,160))
RIGHT = Object(position = Vector2D( 0.75 * DISPLAY_WIDTH/2,0), size = Vector2D(20,160))

Player1 = Player(LEFT,1)
Player2 = Player(RIGHT,2)

BALL = Object(position= Vector2D(0,0), size = Vector2D(20,20))

ball = Ball(BALL, LEFT, RIGHT)



pause = False
#game loop
while True:

    keyPressed = pygame.key.get_pressed()

    if keyPressed[pygame.K_BACKSPACE]:
        exitGame()
    
        pause = not pause
    
    if not pause :
        Player1.getInputs(keyPressed)
        Player2.getInputs(keyPressed)
        ball.move()


    for event in pygame.event.get():

        #exiting game
        if event.type == pygame.QUIT:
            exitGame()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause
                
    #drawing
    SCREEN.fill("Black")

    LEFT.draw(SCREEN)
    RIGHT.draw(SCREEN)
    BALL.draw(SCREEN)

    #updating display
    pygame.display.flip()
    clock.tick(FRAMERATE)
