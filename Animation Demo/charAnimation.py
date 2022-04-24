from sprite import *
import pygame as pg 
from animate import *

pg.init()

bgColor = pg.Color(30, 30, 30)

screen = pg.display.set_mode((800, 800))

counter = 0

running = True
char1Sheet = pg.image.load('characters/char1/firdy.png').convert_alpha()
char1Sheet = SpriteSheet(char1Sheet, 32, 64, [4, 24, 24, 6, 12, 12, 12, 12])
char1Sheet.loadSheet()

# make first frame
#frame0 = get_image(char1Sheet, 32, 64, (0,0,0))

while running == True:
    screen.fill(bgColor)

    if counter % 2 == 0:
        char1Sheet.draw(screen, 3)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.update()
    counter += 1

pg.quit()

    

    
