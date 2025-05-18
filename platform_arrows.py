from __future__ import annotations
from enum import Enum


class PlatformArrows(Enum) : 
    LEFT = "←"
    RIGHT = "→"
    UP = "↑"
    DOWN = "↓"

    def count_arrows(self, line : int, column : int, arrows_counted : int, visited : set[tuple[int, int]], map_matrix : list[list[str]]) -> int :
        """Recursive function returning how many consecutive arrows pointing in the same direction there are. 
        Only takes into account if the character in the direction pointed by the arrow is another of ther same arrow. 
        """
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


    @staticmethod    
    def get_arrow_enum(arrow : str) -> PlatformArrows :
        """Gets an arrow name from it's string representation : example Arrows.LEFT from "←". 
        Should only ever get called with an argument that is an arrow. """
        assert arrow in {a.value for a in PlatformArrows}
        match arrow :
            case "←" :
                return PlatformArrows.LEFT
            case "→" :
                return PlatformArrows.RIGHT 
            case "↑" :
                return PlatformArrows.UP
            case "↓" :
                return PlatformArrows.DOWN
            case _ :
                raise Exception("Invalid arrow ", {arrow})