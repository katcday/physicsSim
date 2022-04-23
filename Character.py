import pygame as pg
import math

class Character:
    def __init__(self, speed, x, y, width, height):
        self.speed = speed
        self.leftx = x
        self.lefty = y
        self.width = width
        self.height = height

    # draws rectangle to screen
    def draw(self, screen):
        pg.draw.rect(screen, (100, 100, 100), (self.leftx, self.lefty + self.height, self.width, self.height))

    def moveR(self, mag=1):
        for i in range(mag):
            self.leftx += self.speed

    def moveL(self, mag=1):
        for i in range(mag):
            self.leftx -= self.speed

    def moveU(self, mag=1):
        for i in range(mag):
            self.lefty -= self.speed

    def moveD(self,mag=1):
        for i in range(mag):
            self.lefty += self.speed

    def setX(self, x):
        self.leftx = x

    def setY(self, y):
        self.lefty = y

    def getX(self):
        return self.leftx 

    def getY(self):
        return self.lefty

    def getWidth(self):
        return self.width

    def collide(self, blocks, bSize):
        # first we need to find hwo many blocks we might intersect with
        widthInB = math.ceil(self.width / bSize)
        # next we find the first one
        j = self.leftx // bSize
        i = (self.lefty + 2 *self.height) // bSize

        current = blocks[i][j]

        collide = False
        # check to see if bottom line collides with block
        for block in range(widthInB):
            if current.getState() == True:
                collide = True
                print(i, j)
            j += 1
            current = blocks[i][j]

        return collide

    

