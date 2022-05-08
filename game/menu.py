import pygame as pg
pg.init()

class MenuButton:
    def __init__(self, leftX, topY, width, height, color, text="", fontF='marion.ttf', tSize=80, tColor=(30,30,30)):
        self.x = leftX
        self.y = topY
        self.w = width
        self.h = height
        self.color = color
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.font = pg.font.SysFont(fontF, tSize)
        self.text = self.font.render(text, True, tColor, self.color)
        self.clicked = False

    def collision(self, mX, mY, clicked):
        if mX > self.x and mX < self.x + self.w and mY > self.y and mY < self.y + self.h:
            if clicked == True:
                self.clicked == True
            return True

    def setText(self, nT):
        self.text = nT

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        textBox = self.text.get_rect()
        textBox.center = (self.x + (self.w // 2), self.y + (self.h // 2))
        screen.blit(self.text, textBox)


class Menu:
    def __init__(self, color = (249, 222, 252), fontF='marion.ttf'):
        self.bgColor = color
        self.font = pg.font.SysFont(fontF, 80)
        self.buttonColor = (247, 239, 208)
        self.buttons = []
        self.close = False

    def setupStart(self):
        self.buttons.append(MenuButton(300, 500, 200, 100, self.buttonColor, "Start"))


    # draws the start menu
    def startMenu(self, screen):
        screen.fill((self.bgColor))
        text = self.font.render('Physics RPG', True, (30, 30, 30), self.bgColor)
 
        # create a rectangular object for the
        # text surface object
        textRect = text.get_rect()
        
        # set the center of the rectangular object.
        textRect.center = (800 // 2, 200 // 2)

        screen.blit(text, textRect)

        for i in self.buttons:
            pg.draw.rect(screen, self.buttonColor, [i.x, i.y, i.w, i.h])
            textRect = i.text.get_rect()
            new = textRect.clamp(i.rect)
            #textRect.center = (i.x + (i.w // 2), i.y + (i.h // 2))
            screen.blit(i.text, new)

        # im gonna make them change color when hovering later
        #for button in self.buttons:
            #if collision(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], False) == True:


    def click(self):
        for button in self.buttons:
            if button.collision(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], True) == True:
                if button == self.buttons[0]:
                    return True
        return False

# used to draw events to the screen 
class Cutscene:
    def __init__(self, leftX, topY, width, height, color=(0,0,0), text=[], fontF='marion.ttf'):
        self.text = text
        self.clicks = 0

        self.x = leftX
        self.y = topY
        self.w = width
        self.h = height
        self.color = color
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.font = pg.font.SysFont(fontF, 30)
        self.fontS = 30
        self.textInFont = []
        for i in self.text:
            self.textInFont.append(self.font.render(i, True, (30, 30, 30), self.color))

    def setupFailure(self):
        self.text = [["Dr. Whitbeck invites you into his office.","You sit down as he passes you your quiz.", "You stare in horror at the 15 scribbled in red",
        "\"It looks like you're going to have a lot of work to do if you want to pass.\"", "Dr. Whitbeck laughs maniacally at your stupidity.",
        "You know you have one option. You must become his favorite."]]
        for i in self.text:
            newSpeech = []
            for line in i:
                newSpeech.append(self.font.render(line, True, (200, 200, 200), self.color))
            self.textInFont.append(newSpeech)

    def failure(self, screen):
        screen.fill((self.color))

        pg.draw.rect(screen, self.color, self.rect)
        step = self.fontS
        nY = self.y + step
        nX = self.x // 2
        for i in self.textInFont[0]:

            textRect = i.get_rect()
            new = textRect.clamp(self.rect)
            #textRect.center = (i.x + (i.w // 2), i.y + (i.h // 2))
            screen.blit(i, (nX, nY))
            nY += step

        if self.clicks > 0:
            return True
        else:
            return False

    def click(self):
        self.clicks += 1
        





