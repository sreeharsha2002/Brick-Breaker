import random
from colorama import Fore
import numpy as np
import config
from ball import Ball
import os
class Canon(Ball):
    def __init__(self, x, y, xlength, ylength, xvel, yvel,ctype):
        super().__init__(x, y, xlength, ylength, xvel, yvel)
        if ctype==0:
            self._type="CANNON0"
        else:
            self._type="CANNON1"
        self.isCollided=False   
    def attach(self, paddleobj):
        if(self._type=="CANNON0"):
            self._y=paddleobj._y
        else:
            self._y=paddleobj._y+paddleobj._ylength-1