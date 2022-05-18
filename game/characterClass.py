from animate import *
import pygame as pg
import math
from menu import *
pg.font.init()

class Character:
    def __init__(self, sheet, sX, sY, speed):
        self.img = pg.image.load(sheet)
        self.sheet = SpriteSheet(self.img, 32, 64, [24, 24, 24, 6, 12, 12, 12, 12])
        self.sheet.loadSheet()
        self.width = 32
        self.height = 64
        self.isFight = False
        # mental Health
        self.health = 10
        # physics knowledge
        self.pk = 1
        self.name = "You"
        self.score = 15

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

    def getHealth(self):
        return self.health

    def getpk(self):
        return self.pk

    def chHealth(self, amt):
        self.health += amt
        if self.health > 10:
            self.health = 10
        elif self.health < 0:
            self.health = 0
    
    def chpk(self, amt):
        self.pk += amt
        if self.pk > 10:
            self.pk = 10
        elif self.pk < 0:
            self.pk = 0

    def chScore(self, amt):
        self.score += amt
        if self.score > 100:
            self.score = 100
        elif self.pk < 0:
            self.score = 0


    def setPos(self, x, y):
        self.x = x
        self.y = y

    def setFight(self, condition):
        self.isFight = condition


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

    def damage(self, amount):
        self.health -= amount

class Whitney(Character):
    def __init__(self, sheet, sX, sY, speed):
        super().__init__(sheet, sX, sY, speed)
        self.clicks = 0
        self.speech = [["Ugh I do know my left from my right."],["Hi I'm Whitney!", "Dr. Whitbeck said you failed the last quiz!", "You must be pretty stupid!"],
        ["Stop bothering me!"]]
        self.sCount = 0
        self.bothered = "What? You wanna go? Dr. Whitbeck's gonna see what a loser you really are!"
        self.speak = False
        self.font = pg.font.Font("game/Fonts/Pixel.ttf", 16)
        self.fight = MenuButton(150, 650, 100, 40, (50,50,50), text="Fight", tSize=25, tColor=(200,200,200))
        # gonna make the battle more reliable
        self.code = "w"
        self.name = "Whitney"
        self.score = 70

    def interact(self, screen):
        pg.draw.rect(screen, (50, 50, 50), [100, 700, 600, 80])
        y = 700
        step = 25
        for i in self.speech[self.sCount]:
            text = self.font.render(i, True, (200, 200, 200), (50, 50, 50))
            textRect = text.get_rect()
            textRect.center = (350, y + (step // 2))
            screen.blit(text, textRect)
            y += step

        # we also need to create a menu button to fight whitney with
        self.fight.draw(screen)
        

    def nextSpeech(self):
        if self.sCount < len(self.speech) - 1:
            self.sCount += 1
        else:
            self.sCount = 0


class Raja(Character):
    def __init__(self, sheet, sX, sY, speed):
        super().__init__(sheet, sX, sY, speed)
        self.clicks = 0
        self.speech = [["I love Calculus"],["Please don't talk to me...", "Or sit near me...", "In fact I think you should just go now."],
        ["Man that quiz was easy!", "I haven't studied in 3 weeks either!!", "(glances around nervously)"]]
        self.sCount = 0
        self.bothered = "Ha! You better watch out, I have my collection of projectiles right here!"
        self.speak = False
        self.font = pg.font.Font("game/Fonts/Pixel.ttf", 16)
        self.fight = MenuButton(150, 650, 100, 40, (50,50,50), text="Fight", tSize=25, tColor=(200,200,200))
        # gonna make the battle more reliable
        self.code = "r"
        self.name = "Raja"
        self.score = 95

    def interact(self, screen):
        pg.draw.rect(screen, (50, 50, 50), [100, 700, 600, 80])
        y = 700
        step = 25
        for i in self.speech[self.sCount]:
            text = self.font.render(i, True, (200, 200, 200), (50, 50, 50))
            textRect = text.get_rect()
            textRect.center = (350, y + (step // 2))
            screen.blit(text, textRect)
            y += step

        # we also need to create a menu button to fight whitney with
        self.fight.draw(screen)
        

    def nextSpeech(self):
        if self.sCount < len(self.speech) - 1:
            self.sCount += 1
        else:
            self.sCount = 0

class Whitbeck(Character):
    def __init__(self, sheet, sX, sY, speed):
        super().__init__(sheet, sX, sY, speed)
        self.clicks = 0
        self.speech = [["God you are awful at physics."], ["Maybe you should study more instead of talking so much."], ["Do NOT ask me for a letter of rec"]]
        self.sCount = 0
        self.bothered = "Ha! You better watch out, I have my collection of projectiles right here!"
        self.speak = False
        self.font = pg.font.Font("game/Fonts/Pixel.ttf", 16)
        # gonna make the battle more reliable
        self.code = "r"
        self.name = "Raja"
        self.score = 95

    def interact(self, screen):
        pg.draw.rect(screen, (50, 50, 50), [100, 700, 600, 80])
        y = 700
        step = 25
        for i in self.speech[self.sCount]:
            text = self.font.render(i, True, (200, 200, 200), (50, 50, 50))
            textRect = text.get_rect()
            textRect.center = (350, y + (step // 2))
            screen.blit(text, textRect)
            y += step
        

    def nextSpeech(self):
        if self.sCount < len(self.speech) - 1:
            self.sCount += 1
        else:
            self.sCount = 0
