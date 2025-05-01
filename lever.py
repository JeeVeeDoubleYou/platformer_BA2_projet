import arcade
from door import Door
import constants

class Lever(arcade.Sprite):

    def __init__ (self, x: float, y:float, one_time_use : bool, starts_activated : bool = False) -> None:
        if starts_activated:
            super().__init__(":resources:images/tiles/leverRight.png", constants.SCALE)
        else:
            super().__init__(":resources:images/tiles/leverLeft.png", constants.SCALE)
        self.on_activation_close = []
        self.on_activation_open = []
        self.on_deactivation_close = []
        self.on_deactivation_open = []
        self.one_time_use = one_time_use        #check if the lever break after activation
        self.broken = False                 #check if the lever is brocken or not
        self.activated = starts_activated        #the activation status of the lever (on/off)
        self.center_x = x
        self.center_y = y

    def link_doors(self, activation_close : list[Door], activation_open : list[Door], 
                 deactivation_close : list[Door], deactivation_open : list[Door]) -> None :
        self.on_activation_close = activation_close
        self.on_activation_open = activation_open
        self.on_deactivation_close = deactivation_close
        self.on_deactivation_open = deactivation_open

    def on_action(self) -> None:
        if self.broken :
            return
        
        self.activated = not self.activated

        if self.one_time_use:
            self.broken = True
            self.color = 255, 255, 255, 128
    
        if self.activated:
            for door in self.on_activation_open:
                door.open()
            for door in self.on_activation_close:
                door.close()
            self.texture = arcade.load_texture(":resources:images/tiles/leverLeft.png")
                
        else:
            for door in self.on_deactivation_open:
                door.open()
            for door in self.on_deactivation_close:
                door.close()
            self.texture = arcade.load_texture(":resources:images/tiles/leverRight.png")
        




