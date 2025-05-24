import arcade
import constants
from weapon import Weapon

class Bow(Weapon):
    """Defines how the bow works"""

    def __init__(self, mouse_position : arcade.Vec2, player_position : arcade.Vec2, camera_bottom_left : arcade.Vec2) -> None :
        super().__init__("assets/kenney-voxel-items-png/bow.png", constants.SCALE*0.7, 135, mouse_position, player_position, camera_bottom_left)
        self.is_active = False
    
    def in_hit_frame(self) -> None :
        """Updates is_active attribute if Bow has been active long enough to be able to shoot"""
        
        if constants.BOW_TIME_OUT == self.frames_from_spawn:
           self.texture = arcade.load_texture("assets/kenney-voxel-items-png/bowArrow.png")
           self.angle += 80
           self.set_texture_angle(55)
           self.__activate()

    def __activate(self) -> None :
        self.is_active = True
           
    
    
