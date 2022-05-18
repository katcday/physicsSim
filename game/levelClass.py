import pygame as pg
from combat import *
from characterClass import *
import random as r

class Level:
    def __init__(self, bgImg, collisionMap, screen, characters=[]):
        self.bg = bgImg
        self.characters = characters
        self.savedPos = []
        for char in self.characters:
            self.savedPos.append([char.getX(), char.getY()])
        self.collisionMap = collisionMap
        self.imPixelsX = ((screen.get_width() // 32) / 2) * 32 - ((self.bg.get_width() // 32) / 2 * 32)
        self.imPixelsY = ((screen.get_height() // 32) / 2) * 32 - ((self.bg.get_height() // 32) / 2 * 32)
        self.clicked = False

    def draw(self, screen, counter, wait):
        # draw background and image
        screen.fill((0,0,0))
        screen.blit(self.bg, (self.imPixelsX, self.imPixelsY))

        if len(self.characters) > 1:
            nonMC = self.characters[1:]
            for char in nonMC:
                char.move('D', 30, counter, screen, False, wait)
                char.draw(screen)

        self.characters[0].draw(screen) 

        self.gui(screen, self.characters[0])   

    # draws players stats
    def gui(self, screen, char):
        # first draw bar to top left and right of screen
        pg.draw.rect(screen, (250, 250, 200), [30, 5, 200, 20])
        pg.draw.rect(screen, (250, 250, 200), [570, 5, 200, 20])
        font = pg.font.Font('game/Fonts/Pixel.ttf', 15)

        text = font.render("Mental Health", True, (200, 200, 200), (0,0,0))
        tb = text.get_rect()
        tb.center = (130, 40)
        screen.blit(text, tb)
        text = font.render("Physics Knowledge", True, (200, 200, 200), (0,0,0))
        tb = text.get_rect()
        tb.center = (670, 40)
        screen.blit(text, tb)

        # draw health bar
        percent = char.getHealth() / 10
        val = int(194 * percent)
        pg.draw.rect(screen, (232, 89, 79), [33, 8, val, 14])

        # draw physics knowledge
        percent = char.getpk() / 10
        val = int(194 * percent)
        pg.draw.rect(screen, (80, 89, 232), [573, 8, val, 14])
        


    def getBlocks(self):
        return self.collisionMap

    # saves character positions and game states 
    def save(self):
        count = 0
        for i in self.characters:
            self.savedPos[count] = [i.getX(), i.getY()]
            count += 1

    def open(self): 
        count = 0
        for i in self.characters:
            i.setPos(self.savedPos[count][0], self.savedPos[count][1])
            count += 1



class Dorm(Level):
    def __init__(self, bg, blocks, screen, characters=[]):
        super().__init__(bg, blocks, screen, characters)
        self.sleep = False
        self.objects = [Bed(387, 458, 324, 361), Books(), Computer(), Bookshelf(), Shower(), Fridge()]
        self.time = 1
        self.timeLim = 1600
        self.font = pg.font.Font("game/Fonts/Pixel.ttf", 20)
        self.hw = False
        self.disMsg = ""
        self.setTime = 0
        self.length = 0

    def setup(self):
        self.characters[0].setPos(418, 336)
        self.time = 1
        self.save()
        self.hw = False
        self.disMsg = ""
        self.setTime = 0
        self.length = 0

    def update(self, screen):
        x = pg.mouse.get_pos()[0]
        y = pg.mouse.get_pos()[1]

        # draw objects
        for o in self.objects:
            if o.clicked == True:
                o.display(screen)

        text = str(self.time // 200)
        text = self.font.render(text, True, (200, 200, 200), (0,0,0))
        tb = text.get_rect()
        tb.center = (400, 60)
        screen.blit(text, tb)

        if self.time < (self.setTime + self.length):
            iniY = 545
            step = 25
            for line in self.disMsg:
                text = self.font.render(line, True, (200, 200, 200), (0,0,0))
                tb = text.get_rect()
                tb.center = (400, iniY)
                screen.blit(text, tb)
                iniY += step


        self.time += 1

    def click(self, screen):
        x = pg.mouse.get_pos()[0]
        y = pg.mouse.get_pos()[1]

        if self.objects[0].collideB(x, y) == True and self.objects[0].clicked == True:
            buttonInd = self.objects[0].findB()
            if buttonInd == 0:
                self.sleep = self.objects[0].button1()
            elif buttonInd == 1:
                self.sleep = self.objects[0].button2()

            # we turn off the display screen
            self.objects[0].cClick(False)
        elif self.objects[0].collide(x, y) == True:
            self.objects[0].cClick(True)

    # book collisoons
        if self.objects[1].collideB(x, y) == True and self.objects[1].clicked == True:
            buttonInd = self.objects[1].findB()
            if buttonInd == 0 and self.time + 200 < self.timeLim:
                self.time += 200
                self.characters[0].chpk(1)

                self.disMsg = ["You feel prepared for tomorrow's quiz now."]
                self.setTime = self.time
                self.length = 60
            elif buttonInd == 0 and self.time + 200 >= self.timeLim:
                self.disMsg = ["It's a bit late to start studying."]
                self.setTime = self.time
                self.length = 60

            # we turn off the display screen
            self.objects[1].cClick(False)

        elif self.objects[1].collide(x, y) == True:
            self.objects[1].cClick(True)
# computer
        if self.objects[2].collideB(x, y) == True and self.objects[2].clicked == True:
            buttonInd = self.objects[2].findB()
            print(buttonInd)
            if buttonInd == 0 and self.time + 200 < self.timeLim and self.characters[0].getpk() > 0:
                self.time += 200
                self.characters[0].chpk(-1)
                self.hw = True
                self.characters[0].chHealth(2)
                self.disMsg = ["Hmmm you may have a hundred this time,", "but you know all to well that that won't be the case on the next quiz."]
                self.setTime = self.time
                self.length = 60
            elif buttonInd == 2 and self.time + 200 >= self.timeLim:
                self.disMsg = ["You don't even have time to cheat on this one."]
                self.setTime = self.time
                self.length = 60
            elif buttonInd == 0 and self.time + 200 < self.timeLim and self.characters[0].getpk() <= 0:
                self.disMsg = ["You are literally so stupid you cannot afford to cheat."]
                self.setTime = self.time
                self.length = 60

            if buttonInd == 1 and self.time + 400 < self.timeLim:
                self.time += 400
                self.characters[0].chHealth(3)
                self.disMsg = ["Mentally: Free"]
                self.setTime = self.time
                self.length = 60
            elif buttonInd == 1 and self.time + 400 >= self.timeLim:
                self.disMsg = ["You can't play video games now! Class is about to start."]
                self.setTime = self.time
                self.length = 60

            if buttonInd == 2 and self.time + 500 < self.timeLim:
                self.time += 500
                self.characters[0].chpk(4)
                self.disMsg = ["That was a slog, but you know you understand the content.", "Hopefully Dr. Whitbeck recognizes it."]
                self.setTime = self.time
                self.length = 60
            elif buttonInd == 2 and self.time + 500 >= self.timeLim:
                self.disMsg = ["There is not enough time to get your homework done."]
                self.setTime = self.time
                self.length = 60

            # we turn off the display screen
            self.objects[2].cClick(False)

        elif self.objects[2].collide(x, y) == True:
            self.objects[2].cClick(True)

    # booksshelf
        if self.objects[3].clicked == True:

            # we turn off the display screen
            self.objects[3].cClick(False)

        elif self.objects[3].collide(x, y) == True:
            self.objects[3].cClick(True)

        if self.objects[4].clicked == True:

            # we turn off the display screen
            self.objects[4].cClick(False)

        elif self.objects[4].collide(x, y) == True:
            self.objects[4].cClick(True)

        if self.objects[5].clicked == True:

            # we turn off the display screen
            self.objects[5].cClick(False)

        elif self.objects[5].collide(x, y) == True:
            self.objects[5].cClick(True)


    def sleepToHealth(self):
        hours = (self.timeLim - self.time) // 200
        print(hours)
        self.characters[0].chHealth(hours)


    def isSleep(self):
        if self.sleep == True or self.time >= self.timeLim:
            print("sleep true")
            print(self.time)
            self.sleep = False
            self.sleepToHealth()
            return 1
        else:
            return 0


class Classroom(Level):
    def __init__(self, bg, blocks, screen, characters=[]):
        super().__init__(bg, blocks, screen, characters)
        self.enemy = 0
        self.dispProgress = True
        self.mainFont = pg.font.Font("game/Fonts/Pixel.ttf", 60)
        self.smallFont = pg.font.Font("game/Fonts/Pixel.ttf", 20)
        self.timer = 1
        self.progTime = 400
        self.timeLim = 2400
        self.leave = MenuButton(10, 750, 100, 40, (50,50,50), text="Go to Dorm", tSize = 17, tColor=(200,200,200))

    def drawProgBar(self, screen):
        bg = (90, 127, 250)
        screen.fill(bg)
        text = "Reputation-Meter"
        text = self.mainFont.render(text, True, (200, 200, 200), bg)
        textRect = text.get_rect()
        textRect.center = (400, 330)
        screen.blit(text, textRect)
        
        pg.draw.rect(screen, (235, 178, 191), [100, 420, 600, 100])
        # draw all the different character bars
        colors = [(199, 14, 56), (235, 0, 235), (12, 41, 235)]
        highest = 0
        middle = 0
        lowest = 0
        order = [0, 0, 0]
        if self.characters[0].score >= self.characters[1].score and self.characters[0].score >= self.characters[2].score:
            order[0] = self.characters[0]
            if self.characters[1].score >= self.characters[2].score:
                order[1] = self.characters[1]
                order[2] = self.characters[2]
            else:
                order[1] = self.characters[2]
                order[2] = self.characters[1]
        elif self.characters[1].score >= self.characters[0].score and self.characters[1].score >= self.characters[2].score:
            order[0] = self.characters[1]
            if self.characters[0].score >= self.characters[2].score:
                order[1] = self.characters[0]
                order[2] = self.characters[2]
            else:
                order[1] = self.characters[2]
                order[2] = self.characters[0]
        else:
            order[0] = self.characters[2]
            if self.characters[0].score >= self.characters[1].score:
                order[1] = self.characters[0]
                order[2] = self.characters[1]
            else:
                order[1] = self.characters[1]
                order[2] = self.characters[0]
        
        colorInd = 0
        for i in order:
            self.scoreVal(i.score, screen, colors[colorInd], i, self.timer, bg)
            colorInd += 1

        words = "Click to continue..."
        words = self.smallFont.render(words, True, (200, 200, 200), bg)
        tb = words.get_rect()
        tb.center = (400, 650)
        screen.blit(words, tb)



    def scoreVal(self, score, screen, color, char, counter, bg):
        val = int((score / 100) * 592)
        pg.draw.rect(screen, color, [104, 424, val, 92])
        ix = char.getX()
        iy = char.getY()
        char.setPos(104 + val - (char.width // 2), 520)
        char.move('D', 30, counter, screen, False, 3)
        char.draw(screen)
        char.setPos(ix, iy)
        text = self.smallFont.render(str(score) + "%", True, (200, 200, 200), bg)
        textRect = text.get_rect()
        textRect.center = (104 + val, 400)
        screen.blit(text, textRect)


    # sets up the characters in their correct positions.
    # if other variables need to be changed they are also handled here
    def setup(self):
        mc = self.characters[0]
        mc.setPos(265, 133)

        w = self.characters[1]
        w.setPos(354, 419)

        r = self.characters[2]
        r.setPos(400, 520)

        wb = self.characters[3]
        wb.setPos(399, 95)

        for c in self.characters[1:]:
            c.setFight(False)

        self.timer = 1
        self.disProgress = True

        self.save()

    def click(self, screen):
        x = pg.mouse.get_pos()[0]
        y = pg.mouse.get_pos()[1]

        if self.timer <= self.progTime:
            self.timer = self.progTime
        else:
            if self.clicked == True:
                self.clicked = False
                counter = 1
                # when there is a second click we need to turn off the text and see if they clicked fight
                for char in self.characters[1:3]:
                    if char.speak == True and char.fight.collision(x, y, True) == True:
                        char.isFight = True
                        self.enemy = counter

                    char.speak = False
                    counter += 1
                self.characters[3].speak = False
            else:
                for char in self.characters[1:]:
                    if x > char.getX() and x < char.getX() + 32 and y > char.getY() and y < char.getY() + 64:
                        self.clicked = True
                        char.speak = True
                        char.nextSpeech()

            if self.leave.collision(x, y, True) == True:
                self.timer = self.timeLim

# what is wrong with this i will never knwo will only loop through one character ahhhhhh tears hair out
    def sartFight(self, levels):
        #print(self.characters)
        for char in self.characters[1:3]:
            #print(char)
            #print(char.code)
            if char.isFight == True:
                print("true")
                # now we need to reset battle level
                levels[2].reset(self.characters[0], self.characters[self.enemy], 800)
                return True
            else:
                return False

    def startFight(self, levels):
        if self.characters[1].isFight == True:
            levels[2].reset(self.characters[0], self.characters[self.enemy], 800)
            return True
        elif self.characters[2].isFight == True:
            levels[2].reset(self.characters[0], self.characters[self.enemy], 800)
            return True
        else:
            return False


    def update(self, screen):
        if self.dispProgress == True:
            self.drawProgBar(screen)
        if self.clicked == True:
            for char in self.characters[1:]:
                if char.speak == True:
                    char.interact(screen)

        if self.timer >= self.progTime:
            self.dispProgress = False
            text = str((self.timer - 400) // 200)
            text = self.smallFont.render(text, True, (200, 200, 200), (0,0,0))
            tb = text.get_rect()
            tb.center = (400, 40)
            screen.blit(text, tb)
            self.leave.draw(screen)
        else:
            self.dispProgress = True
        self.timer += 1


        #print(self.characters[2].isFight)

    def timeUp(self):
        if self.timer >= self.timeLim:
            return True
        else:
            return False



class Battle(Level):
    def __init__(self, bg, blocks, screen, characters=[]):
        super().__init__(bg, blocks, screen, characters)
        self.attacks = []
        self.enemy = []
        self.mc = []
        self.heroHealth = 6
        self.img = 0
        self.imgR = 0
        self.attacks = []
        self.pRad = 6
        # is 1 if the character is not dead yet
        self.state = 1
        self.gameover = False
        # counter to win game
        self.timeLim = 1000
        self.counter = 0
        self.attackTime = 100
        # stores position of next bloom for whitney
        self.nx = 0
        self.ny = 0
        # projectile speed
        self.ps = 1
        self.waitTime = 10
        # main character projectiles stuff
        self.mcProj = []
        # mc and enemy points for CURRENT battle
        self.mcPoints = 0
        self.enPoints = 0
        self.dTaken = False
        self.eDam = False


    def setup(self):
        mc = self.characters[0]
        mc.setPos(384, 388)
        self.gameover = False
        self.mcProj = [Attack(10)]
        self.save()

    def update(self, screen):
        x = pg.mouse.get_pos()[0]
        y = pg.mouse.get_pos()[1]

        winCond = self.battle()
        for i in self.attacks:
                i.drawBloom(screen)

        if self.hasAmmo() == True:
            self.mcProj[0].drawProj(self.characters[0].getX(), self.characters[0].getY(), self.characters[0].height, self.characters[0].width, x, y, screen)

        for i in self.mcProj[0].projectiles:
            i.moveOnRad()
            i.draw(screen)


    def checkLoss(self):
        if self.gameover == True:
            if self.state == 0:
                return 0
            else:
                return 1
        else:
            return 2

    def hasAmmo(self):
        if self.mc.getpk() >= 1:
            return True
        else:
            return False


    def reset(self, main, enemy, timer):
        self.setup()
        self.characters = [main, enemy]
        self.enemy = enemy
        self.mc = main
        self.heroHealth = self.characters[0].getHealth()
        self.timeLim = timer
        self.counter = 1
        self.attacks = []
        self.ps = 1
        self.attackTime = 100
        self.waitTime = 10
        self.mcPoints = 0
        self.enPoints = 0
        self.dTaken = False
        self.eDam = False

        # load whitney's little things
        if self.enemy.code == "w" or self.enemy.code == "r":
            self.img = pg.image.load('Images/wDam.png')
            self.pRad = 6
            self.attackTime = 100

    # click function that is useless for rn but will be able to shoot in future
    def click(self, screen):
        x = pg.mouse.get_pos()[0]
        y = pg.mouse.get_pos()[1]
        if self.hasAmmo() == True:
            self.mcProj[0].addMCProj(self.mc.getX(), self.mc.getY(), self.mc.height, self.mc.width, x, y)
            self.mc.chpk(-1)

    # ok so this will actually do the battle and it will look at the character's code to determine whihc battle to play
    def battle(self):
        # do whitneys battle
        if self.enemy.code == "w" or self.enemy.code == "r":

            if self.counter % self.timeLim == 0:
                self.gameover = True
                self.battleSum()

            if self.counter % self.attackTime == 0:
                self.nx = r.randint(222, 578)
                self.ny = r.randint(127, 704)
                self.enemy.setPos(self.nx, self.ny)
                
            if self.counter % (self.attackTime + 10) == 0:# make bloom around character
                self.attacks.append(Attack(self.pRad, 10, self.ps))
                self.attacks[-1].setBloom(30, self.nx + (self.enemy.width // 2), self.ny + (self.enemy.height // 2))
                self.ps += 1
                if self.attackTime > 40:
                    self.attackTime -= 10
                    self.waitTime += 5

            for attack in self.attacks:
                if attack.collideCharacter(self.mc.getX(), self.mc.getY(), self.mc.height, self.mc.width) == True:
                    self.mc.damage(1)
                    self.enPoints += 0
                    self.dTaken = True

            for attack in self.mcProj:
                if attack.collideCharacter(self.enemy.getX(), self.enemy.getY(), self.enemy.height, self.enemy.width) == True:
                    self.eDam = True
                    print("hit registered")
                    self.mcPoints += 3
        
        # returns 0 if character has lost all health
        # 
        if self.mc.getHealth() <= 0:
            self.mcPoints -= 10
            # 0 if dead
            self.state = 0
            self.gameover = True
            self.battleSum()
        else:
            # 1 if alive
            self.state = 1

        self.counter += 1

    def battleSum(self):
        if self.dTaken == False:
            self.mcPoints += 10
        if self.eDam == False:
            self.enPoints += 10
        self.mc.chScore(self.mcPoints)
        self.enemy.chScore(self.enPoints)


        


