from animate import *
import pygame as pg

class Character:
    def __init__(self, sheet, sX, sY, speed):
        self.img = pg.image.load(sheet)
        self.sheet = SpriteSheet(self.img, 32, 64, [4, 24, 24, 6, 12, 12, 12, 12])
        self.sheet.loadSheet()

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
            self.sheet.spliceFrames(2, start, end)
            start += 6
            end += 6

        self.stand = self.sheet.tempDump()

        self.x = sX
        self.y = sY
        self.speed = speed

    def walk(direction, fps, counter, screen):
        # we want to update this every 10 fps
        waitTime = 10 / fps
        waitTime = int(waitTime * 10)

        if direction == "U":
            self.walk[0].resetAn()
            self.walk[2].resetAn()
            self.walk[3].resetAn()
            ind = 1
            self.y -= 1

        if direction == "D":
            self.walk[1].resetAn()
            self.walk[2].resetAn()
            self.walk[0].resetAn()
            ind = 3
            self.y += 1

        if direction == "L":
            self.walk[1].resetAn()
            self.walk[0].resetAn()
            self.walk[3].resetAn()
            ind = 2
            self.x -= 1

        if direction == "R":
            self.walk[1].resetAn()
            self.walk[2].resetAn()
            self.walk[3].resetAn()
            ind = 0
            self.x += 1

        img = self.walk[ind].getFrame()

        if counter % waitTime == 0:
            screen.blit(img, (self.x, self.y))
            


