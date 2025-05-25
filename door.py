import arcade
import constants

class Door(arcade.Sprite):

    __slots__ = ('__closed', )

    def __init__ (self, position_x: float, position_y: float) -> None:
        super().__init__(":resources:images/tiles/lockYellow.png", constants.SCALE)
        self.__closed = True
        self.center_x = position_x
        self.center_y = position_y

    def close(self) -> None :
        self.__closed = True
        self.alpha =  255 

    def open(self) -> None :
        self.__closed = False
        self.alpha = 64 

    @property
    def is_closed(self) -> bool :
        return self.__closed
        


