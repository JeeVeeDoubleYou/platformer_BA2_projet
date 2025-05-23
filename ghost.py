import arcade 
import constants
from blob import Blob

"""Speed of the ghost blobs"""
GHOST_SPEED = -1       # is negative to make the slime move in the direction it is facing (technicality)
SPAWN_HEIGHT = 10     # ATTENTION : What is this? Also, shoudn't it be defined in cconstants?

class Ghost(Blob):
    """Represents a blob, how it moves and checks for collistions"""

    def __init__(self, x: float, y: float,) -> None :
        
        super().__init__(x, y-SPAWN_HEIGHT)
        self.texture = arcade.load_texture("assets/kenney-extended-enemies-png/ghost.png")
        self.sync_hit_box_to_texture()
        self.speed = GHOST_SPEED
        self.alpha = 255

    # ATTENTION : Documenter le alpha (transparence), bonne facon d'appeler d'appeler le super move?
    def move(self, wall_list : arcade.SpriteList[arcade.Sprite]) -> None:
        Blob.move(self,wall_list)
        if self.alpha > 10:
            self.alpha -= 1 
    