import pygame as pg 

pg.init()

class Sprite:
    def __init__(self, sheet, iX, iY, speed):
        self.sheet = sheet
        self.x = iX
        self.y = iY
        self.speed = speed
        
    def moveU(self):
        self.y -= self.speed

    def moveD(self):
        self.y += self.speed

    def moveL(self):
        self.x -= self.speed

    def moveR(self):
        self.x += self.speed
