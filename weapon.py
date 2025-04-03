import arcade
import constants
import math
from math_personal import sin_deg, cos_deg, atan2_deg



class Weapon(arcade.Sprite):

    time = 0
    """define how the weapon work and calculate it's movement"""
    def set_texture_angle(self, angle_texture: float) -> None :
        self.texture_angle = angle_texture


    def time_counting(self) -> None :
        self.time += 1

    def set_angle(self, delta_x: float, delta_y: float) -> None :
        #self.angle_rad = math.atan2(delta_x, delta_y)
        #self.angle = self.angle_rad*(180/math.pi)-45 
        self.angle = atan2_deg(delta_x, delta_y)-self.texture_angle


    def update_position(self, player_x: float, player_y: float) -> None :
        DISTANCE_ARME_JOUEUR = 25 
        DELTA_H = 5
        
        self.center_x = player_x+DISTANCE_ARME_JOUEUR*sin_deg(self.angle+self.texture_angle)
        self.center_y = player_y+DISTANCE_ARME_JOUEUR*cos_deg(self.angle+self.texture_angle)-DELTA_H


    

    
