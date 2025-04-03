import arcade
import constants
from weapon import Weapon

class Sword(Weapon):
    """define how the sword work """

    def __init__(self, delta_x: float, delta_y: float ,player_x: float ,player_y: float) -> None :
        super().__init__("assets/kenney-voxel-items-png/sword_silver.png", constants.SCALE*0.7)
        Weapon.set_texture_angle(self, 45)
        Weapon.set_angle(self, delta_x, delta_y)
        Weapon.update_position(self, player_x, player_y)
        self.frames_from_spawn = 0
        self.rgb =255, 0, 0
        self.texture_angle =45
        #Sword.start(delta_x, delta_y, player_x, player_y)
        
    def hit_frame(self) -> bool :
        FRAMES_FOR_DAMAGES = 5
        if FRAMES_FOR_DAMAGES < self.frames_from_spawn:
            self.rgb = 255 ,255 ,255
            return False
        return True
