from abc import abstractmethod
import arcade
from math_personal import sin_deg, cos_deg, atan2_deg
import constants


class Weapon(arcade.Sprite):
    """Defines how the weapon works and calculates it's movement"""

    __is_active : bool
    texture_angle : float
    
    def __init__(self, texture : str, scale : float, initial_angle : float, mouse_position : arcade.Vec2, player_position : arcade.Vec2, camera_bottom_left : arcade.Vec2) :
        super().__init__(texture, scale)
        self.frames_from_spawn = 0
        self.set_texture_angle(initial_angle)
        self.update_angle(mouse_position, player_position, camera_bottom_left)
        self.update_position(player_position)

    @abstractmethod
    def in_hit_frame(self) -> None :
        ...

    def update_angle(self, mouse_position : arcade.Vec2, player_position : arcade.Vec2, camera_bottom_left : arcade.Vec2) -> None:
        """Takes mouse, player and camera positions as arguments and changes the angle of the weapon in consequence"""
        delta_x = mouse_position.x + camera_bottom_left.x - player_position.x
        delta_y = mouse_position.y + camera_bottom_left.y - player_position.y - constants.WEAPON_OFFSET_Y
        self.angle = atan2_deg(delta_x, delta_y) - self.texture_angle
        
    def set_texture_angle(self, texture_angle: float) -> None :
        self.texture_angle = texture_angle


    def update_position(self, player_position : arcade.Vec2) -> None :
        
        self.center_x = player_position.x+ constants.DISTANCE_ARME_JOUEUR*sin_deg(self.angle+self.texture_angle)
        self.center_y = player_position.y+ constants.DISTANCE_ARME_JOUEUR*cos_deg(self.angle+self.texture_angle)- constants.WEAPON_OFFSET_Y
        
        self.frames_from_spawn += 1
        self.in_hit_frame()

    @property
    def is_active(self) -> bool :
        return self.__is_active

    @is_active.setter
    def is_active(self, active : bool) -> None :
        self.__is_active = active