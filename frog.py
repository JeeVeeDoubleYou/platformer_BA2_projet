import arcade 
import constants
import random
from blob import Blob

class Frog(Blob):
    """Represents a frog enemy that jumps randomly but moves horizontally like a Blob."""

    __slots__ = ()

    def __init__(self, x: float, y: float) -> None :
        """
        Initialize the frog at position (x, y), adjusting for sprite offset.
        """
        super().__init__(x, y-22)
        self.initial_y = y-22
        self.texture = arcade.load_texture("assets/kenney-extended-enemies-png/frog.png")
        self.sync_hit_box_to_texture()
        self.speed = constants.FROG_SPEED

    def move(self, wall_list : arcade.SpriteList[arcade.Sprite], _ : arcade.Vec2) -> None:
        """
        Moves the frog horizontally (like a blob) and makes it jump randomly when on the ground.
        """
        if self.center_y <= self.initial_y :
            self.center_y = self.initial_y
            if random.randint(1,50) == 1:
                self.change_y = 18
                self.center_y += self.change_y
            super().move(wall_list, _)
        else :
            self.change_y -= constants.FROG_GRAVITY
            self.center_y += self.change_y
        
        
        
    
    