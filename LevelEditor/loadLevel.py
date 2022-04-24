import pygame as pg
import pickle
from Block import *
from Character import *

pg.init()

# game state variables
screen = pg.display.set_mode((800, 800))
bSize = 4

running = True
clicking = False

up = False
down = False
left = False
right = False

im = pg.image.load('Images/dorm.png')
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
blocks = []
clickTo = False

# load in pickle file
infile = open('test.pkl','rb')
blocks = pickle.load(infile, encoding='latin1')

# make a character
trial = Character(1, 400, 400, 20, 20)

# main loop
while running:
    # draw background and image
    screen.fill((0,0,0))
    screen.blit(im, (imPixelsX,imPixelsY))


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
            if event.key == pg.K_s:
                down = False
            if event.key == pg.K_a:
                left = False
            if event.key == pg.K_d:
                right = False
            
    # move, but if you collide, move back to where you were
    if up == True:
        trial.moveU()
        if trial.collide(blocks, bSize) == True:
            trial.moveD()
    if down == True:
        trial.moveD()
        if trial.collide(blocks, bSize) == True:
            trial.moveU()
    if left == True:
        trial.moveL()
        if trial.collide(blocks, bSize) == True:
            trial.moveR()
    if right == True:
        trial.moveR()
        if trial.collide(blocks, bSize) == True:
            trial.moveL()


    #for row in blocks:
        #for block in row:
            #block.draw(screen)

    # draw character
    trial.draw(screen)

    pg.display.update()

pg.quit()