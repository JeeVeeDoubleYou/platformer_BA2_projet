import arcade 
import constants

"""Speed of the blue blobs"""
BLUE_BLOB_SPEED = 2

class Blob(arcade.Sprite):
    """Represents a blob, how it moves and checks for collistions"""

    def __init__(self, x: float, y: float) -> None :
        
        super().__init__(":resources:/images/enemies/slimeBlue.png", constants.SCALE)
        
        self.speed = BLUE_BLOB_SPEED

        self.center_x = x
        self.center_y = y

    def move(self, wall_list : arcade.SpriteList[arcade.Sprite]) -> None:
        """Makes blob move without falling or hitting boxes, changes direction when necessary"""
        
        self.strafe(self.speed)

        self.center_x += 20*self.speed
        self.center_y -= 10

        # Bool that checks if the blob is on the edge of a platform at current time
        is_on_edge = (arcade.check_for_collision_with_list(self, wall_list) == [])

        self.center_x -= 20*self.speed
        self.center_y += 10

        # Checks if blob is on the edge of the platform or if it is touching a wall other than the floor underneath it
        if arcade.check_for_collision_with_list(self, wall_list) != [] or is_on_edge:
            self.speed = -self.speed
            self.texture.flip_left_right

    def die(self) -> None:
        """Makes the blob disappear"""
        self.remove_from_sprite_lists()