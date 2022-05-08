import pygame as pg

# stores the collision info. bSize determines the length of one side of the square in pixels 
class Block:
    def __init__(self, bSize, x, y):
        # true if passable
        self.collide = False
        self.size = bSize
        self.x = x
        self.y = y

    # returns whether you can pass through the block or not
    def getState(self):
        return self.collide

    # changes the state
    def newState(self, state):
        self.collide = state

    # draws the block. must be given the pygame screen
    def draw(self, screen):
        if self.collide == True:
            pg.draw.rect(screen, (50, 100, 50), (self.x, self.y, self.size, self.size))