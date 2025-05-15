
from lever import Lever
import random
from typing import Final
from monster import Monster
 
from bat import Disk
import arcade
import math

"""Speed of b
ats"""
BOSS_SPEED = 3

"""Radius in which bat can move around it's spawning point"""
ACTION_RADIUS = 400

"""Number of frames every which we change direction randomly"""
FRAMES = 80

class Boss(Monster, Lever):
    """Represents a bat, defines how it moves"""
    
    __initial_x : Final[float]
    __initial_y : Final[float]

    def __init__(self, x: float, y: float) -> None :
        
        super().__init__("assets/kenney-extended-enemies-png/bat.png")

        self.center_x = x
        self.center_y = y

        self.change_x = 0
        self.change_y = 0
        self.speed = BOSS_SPEED

        self.__initial_x = x
        self.__initial_y = y

        self.hit_points = 3
        self.texture = arcade.load_texture("assets/kenney-extended-enemies-png/spinner.png")
        self.sync_hit_box_to_texture()
        self.scale = (1,1)

        self.angle_deplacement = 0.0

        self.__frames_until_random = FRAMES

        self.action_area = Disk(self.__initial_x, self.__initial_y, ACTION_RADIUS)

    def move(self, wall: arcade.SpriteList[arcade.Sprite]) -> None:
        self.__update_position()

    def ia(self,player_x : float, player_y: float) -> None:
        self.__frames_until_random -= 1
        if self.__frames_until_random == 0:
            if not self.action_area.contains_point((self.center_x, self.center_y)):
                self.angle_deplacement = math.pi + math.atan2(self.center_y - self.__initial_y ,self.center_x - self.__initial_x)
                self.__frames_until_random = FRAMES
                self.speed = 2*BOSS_SPEED
                print("repositioning")
            elif self.action_area.contains_point((player_x,player_y)):
                choice = random.randint(0,3)
                match choice:
                    case 0:
                        self.speed = 0
                        self.__frames_until_random = FRAMES//2
                        print("pause")

                    case 1:
                        self.angle_deplacement = math.pi + math.atan2(self.center_y - player_y ,self.center_x - player_x)
                        self.speed =2*BOSS_SPEED
                        self.__frames_until_random = FRAMES
                        print("attaque")

                    case 2:
                        self.__frames_until_random = FRAMES
                        self.angle_deplacement = 45*random.randint(0,7)       #pour obtenire une mouvement mecanique de scie
                        self.__frames_until_random = FRAMES
                        self.speed = BOSS_SPEED
                        print("move")

                    case 3:
                        self.__frames_until_random = FRAMES
                        self.angle_deplacement =math.pi/2 + math.atan2(self.center_y - player_y ,self.center_x - player_x)
                        self.speed =3*BOSS_SPEED
                        self.__frames_until_random = FRAMES//2
                        print("dash")
            self.__new_speed()
        
        

    def __update_position(self) -> None:
        """Updates position by adding one amount of 'speed'"""
        self.center_x += self.change_x
        self.center_y += self.change_y

    def __new_speed(self) -> None:
        """Calculates the x and y speeds in order to keep a total constant speed of 'speed', 
        depending on the angle of the movement, given in degres and with respect to the x axis going right.
        """
        self.change_x = math.cos(self.angle_deplacement) * self.speed
        self.change_y = math.sin(self.angle_deplacement) * self.speed

    
    
    def die(self) -> None:
        self.hit_points -=1
        self.speed *= -1
        self.__new_speed()
        if self.hit_points == 0 :
            self.on_action()
            self.remove_from_sprite_lists() 

    
    
            




        

