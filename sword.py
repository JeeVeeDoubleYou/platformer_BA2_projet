import arcade
from UI import UI
import constants
from lever import Lever
from monster import Monster
from weapon import Weapon

class Sword(Weapon):
    """Defines how the sword works"""

    __slots__ = ()

    def __init__(self, mouse_position : arcade.Vec2, player_position : arcade.Vec2, camera_bottom_left : arcade.Vec2) -> None :
        super().__init__("assets/kenney-voxel-items-png/sword_silver.png", constants.SCALE*0.7, 45, mouse_position, player_position, camera_bottom_left)
        self.rgb = 255, 0, 0 # Visual, makes the sworld be red when active
        self.is_active = True
        
    def in_hit_frame(self) -> None :
        """
        Deactivates the sword after it has been active for a defined number of frames.

        This method checks if the sword has exceeded the configured active frames duration,
        and calls `deactivate()` to disable the sword when that threshold is passed.
        """
        if constants.SWORD_ACTIVE_FRAMES < self.frames_from_spawn:
            self.deactivate()

    def deactivate(self) -> None:
        """Deactivate the sword and reset its visual state."""
        self.rgb = 255, 255, 255
        self.is_active = False

    def check_collision(self, monster_list : arcade.SpriteList[Monster], lever_list : arcade.SpriteList[Lever], ui : UI) -> bool :
        """Checks if there was a collision between weapon an monster or lever. 
        Returns True if there was, False otherwise.
        """
        if self.is_active :

            # Check collision with monsters
            for monster in arcade.check_for_collision_with_list(self, monster_list) :
                monster.die()
                ui.update_boss_life(monster)
                self.deactivate()
                return True
            
            # Check collision with levers
            for lever in arcade.check_for_collision_with_list(self, lever_list):
                if lever.is_active:
                    lever.on_action()
                    self.deactivate()
                    return True
        return False