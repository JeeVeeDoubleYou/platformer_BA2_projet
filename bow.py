import arcade
import constants
from weapon import Weapon



class Bow(Weapon):
    """define how the sword work """

    def __init__(self, mouse_position : arcade.Vec2, player_position : arcade.Vec2, camera_bottom_left : arcade.Vec2) -> None :
        super().__init__("assets/kenney-voxel-items-png/bow.png", constants.SCALE*0.7, 135, mouse_position, player_position, camera_bottom_left)
        self.is_active = False
    
    def in_hit_frame(self) -> None :
        necessary_time_before_shooting = 15
        if necessary_time_before_shooting == self.frames_from_spawn:
           self.texture = arcade.load_texture("assets/kenney-voxel-items-png/bowArrow.png")
           self.angle += 90
           self.set_texture_angle(55)
           self.is_active = True
           
    
    
