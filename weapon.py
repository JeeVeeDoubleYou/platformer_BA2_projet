import arcade
import constants
import math
from player import Player


class Weapon(arcade.Sprite):
    """define how the weapon work and calculate it's movement"""
    def __init__(self, delta_x: float, delta_y: float ,player_x: float ,player_y: float) -> None :
        super().__init__("assets/kenney-voxel-items-png/sword_silver.png", constants.SCALE*0.7)
        self.set_angle(delta_x, delta_y)
        self.update_position(player_x, player_y)
        self.time = 0
        self.color=255,0,0

    def move(self, player_x: float, player_y :float) -> None :
        self.update_position(player_x, player_y)

    def hit_frame(self, timer: int) -> bool :
        self.time +=1
        if timer < self.time:
            self.color=255,255,255
            return False
        return True

    def set_angle(self, delta_x: float, delta_y: float) -> None :
        self.angle_rad = math.atan2(delta_x, delta_y)
        self.angle = self.angle_rad*(180/math.pi)-45

    def update_position(self, player_x: float, player_y: float) -> None :
        DISTANCE_EPEE_JOUEUR = 30 #
        DELTA_H = 5
        
        self.center_x = player_x+DISTANCE_EPEE_JOUEUR*math.sin(self.angle_rad)
        self.center_y = player_y+DISTANCE_EPEE_JOUEUR*math.cos(self.angle_rad)-DELTA_H


    

    
