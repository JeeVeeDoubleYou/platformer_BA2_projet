import random
from typing import Final
from monster import Monster
import arcade
import math

"""Speed of b
ats"""
BAT_SPEED = 2

"""Radius in which bat can move around it's spawning point"""
ACTION_RADIUS = 75

"""Number of frames every which we change direction randomly"""
FRAMES = 2

class Bat(Monster):
    """Represents a bat, defines how it moves"""
    
    __initial_x : Final[float]
    __initial_y : Final[float]

    def __init__(self, x: float, y: float) -> None :
        
        super().__init__("assets/kenney-extended-enemies-png/bat.png")

        self.center_x = x
        self.center_y = y
        
        self.__initial_x = x
        self.__initial_y = y

        self.angle_deg = 0.0

        self.__frames_until_random = FRAMES

        self.action_area = Disk(self.__initial_x, self.__initial_y, ACTION_RADIUS)

    def move(self, wall_list : arcade.SpriteList[arcade.Sprite]) -> None:
        "Makes the bat move"
        
        self.__frames_until_random -= 1

        if self.__frames_until_random == 0 or  not self.__can_move(self.__new_speed(self.angle_deg)):
            self.__frames_until_random = FRAMES
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


    def __new_speed(self, angle__deg : float, speed : float = BAT_SPEED) -> tuple[float, float]:
        """Calculates the x and y speeds in order to keep a total constant speed of 'speed', 
        depending on the angle of the movement, given in degres and with respect to the x axis going right.
        """
        x_speed = math.cos(math.radians(angle__deg)) * BAT_SPEED
        y_speed = math.sin(math.radians(angle__deg)) * BAT_SPEED
        if x_speed*self.scale_x > 0.5  :
            """flip the bat if it go fast enought in the direction it is not facing"""
            self.scale_x *= -1      #flip the sprite horizontaly

        return (x_speed, y_speed)

    
    def __can_move(self, speed : tuple[float, float]) -> bool : 
        """Returns True if moving the bat once with (speed) keeps it inside it's action area,
        False otherwise. """

        return self.action_area.contains_point((self.center_x + speed[0], self.center_y + speed[1]))

class Disk :

    """Immable class defining a 2D disk around a certain center point with a given radius."""

    __center_x : Final[float]
    __center_y : Final[float]
    __radius : Final[float]

    def __init__(self, center_x : float, center_y : float, radius : float) -> None:
        assert radius > 0
        self.__center_x = center_x
        self.__center_y = center_y
        self.__radius = radius
    
    def contains_point(self, position : tuple[float, float]) -> bool :
        """Returns True if the disk contains the point (position), False otherwise."""
        x, y = position
        return (self.__center_x - x)**2 + (self.__center_y - y)**2 <= self.__radius**2      #C'est plus rapide de calculer un carre qu'une racine