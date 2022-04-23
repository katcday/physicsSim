import pygame as pg
import pickle
from Block import *
from Character import *

pg.init()


screen = pg.display.set_mode((800, 800))
bSize = 8

running = True
clicking = False

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

infile = open('test.pkl','rb')
blocks = pickle.load(infile, encoding='latin1')

trial = Character(2, 400, 400, 20, 20, screen)


# main loop
while running:

    screen.blit(im, (imPixelsX,imPixelsY))
    
    start = 0
    for row in range(screen.get_height() // bSize):
        pg.draw.line(screen, (0,0,0), (0, start), (screen.get_width(), start))
        start += bSize

    start = 0
    for column in range(screen.get_width() // bSize):
        pg.draw.line(screen, (0,0,0), (start, 0), (start, screen.get_height()))
        start += bSize


    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


    for row in blocks:
        for block in row:
            block.draw()

    character.draw()


    pg.display.update()

pg.quit()