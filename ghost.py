import arcade 
import constants
from blob import Blob

class Ghost(Blob):
    """Represents a ghost, which is an enemy. Touching a ghost will kill the player."""

    __slots__ = ()

    def __init__(self, x: float, y: float,) -> None :
        
        super().__init__(x, y - constants.GHOST_SPAWN_HEIGHT)
        self.texture = arcade.load_texture("assets/kenney-extended-enemies-png/ghost.png")
        self.sync_hit_box_to_texture()
        self.speed = constants.GHOST_SPEED
        self.alpha = 255

    def move(self, wall_list : arcade.SpriteList[arcade.Sprite], _ : arcade.Vec2) -> None:
        """Makes the ghost move, like a blob."""
        super().move(wall_list, _)
        self.__make_transparent()
    
    def __make_transparent(self) -> None :
        """Makes the ghost lighter until almost transparent."""
        if self.alpha > 10: 
            self.alpha -= 1 