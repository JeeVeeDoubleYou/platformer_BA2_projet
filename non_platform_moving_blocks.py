from typing import Final

import arcade

import constants
from plateforme import Direction


class NonPlatformMovingBlocks :
    __sprite : Final[arcade.Sprite]
    __direction : Final[Direction]
    __horizontal_bounds : Final[tuple[int, int]| None] # (Left, Right)
    __vertical_bounds : Final[tuple[int, int]| None] # (Up, Down)
    __initial_position : Final[arcade.Vec2]
    __speed : int

    def __init__(self, sprite : arcade.Sprite, general_direction : Direction, movement : tuple[int, int], initial_position : arcade.Vec2):
        self.__sprite = sprite
        self.__direction = general_direction
        self.__initial_position = initial_position
        self.__speed = constants.PLATFORM_SPEED

        self.__vertical_bounds = (int(self.__initial_position.y + movement[0]), int(self.__initial_position.y - movement[1])) \
            if general_direction == Direction.VERTICAL \
                else None
        self.__horizontal_bounds = (int(self.__initial_position.x - movement[0]), int(self.__initial_position.x + movement[1])) \
            if general_direction == Direction.HORIZONTAL \
                else None

          
    def move(self, recursion : int = 0) -> None : 
        # ATTENTION : Ca marche pas du tout!
        match self.__direction :
            case Direction.VERTICAL :
                assert self.__vertical_bounds is not None
                if self.__sprite.top >= self.__vertical_bounds[0] :
                    self.__sprite.top = self.__vertical_bounds[0]
                    if self.__speed > 0:
                        self.__speed *= -1

                if self.__sprite.bottom <= self.__vertical_bounds[1] :
                    self.__sprite.bottom = self.__vertical_bounds[1]
                    if self.__speed < 0 :
                        self.__speed *= -1
                
                self.__sprite.center_y += self.__speed

            case Direction.HORIZONTAL :
                assert self.__horizontal_bounds is not None
                if self.__sprite.left <= self.__horizontal_bounds[0] :
                    self.__sprite.left = self.__horizontal_bounds[0]
                    if self.__speed > 0:
                        self.__speed *= -1

                if self.__sprite.right >= self.__horizontal_bounds[1] :
                    self.__sprite.right = self.__horizontal_bounds[1]
                    if self.__speed < 0:
                        self.__speed *= -1

                self.__sprite.center_x += self.__speed
