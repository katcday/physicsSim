import pygame as pg

pg.init()

def get_image(sheet, x, y, width, height, color):
    # make an empty pygame surface
    image = pg.Surface((width, height))

    # take picture and blit onto new surface
    image.blit(sheet, (0, 0), (x, y, width, height))

    image.set_colorkey(color)

    return image


class Animation:
    def __init__(self):
        self.length = 0
        self.frames = []
        self.place = 0

    def addFrame(self, image):
        self.frames.append(image)
        self.length = len(self.frames)

    def getFrame(self):
        frame = self.frames[self.place]
        print(self.length)

        self.place += 1
        print(self.place)
        
        if self.place == self.length:
            self.place = 0

        return frame



class SpriteSheet:
    # width and height are of each sprite
    def __init__(self, sheet, width, height, rowNums=0):
        # sheet = sprite sheet png
        self.sheet = sheet
        self.width = width
        self.height = height
        self.animations = []
        # a list that contains the amount of frames in each subsequent row
        self.rowNums = rowNums
        self.tempAnimations = []

    def buildAnimation(self, numInRow, rowNum):
        self.animations.append(Animation())
        current = len(self.animations) - 1
        animation = self.animations[current]

        x = self.width
        y = self.height * rowNum

        for im in range(numInRow):
            animation.addFrame(get_image(self.sheet, x, y, self.width, self.height, (0,0,0)))
            x += self.width

    def loadSheet(self):
        for animation in range(len(self.rowNums)):
            self.buildAnimation(self.rowNums[animation], animation + 1)

    def draw(self, screen, animation):
        animation = self.animations[animation]
        
        screen.blit(animation.getFrame(), (0,0))

    # this will create a splice of a set amount of frames and store it to the temporary animation list
    def spliceFrames(self, animationInd, startInd, endInd):
        frames = self.animations[animationInd].frames[startInd:endInd]

        newAn = Animation()

        for frame in frames:
            newAn.addFrame(frame)

        self.tempAnimations.append(newAn)

    def drawTemp(self, screen, animationInd):
        animation = self.tempAnimations[animationInd]
        
        screen.blit(animation.getFrame(), (0,0))

    def returnTemp(self, animationInd):
        animation = self.tempAnimations[animationInd]
        return animation.getFrame()

            

