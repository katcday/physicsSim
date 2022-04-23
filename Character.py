import pygame as pg

class Character:
    def __init__(self, speed, x, y, width, height, screen):
        self.speed = speed
        self.leftx = x
        self.lefty = y
        self.width = width
        self.height = height
        self.screen = screen

    def draw(self):
        pg.draw.rect(self.screen, (100, 100, 100), (self.leftx, self.lefty + self.height, width, height))

    def moveX(self):
        self.x += self.speed

    def moveY(self):
        self.y += self.speed

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def getX(self):
        return self.x 

    def getY(self):
        return self.y

    def getWidth(self):
        return self.width

