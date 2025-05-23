import arcade 
from constants import GHOST_SPEED, GHOST_SPAWN_HEIGHT
from blob import Blob

class Ghost(Blob):
    """Represents a ghost, which is an enemy. Touching a ghost will kill the player."""

    def __init__(self, x: float, y: float,) -> None :
        
        super().__init__(x, y-GHOST_SPAWN_HEIGHT)
        self.texture = arcade.load_texture("assets/kenney-extended-enemies-png/ghost.png")
        self.sync_hit_box_to_texture()
        self.speed = GHOST_SPEED
        self.alpha = 255

    def move(self, wall_list : arcade.SpriteList[arcade.Sprite]) -> None:
        super().move(wall_list)
        self.make_transparent()
    
    def make_transparent(self) -> None :
        """Makes the ghost lighter until almost transparent-"""
        if self.alpha > 10: 
            self.alpha -= 1 