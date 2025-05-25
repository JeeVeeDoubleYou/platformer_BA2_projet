import arcade
from UI import UI
import constants
from lever import Lever
from monster import Monster
from weapon import Weapon

class Sword(Weapon):
    """Defines how the sword works"""

    def __init__(self, mouse_position : arcade.Vec2, player_position : arcade.Vec2, camera_bottom_left : arcade.Vec2) -> None :
        super().__init__("assets/kenney-voxel-items-png/sword_silver.png", constants.SCALE*0.7, 45, mouse_position, player_position, camera_bottom_left)
        self.rgb = 255, 0, 0 # Visual, makes the sworld be red when active
        self.is_active = True
        
    def in_hit_frame(self) -> None :
        if constants.SWORD_ACTIVE_FRAMES < self.frames_from_spawn:
            self.deactivate()

    def deactivate(self) -> None:
        self.rgb = 255, 255, 255
        self.is_active = False

    def check_collision(self, monster_list : arcade.SpriteList[Monster], lever_list : arcade.SpriteList[Lever], ui : UI) -> bool :
        """Checks if there was a collision between weapon an monster or lever. 
        Returns True if there was, False otherwise.
        """
        if self.is_active :
            for monster in arcade.check_for_collision_with_list(self, monster_list) :
                monster.die()
                ui.update_boss_life(monster)
                self.deactivate()
                return True
            for lever in arcade.check_for_collision_with_list(self, lever_list):
                if lever.is_active:
                    lever.on_action()
                    self.deactivate()
                    return True
        return False