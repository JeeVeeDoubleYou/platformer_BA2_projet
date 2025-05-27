from typing import Final

import arcade

import constants 
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
        
        self.__vertical_bounds = (int(self.__initial_position.y + movement[0]), int(self.__initial_position.y - movement[1]))
    
        self.__horizontal_bounds = (int(self.__initial_position.x - movement[0]), int(self.__initial_position.x + movement[1]))
        
        # Info : Il faudrait changer tous les mouvement pour associer top à droite (plutôt que top à gauche), 
        # comme ca on a pas besoin du match direction car movement[0] sera la direction initiale, mais il faudrait changer une bonne
        # partie du code pour que se soit cohérent, je n'ai pas le temps.

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

    def move(self) -> None : 
        """Makes non_platform_moving_blocks move."""
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
        
