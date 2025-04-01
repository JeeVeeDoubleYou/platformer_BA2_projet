import arcade
import constants
from weapon import Weapon



class Bow(Weapon):
    """define how the sword work """

    def __init__(self, delta_x: float, delta_y: float ,player_x: float ,player_y: float) -> None :
        super().__init__("assets/kenney-voxel-items-png/bow.png", constants.SCALE*0.7)
        Weapon.set_texture_angle(self, 135)
        Weapon.set_angle(self, delta_x, delta_y)
        Weapon.update_position(self, player_x, player_y)
        self.time = 0
        self.charged = False
        #Sword.start(delta_x, delta_y, player_x, player_y)
    
    def can_shoot_arrow(self) -> None :
        TIMMER = 30
        if TIMMER < self.time:
           #arcade.Sprite.texture.fset(self, "assets/kenney-voxel-items-png/bow.png")
           self.texture = arcade.load_texture("assets/kenney-voxel-items-png/bowArrow.png")
           self.angle += 90
           Weapon.set_texture_angle(self, 45)
           
           self.charged = True
           
    
    
