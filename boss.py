
from lever import Lever
import random
from typing import Final
from monster import Monster
 
from helper import Disk
import arcade
import math

"""Speed of boss"""
BOSS_SPEED = 3

"""Radius in which boss can move around it's spawning point"""
ACTION_RADIUS = 500

"""Number of frames every which we change direction randomly"""
FRAMES = 80


from enum import IntEnum


class Attack(IntEnum) : 
        PAUSE = 0
        RUSH = 1
        WALK = 2
        DASH = 3


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

        self.choice : Attack = Attack.WALK

        self.hit_points = 3
        self.texture = arcade.load_texture("assets/kenney-extended-enemies-png/spinner.png")
        self.sync_hit_box_to_texture()
        self.scale = (1,1)

        self.angle_deplacement = 0.0

        self.frame_until_action = FRAMES

        self.action_area = Disk(self.__initial_x, self.__initial_y, ACTION_RADIUS)

    def move(self, wall: arcade.SpriteList[arcade.Sprite]) -> None:
        self.__update_position()

    def ia(self,player_x : float, player_y: float) -> None:
        self.frame_until_action -= 1
        if self.frame_until_action == 15:             #indicate the next move #couleurs temporaire
                match self.choice:
                    case Attack.PAUSE:  #bleu
                        self.rgb = 0, 0, 255

                    case Attack.RUSH:   #rouge
                        self.rgb = 255, 0, 0
                        
                    case Attack.WALK:   #cyan   
                        self.rgb = 0, 255, 255   
                       
                    case Attack.DASH:   #magenta
                        self.rgb = 255, 0, 255

        if self.frame_until_action == 0:
            self.rgb = 255, 255, 255
            if not self.action_area.contains_point((self.center_x, self.center_y)):
                self.angle_deplacement = math.pi + math.atan2(self.center_y - self.__initial_y ,self.center_x - self.__initial_x)
                self.frame_until_action = FRAMES
                self.speed = 2*BOSS_SPEED
            elif self.action_area.contains_point((player_x,player_y)):
                match self.choice:          #chooses a random move to do 
                    case Attack.PAUSE:
                        self.speed = 0
                        self.frame_until_action = random.randint(40,80)
                        can_do = [Attack.WALK, Attack.RUSH, Attack.DASH]
                        self.choice = random.choice(can_do)

                    case Attack.RUSH:
                        self.angle_deplacement = math.pi + math.atan2(self.center_y - player_y ,self.center_x - player_x)
                        self.speed =2*BOSS_SPEED
                        self.frame_until_action = random.randint(20,60)
                        can_do = [Attack.PAUSE, Attack.RUSH, Attack.DASH]
                        self.choice = random.choice(can_do)

                    case Attack.WALK:         
                        self.frame_until_action = random.randint(60,100)
                        self.angle_deplacement = 45*random.randint(0,7)       #pour obtenire une mouvement mecanique de scie
                        self.speed = BOSS_SPEED
                        can_do = [Attack.WALK, Attack.RUSH, Attack.DASH]
                        self.choice = random.choice(can_do)
                        

                    case Attack.DASH:
                        self.frame_until_action = random.randint(20,40)
                        if random.getrandbits(1):
                            left_or_right = 2*math.pi/3
                        else:
                            left_or_right = -2*math.pi/3
                        self.angle_deplacement =left_or_right + math.atan2(self.center_y - player_y ,self.center_x - player_x)
                        self.speed =3*BOSS_SPEED
                        can_do =[Attack.RUSH, Attack.DASH]
                        self.choice = random.choice(can_do)

                        
                        
            else :
                self.speed=0
                self.frame_until_action = FRAMES
                    
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

        self.choice = Attack.WALK       #Make the boss back off 
        self.speed = -2*BOSS_SPEED
        self.frame_until_action = 30

        self.__new_speed()
        if self.hit_points == 0 :
            self.on_action()
            self.remove_from_sprite_lists() 

    
    
            




        

