import random
from colorama import Fore
import numpy as np
import config
from gameobject import GameObject
import os
class Ball(GameObject):
    def __init__(self, x, y, xlength, ylength,xvel,yvel):
        super().__init__(x, y, xlength, ylength,xvel,yvel)
        self._type="BALL"
        self.isThrough=False
        self.isFire=False
        self.isCollidedWithPaddle=True
    def _checkCollision(self,paddleobj):
        flag=0
        if(self._x + self._xvel >= paddleobj._x):
            flag=1
            val=int(((self._yvel)*(paddleobj._x -1 -self._x))/self._xvel)
            #print(val)
            if(self._y+val >= paddleobj._y and self._y+val < paddleobj._y + paddleobj._ylength):
                self._yvel+= self._y+val-paddleobj._y - int(paddleobj._ylength/2)
                self._xvel = -1*self._xvel
                self._y+= val - self._yvel
                self._x= paddleobj._x -1 -self._xvel
                for i in paddleobj.powerups.keys():
                    if(len(paddleobj.powerups[i])!=0):
                        self.isCollidedWithPaddle=True
                        break
                
        if(self._x + self._xvel >= config.FRAMEHEIGHT ):
            self._x= config.FRAMEHEIGHT - self._xvel-1
            self._xvel= 0
            self._yvel= 0
        elif( self._x + self._xvel <= 0):
            flag=1
            if self._type=="BULLET":
                self.isCollided=True
            self._x=  0 - self._xvel
            self._xvel= -1*self._xvel
        if(self._y + self._yvel >= config.FRAMEWIDTH ):
            flag=1
            self._y=config.FRAMEWIDTH - self._yvel -1 
            self._yvel= -1*self._yvel
        elif( self._y + self._yvel <= 0):
            flag=1
            self._y= 0 - self._yvel 
            self._yvel= -1*self._yvel
        # if flag==1:
        #     os.system('aplay -q ./sounds/break.wav&')
    
    def findy(self,x):
        return int(((self._yvel/self._xvel)*(x-self._x))+self._y)
    def findx(self,y):
        return int(((self._xvel/self._yvel)*(y-self._y))+self._x)
    def checkInBrick(self,brickobj,pointtup,check):
        flag =False
        br=brickobj[0]
        for i in brickobj:
            if(check=='x'):
                if(i._x == pointtup[0]):
                    if(i._y<=pointtup[1]<i._y+i._ylength):
                        flag = True
                        br=i
                        break
            elif(check=='y'):
                if(i._y == pointtup[1]):
                    if(i._x<=pointtup[0]<i._x+i._xlength):
                        flag = True
                        br=i
                        break
            elif(check=='xi'):
                if(i._x+i._xlength-1 == pointtup[0]):
                    if(i._y<=pointtup[1]<i._y+i._ylength):
                        flag = True
                        br=i
                        break
            elif(check=='yi'):
                if(i._y + i._ylength-1 == pointtup[1]):
                    if(i._x<=pointtup[0]<i._x+i._xlength):
                        flag = True
                        br=i
                        break
            elif(check=='all'):
                if(i._x<=pointtup[0]<i._x+i._xlength and i._y<=pointtup[1]<i._y+i._ylength ):
                    flag = True
                    br=i
                    break
        if(flag==False):
            return False
        else:
            return br
    def distance(self,tup1,tup2):
        return (tup1[0]-tup2[0])**2 + (tup1[1]-tup2[1])**2
    def nearerBrick(self,points):
        min=100000
        brick=points[0]
        for i in points:
            dis=self.distance((self._x,self._y),i[0])
            if(min > dis):
                brick=i
                min=dis
        return brick
    


    def contactPoint(self,nb,brickobj):
        if ((nb[0][0]==nb[1]._x and nb[0][1]==nb[1]._y)
            or (nb[0][0]==nb[1]._x and nb[0][1]==nb[1]._y+nb[1]._ylength-1)
            or (nb[0][0]==nb[1]._x+nb[1]._xlength-1 and nb[0][1]==nb[1]._y)
            or (nb[0][0]==nb[1]._x+nb[1]._xlength-1 and nb[0][1]==nb[1]._y+nb[1]._ylength-1) ):
            return "reverse"
        elif(nb[0][0]==nb[1]._x):
            return "up"
        elif(nb[0][0]==nb[1]._x+nb[1]._xlength-1):
            return "down"
        elif(nb[0][1]==nb[1]._y):
            return "left"
        elif(nb[0][1]==nb[1]._y+nb[1]._ylength-1):
            return "right"
    def velFactor(self,nb,point):
        xf=1
        yf=1
        if(self._xvel*(point[0]-nb[0][0])<0):
            xf=-1
        elif(self._xvel*(point[0]-nb[0][0])>0):
            xf=0
        if(self._yvel*(point[1]-nb[0][1])<0):
            yf=-1
        elif(self._yvel*(point[1]-nb[0][1])>0):
            yf=0
        return xf,yf
    def checkPoints(self,tups,brickobj,nb):
        outpoints=[]
        
        for point in tups:
            flag=0
            for i in brickobj:
                if (i._x<=point[0]<i._x+i._xlength  and i._y<=point[1]<i._y+i._ylength):
                    flag=1
                    break
            if(flag==0):
                xf,yf=self.velFactor(nb,point)
                if not(xf==0 or yf==0):
                    newtypepoint=(point,(xf,yf))
                    outpoints.append(newtypepoint)
        if(len(outpoints)==0):
            diff=(nb[0][0]-nb[1]._x, nb[0][1]-nb[1]._y)
            xc=0
            yc=0
            if(diff[0]==0 and diff[1]==0):
                xc=nb[0][0]-1
                yc= nb[0][1]-1
            elif(diff[0]==nb[1]._xlength-1 and diff[1]==0):
                xc = nb[0][0]+1
                yc = nb[0][1]-1
            elif(diff[0]==0 and diff[1]==nb[1]._ylength-1):
                xc = nb[0][0]-1
                yc = nb[0][1]+1
            elif(diff[0]==nb[1]._xlength-1 and diff[1]==nb[1]._ylength-1):
                xc = nb[0][0]+1
                yc = nb[0][1]+1
            return False, (xc,yc)
        return True,outpoints 

    def getNeighbourBricks(self,nb,brickobj,nbricks):
        for i in brickobj:
            if(
            (i._x==nb._x+3 and i._y==nb._y-8) or
            (i._x==nb._x+3 and i._y==nb._y) or
            (i._x==nb._x+3 and i._y==nb._y+8) or
            (i._x==nb._x and i._y==nb._y-8) or
            (i._x==nb._x and i._y==nb._y+8) or
            (i._x==nb._x-3 and i._y==nb._y-8) or
            (i._x==nb._x-3 and i._y==nb._y) or
            (i._x==nb._x-3 and i._y==nb._y+8)
            ):
                if (i.isVisited==False):
                    nbricks.append(i)
                    i.isVisited=True
                    if(i.strength==6):
                        self.getNeighbourBricks(i,brickobj,nbricks)
                    
                
    def _checkCollisionWithBrick(self,brickobj,paddleobj):
        x2=self._x+self._xvel
        y2=self._y+self._yvel
        # str1=f"3 {self._x},{self._y}\n"
        # os.write(1, str.encode(str1))
        points=[]
        for i in brickobj:
            if((x2>self._x and (self._x<=i._x<=x2) 
            or ((x2<self._x and (self._x>=i._x>=x2))))):
                pointtup=(i._x,self.findy(i._x),i)
                br=self.checkInBrick(brickobj,pointtup,'x')
                if (br!=False):
                    # print('inx')
                    points.append((pointtup,br))
            if((x2>self._x and (self._x<=i._x+i._xlength-1<=x2) 
            or ((x2<self._x and (self._x>=i._x+i._xlength-1>=x2))))):        
                pointtup=(i._x+i._xlength-1,self.findy(i._x+i._xlength-1),i)
                br=self.checkInBrick(brickobj,pointtup,'xi')
                if (br!=False):
                    # print('inx')
                    points.append((pointtup,br))
            if((y2>self._y and (self._y<=i._y<=y2) 
            or ((y2<self._y and (self._y>=i._y>=y2))))):
                pointtup=(self.findx(i._y),i._y,i)
                br=self.checkInBrick(brickobj,pointtup,'y')
                if (br!=False):
                    # str2=f"5 {y2} {self._y}\n"
                    # os.write(1, str.encode(str2))
                    points.append((pointtup,br))
            if((y2>self._y and (self._y<=i._y+i._ylength-1<=y2) 
            or ((y2<self._y and (self._y>=i._y+i._ylength-1>=y2))))):        
                pointtup=(self.findx(i._y+i._ylength-1),i._y+i._ylength-1,i)
                # str2=f"5 {y2} {self._y}\n"
                # os.write(1, str.encode(str2))
                br=self.checkInBrick(brickobj,pointtup,'yi')
                if (br!=False):
                    
                    points.append((pointtup,br))
        if (len(points)!=0):
            nb=self.nearerBrick(points)
            where=self.contactPoint(nb,brickobj)
            # str2=f"{nb[1]._x},{nb[1]._y}\n"
            # str3=f"{nb[0][0]},{nb[0][1]}\n"
            # os.write(1, str.encode(str2))
            # os.write(1, str.encode(str3))
            if self._type=="BULLET":
                self.isCollided=True
                nb[1].collideValues.append(-1)
                nb[1].collideValues.append(0)
            else:
                nb[1].collideValues.append(self._xvel)
                nb[1].collideValues.append(self._yvel)
            if nb[1]._type=="BOSS":
                nb[1]._yvel=-1*nb[1]._yvel
                nb[1]._y+=nb[1]._yvel*3
            
            if(where=='up'):
                if not(self.isThrough): self._xvel=-1*self._xvel
                self._x=nb[0][0]-1-self._xvel
                self._y=int(nb[0][1]) - self._yvel
            elif(where=='down'):
                if not(self.isThrough): self._xvel=-1*self._xvel
                self._x=nb[0][0]+1-self._xvel
                self._y=int(nb[0][1])-self._yvel
            elif(where=='left'):
                if not(self.isThrough): self._yvel=-1*self._yvel
                self._y=nb[0][1]-1-self._yvel
                self._x=int(nb[0][0])-self._xvel
            elif(where=='right'):
                if not(self.isThrough): self._yvel=-1*self._yvel
                self._y=nb[0][1]+1-self._yvel
                self._x=int(nb[0][0])-self._xvel
            elif(where=='reverse'):
                tups=((nb[0][0]-1,nb[0][1]),(nb[0][0]+1,nb[0][1]),(nb[0][0],nb[0][1]+1),
                (nb[0][0],nb[0][1]-1))
                checkBool,outpoints=self.checkPoints(tups,brickobj,nb)
                if(checkBool):
                    if not(self.isThrough): self._yvel=outpoints[0][1][1] *self._yvel
                    if not(self.isThrough): self._xvel=outpoints[0][1][0]*self._xvel
                    self._y=outpoints[0][0][1]-self._yvel
                    self._x=outpoints[0][0][0]-self._xvel
                elif(checkBool==False):
                    if not(self.isThrough): self._yvel=-1*self._yvel
                    if not(self.isThrough): self._xvel=-1*self._xvel
                    self._y=outpoints[1]-self._yvel
                    self._x=outpoints[0]-self._xvel
                    if (nb[1].strength==6 or self.isFire):
                        nbricks=[nb[1]]
                        self.getNeighbourBricks(nb[1],brickobj,nbricks)
                        for nbrick in nbricks:
                            paddleobj.set_score(nbrick.strength)
                            nbrick.strength=0
                    else:
                        for ite in tups:
                            brbrick=self.checkInBrick(brickobj,ite,'all')
                            if brbrick:
                                if not(brbrick._x==nb[1]._x and brbrick._y==nb[1]._y):
                                    if (brbrick.strength!=5):
                                        paddleobj.set_score(1)
                                        brbrick.strength-=1
                                        if brbrick._type=="RBRICK":
                                            brbrick._type="BRICK"
                                        brbrick.collideValues.append(nb[1].collideValues[0])
                                        brbrick.collideValues.append(nb[1].collideValues[1])
                                    elif (brbrick.strength==6 or self.isFire):
                                        nbricks=[brbrick]
                                        self.getNeighbourBricks(brbrick,brickobj,nbricks)
                                        for nbrick in nbricks:
                                            nbrick.collideValues.append(nb[1].collideValues[0])
                                            nbrick.collideValues.append(nb[1].collideValues[1])
                                            paddleobj.set_score(nbrick.strength)
                                            nbrick.strength=0
                                    if (self.isThrough): brbrick.strength=0

            if ((nb[1].strength==6 or self.isFire) and nb[1]._type!="BOSS"):
                    nbricks=[nb[1]]
                    self.getNeighbourBricks(nb[1],brickobj,nbricks)
                    for nbrick in nbricks:
                        nbrick.collideValues.append(nb[1].collideValues[0])
                        nbrick.collideValues.append(nb[1].collideValues[1])
                        paddleobj.set_score(nbrick.strength)
                        nbrick.strength=0
            else:
                if(nb[1].strength!=5 and nb[1].strength!=0):
                    paddleobj.set_score(1)
                    nb[1].strength-=1
                    if config.MUSIC:
                        os.system('aplay -q ./sounds/break.wav&')
                    if nb[1]._type=="RBRICK":
                        nb[1]._type="BRICK"
                if (self.isThrough): nb[1].strength=0
    def move(self,paddleobj,brickobj):
        # str1=f"1 {self._y}\n"
        # str2=f"2 {self._y}\n"
        # os.write(1, str.encode(str1))
        # os.write(1, str.encode(str2)) 
        self._checkCollision(paddleobj)
        self._checkCollisionWithBrick(brickobj,paddleobj)
        self._x+=self._xvel
        self._y+=self._yvel
        if self._type=="BULLET":
            self._xvel=-1
            self._yvel=0
        
    
    def attach(self,paddleobj,pblength):
        self._y=paddleobj._y+pblength