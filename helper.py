from typing import Final

def matrix_line_num_to_arcade(line : int, total_height : int) -> int :
        """Tranforms a line number taken from looping through the map matrix to the line number considered by arcade.
        Arcade convention is top line is height - 1, last line is 0."""
        assert (line < total_height)
        return total_height - (line + 1)

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