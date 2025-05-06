from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Final

import arcade
import constants


class Direction(Enum) :
    VERTICAL = auto()
    HORIZONTAL = auto()


class NonPlatformMovement :
    sprite : Final[arcade.Sprite]
    general_direction : Final[Direction]
    bounds : Final[tuple[int, int]] # (Left or Up, Right or Down)
    initial_position : arcade.Vec2
    going_in_initial_direction : bool # initial direction is up or right

    def __init__(self, sprite : arcade.Sprite, general_direction : Direction, bounds : tuple[int, int], initial_position : arcade.Vec2):
        self.sprite = sprite
        self.general_direction = general_direction
        self.bounds = bounds
        self.initial_position = initial_position
        self.going_in_initial_direction = True

    def move(self, recursion : int = 0) -> None : 
        # ATTENTION : Ca marche pas du tout!
        if recursion > 1 :
            return
        recursion += 1
        match self.general_direction :
            case Direction.VERTICAL :
                if self.going_in_initial_direction :
                    if abs((self.sprite.center_y - self.initial_position.y) + constants.PLATFORM_SPEED) <= self.bounds[0] or (self.sprite.center_x < self.initial_position.x)  :
                        self.sprite.center_y += constants.PLATFORM_SPEED
                    else : 
                        self.going_in_initial_direction = False
                        self.move(recursion)
                else : 
                    if abs((self.sprite.center_y - self.initial_position.y) - constants.PLATFORM_SPEED) <= self.bounds[1] or (self.sprite.center_x > self.initial_position.x):
                        self.sprite.center_y -= constants.PLATFORM_SPEED
                    else : 
                        self.going_in_initial_direction = True
                        self.move(recursion)
            case Direction.HORIZONTAL :
                if self.going_in_initial_direction :
                    if abs((self.sprite.center_x - self.initial_position.x) + constants.PLATFORM_SPEED) <= self.bounds[1] - 32 or (self.sprite.center_x + constants.PLATFORM_SPEED) < self.initial_position.x :
                        self.sprite.center_x += constants.PLATFORM_SPEED 
                    else : 
                        self.going_in_initial_direction = False
                        self.move(recursion)
                else : 
                    if abs((self.sprite.center_x - self.initial_position.x) - constants.PLATFORM_SPEED) <= self.bounds[0] - 32 or (self.sprite.center_x - constants.PLATFORM_SPEED) > self.initial_position.x :
                        self.sprite.center_x -= constants.PLATFORM_SPEED
                    else : 
                        self.going_in_initial_direction = True
                        self.move(recursion)


class PlatformArrows(Enum) : 
    LEFT = "←"
    RIGHT = "→"
    UP = "↑"
    DOWN = "↓"

    def count_arrows(self, line : int, column : int, arrows_counted : int, visited : set[tuple[int, int]], map_matrix : list[list[str]]) -> int :
        visited.add((line, column))
        match self :
            case PlatformArrows.LEFT :
                if column == 0 :
                    return arrows_counted
                if map_matrix[line][column - 1] == self.value :
                    return self.count_arrows(line, column - 1, arrows_counted + 1, visited, map_matrix)
            case PlatformArrows.RIGHT :
                if column == len(map_matrix[0]) - 1 :
                    return arrows_counted
                if map_matrix[line][column + 1] == self.value :
                    return self.count_arrows(line, column + 1, arrows_counted + 1, visited, map_matrix)
            case PlatformArrows.UP : 
                if line == 0 :
                    return arrows_counted
                if map_matrix[line - 1][column] == self.value :
                    return self.count_arrows(line - 1, column, arrows_counted + 1, visited, map_matrix)
            case PlatformArrows.DOWN :
                if line == len(map_matrix) - 1 :
                    return arrows_counted
                if map_matrix[line + 1][column] == self.value :
                    return self.count_arrows(line + 1, column, arrows_counted + 1, visited, map_matrix)
        return arrows_counted


class Platform :
    __sprite_set : set[tuple[int, int]] 
    # ATTENTION : Ici on fait *64 pour match avec sprite.center_x/y dans map, mais ca match plus avec movement ducoup
    direction : Direction | None # Horizontal or vertical
    movement : tuple[int, int] # (Left or Up, Right or Down)

    def __init__(self) -> None :
        self.direction = None
        self.movement = (0,0)
        self.__sprite_set = set()

    def __repr__(self) -> str:
        return f"Platform({self.sprite_set}) with {self.direction} direction, moving in {self.movement}"

    def add_arrow_info(self, arrow : PlatformArrows, count : int) -> None :
        # ATTENTION : Can (and should) be cleaned up, later. Also not sure about the count, see comment under sprite set.
        count *= constants.PIXELS_IN_BLOCK
        if self.direction == None :
            if arrow == PlatformArrows.LEFT :
                self.direction = Direction.HORIZONTAL
                self.movement = (count, 0)
            if arrow == PlatformArrows.RIGHT :
                self.direction = Direction.HORIZONTAL
                self.movement = (0, count)
            if arrow == PlatformArrows.UP :
                self.direction = Direction.VERTICAL
                self.movement = (count, 0)
            if arrow == PlatformArrows.DOWN :
                self.direction = Direction.VERTICAL
                self.movement = (0, count)
        else :
            if (self.direction == Direction.HORIZONTAL and (arrow == PlatformArrows.UP or arrow == PlatformArrows.DOWN)) or (self.direction == Direction.VERTICAL and (arrow == PlatformArrows.LEFT or arrow == PlatformArrows.RIGHT)):
                raise Exception("A platform can't move both vertically and horizontaly")
            if ((arrow == PlatformArrows.UP or arrow == PlatformArrows.LEFT) and not self.movement[0] == 0) or ((arrow == PlatformArrows.DOWN or arrow == PlatformArrows.RIGHT) and not self.movement[1] == 0):
                raise Exception("A platform can't be affected by multiple series of arrows going in the same direction")
            if arrow == PlatformArrows.UP or arrow == PlatformArrows.LEFT :
                self.movement = (count, self.movement[1])
            if arrow == PlatformArrows.DOWN or arrow == PlatformArrows.RIGHT :
                self.movement = (self.movement[0], count)
        
    def add_to_sprite_set(self, coordinates : tuple[int, int]) -> None :
        # ATTENTION : Is there some way to overwrite the sprite_set.add function?
        self.__sprite_set.add((coordinates[0] * constants.PIXELS_IN_BLOCK, coordinates[1] * constants.PIXELS_IN_BLOCK))
    
    @property
    def sprite_set(self) -> set[tuple[int, int]] :
        return self.__sprite_set
    
    def contains(self, sprite : arcade.Sprite) -> bool :
        """
        Return True if sprite belongs to platform, False if it doesn't.
        Should *only ever* be called to sprites that haven't moved yet.
        """
        return (sprite.center_y, sprite.center_x) in self.sprite_set
    
    def add_half_to_movement(self) -> None :
        if not self.movement[0] == 0 :
            self.movement = (int(self.movement[0] + 0.5 * constants.PIXELS_IN_BLOCK), self.movement[1])
        if not self.movement[1] == 0 :
            self.movement = (self.movement[0], int(self.movement[1] + 0.5 * constants.PIXELS_IN_BLOCK))
        # ATTENTION : Should not be called where it is called, outside the class, but im not sure where to call it.