import pygame as pg
from characterClass import *
from animate import *
import pickle

# first load in image
# then it will create a character object
# next it will load in all animation
# then you load in temp animations 
# it needs to set these equal to the characters walking animations
# as well as standing animations

pg.init()

characterTag = 'char1'
imageName = 'characters/char1/char1.png'

character = Character(imageName, 0, 0, 1)

# save character to a pickle file
pickle.dump(character, open(characterTag + '.pkl', 'wb'))