import pygame as pg

class Block:
    def __init__(self, bSize, x, y, screen):
        self.collide = False
        self.size = bSize
        self.x = x
        self.y = y
        self.screen = screen

    def getState(self):
        return self.collide

    def newState(self, state):
        self.collide = state

    def draw(self):
        if self.collide == True:
            pg.draw.rect(self.screen, (50, 100, 50), (self.x, self.y, self.size, self.size))