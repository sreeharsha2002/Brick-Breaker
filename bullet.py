import random
from colorama import Fore
import numpy as np
import config
from ball import Ball
import os
class Bullet(Ball):
    def __init__(self, x, y, xlength, ylength, xvel, yvel):
        super().__init__(x, y, xlength, ylength, xvel, yvel)
        self._type="BULLET"
        self.isCollided=False