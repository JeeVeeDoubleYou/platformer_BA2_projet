from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Final
import constants


class Direction(Enum) :
    VERTICAL = auto()
    HORIZONTAL = auto()

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
        # ATTENTION : Can (and should) be cleaned up, later.
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