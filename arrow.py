import arcade 
import constants
from math_personal import sin_deg, cos_deg, atan2_deg
from bow import Bow



class Arrow(arcade.Sprite):
    """Represents an arrow, from a bow"""
    
    def __init__(self, bow: Bow) -> None :
        
        super().__init__("assets/kenney-voxel-items-png/arrow.png", constants.SCALE*0.7)
        self.angle = bow.angle+bow.texture_angle
        self.center_x = bow.center_x
        self.center_y = bow.center_y
        self.change_x = constants.ARROW_SPEED*sin_deg(self.angle)
        self.change_y = constants.ARROW_SPEED*cos_deg(self.angle)

    def move(self) -> None :
        """Defines the movement of an arrow."""
        
        self.change_y -= constants.ARROW_GRAVITY
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle = atan2_deg(self.change_x,self.change_y)-45
        

    



        