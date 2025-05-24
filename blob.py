import arcade 
import constants
from monster import Monster

class Blob(Monster):
    """Represents a blob, how it moves and checks for collistions"""

    def __init__(self, x: float, y: float,) -> None :
        
        super().__init__(":resources:/images/enemies/slimeBlue.png")
        self.speed = constants.BLUE_BLOB_SPEED
        self.center_x = x
        self.center_y = y
        self.alpha = 255

    def move(self, wall_list : arcade.SpriteList[arcade.Sprite]) -> None:
        """Makes blob move without falling or hitting boxes, changes direction when necessary"""

        self.strafe(self.speed)

        # Checks if blob is on the edge of the platform or if it is touching a wall other than the floor underneath it
        if self.can_move(wall_list):
            self.speed = -self.speed
            self.scale_x *= -1      #flip the slime horizontaly
            self.strafe(self.speed)

    def can_move(self, wall_list : arcade.SpriteList[arcade.Sprite]) -> bool:
        self.center_x += 20*self.speed
        self.center_y -= 10
        # Bool that checks if the blob is on the edge of a platform at current time
        is_on_edge = (arcade.check_for_collision_with_list(self, wall_list) == [])
        self.center_x -= 20*self.speed
        self.center_y += 10
        is_not_blocked = arcade.check_for_collision_with_list(self, wall_list) != []
        return is_on_edge or is_not_blocked
        


