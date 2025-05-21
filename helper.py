from typing import Final

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