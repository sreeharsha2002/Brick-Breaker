import random
from colorama import Fore
import numpy as np
import config
from brick import Brick
import os
class Boss(Brick):
    def __init__(self, x, y, xlength, ylength, xvel, yvel,strength,btype):
        super().__init__(x, y, xlength, ylength, xvel, yvel,strength,btype)
        self._type="BOSS"
        self.isCollided=False

    def _checkCollision(self,mul):
        if(mul==1 and self._y + self._ylength - 1 + 1 >= config.FRAMEWIDTH ):
            self._y=config.FRAMEWIDTH - 1 - self._ylength -1 
            
        elif( mul==-1 and self._y - 1 <= 0):
            self._y= 1 + 1    
    def move(self, paddleobj):
        if self._y+int(self._ylength/2) > paddleobj._y+int(paddleobj._ylength/2):
            self._yvel=-1
        else:
            self._yvel=1
        self._checkCollision(self._yvel)
        self._y+=self._yvel
        