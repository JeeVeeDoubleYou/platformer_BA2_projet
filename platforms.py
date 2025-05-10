from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Final

import arcade
import constants
from platform_arrows import PlatformArrows


class Direction(Enum) :
    VERTICAL = auto()
    HORIZONTAL = auto()

class Platform :
    __sprite_set : set[tuple[int, int]] # Set contenant le (center_x, center_y) initial des éléments de la platforme. ! : ils sont en pixels, pas en "cases"
    __direction : Direction | None # Horizontal or Vertical
    __vertical_movement : tuple[int, int] | None # (Up, Down) en pixels
    __horizontal_movement : tuple[int, int] | None # (Left, Right) en pixels

    def __init__(self) -> None :
        self.__direction = None
        self.__vertical_movement = None
        self.__horizontal_movement = None
        self.__sprite_set = set()

    def __repr__(self) -> str:
        return f"Platform({self.sprite_set}) with {self.__direction} direction, moving in {self.__horizontal_movement if self.__horizontal_movement is not None else self.__vertical_movement}"
    
    def __set_movement(self, *, left : int = 0, right : int = 0, up : int = 0, down : int = 0) -> None :
        """Sets the movement of the platform. Should be called with one or both arguments in a direction, 
        will throw an Exception if called with both horizontal and vertical arguments.
        If called with horizontal arguments but direction is already set to vertical, with throw an exception. (Same for vertical)
        If called with only one horizontal/vertical argument, will keep the other as is, or set it to zero.
        If direction isn't already set, will set it.
        """
        horizontal = left != 0 or right != 0
        vertical = up != 0 or down != 0

        if (horizontal and vertical) or (horizontal and self.is_vertical) or (vertical and self.is_horizontal) :
            raise Exception("A platform can't move both vertically and horizontally")
        
        if horizontal :
            if self.__horizontal_movement is None :
                self.__horizontal_movement = (left, right)
            else :
                l, r = self.__horizontal_movement
                if l * left != 0 or r * right != 0 :
                    raise Exception("A platform can't have more that one line of arrows applying to it per direction")
                self.__horizontal_movement = (l if left == 0 else left, r if right == 0 else right)
        if vertical :
            if self.__vertical_movement is None :
                self.__vertical_movement = (up, down)
            else :
                u, d = self.__vertical_movement
                if u * up != 0 or d * down != 0 :
                    raise Exception("A platform can't have more that one line of arrows applying to it per direction")
                self.__vertical_movement = (u if up == 0 else up, d if down == 0 else down)
        
        self.direction = Direction.HORIZONTAL if horizontal else Direction.VERTICAL


    def add_arrow_info(self, arrow : PlatformArrows, count : int) -> None :
        distance = count * constants.PIXELS_IN_BLOCK # Converts number of arrows into number of pixels
        match arrow :
            case PlatformArrows.LEFT :
                self.__set_movement(left=distance)
            case PlatformArrows.RIGHT :
                self.__set_movement(right=distance)
            case PlatformArrows.UP :
                self.__set_movement(up=distance)
            case PlatformArrows.DOWN :
                self.__set_movement(down=distance)
        
    def add_sprite(self, coordinates : tuple[int, int]) -> None :
        """Adds sprite to the platform, using it's initial coordinates."""
        self.__sprite_set.add((coordinates[0] * constants.PIXELS_IN_BLOCK, coordinates[1] * constants.PIXELS_IN_BLOCK))
    
    @property
    def sprite_set(self) -> set[tuple[int, int]] :
        return self.__sprite_set
    
    @property
    def is_vertical(self) -> bool :
        return self.__direction == Direction.VERTICAL
    
    @property
    def is_horizontal(self) -> bool :
        return self.__direction == Direction.HORIZONTAL
    
    @property
    def moves(self) -> bool :
        return not (self.__vertical_movement is None and self.__horizontal_movement is None)
    
    @property
    def movement(self) -> tuple[int, int] | None :
        return self.__horizontal_movement if self.__horizontal_movement is not None else self.__vertical_movement

    @property
    def direction(self) -> Direction | None :
        return self.__direction
    
    @direction.setter
    def direction(self, direction : Direction) -> None :
        assert self.direction is None
        match direction :
            case Direction.VERTICAL :
                assert self.__horizontal_movement is None
            case Direction.HORIZONTAL :
                assert self.__vertical_movement is None
        self.__direction = direction

    
    def contains(self, sprite : arcade.Sprite) -> bool :
        """
        Return True if sprite belongs to platform, False if it doesn't.
        Should *only ever* be called to sprites that haven't moved yet.
        """
        return (sprite.center_y, sprite.center_x) in self.sprite_set