from __future__ import annotations
from abc import abstractmethod
import arcade
from UI import UI
from arrow import Arrow
from lever import Lever
from math_personal import sin_deg, cos_deg, atan2_deg
import constants
from monster import Monster


class Weapon(arcade.Sprite):
    """Defines how the weapon works and calculates it's movement"""

    __texture_angle : float
    
    def __init__(self, texture : str, scale : float, initial_angle : float, mouse_position : arcade.Vec2, player_position : arcade.Vec2, camera_bottom_left : arcade.Vec2) :
        super().__init__(texture, scale)
        self.frames_from_spawn = 0
        self.__is_active = False
        self.set_texture_angle(initial_angle)
        self.__update_angle(mouse_position, player_position, camera_bottom_left)
        self.__update_position(player_position)

    @abstractmethod
    def in_hit_frame(self) -> None :
        ...

    def on_mouse_release(self) -> Arrow | None :
        """
        Handles logic when the mouse is released while this weapon is active.
        """
        return None

    def check_collision(self, monster_list : arcade.SpriteList[Monster], lever_list : arcade.SpriteList[Lever], ui : UI) -> bool :
        """ 
        Called tp check if the weapon collided with other game entities (e.g., monsters, levers, etc.).
        This method can be overridden in subclasses to define specific collision behavior.
        Returns True if there was a collision, False otherwise.
        """
        return False

    def update_weapon(self, mouse_position : arcade.Vec2, player_position : arcade.Vec2, camera_bottom_left : arcade.Vec2) -> None:
        """Updates the weapon position, angle, and activation status"""
        self.frames_from_spawn += 1
        self.__update_angle(mouse_position, player_position, camera_bottom_left)
        self.__update_position(player_position)
        self.in_hit_frame()

    def __update_angle(self, mouse_position : arcade.Vec2, player_position : arcade.Vec2, camera_bottom_left : arcade.Vec2) -> None:
        """ Updates the weapon's angle based on the mouse, player, and camera positions.
        """
        
        # Calculate mouse coordinates relative to world
        world_mouse_x = mouse_position.x + camera_bottom_left.x
        world_mouse_y = mouse_position.y + camera_bottom_left.y

        # Calculate angle from player to mouse, taking offsets into account
        delta_x = world_mouse_x - player_position.x
        delta_y = world_mouse_y - player_position.y - constants.WEAPON_OFFSET_Y
        self.angle = atan2_deg(delta_x, delta_y) - self.__texture_angle


    def __update_position(self, player_position : arcade.Vec2) -> None :
        """Updates the position of the weapon, to keep it static relative to the player"""
        
        self.center_x = player_position.x + constants.DISTANCE_ARME_JOUEUR*sin_deg(self.angle + self.__texture_angle)
        self.center_y = player_position.y + constants.DISTANCE_ARME_JOUEUR*cos_deg(self.angle + self.__texture_angle) - constants.WEAPON_OFFSET_Y

    @property
    def total_angle(self) -> float :
        return self.angle + self.texture_angle
    
    @property
    def is_active(self) -> bool :
        return self.__is_active

    @is_active.setter
    def is_active(self, active : bool) -> None :
        self.__is_active = active

    def set_texture_angle(self, texture_angle: float) -> None:
        self.__texture_angle = texture_angle

    @property
    def texture_angle(self) -> float :
        return self.__texture_angle
    