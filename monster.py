from abc import abstractmethod
import constants
import arcade

class Monster(arcade.Sprite):
    """A monster with a way to move and to die. 
    Monster is an abstract class, so it can't be instantiated.
    The class extends arcade.Sprite
    """

    def __init__(self, texture : str) -> None :
        super().__init__(texture, constants.SCALE)

    @abstractmethod
    def move(self, wall_list : arcade.SpriteList[arcade.Sprite] | None = None) -> None:
        """Moves the monster"""
        ...

    def die(self) -> None:
        """Kills the monster meaning removes it from it game"""
        self.remove_from_sprite_lists()