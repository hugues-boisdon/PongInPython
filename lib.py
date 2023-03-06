""" PONG IN PYTHON - Lib
Author : Hugues Boisdon
"""

#imports
import pygame
from sys import exit
import numpy
from random import random


#constants
FRAMERATE = 60
DISPLAY_WIDTH  = 1400
DISPLAY_HEIGHT = 600
DISPLAY_RATIO  = DISPLAY_HEIGHT / DISPLAY_WIDTH

PLAYER_SPEED = 400
PLAYER_BORDER_PADDING = 80

BALL_SPEED = 800


#library

def exitGame():
    pygame.quit()
    exit()

def wTs(x : int, y : int) -> tuple:
    """ WORLD TO SCREEN
    Transposing Vector2D to screen coordinates

    position : (px,px) in world coordinates
    return   : (x , y) in screen coordinates
    """
    X = DISPLAY_WIDTH/2 + x
    Y = DISPLAY_HEIGHT/2 - y
    return Vector2D(X,Y)



class Vector2D:
    x : int # pixels
    y : int # pixels

    def __init__(self, _x : int, _y : int):
        self.x = _x
        self.y = _y
    
    def __str__(self):
        screenPos = self.toScreen()
        return f'world({self.x},{self.y})  screen({screenPos.x},{screenPos.y})'

    def toTuple(self) -> tuple:
        return (self.x, self.y)

    def toScreen(self) -> tuple:
        return wTs(self.x, self.y)


    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __truediv__(self, num):
        return Vector2D(numpy.floor(self.x / num), numpy.floor(self.y / num))
    

class Object:

    position : Vector2D
    size : Vector2D

    def __init__(self, position : Vector2D, size : Vector2D):
        self.position = position
        self.size = size

        self.rect = pygame.Rect(0,0,0,0)
        self.calculateRect()
    
    def calculateRect(self):
        truePos = self.position.toScreen()
        left = truePos.x - self.size.x/2
        top  = truePos.y - self.size.y/2
        self.rect.update((left,top),self.size.toTuple())
    
    def draw(self, screen):
        self.calculateRect()
        pygame.draw.rect(screen,'White',self.rect)



class Player:

    def __init__(self, _object : Object, index : int):
        self.object = _object
        self.index = index
    
    def getInputs(self, keyPressed : dict):

        newPos = self.object.position
        
        if self.index == 1:

            if keyPressed[pygame.K_z]:
                newPos += Vector2D(0, PLAYER_SPEED / FRAMERATE)
            if keyPressed[pygame.K_s]:
                newPos -= Vector2D(0, PLAYER_SPEED / FRAMERATE)

        elif self.index == 2:

            if keyPressed[pygame.K_UP]:
                newPos += Vector2D(0, PLAYER_SPEED / FRAMERATE)
            if keyPressed[pygame.K_DOWN]:
                newPos -= Vector2D(0, PLAYER_SPEED / FRAMERATE)


        if newPos.x < - DISPLAY_WIDTH/2 + PLAYER_BORDER_PADDING:
            newPos.x = - DISPLAY_WIDTH/2 + PLAYER_BORDER_PADDING

        elif newPos.x > DISPLAY_WIDTH/2 - PLAYER_BORDER_PADDING:
            newPos.x = DISPLAY_WIDTH - PLAYER_BORDER_PADDING

        if newPos.y < - DISPLAY_HEIGHT/2 + PLAYER_BORDER_PADDING:
            newPos.y = - DISPLAY_HEIGHT/2 + PLAYER_BORDER_PADDING

        elif newPos.y > DISPLAY_HEIGHT/2 - PLAYER_BORDER_PADDING:
            newPos.y = DISPLAY_HEIGHT/2 - PLAYER_BORDER_PADDING
        
        self.object.position = newPos


class Ball:

    def __init__(self, _object : Object, p1 :Object ,p2 : Object):
        self.object = _object
        self.angleDir = 2*numpy.pi*0.1
        self.player1 : Object = p1
        self.player2 : Object = p2

        self.touchedLeft  = False
        self.touchedRight = False
    
    def move(self):

        newPos = self.object.position

        if newPos.y < - DISPLAY_HEIGHT/2:
            newPos.y = - DISPLAY_HEIGHT/2
            self.angleDir = - self.angleDir

        elif newPos.y > DISPLAY_HEIGHT/2:
            newPos.y = DISPLAY_HEIGHT/2
            self.angleDir = - self.angleDir



        touchingLeftPlayer = (newPos.x > self.player1.position.x - self.player1.size.x/2) and (newPos.x < self.player1.position.x + self.player1.size.x/2) 
        touchingLeftPlayer = touchingLeftPlayer and (newPos.y > self.player1.position.y - self.player1.size.y/2) and (newPos.y < self.player1.position.y + self.player1.size.y/2)

        touchingRightPlayer = (newPos.x > self.player2.position.x - self.player2.size.x/2) and (newPos.x < self.player2.position.x + self.player2.size.x/2) 
        touchingRightPlayer = touchingRightPlayer and (newPos.y > self.player2.position.y - self.player2.size.y/2) and (newPos.y < self.player2.position.y + self.player2.size.y/2)



        if newPos.x < - DISPLAY_WIDTH/2:
            newPos.x = - DISPLAY_WIDTH/2
            self.angleDir = -numpy.pi - self.angleDir

        elif newPos.x > DISPLAY_WIDTH/2:
            newPos.x = DISPLAY_WIDTH/2
            self.angleDir = -numpy.pi - self.angleDir

        if touchingLeftPlayer :
            if not self.touchedLeft :
                self.touchedLeft  = True
                self.angleDir = -numpy.pi - self.angleDir
        else:
            self.touchedLeft = False
        
        if touchingRightPlayer:
            if not self.touchedRight:
                self.touchedRight  = True
                self.angleDir = -numpy.pi - self.angleDir
        else:
            self.touchedRight = False

        move =  Vector2D(BALL_SPEED / FRAMERATE *numpy.cos(self.angleDir),BALL_SPEED / FRAMERATE *numpy.sin(self.angleDir))

        newPos += move
        self.object.position = newPos






