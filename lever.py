import arcade
from door import Door
import constants

class Lever(arcade.Sprite):

    def __init__ (self, x: float, y:float) -> None:
        super().__init__(":resources:images/tiles/leverRight.png", constants.SCALE*1)
        self.on_activation_close : list[Door] = []
        self.on_activation_open : list[Door] = []
        self.on_deactivation_close : list[Door] = []
        self.on_deactivation_open : list[Door] = []
        self.off_deactivate = False  
        self.on_deactivate = False  
        self.broken = False                 #check if the lever is brocken or not
        self.activated = False        #the activation status of the lever (on/off)
        self.center_x = x
        self.center_y = y

    def link_doors(self, activation_close : list[Door], activation_open : list[Door], 
                 deactivation_close : list[Door], deactivation_open : list[Door], on_deactivate : bool = False, off_deactivate : bool = False,
                 start_on : bool = False) -> None :
        self.off_deactivate = off_deactivate
        self.on_deactivate = on_deactivate
        self.activated = start_on
        if self.activated:
            self.on_action
        self.on_activation_close = activation_close
        self.on_activation_open = activation_open
        self.on_deactivation_close = deactivation_close
        self.on_deactivation_open = deactivation_open

    def on_action(self) -> None:
        if self.broken :
            return
        
        self.activated = not self.activated

        if self.activated:
            if self.on_deactivate:
                self.broken = True
                self.alpha =  128
            for door in self.on_activation_open:
                door.open()
            for door in self.on_activation_close:
                door.close()
            self.texture = arcade.load_texture(":resources:images/tiles/leverLeft.png")
                
        else:
            if self.off_deactivate:
                self.broken = True
                self.alpha =  128
            for door in self.on_deactivation_open:
                door.open()
            for door in self.on_deactivation_close:
                door.close()
            self.texture = arcade.load_texture(":resources:images/tiles/leverRight.png")

        self.sync_hit_box_to_texture()
        




