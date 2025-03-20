import arcade
import constants
import math
from player import Player

class Weapon(arcade.Sprite):

    def __init__(self, x: int, y: int ,px ,py) -> None :
        super().__init__("assets/kenney-voxel-items-png/sword_silver.png", constants.SCALE*0.7)
        teta=math.atan2(x,y)
        self.angle = teta*(180/math.pi)-45
        self.center_x = px+35*math.sin(teta)
        self.center_y = py+35*math.cos(teta)
    def move(self, x, y) -> None :
        teta=(45+self.angle)*(math.pi/180)
        self.center_x = x+35*math.sin(teta)
        self.center_y = y+35*math.cos(teta)

    

    
