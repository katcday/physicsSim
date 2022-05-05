import pygame as pg
from animate import *
from characterClass import *
import os
import pickle
from Block import *
from combat import *
import random as r

pg.init()

# change demoFile to load it
lvlName = 'miniGameDemo'

characters = []

# loop through all info files to load in level information
for files in os.listdir('levels/' + lvlName + '/Map'):
    if files.endswith('png'):
        fileName = 'levels/' + lvlName + '/Map/' + files
        background = fileName

# loads collision map
for files in os.listdir('levels/' + lvlName + '/CollisionMap'):
    fileName = 'levels/' + lvlName +'/CollisionMap/' + files
    blocks = fileName


# loads characters
for files in os.listdir('levels/' + lvlName + '/Characters/main/'):
    #infile = open(files,'rb')
    #characters.append(pickle.load(infile, encoding='latin1'))
    if files.endswith('png'):
        fileName = 'levels/' + lvlName +'/Characters/main/' + files

        characters.append(Character(fileName, 400, 400, 4))

# loads characters
for files in os.listdir('levels/' + lvlName + '/Characters/whitney/'):
    #infile = open(files,'rb')
    #characters.append(pickle.load(infile, encoding='latin1'))
    if files.endswith('png'):
        fileName = 'levels/' + lvlName +'/Characters/whitney/' + files

        characters.append(Character(fileName, 250, 300, 4))



# load in pickle file
infile = open(blocks,'rb')
blocks = pickle.load(infile, encoding='latin1')

# game state variables
screen = pg.display.set_mode((800, 800))
bSize = 4

running = True
clicking = False

up = False
down = False
left = False
right = False

im = pg.image.load(background)
# get images height 
imHeight = im.get_height()
imWidth = im.get_width()

# chunks of 32 pixels
imChunksW = (imWidth // 32) / 2
imChunksH = (imHeight // 32) / 2

# calc how many pixels to center it
imPixelsX = ((screen.get_width() // 32) / 2) * 32 - (imChunksW * 32)
imPixelsY = ((screen.get_height() // 32) / 2) * 32 - (imChunksH * 32)

# make objects for all blocks
clickTo = False
counter = 1
lastDir = "D"
moving = False

FPS = 30
fpsClock = pg.time.Clock()
wait = 4

# battle class
trial = Attack(15)
trial.setBloom(50, 400, 400)

attacks = []

collided = False
drawChar = True

characters[1].setPos(250, 300)

# main loop
while running:
    # draw background and image
    screen.fill((0,0,0))
    screen.blit(im, (imPixelsX,imPixelsY))

    #dcharacters[0].draw()


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
            
    # move, but if you collide, move back to where you were
    if up == True:
        characters[0].move('U', 30, counter, screen, True, wait)
        if characters[0].collide(blocks, bSize) == True:
            characters[0].move('D', 30, counter, screen, True, wait)
    if down == True:
        characters[0].move('D', 30, counter, screen, True, wait)
        if characters[0].collide(blocks, bSize) == True:
            characters[0].move('U', 30, counter, screen, True, wait)
    if left == True:
        characters[0].move('L', 30, counter, screen, True, wait)
        if characters[0].collide(blocks, bSize) == True:
            characters[0].move('R', 30, counter, screen, True, wait)
    if right == True:
        characters[0].move('R', 30, counter, screen, True, wait)
        if characters[0].collide(blocks, bSize) == True:
            characters[0].move('L', 30, counter, screen, True, wait)

    if up == False and down == False and left == False and right == False:
        if lastDir == "U":
            characters[0].move('U', 30, counter, screen, False, wait)
        if lastDir == "D":
            characters[0].move('D', 30, counter, screen, False, wait)
        if lastDir == "L":
            characters[0].move('L', 30, counter, screen, False, wait)
        if lastDir == "R":
            characters[0].move('R', 30, counter, screen, False, wait)

    if counter % 50 == 0:
        attacks.append(Attack(15))
        attacks[-1].setBloom(30, r.randint(222, 578), r.randint(127, 704))

    for i in attacks:
        i.drawBloom(screen)
        collided = i.collideCharacter(characters[0].getX(), characters[0].getY(), 64, 32)
        if collided == True:
            drawChar = False


    counter += 1
    if drawChar == True:
        characters[0].draw(screen)

    characters[1].move('D', 30, counter, screen, False, wait)
    characters[1].draw(screen)

    pg.display.update()
    fpsClock.tick(FPS)

    #print(str(pg.mouse.get_pos()[0]) + " " + str(pg.mouse.get_pos()[1])) 

    pg.display.update()

pg.quit()