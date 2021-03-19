import random
from colorama import Fore,Back
import numpy as np
import config
from gameobject import GameObject
from ball import Ball
from canon import Canon
from config import FRAMEHEIGHT,FRAMEWIDTH,PADDLEMOVE,EXPANDSIZE,SHRINKSIZE,INCREASEBALLXSPEED,INCREASEBALLYSPEED,POWERUPTIME

class PowerUp(GameObject):
    def __init__(self, x, y, xlength, ylength,xvel,yvel,ptype):
        super().__init__(x, y, xlength, ylength,xvel,yvel)
        self._type=ptype
        self.isCollided=False
        self.isVel=False
        if self._type=='@':
            self.isVel=True
    def ballvel(self,vel):
        if(vel<0):
            return -1
        else:
            return 1
    def _checkCollision(self,paddleobj,ballobj,cannonobj):
        if(self._x+self._xvel>=paddleobj._x and 
        paddleobj._y<=self._y<paddleobj._y+paddleobj._ylength):
            self._x=paddleobj._x-1-self._xvel
            # print(self._type,self._x,self._y)
            if(self._type=="E"):
                paddleobj.powerups[self._type].append(POWERUPTIME)
                paddleobj._ylength+=EXPANDSIZE
            elif(self._type=="S"):
                paddleobj.powerups[self._type].append(POWERUPTIME)
                if(paddleobj._ylength!=3):
                    paddleobj._ylength-=SHRINKSIZE
            elif(self._type=="M"):
                newballs=[]
                for ball in ballobj:
                    nball=Ball(ball._x,ball._y,ball._xlength,ball._ylength,
                    -1*ball._xvel,-1*ball._yvel)
                    nball.isCollidedWithPaddle=False
                    newballs.append(nball)
                for i in newballs:
                    ballobj.append(i)
                paddleobj.powerups[self._type].append(-1)
            elif(self._type=="F"):
                paddleobj.powerups[self._type].append(POWERUPTIME)
                for ball in ballobj:
                    ball._xvel=ball._xvel+ self.ballvel(ball._xvel)*INCREASEBALLXSPEED
                    ball._yvel= ball._yvel+ self.ballvel(ball._yvel)*INCREASEBALLYSPEED
            elif(self._type=="T"):
                paddleobj.powerups[self._type].append(POWERUPTIME)
                for ball in ballobj:
                    ball.isThrough=True
            elif(self._type=="G"):
                paddleobj.powerups[self._type].append(POWERUPTIME)
            elif(self._type=="B"):
                paddleobj.powerups[self._type].append(40)
                cannonobj.append(Canon(paddleobj._x-1,paddleobj._y,1,1,0,0,0))
                cannonobj.append(Canon(paddleobj._x-1,paddleobj._y+paddleobj._ylength-1,1,1,0,0,1))
            elif(self._type=="@"):
                rIndex=[]
                for i in ballobj:
                    rIndex.append(i)
                for i in rIndex:
                    ballobj.remove(i)
            elif(self._type=="A"):
                paddleobj.powerups[self._type].append(POWERUPTIME)
                for ball in ballobj:
                    ball.isFire=True
                 
            self.isCollided=True 
        if(self._x + self._xvel >= config.FRAMEHEIGHT):
            self._x=0
            self.isCollided =True
        elif( self._x + self._xvel <= 0):
            self._x=  0 - self._xvel
            self._xvel= -1*self._xvel
        if(self._y + self._yvel >= config.FRAMEWIDTH ):
            self._y=config.FRAMEWIDTH - self._yvel -1 
            self._yvel= -1*self._yvel
        elif( self._y + self._yvel <= 0):
            self._y= 0 - self._yvel 
            self._yvel= -1*self._yvel
    def setVel(self,vel):
        self._xvel=vel[0]
        self._yvel=vel[1]
        self.isVel=True

    def colorBrick(self):
        obj=np.full([self._xlength,self._ylength],(Fore.WHITE+Back.BLACK))
        return obj

    def move(self,paddleobj,ballobj,cannonobj):
        self._checkCollision(paddleobj,ballobj,cannonobj)
        self._x+=self._xvel
        self._y+=self._yvel