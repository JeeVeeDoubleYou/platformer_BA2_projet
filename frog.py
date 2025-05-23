import arcade 
import constants
import random
from blob import Blob


"""Speed of the blue blobs"""
FROG_SPEED = -1       # is negative to make the frog move in the direction it is facing (technicality)
JUMP_SPEED = 10
FROG_GRAVITY = 1

class Frog(Blob):
    """Represents a blob, how it moves and checks for collistions"""

    def __init__(self, x: float, y: float,) -> None :
        self.initial_y = y-22
        super().__init__(x, y-22)
        self.texture = arcade.load_texture("assets/kenney-extended-enemies-png/frog.png")
        self.sync_hit_box_to_texture()
        self.speed = FROG_SPEED

    def move(self, wall_list : arcade.SpriteList[arcade.Sprite]) -> None:
        if self.center_y <= self.initial_y:
            self.center_y = self.initial_y
            if random.randint(1,50) == 1:
                self.change_y = 18
                self.center_y += self.change_y
                # arcade.play_sound(arcade.load_sound(":resources:sounds/jump2.wav"))
            Blob.move(self,wall_list)
        else:
            self.change_y -= FROG_GRAVITY
            self.center_y += self.change_y
        
        
        
    
    