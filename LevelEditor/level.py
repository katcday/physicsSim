import pygame as pg
import pickle
from Block import *

pg.init()

screen = pg.display.set_mode((800, 800))
# this is the size of blocks you are selecting
bSize = 4

running = True
clicking = False

# load in image
im = pg.image.load('Images/emptyClass.png')

# calc how many pixels to center it
imPixelsX = ((screen.get_width() // 32) / 2) * 32 - (((im.get_width() // 32) / 2)* 32)
imPixelsY = ((screen.get_height() // 32) / 2) * 32 - (((im.get_height() // 32) / 2)* 32)

# make objects for all blocks
blocks = []
clickTo = False

bX = 0
bY = 0
# maps the blocks in rows. It segments the image into blocks
# loo through every row in image
for row in range(screen.get_height() // bSize):
    newRow = []
    bX = 0
    # loop through every block in the row
    for column in range(screen.get_width() // bSize):
        newRow.append(Block(bSize, bX, bY))
        bX += bSize
    bY += bSize
    # add it to list
    blocks.append(newRow)


# main loop
while running:
    # fill background and draw image
    screen.fill((0,0,0))
    screen.blit(im, (imPixelsX,imPixelsY))

    # loop through events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # if the mouse is clicked than start drawing on blocks
        if event.type == pg.MOUSEBUTTONDOWN:
            clicking = True
            click = pg.mouse.get_pos()
            x = (click[0] // bSize)
            y = (click[1] // bSize)
            clickTo = not blocks[y][x].getState()

        # when mouse is up stop drawing
        if event.type == pg.MOUSEBUTTONUP:
            clicking = False
    
    # change state of the blocks
    if clicking == True:
        click = pg.mouse.get_pos()
        x = (click[0] // bSize)
        y = (click[1] // bSize)
        blocks[y][x].newState(clickTo)

    for row in blocks:
        for block in row:
            block.draw(screen)


    pg.display.update()

# save blocks to a pickle file
with open("emptyClassCollisions", "wb") as f:
    pickle.dump(blocks, f)
pg.quit()