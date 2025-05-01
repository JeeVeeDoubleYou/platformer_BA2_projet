import arcade
import constants

class Door(arcade.Sprite):


    def __init__ (self, starts_closed: bool = True) -> None:
        super().__init__("lockYellow.png", constants.SCALE)
        self.__closed = starts_closed
        if not self.__closed:
            self.rgb = 255, 255, 255 # ATTENTION : sert a rien pour l'instant

    def close(self) -> None :
        self.__closed = True
        # Do coloring

    def open(self) -> None :
        self.__closed = False
        # Do coloring

    @property
    def is_closed(self) -> bool :
        return self.__closed
        


