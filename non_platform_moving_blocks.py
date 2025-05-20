from typing import Final

import arcade

import constants 
from constants import HALF_BLOCK
from platforms import Direction


class NonPlatformMovingBlocks :
    __sprite : Final[arcade.Sprite]
    __direction : Final[Direction]
    __horizontal_bounds : Final[tuple[int, int]| None] # (Left, Right)
    __vertical_bounds : Final[tuple[int, int]| None] # (Up, Down)
    __initial_position : Final[arcade.Vec2]
    __speed : int

    def __init__(self, sprite : arcade.Sprite, general_direction : Direction, movement : tuple[int, int], initial_position : arcade.Vec2):
        # INFO : Movement comes from platform, it's a value in pixels : ie. number of arrows * constants.PIXELS_IN_BLOCK
        self.__sprite = sprite
        self.__direction = general_direction
        self.__initial_position = initial_position
        self.__speed = constants.PLATFORM_SPEED 

        # actual_half_width = (sprite.right - sprite.left) / 2

        # actual_half_height = (sprite.top - sprite.bottom) / 2

        # self.__vertical_bounds = (int(self.__initial_position.y + movement[0] + actual_half_height), int(self.__initial_position.y - movement[1] - actual_half_height)) \
        #     if general_direction == Direction.VERTICAL \
        #         else None
        # self.__horizontal_bounds = (int(self.__initial_position.x - movement[0] - actual_half_width), int(self.__initial_position.x + movement[1] + actual_half_width)) \
        #     if general_direction == Direction.HORIZONTAL \
        #         else None
        
        self.__vertical_bounds = (int(self.__initial_position.y + movement[0]), int(self.__initial_position.y - movement[1]))
    
        self.__horizontal_bounds = (int(self.__initial_position.x - movement[0]), int(self.__initial_position.x + movement[1]))

        print(movement[0] / 64, movement[1] / 64)
        
        # ATTENTION : Il faudrait changer tous les mouvement pour associer top à droite, comme ca on a pas besoin du match direction car movement[0] sera la direction initiale
        # Mettre la vitesse initiale à droite ou vers le haut, sauf s'il n'y a pas de movement dans ces directions
        match self.__direction :
            case Direction.VERTICAL :
                if movement[0] == 0 :
                    self.__speed = - constants.PLATFORM_SPEED 
                else : 
                    self.__speed = constants.PLATFORM_SPEED 
            case Direction.HORIZONTAL :
                if movement[1] == 0 :
                    self.__speed = - constants.PLATFORM_SPEED 
                else : 
                    self.__speed = constants.PLATFORM_SPEED 

          
    # def move(self) -> None : 
    #     match self.__direction :
    #         case Direction.VERTICAL :
    #             assert self.__vertical_bounds is not None

    #             self.__sprite.center_y += self.__speed

    #             if self.__sprite.top >= self.__vertical_bounds[0] :
    #                 self.__sprite.top = self.__vertical_bounds[0]
    #                 if self.__speed > 0:
    #                     self.__speed *= -1

    #             if self.__sprite.bottom <= self.__vertical_bounds[1] :
    #                 self.__sprite.bottom = self.__vertical_bounds[1]
    #                 if self.__speed < 0 :
    #                     self.__speed *= -1

    #         case Direction.HORIZONTAL :
    #             assert self.__horizontal_bounds is not None

    #             self.__sprite.center_x += self.__speed

    #             if self.__sprite.left <= self.__horizontal_bounds[0] :
    #                 self.__sprite.left = self.__horizontal_bounds[0]
    #                 if self.__speed < 0:
    #                     self.__speed *= -1

    #             if self.__sprite.right >= self.__horizontal_bounds[1] :
    #                 self.__sprite.right = self.__horizontal_bounds[1]
    #                 if self.__speed > 0 :
    #                     self.__speed *= -1

    def move(self) -> None : 
        match self.__direction :
            case Direction.VERTICAL :
                assert self.__vertical_bounds is not None
                self.__sprite.center_y += self.__speed

                if self.__sprite.center_y >= self.__vertical_bounds[0] :
                    self.__speed *= -1

                if self.__sprite.center_y <= self.__vertical_bounds[1] :
                    self.__speed *= -1


            case Direction.HORIZONTAL :
                assert self.__horizontal_bounds is not None
                self.__sprite.center_x += self.__speed

                if self.__sprite.center_x <= self.__horizontal_bounds[0] :
                    self.__speed *= -1

                if self.__sprite.center_x >= self.__horizontal_bounds[1] :
                    self.__speed *= -1
        
