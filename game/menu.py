import pygame as pg
pg.init()
pg.font.init()

class MenuButton:
    def __init__(self, leftX, topY, width, height, color, text="", fontF='game/Fonts/Pixel.ttf', tSize=80, tColor=(30,30,30)):
        self.x = leftX
        self.y = topY
        self.w = width
        self.h = height
        self.color = color
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.font = pg.font.Font(fontF, tSize)
        self.text = self.font.render(text, True, tColor, self.color)
        self.clicked = False

    def collision(self, mX, mY, clicked):

        if mX > self.x and mX < self.x + self.w and mY > self.y and mY < self.y + self.h:
            if clicked == True:
                self.setClick(True)
            return True
        return False

    def setText(self, nT):
        self.text = nT

    def setClick(self, state):
        self.clicked = state

    def draw(self, screen):
        # draw background rect
        pg.draw.rect(screen, self.color, self.rect)
        # get rect for textbox
        textBox = self.text.get_rect()
        # center text
        textBox.center = (self.x + (self.w // 2), self.y + (self.h // 2))
        # blit text
        screen.blit(self.text, textBox)



class Menu:
    def __init__(self, color = (249, 222, 252), fontF='game/Fonts/Pixel.ttf'):
        self.bgColor = color
        self.font = pg.font.Font(fontF, 80)
        self.buttonColor = (247, 239, 208)
        self.buttons = []
        self.close = False
        self.timer = 1
        self.rules = False

    def setupStart(self):
        self.buttons.append(MenuButton(300, 500, 200, 50, self.buttonColor, "Start", tSize = 35))
        self.buttons.append(MenuButton(300, 565, 200, 50, self.buttonColor, "Rules", tSize = 35))


    # draws the start menu
    def startMenu(self, screen, characters):
        if self.rules == False:
            screen.fill((self.bgColor))
            text = self.font.render('Physics RPG', True, (30, 30, 30), self.bgColor)
    
            # create a rectangular object for the
            # text surface object
            textRect = text.get_rect()
            
            # set the center of the rectangular object.
            textRect.center = (800 // 2, 250)

            screen.blit(text, textRect)

            for i in self.buttons:
                pg.draw.rect(screen, self.buttonColor, [i.x, i.y, i.w, i.h])
                textRect = i.text.get_rect()
                textRect.center = (i.x + (i.w // 2), i.y + (i.h // 2))
                screen.blit(i.text, textRect)

            # im gonna make them change color when hovering later
            #for button in self.buttons:
                #if collision(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], False) == True:
            x = 200 - 16
            step = 200
            y = 350
            for char in characters[0:3]:
                char.setPos(x, y)
                char.move('D', 30, self.timer, screen, False, 5)
                char.draw(screen)
                x += step
        else:
            self.showRules(screen)

        

        self.timer += 1


    def click(self):
        if self.rules == False:
            for button in self.buttons:
                if button.collision(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], True) == True:
                    if button == self.buttons[0]:
                        return True
                    elif button == self.buttons[1]:
                        self.rules = True
            return False
        else: 
            self.rules = False
            return False

    def showRules(self, screen):
        font = pg.font.Font('game/Fonts/Pixel.ttf', 20)
        screen.fill((90, 127, 250))
        words = ["You are a physics student trying to get Dr. Whitbeck", "to give you an A. You must defeat the other students in", "battle to increase your reputation and lower theirs.", 
        "To win battles you may expend physics knowledge", "to do damage on your opponent. If the opponent's attack hits", "you, your mental health will be lowered.", "When your reputation is higher than the other players,", "you will be Dr. Whitbeck's favorite.",
        "", "", "Use WASD keys to move your character.", "Use the mouse/trackpad to interact with objects and characters.","", "", "Click to continue..."]

        iniY = 200
        step = 30
        for line in words:
                text = font.render(line, True, (250, 250, 250), (90, 127, 250))
                tb = text.get_rect()
                tb.center = (400, iniY)
                screen.blit(text, tb)
                iniY += step

# used to draw events to the screen 
class Cutscene:
    def __init__(self, leftX, topY, width, height, color=(0,0,0), text=[], fontF='game/Fonts/Pixel.ttf'):
        self.text = text
        self.clicks = 0

        self.x = leftX
        self.y = topY
        self.w = width
        self.h = height
        self.color = color
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.font = pg.font.Font(fontF, 15)
        self.fontS = 25
        self.textInFont = []
        self.time = 1
        for i in self.text:
            self.textInFont.append(self.font.render(i, True, (30, 30, 30), self.color))
        
    def setTime(self):
        self.time += 1

    def setupFailure(self):
        self.text = [["Dr. Whitbeck invites you into his office.","You sit down as he passes you your quiz.", "You stare in horror at the 15 scribbled in red",
        "\"It looks like you're going to have a lot of work to do if you want to pass.\"", "Dr. Whitbeck laughs maniacally at your stupidity.",
        "You know you have one option. You must become his favorite."]]
        for i in self.text:
            newSpeech = []
            for line in i:
                newSpeech.append(self.font.render(line, True, (200, 200, 200), self.color))
            self.textInFont.append(newSpeech)


    def failure(self, screen, characters, counter):
        screen.fill((self.color))

        pg.draw.rect(screen, self.color, self.rect)
        step = self.fontS + 10
        nY = self.y + step
        nX = self.x // 2
        for i in self.textInFont[0]:

            textRect = i.get_rect()
            new = textRect.clamp(self.rect)
            #textRect.center = (i.x + (i.w // 2), i.y + (i.h // 2))
            screen.blit(i, (nX, nY))
            nY += step

        words = "Click to continue..."
        words = self.font.render(words, True, (200, 200, 200), self.color)
        tb = words.get_rect()
        tb.center = (400, 500)
        screen.blit(words, tb)


        characters[0].setPos(560, 300)
        characters[0].move('D', 30, counter, screen, False, 5)
        characters[0].draw(screen)

        characters[3].setPos(600, 300)
        characters[3].move('D', 30, counter, screen, False, 5)
        characters[3].draw(screen)


        if self.clicks > 0:
            return True
        else:
            return False

        self.setTime()

    def click(self):
        self.clicks += 1


class Objects:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.clicked = False
        self.buttons = []

    def collide(self, mx, my):
        if mx > self.x1 and mx < self.x2 and my > self.y1 and my < self.y2:
            return True
            print(True)
        else: 
            return False

    def cClick(self, state):
        self.clicked = state

    def collideB(self, mx, my):
        for button in self.buttons:
            if button.collision(mx, my, True) == True:
                #print(button.x)
                return True
        return False

    def findB(self):
        counter = 0
        for button in self.buttons:
            if button.clicked == True:
                button.setClick(False)
                return counter
            counter += 1
        return -1


class Bed(Objects):
    def __init__(self, x1, x2, y1, y2):
        super().__init__(x1, x2, y1, y2)
        self.disText = "Do you want to go to sleep?"
        self.buttons = [MenuButton(100, 650, 300, 50, (50, 50, 50), text="yes", tColor=(200, 200, 200), tSize = 25), MenuButton(400, 650, 300, 50, (50, 50, 50), text="no", tColor=(200, 200, 200), tSize = 25)]
        self.font = pg.font.Font("game/Fonts/Pixel.ttf", 30)

    def display(self, screen):
        pg.draw.rect(screen, (50, 50, 50), [100, 600, 600, 50])
        text = self.font.render(self.disText, True, (200, 200, 200), (50, 50, 50))
        textRect = text.get_rect()
        textRect.center = (400, 625)
        screen.blit(text, textRect)

        for button in self.buttons:
            button.draw(screen)

    def button1(self):
        return True

    def button2(self):
        return False

class Books(Objects):
    def __init__(self, x1=442, x2=478, y1=416, y2=443):
        super().__init__(x1, x2, y1, y2)
        self.disText = "Do you want to go to study?"
        self.buttons = [MenuButton(100, 650, 300, 50, (50, 50, 50), text="yes", tColor=(200, 200, 200), tSize = 25), MenuButton(400, 650, 300, 50, (50, 50, 50), text="no", tColor=(200, 200, 200), tSize = 25)]
        self.font = pg.font.Font("game/Fonts/Pixel.ttf", 30)

    def display(self, screen):
        pg.draw.rect(screen, (50, 50, 50), [100, 600, 600, 50])
        text = self.font.render(self.disText, True, (200, 200, 200), (50, 50, 50))
        textRect = text.get_rect()
        textRect.center = (400, 625)
        screen.blit(text, textRect)

        for button in self.buttons:
            button.draw(screen)

    def button1(self):
        return True

    def button2(self):
        return False

class Computer(Objects):
    def __init__(self, x1=518, x2=576, y1=482, y2=511):
        super().__init__(x1, x2, y1, y2)
        self.disText = "What do you want to do on the computer?"
        self.buttons = [MenuButton(100, 650, 300, 50, (50, 50, 50), text="Chegg it.", tColor=(200, 200, 200), tSize = 25), MenuButton(400, 650, 300, 50, (50, 50, 50), text="Video Games", tColor=(200, 200, 200), tSize = 25),
            MenuButton(100, 700, 600, 50, (50, 50, 50), text="Homework", tColor=(200, 200, 200), tSize = 25)]
        self.font = pg.font.Font("game/Fonts/Pixel.ttf", 30)
        self.font = pg.font.Font("game/Fonts/Pixel.ttf", 30)

    def display(self, screen):
        pg.draw.rect(screen, (50, 50, 50), [100, 600, 600, 50])
        text = self.font.render(self.disText, True, (200, 200, 200), (50, 50, 50))
        textRect = text.get_rect()
        textRect.center = (400, 625)
        screen.blit(text, textRect)

        for button in self.buttons:
            button.draw(screen)

    def button1(self):
        return True

    def button2(self):
        return False




        





