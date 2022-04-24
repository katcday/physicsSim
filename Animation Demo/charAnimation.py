from sprite import *
import pygame as pg 
from animate import *

pg.init()

FPS = 20
fpsClock = pg.time.Clock()

bgColor = pg.Color(30, 30, 30)

screen = pg.display.set_mode((800, 800))

counter = 0

running = True
char1Sheet = pg.image.load('characters/char1/firdy.png').convert_alpha()
char1Sheet = SpriteSheet(char1Sheet, 32, 64, [4, 24, 24, 6, 12, 12, 12, 12])
char1Sheet.loadSheet()

# make walking animation for 1 direction
char1Sheet.spliceFrames(1, 0, 5)

# make first frame
#frame0 = get_image(char1Sheet, 32, 64, (0,0,0))

while running == True:
    screen.fill(bgColor)

    char1Sheet.drawTemp(screen, 0)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.update()
    fpsClock.tick(FPS)

pg.quit()

    

    
