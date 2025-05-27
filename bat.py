import random
from typing import Final
from monster import Monster
import arcade
import math
from helper import Disk
import constants

class Bat(Monster):
    """Represents a bat, defines how it moves"""

    __slots__ = ('initial_x', 'initial_y', 'angle_def', '__frames_until_random', 'action_area', )
    
    __initial_x : Final[float]
    __initial_y : Final[float]

    def __init__(self, x: float, y: float) -> None :
        
        super().__init__("assets/kenney-extended-enemies-png/bat.png")

        self.center_x = x
        self.center_y = y
        
        self.__initial_x = x
        self.__initial_y = y

        self.angle_deg = 0.0

        self.__frames_until_random = constants.BAT_FRAMES

        self.action_area = Disk(self.__initial_x, self.__initial_y, constants.BAT_ACTION_RADIUS)

    def move(self, _wall : arcade.SpriteList[arcade.Sprite], _pos : arcade.Vec2) -> None:
        """Update the bat's movement direction randomly and moves."""
        
        self.__frames_until_random -= 1

        # Choose new movement angle when timer runs out or continuing in current path would lead to outside the action area
        if self.__frames_until_random == 0 or  not self.__can_move(self.__new_speed(self.angle_deg)):
            self.__frames_until_random = constants.BAT_FRAMES
            while True :
                # Check bat isn't stuck
                temp_angle_change = random.gauss(0,20) 
                if self.__can_move(self.__new_speed(self.angle_deg + temp_angle_change)) :
                    break
            self.__update_angle(temp_angle_change)

        # Checks if the bat can move once in the current direction it's going
        if self.__can_move(self.__new_speed(self.angle_deg)) :
            self.__update_position(self.__new_speed(self.angle_deg))
            return
  
        

    def __update_position(self, speed : tuple[float, float]) -> None:
        """Updates position by adding one amount of 'speed'"""
        self.center_x += speed[0]
        self.center_y += speed[1]

    def __update_angle(self, difference : float) -> None :
        """Updates angle by adding difference to current angle.
        Warning : angles go clockwise."""
        temp_angle = self.angle_deg + difference
        self.angle_deg = temp_angle % 360


    def __new_speed(self, angle__deg : float) -> tuple[float, float]:
        """Calculates the x and y speeds in order to keep a total constant speed of 'speed', 
        depending on the angle of the movement, given in degres and with respect to the x axis going right.
        """
        x_speed = math.cos(math.radians(angle__deg)) * constants.BAT_SPEED
        y_speed = math.sin(math.radians(angle__deg)) * constants.BAT_SPEED
        if x_speed*self.scale_x > 0.5  :
            # Flips the bat horizontaly if it goes fast enough in the direction it isn't facing.
            self.scale_x *= -1  

        return (x_speed, y_speed)

    
    def __can_move(self, speed : tuple[float, float]) -> bool : 
        """Returns True if moving the bat once with (speed) keeps it inside it's action area,
        False otherwise. """

        return self.action_area.contains_point((self.center_x + speed[0], self.center_y + speed[1]))

