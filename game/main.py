import pygame as pg
from animate import *
from characterClass import *
import pickle
from Block import *
from combat import *
import random as r
from levelClass import *
from controlFunctions import *
from menu import *

pg.init()
pg.font.init()
screen = pg.display.set_mode((800, 800))

# first we need to build all of our levels
# so we are going to create a list that holds three different level objects to begin with
levels = []

# then we need to load in the background images and collision maps
# tbh im just gonna set the path manually bc it is so much more annoying to loop through

# we also need to build our characters first
characters = []
# load in main character image
char1 = 'game/characters/main/char1.png'
characters.append(Character(char1, 400, 400, 5))

char2 = 'game/characters/whitney/char2.png'
characters.append(Whitney(char2, 250, 500, 3))

char3 = 'game/characters/raja/char3.png'
characters.append(Raja(char3, 350, 500, 3))

char4 = 'game/characters/wb/char4.png'
characters.append(Whitbeck(char4, 350, 500, 3))

# lets make the dorm
bg = pg.image.load('game/dorm/bg/dorm.png')
collMap = 'game/dorm/collisionMap/dormCollisions.pkl'
infile = open(collMap,'rb')
blocks = pickle.load(infile, encoding='latin1')
levels.append(Dorm(bg, blocks, screen, [characters[0]]))
# close our sweet sweet pickle file
infile.close()

# now the classroom!!
bg = pg.image.load('game/classroom/bg/physicsRoom.png')
collMap = 'game/classroom/collisionMap/classCollisions'
infile = open(collMap,'rb')
blocks = pickle.load(infile, encoding='latin1')
levels.append(Classroom(bg, blocks, screen, characters[0:]))
# close our sweet sweet pickle file
infile.close()

# finally the battle ground
bg = pg.image.load('game/battle/bg/emptyClass.png')
collMap = 'game/battle/collisionMap/emptyClassCollisions'
infile = open(collMap,'rb')
blocks = pickle.load(infile, encoding='latin1')
levels.append(Battle(bg, blocks, screen, characters[0:]))
# close our sweet sweet pickle file
infile.close()

for level in levels:
    level.setup()

# setup menus and cutscenese
menu = Menu()
menu.setupStart()

failure = Cutscene(50, 50, 700, 700)
failure.setupFailure()


# now that our files are loaded we will setup some game variables that many functions and classes use
running = True

# so each game level will have a main function that gets called when it's being used
# right now we are going to use keybinds to switch between the levels 123 will correspond to indexes 012
dorm = False
classroom = True
battle = False

# keeps track of the index of the current level
currentLev = 1

# direction variables for main character
up = False
down = False
left = False
right = False
lastDir = 'D'
counter = 0
wait = 4
bSize = 4

#print(pg.font.get_fonts())

# variable is False at beginning and plays menu when menu is exited it plays game
playGame = False
startFail = False
startMenu = True

# setup all levels before game starts
for level in levels:
    level.setup()

# fps stuff
FPS = 30
fpsClock = pg.time.Clock()

levels[currentLev].open()

# game loop
while running:
    if playGame == True:
        if dorm == True:
            levels[0].draw(screen, counter, wait)
            moveMC(up, down, left, right, lastDir, counter, screen, wait, characters[0], levels[0].getBlocks(), bSize)
        elif classroom == True:
            levels[1].draw(screen, counter, wait)
            moveMC(up, down, left, right, lastDir, counter, screen, wait, characters[0], levels[1].getBlocks(), bSize)
        elif battle == True:
            levels[2].draw(screen, counter, wait)
            moveMC(up, down, left, right, lastDir, counter, screen, wait, characters[0], levels[2].getBlocks(), bSize)


        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            # if the key is pressed start moving in that direction
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    up = True
                if event.key == pg.K_s:
                    down = True
                if event.key == pg.K_a:
                    left = True
                if event.key == pg.K_d:
                    right = True
                if event.key == pg.K_1:
                    dorm = True
                    levels[currentLev].save()
                    levels[0].open()
                    classroom = False
                    battle = False
                    currentLev = 0
                if event.key == pg.K_2:
                    dorm = False
                    classroom = True
                    battle = False
                    levels[currentLev].save()
                    levels[1].open()
                    currentLev = 1
                if event.key == pg.K_3:
                    dorm = False
                    classroom = False
                    battle = True
                    levels[currentLev].save()
                    levels[2].open()
                    currentLev = 2

            # stop moving when key is released
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    up = False
                    lastDir = "U"
                if event.key == pg.K_s:
                    down = False
                    lastDir = "D"
                if event.key == pg.K_a:
                    left = False
                    lastDir = "L"
                if event.key == pg.K_d:
                    right = False
                    lastDir = "R"

            if event.type == pg.MOUSEBUTTONDOWN:
                levels[currentLev].click(screen)

        levels[currentLev].update(screen)
        if currentLev == 1:
            checkFight = levels[currentLev].startFight(levels)
            if checkFight == True:
                classroom = False
                battle = True
                currentLev = 2
                # make sure to run setup level when there's a change so characters appear in correct place
                levels[currentLev].setup()
            elif levels[currentLev].timeUp() == True:
                classroom = False
                dorm = True
                currentLev = 0
                levels[currentLev].setup()

        elif currentLev == 2:
            gameState = levels[currentLev].checkLoss()
            if gameState == 0:
                currentLev = 0
                battle = False
                dorm = True
                levels[currentLev].setup()
            if gameState == 1:
                currentLev = 1
                battle = False
                classroom = True
                levels[currentLev].setup()

        elif currentLev == 0:
            gameState = levels[currentLev].isSleep()
            if gameState == 1:
                currentLev = 1
                levels[currentLev].setup()
                dorm = False
                classroom = True

    # start menu
    elif startMenu == True:
        # show menu
        menu.startMenu(screen, characters)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
            if event.type == pg.MOUSEBUTTONDOWN:
                startFail = menu.click()
                if startFail == True:
                    startMenu = False
                    levels[currentLev].setup()

    # rhis is just the stuff for the start of the game
    elif startFail == True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
            if event.type == pg.MOUSEBUTTONDOWN:
                failure.click()
            
        # runs the first cutscene where you fail the quiz
        playGame = failure.failure(screen, characters, counter)
        if playGame == True:
            startFail = False
            levels[1].setup()


    print(pg.mouse.get_pos())


    pg.display.update()
    fpsClock.tick(FPS)
    counter += 1

pg.quit()