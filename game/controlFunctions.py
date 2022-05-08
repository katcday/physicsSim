import pygame as pg
from animate import *
from characterClass import *
import pickle
from Block import *
from combat import *
import random as r
from levelClass import *

def moveMC(up, down, left, right, lastDir, counter, screen, wait, char, blocks, bSize):
    # move, but if you collide, move back to where you were
    if up == True:
        char.move('U', 30, counter, screen, True, wait)
        if char.collide(blocks, bSize) == True:
            char.move('D', 30, counter, screen, True, wait)
    if down == True:
        char.move('D', 30, counter, screen, True, wait)
        if char.collide(blocks, bSize) == True:
            char.move('U', 30, counter, screen, True, wait)
    if left == True:
        char.move('L', 30, counter, screen, True, wait)
        if char.collide(blocks, bSize) == True:
            char.move('R', 30, counter, screen, True, wait)
    if right == True:
        char.move('R', 30, counter, screen, True, wait)
        if char.collide(blocks, bSize) == True:
            char.move('L', 30, counter, screen, True, wait)

    if up == False and down == False and left == False and right == False:
        if lastDir == "U":
            char.move('U', 30, counter, screen, False, wait)
        if lastDir == "D":
            char.move('D', 30, counter, screen, False, wait)
        if lastDir == "L":
            char.move('L', 30, counter, screen, False, wait)
        if lastDir == "R":
            char.move('R', 30, counter, screen, False, wait)