import os
import random
import math
import time
import numpy as np
from colorama import init as coloramaInit, Fore, Style,Back
from terminalfns import clearScreen
from config import FRAMEHEIGHT,FRAMEWIDTH,POWERUPS,NOLIVES,BOSSSTRENGTH,MUSIC
from ball import Ball
from paddle import Paddle
from brick import Brick
from powerup import PowerUp
from boss import Boss
from bullet import Bullet
from input import Get,input_to
class RenderGame():
    def __init__(self):
        coloramaInit()
        clearScreen()
        self.__gameobjects=[]
        self.__colorArray=np.full([FRAMEHEIGHT,FRAMEWIDTH],(Fore.WHITE + Back.BLACK))
        self.__arr=np.full([FRAMEHEIGHT, FRAMEWIDTH], (' '))
        self.__arr[::,0]='|'
        self.__arr[::,-1]='|'
        self.__arr[0,::]='-'
        self.__arr[-1,::]='-'
        self._starttime=time.time()
        self.lasttime=time.time()
        self.lives=NOLIVES
        self.levels=3
        self.falltime=0
        self.gravity=0
        self.bossStrength=BOSSSTRENGTH
        self.defenseWalls=2
        self.bomb=0
        self._loopGame()

    def _scores(self,paddleobj):
        padding = ' '*10
        str1=f"Score:{paddleobj[0].get_score()}{padding}\n"
        str1+=f"Lives Remaining:{self.lives}{padding}\n"
        str1+=f"Level:{3-self.levels}{padding}\n"
        if 3-self.levels==3:
            bs=np.full(BOSSSTRENGTH,('X'))
            sbs=np.full(BOSSSTRENGTH,('-'))
            bs[self.bossStrength:]=sbs[self.bossStrength:]
            strbs='['
            for i in bs:
                strbs+=i
            strbs+=']'
            str1+=f"BossStrength:{strbs}{padding}\n"
        else:
            str1+=f"BossStrength:{self.bossStrength}{padding}\n"
        str1+=f"Time : {int((time.time()-self._starttime))} seconds{padding}\n"    
        os.write(1,str.encode(str1))
        
    def printToArray(self,coorlength,obj):
        from_x = int(coorlength["coor"][0])
        to_x = from_x + coorlength["length"][0] - 1

        from_y = int(coorlength["coor"][1])
        to_y = from_y + coorlength["length"][1] - 1

        self.__arr[from_x:to_x + 1,from_y: to_y + 1] = obj.draw()
        if(obj._type=='BRICK' or obj._type=='RBRICK' or obj._type in ['E','S','M','F','T','G']):
            self.__colorArray[from_x:to_x + 1,from_y: to_y + 1]=obj.colorBrick()

    def _printGame(self):
        
        for items in self.__gameobjects:
            for item in items:
                coorlength=item.retcoorlength()
                self.printToArray(coorlength,item)
        st=""
        for i in range(0,FRAMEHEIGHT):
            
            for j in range(0,FRAMEWIDTH):
                st+=self.__colorArray[i][j]+self.__arr[i][j]
            st+='\n'
        os.write(1,str.encode(st))


    def _resetArray(self):
        self.__arr=np.full([FRAMEHEIGHT, FRAMEWIDTH], (' '))
        self.__arr[::,0]='|'
        self.__arr[::,-1]='|'
        self.__arr[0,::]='-'
        self.__arr[-1,::]='-'
        self.__colorArray=np.full([FRAMEHEIGHT,FRAMEWIDTH],(Fore.WHITE + Back.BLACK))

    def _update(self,ballobj,paddleobj,ch,brickobj,powerupobj,bulletobj,cannonobj):
        self.__gameobjects=[]
        self.__gameobjects.append(powerupobj)
        self.__gameobjects.append(brickobj)
        self.__gameobjects.append(ballobj)
        self.__gameobjects.append(paddleobj)
        self.__gameobjects.append(bulletobj)
        self.__gameobjects.append(cannonobj)
        
        
        self._resetArray()
        pblength=[]
        for i in ballobj:
            pblength.append(i._y-paddleobj[0]._y)

        paddleobj[0].move(ch)
        for iti in range(len(ballobj)):
            # print(ballobj[iti].isCollidedWithPaddle)
            if(ballobj[iti].isCollidedWithPaddle):
                ballobj[iti].attach(paddleobj[0],pblength[iti])  
        if self.bossStrength==12:
            if self.defenseWalls==2:
                for i in range(0,200,8):
                    brickobj.append(Brick(11,i,3,8,0,0,random.randint(1,4),0))
                self.defenseWalls-=1
        if self.bossStrength==8:
            if self.defenseWalls==1:
                for i in range(0,200,8):
                    brickobj.append(Brick(15,i,3,8,0,0,random.randint(1,4),0))    
                self.defenseWalls-=0   

        if(1000*(time.time()-self.lasttime)>=100):
            for iti in range(len(ballobj)):   
                if not(ballobj[iti].isCollidedWithPaddle):
                    ballobj[iti].move(paddleobj[0],brickobj)
            if len(paddleobj[0].powerups["B"])!=0:
                if MUSIC:
                    os.system('aplay -q ./sounds/bullet.wav&')
                bulletobj.append(Bullet(paddleobj[0]._x-1,paddleobj[0]._y,1,1,-1,0))
                bulletobj.append(Bullet(paddleobj[0]._x-1,paddleobj[0]._y+paddleobj[0]._ylength-1,1,1,-1,0))
            for iti in range(len(bulletobj)):   
                if not(bulletobj[iti].isCollided):
                    bulletobj[iti].move(paddleobj[0],brickobj)
            for iti in powerupobj:
                if iti.isVel:
                    iti.move(paddleobj[0],ballobj,cannonobj) 
            if len(ballobj)==0:
                self.lives-=1
                ballobj.append(Ball(FRAMEHEIGHT-3,paddleobj[0]._y+int(paddleobj[0]._ylength/2)
                ,1,1,-2,2))
            if (3-self.levels)==3:
                for i in brickobj:
                    if i._type=="BOSS":
                        i.move(paddleobj[0])
                        self.bossStrength=i.strength
                        break        
            paddleobj[0].removePowerUp(ballobj)  
            self.lasttime=time.time()
            self.falltime+=1
            self.gravity+=1
            self.bomb+=1
        for item in cannonobj:
            item.attach(paddleobj[0])
        
        if self.falltime>50:
            flag=0
            for i in ballobj:
                if i._x==paddleobj[0]._x-1 and paddleobj[0]._y <= i._y < paddleobj[0]._y+paddleobj[0]._ylength:
                    flag=1
                    break
            if flag:
                self.falltime=0
                for i in brickobj:
                    if not(3-self.levels==3 and i._type=="BOSS" ): 
                        i._x+=1
                    if i._x+3>=FRAMEHEIGHT-3:
                        self.lives=0
                for i in powerupobj:
                    if i._xvel==0 and i._yvel==0:
                        i._x+=1
        if self.gravity>5:
            for i in powerupobj:
                if i.isVel:
                    self.gravity=0
                    i._xvel+=1
        if self.bomb>30:
            for i in brickobj:
                if i._type=="BOSS":
                    powerupobj.append(PowerUp(i._x+i._xlength,i._y+int(i._ylength/2),1,1,0,1,'@'))
                    self.bomb=0
                    break
    
    def checkPowerupIsCollided(self,powerupobj):
        rIndex=[]
        for i in powerupobj:
            if(i.isCollided==True):
                rIndex.append(i)
        for i in rIndex:
            powerupobj.remove(i)

    def fillBricks(self,num):
        array=[]
        array2=[]
        if num==1:
            a=0
            for i in range(0,18,3):
                for j in range(0,144,8):
                    stren=random.randint(1,5)
                    hl=int(j/8)
                    whbrick=np.random.choice(2,1,p=[0.9,0.1])
                    if whbrick:
                        stren=3
                    if(hl==a or hl== a+1 or hl==17-a or hl==17-a-1) and int(i/3)!=5:
                        stren=6
                        whbrick=0
                    array.append(Brick(9+i,30+j,3,8,0,0,stren,whbrick))
                    
                    if (stren==3 or stren==4):
                        array2.append(PowerUp(9+i,30+j,1,1,0,0,random.choice(POWERUPS)))
                a+=2
        if num==2:
            a=10
            for i in range(0,18,3):
                for j in range(0,144,8):
                    stren=random.randint(1,5)
                    hl=int(j/8)
                    whbrick=np.random.choice(2,1,p=[0.9,0.1])
                    if whbrick:
                        stren=3
                    if(hl==a or hl== a+1 or hl==17-a or hl==17-a-1) and int(i/3)!=0:
                        stren=6
                        whbrick=0
                    
                    if not((int(i/3)==0 and int(j/8)==0) or (int(i/3)==0 and int(j/8)==17)):
                        array.append(Brick(9+i,30+j,3,8,0,0,stren,whbrick))
                        if (stren==3 or stren==4):
                            array2.append(PowerUp(9+i,30+j,1,1,0,0,random.choice(POWERUPS)))
                a-=2
        if num==3:
            array.append(Boss(0,int(FRAMEWIDTH/2),7,33,0,1,20,0))
            for i in range(9,18,3):
                for j in range(0,144,8):
                    stren=random.randint(1,5)
                    if stren==5:
                        array.append(Brick(9+i,30+j,3,8,0,0,stren,0))

                    
                
        return array,array2


    def checkBricks(self,brickobj,powerupobj):
        flag=0
        rIndex=[]
        for i in brickobj:
            if(i.strength==0):
                for iti in powerupobj:
                    if(iti._x==i._x and iti._y==i._y):
                        iti.setVel(i.collideValues)
                rIndex.append(i)
        for i in rIndex:
            flag+=1
            brickobj.remove(i)
        if MUSIC:
            if flag>3:
                os.system('aplay -q ./sounds/Explosion+3.wav&')
            if 1<=flag<=3:
                os.system('aplay -q ./sounds/break.wav&')
        
    def checkBall(self,ballobj,paddleobj):
        rIndex=[]
        for i in ballobj:
            if(i._xvel==0 and i._yvel==0):
                rIndex.append(i)
        for i in rIndex:
            ballobj.remove(i)
            if(len(ballobj)==0):
                self.lives-=1
               # print(paddleobj[0]._y)
                ballobj.append(Ball(FRAMEHEIGHT-3,paddleobj[0]._y+int(paddleobj[0]._ylength/2)
                ,1,1,-2,2))

    def checkBullets(self,bulletobj,cannonobj,paddleobj):
        if len(paddleobj[0].powerups["B"])==0:
            rIndex=[]
            for i in cannonobj:
                rIndex.append(i)
            for i in rIndex:
                cannonobj.remove(i)

        rIndex=[]
        for i in bulletobj:
            if(i.isCollided):
                rIndex.append(i)
        for i in rIndex:
            bulletobj.remove(i)

    def status(self):
        if(self.lives==0):
            return 0
        return 1
               
    def leveling(self,brickobj,paddleobj):
        flag=0
        for i in brickobj:
            if(i.strength!=5):
                flag=1
            else:
                if(len(paddleobj[0].powerups["T"])!=0):
                    flag=1                
        return flag 
    def fillthescreen(self,paddleobj,ballobj,brickobj,powerupobj,cannonobj,bulletobj,num):
        ballobj=[]
        brickobj=[]
        powerupobj=[]
        cannonobj=[]
        bulletobj=[]
        sco=0
        if len(paddleobj)!=0:
            sco=paddleobj[0].get_score()
        paddleobj=[]
        paddleobj.append(Paddle(FRAMEHEIGHT-2,int(FRAMEWIDTH/2),1,7,0,0))
        paddleobj[0]._score=sco
        ballobj.append(Ball(FRAMEHEIGHT-3,paddleobj[0]._y+int(paddleobj[0]._ylength/2),1,1,-2,2))
        brickobj,powerupobj=self.fillBricks(num)
        return paddleobj,ballobj,brickobj,powerupobj,cannonobj,bulletobj
        
   
        

    def _loopGame(self):
        paddleobj= []
        ballobj=[]
        brickobj=[]
        powerupobj=[]
        bulletobj=[]
        cannonobj=[]
        flag=0
        while (self.status()):
            if self.leveling(brickobj,paddleobj)==0:
                self.levels-=1
                num=3-self.levels
                paddleobj,ballobj,brickobj,powerupobj,cannonobj,bulletobj=self.fillthescreen(paddleobj,ballobj,brickobj,powerupobj,cannonobj,bulletobj,num)
                
            getch=Get()
            ch=input_to(getch,0.1)
            if ch=='e':
                flag=1
                break
            # if ch=='k':
            #     bulletobj.append(Bullet(FRAMEHEIGHT-4,int(FRAMEWIDTH/2),1,1,-1,0))
            if(ch=='f'):
                for i in ballobj:
                    i.isCollidedWithPaddle=False
            print("\033[0;0H")
            
            self._update(ballobj,paddleobj,ch,brickobj,powerupobj,bulletobj,cannonobj)
            self.checkBricks(brickobj,powerupobj)
            self.checkBall(ballobj,paddleobj)
            self.checkPowerupIsCollided(powerupobj)
            self.checkBullets(bulletobj,cannonobj,paddleobj)
            self._scores(paddleobj)
            self._printGame()
            if ch=='s':
                self.levels-=1
                num=3-self.levels
                paddleobj,ballobj,brickobj,powerupobj,cannonobj,bulletobj=self.fillthescreen(paddleobj,ballobj,brickobj,powerupobj,cannonobj,bulletobj,num)
                print(f'Skipped level{3-self.levels-1}')
            if self.levels==-1:
                flag=2
                break 
        if flag:
            print("You Exited")
            print(f"With Score {paddleobj[0].get_score()}")
        if flag==2:
            print("You completed all levels")
            print(f"With Score {paddleobj[0].get_score()}")    
        else:
            if(self.lives==0):
                os.system('aplay -q ./sounds/lost.wav&')
                print("You Lost")
                print(f"With Score {paddleobj[0].get_score()}")
            else:
                print("You Won")
                print(f"With Score {paddleobj[0].get_score()}")
            



