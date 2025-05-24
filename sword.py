import arcade
import constants
from weapon import Weapon

"""Number of frames after spawn during which the sword can hit an enemy"""
SWORD_ACTIVE_FRAMES = 7

class Sword(Weapon):
    """Defines how the sword works"""

    def __init__(self, mouse_position : arcade.Vec2, player_position : arcade.Vec2, camera_bottom_left : arcade.Vec2) -> None :
        super().__init__("assets/kenney-voxel-items-png/sword_silver.png", constants.SCALE*0.7, 45, mouse_position, player_position, camera_bottom_left)
        self.rgb =255, 0, 0
        self.texture_angle = 45
        self.is_active = True
        
    def in_hit_frame(self) -> None :
        if SWORD_ACTIVE_FRAMES < self.frames_from_spawn:
            self.rgb = 255, 255, 255
            self.deactivate()

    def deactivate(self) -> None:
        self.is_active = False
