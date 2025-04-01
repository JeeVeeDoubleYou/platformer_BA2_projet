import arcade 
import constants
import math_personaliser
from bow import Bow


ARROW_SPEED = 20
ARROW_GRAVITY = 1

class Arrow(arcade.Sprite):
    def __init__(self, bow: Bow, player_x_speed: float, player_y_speed: float) -> None :
        
        super().__init__("assets/kenney-voxel-items-png/arrow.png", constants.SCALE*0.7)
        self.angle = bow.angle+bow.texture_angle
        self.center_x = bow.center_x
        self.center_y = bow.center_y
        self.change_x = player_x_speed+ARROW_SPEED*math_personaliser.sin_deg(self.angle)
        self.change_y = player_y_speed+ARROW_SPEED*math_personaliser.cos_deg(self.angle)
        
    def move(self) -> None :
        self.change_y -= ARROW_GRAVITY
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle = math_personaliser.atan2_deg_aprox(self.change_x,self.change_y)-45
        

    



        