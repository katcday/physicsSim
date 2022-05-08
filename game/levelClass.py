import pygame as pg

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

        
                

    def getBlocks(self):
        return self.collisionMap

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

    def setup(self):
        self.characters[0].setPos(418, 336)
        print("here")
        self.save()

    def update(self, screen):
        x = pg.mouse.get_pos()[0]
        y = pg.mouse.get_pos()[1]

class Classroom(Level):
    def __init__(self, bg, blocks, screen, characters=[]):
        super().__init__(bg, blocks, screen, characters)

    def setup(self):
        mc = self.characters[0]
        mc.setPos(265, 133)

        w = self.characters[1]
        w.setPos(354, 419)
        self.save()

    def click(self, screen):
        x = pg.mouse.get_pos()[0]
        y = pg.mouse.get_pos()[1]

        if self.clicked == True:
            self.clicked = False
            for char in self.characters[1:]:
                self.speak = False
        else:
            for char in self.characters[1:]:
                if x > char.getX() and x < char.getX() + 32 and y > char.getY() and y < char.getY() + 64:
                    self.clicked = True
                    char.speak = True
                    char.nextSpeech()


    def update(self, screen):
        if self.clicked == True:
            for char in self.characters[1:]:
                if char.speak == True:
                    char.interact(screen)


class Battle(Level):
    def __init__(self, bg, blocks, screen, characters=[]):
        super().__init__(bg, blocks, screen, characters)
        self.attacks = []

    def setup(self):
        mc = self.characters[0]
        mc.setPos(384, 388)
        self.save()

    def update(self, screen):
        x = pg.mouse.get_pos()[0]
        y = pg.mouse.get_pos()[1]
