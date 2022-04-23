import pygame as pg
import pickle
from Block import *

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

bX = 0
bY = 0
for row in range(screen.get_height() // bSize):
    newRow = []
    bX = 0
    for column in range(screen.get_width() // bSize):
        newRow.append(Block(bSize, bX, bY, screen))
        bX += bSize
    bY += bSize
    blocks.append(newRow)


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

        if event.type == pg.MOUSEBUTTONDOWN:
            clicking = True
            click = pg.mouse.get_pos()
            x = (click[0] // bSize)
            y = (click[1] // bSize)
            clickTo = not blocks[y][x].getState()

        if event.type == pg.MOUSEBUTTONUP:
            clicking = False
    
    if clicking == True:
        click = pg.mouse.get_pos()
        x = (click[0] // bSize)
        y = (click[1] // bSize)
        blocks[y][x].newState(clickTo)

    for row in blocks:
        for block in row:
            block.draw()


    pg.display.update()
pickle.dump(blocks, open('test.pkl', 'wb'))
pg.quit()