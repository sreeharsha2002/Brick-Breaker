import os
from game import RenderGame
if __name__ == "__main__":
    os.system('setterm -cursor off')
    RenderGame()
    os.system('setterm -cursor on')