from monster import Monster
import arcade

class Bat(Monster):
    """Represents a bat, defines how it moves"""

    def __init__(self, x: float, y: float) -> None :
        
        super().__init__("assets/kenney-extended-enemies-png/bat.png")

        self.center_x = x
        self.center_y = y

    def move(self, wall_list : arcade.SpriteList[arcade.Sprite] | None = None) -> None:
       "Makes the bat move"
       
       pass