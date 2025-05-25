from abc import abstractmethod
import constants
import arcade

class Monster(arcade.Sprite):
    """A monster with a way to move and to die. 
    Monster is an abstract class, so it can't be instantiated.
    The class extends arcade.Sprite.
    """

    def __init__(self, texture : str) -> None :
        super().__init__(texture, constants.SCALE)

    @abstractmethod
    def move(self, wall_list : arcade.SpriteList[arcade.Sprite], player_position : arcade.Vec2) -> None :
        """Moves the monster"""
        ...

    def die(self) -> None:
        """Kills the monster, removing it from it game"""
        arcade.play_sound(arcade.load_sound(":resources:sounds/hurt4.wav")) 
        self.remove_from_sprite_lists()