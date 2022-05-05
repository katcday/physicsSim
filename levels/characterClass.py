from animate import *
import pygame as pg
import math

class Character:
    def __init__(self, sheet, sX, sY, speed):
        self.img = pg.image.load(sheet)
        self.sheet = SpriteSheet(self.img, 32, 64, [24, 24, 24, 6, 12, 12, 12, 12])
        self.sheet.loadSheet()
        self.width = 32
        self.height = 64

        start = 0
        end = 5
        for i in range(4):
            self.sheet.spliceFrames(1, start, end)
            start += 6
            end += 6

        self.walk = self.sheet.tempDump()

        start = 0
        end = 5
        for i in range(4):
            self.sheet.spliceFrames(0, start, end)
            start += 6
            end += 6

        self.stand = self.sheet.tempDump()

        self.x = sX
        self.y = sY
        self.speed = speed
        self.nextFrame = self.stand[0].getFrame()

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction, fps, counter, screen, move, wait):
        # we want to update this every 10 fps
        # we want to update this every 10 fps

        if move == True:

            if direction == "U":
                self.walk[0].resetAn()
                self.walk[2].resetAn()
                self.walk[3].resetAn()
                ind = 1
                self.y -= self.speed

            if direction == "D":
                self.walk[1].resetAn()
                self.walk[2].resetAn()
                self.walk[0].resetAn()
                ind = 3
                self.y += self.speed

            if direction == "L":
                self.walk[1].resetAn()
                self.walk[0].resetAn()
                self.walk[3].resetAn()
                ind = 2
                self.x -= self.speed

            if direction == "R":
                self.walk[1].resetAn()
                self.walk[2].resetAn()
                self.walk[3].resetAn()
                ind = 0
                self.x += self.speed

            if counter % wait == 0:
                self.nextFrame = self.walk[ind].getFrame()

        else:

            # stand motion will need to use last direction
            if direction == "U":
                self.stand[0].resetAn()
                self.stand[2].resetAn()
                self.stand[3].resetAn()
                ind = 1

            if direction == "D":
                self.stand[1].resetAn()
                self.stand[2].resetAn()
                self.stand[0].resetAn()
                ind = 3

            if direction == "L":
                self.stand[1].resetAn()
                self.stand[3].resetAn()
                self.stand[0].resetAn()
                ind = 2

            if direction == "R":
                self.stand[1].resetAn()
                self.stand[2].resetAn()
                self.stand[3].resetAn()
                ind = 0
            
            if counter % wait == 0:
                self.nextFrame = self.stand[ind].getFrame()
        


        #if counter % waitTime == 0:
            #screen.blit(img, (self.x, self.y))
        #creen.blit(img, (self.x, self.y))

    def collide(self, blocks, bSize):
        # first we need to find hwo many blocks we might intersect with
        widthInB = math.ceil(self.width / bSize)
        # next we find the first one
        leftx = self.x
        lefty = self.y + (self.height)
        j = int(leftx // bSize)
        i = int(lefty // bSize)

        current = blocks[i][j]

        collide = False
        # check to see if bottom line collides with block
        for block in range(widthInB):
            if current.getState() == True:
                collide = True
            j += 1
            current = blocks[i][j]

        return collide

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def draw(self, screen):
        screen.blit(self.nextFrame, (self.x, self.y))
            


