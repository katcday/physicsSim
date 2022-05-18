import pygame as pg
import math
pg.init()

# so these will include the combat functions


# first we need a projectile class
# later I would like to add images or animations
class Projectile:
    def __init__(self, x, y, xs, ys, color=(200, 80, 60), r=10):
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys
        self.collided = False
        self.r = r
        self.color = color
        self.angle = 0
        # radius for main characters projectile
        self.rad = 0
        # intital center values
        self.centX = 0
        self.centY = 0

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def setX(self, x):
        self.x = x

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setXS(self, speed):
        self.xs = speed

    def setY(self, y):
        self.y = y

    def setYS(self, speed):
        self.ys = speed
    
    def swapXS(self):
        self.xs *= -1

    def swapYS(self):
        self.ys *= -1

    def move(self):
        self.x += xs
        self.y += ys

    def setmcProj(self, radius, angle, cX, cY):
        self.rad = radius
        self.angle = angle
        self.centX = cX
        self.centY = cY

    def moveOnRad(self):
        self.x = int(self.centX + self.rad * math.cos(self.angle))
        self.y = int(self.centY + self.rad * math.sin(self.angle))
        self.rad += 5


# so we want to have functions that make a group of 
# projectiles and control them prolly j have to make 
# a class

class Attack:
    def __init__(self, thingRad, s=0, ps=1):
        self.projectiles = []
        self.counter = 0
        self.pRad = thingRad
        self.bRad = 0
        self.bCenter = []
        self.bouncers = []
        self.lx = 0
        self.rx = 0
        self.uy = 0
        self.dy = 0
        # separation val
        self.s = s
        # projectile speed
        self.ps = ps

    # the first time it runs you will want to 
    # create the right amount of projectiles for the attack
    def setBloom(self, radius, x, y):
        # we need to find the circumference of the circle
        self.bRad = radius
        self.bCenter = [x, y]
        circ = 2 * math.pi * radius

        numThings = int(circ // (self.pRad + self.s))

        step = int(360 / numThings)

        nx = x + radius * math.cos((step * math.pi) / 180)
        ny = y + radius * math.sin((step * math.pi) / 180)

        nTheta = step * 2

        for i in range(numThings):
            self.projectiles.append(Projectile(nx, ny, 1, 1))
            nx = x + (radius * math.cos((nTheta * math.pi) / 180))
            ny = y + (radius * math.sin((nTheta * math.pi) / 180))
            nTheta += step

    def bloomMove(self):
        circ = 2 * math.pi * self.bRad

        step = int(360 / len(self.projectiles))

        nx = self.bCenter[0] + self.bRad * math.cos((step * math.pi) / 180)
        ny = self.bCenter[1] + self.bRad * math.sin((step * math.pi) / 180)

        nTheta = step * 2

        for i in self.projectiles:
            i.setX(self.bCenter[0] + (self.bRad * math.cos((nTheta * math.pi) / 180)))
            i.setY(self.bCenter[1] + (self.bRad * math.sin((nTheta * math.pi) / 180)))
            nTheta += step

    def setBounce(self, upperY, lowerY, leftX, rightX):
        self.uy = upperY
        self.ly = lowerY
        self.lx = leftX
        self.rx = rightX

    def addBounce(self, projectile):
        self.bouncers.append(projectile)

    def bounce(self):
        for i in projectiles:
            if i.getX() < self.ly or i.getX() > self.rx:
                i.swapXS()
            if i.getY() < self.uy or i.getY() > self.dy:
                i.swapYS()
            i.move()


    def drawBloom(self, screen):
        self.bRad += self.ps
        self.bloomMove()
        for i in self.projectiles:
            i.draw(screen)

    def collideCharacter(self, leftx, topy, h, w):
        leftx += 13
        topy += 30
        h -= 30
        w -= 13
        for i in self.projectiles:
            nX = i.getX() - max(leftx, min(i.getX(), leftx + w))
            nY = i.getY() - max(topy, min(i.getY(), topy + h))
            if (nX * nX + nY * nY) < (self.pRad * self.pRad) and i.collided == False:
                i.collided = True
                return True
        
        return False

    def addMCProj(self, leftx, topy, h, w, mx, my):
        r = w
        centX = leftx + (w // 2)
        centY = topy + (h // 2)

        angle = self.getMCAng(r, centX, centY, mx, my)

        nx = int(centX + r * math.cos(angle))
        ny = int(centY + r * math.sin(angle))

        self.projectiles.append(Projectile(nx, ny, 2, 2, (50, 100, 150), 10))
        self.projectiles[-1].setmcProj(r, angle, centX, centY)

    def drawProj(self, leftx, topy, h, w, mx, my, screen):
        r = w
        centX = leftx + (w // 2)
        centY = topy + (h // 2)

        angle = self.getMCAng(r, centX, centY, mx, my)

        nx = int(centX + r * math.cos(angle))
        ny = int(centY + r * math.sin(angle))

        pg.draw.circle(screen, (50, 100, 150), (nx,ny), 10)

    def getMCAng(self, r, centX, centY, mx, my):
        hyp = math.sqrt((centX - mx)**2 + (centY - my)**2)
        a = abs(centX - mx)
        angle = math.acos(a / hyp)

        if mx > centX and my > centY:
            return angle
        elif mx > centX and my < centY:
            return ((math.pi / 2) - angle + (3 * math.pi) / 2)
        elif mx < centX and my < centY:
            return angle + math.pi
        else:
            return math.pi - angle

    






