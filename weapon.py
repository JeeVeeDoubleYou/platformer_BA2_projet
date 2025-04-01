import arcade
import constants
import math
import math_perso



class Weapon(arcade.Sprite):
    """define how the weapon work and calculate it's movement"""
    def set_texture_angle(self, angle_texture: float) -> None :
        self.texture_angle = angle_texture


    def time(self):
        self.time += 1

    def set_angle(self, delta_x: float, delta_y: float) -> None :
        #self.angle_rad = math.atan2(delta_x, delta_y)
        #self.angle = self.angle_rad*(180/math.pi)-45 
        self.angle = math_perso.atan2_deg(delta_x, delta_y)-self.texture_angle


    def update_position(self, player_x: float, player_y: float) -> None :
        DISTANCE_ARME_JOUEUR = 20 
        DELTA_H = 5
        
        self.center_x = player_x+DISTANCE_ARME_JOUEUR*math_perso.sin_deg(self.angle+self.texture_angle)
        self.center_y = player_y+DISTANCE_ARME_JOUEUR*math_perso.cos_deg(self.angle+self.texture_angle)-DELTA_H


    

    
