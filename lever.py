import arcade
from door import Door
import constants

class Lever(arcade.Sprite):

    """
    Represents a lever on the map that can be toggled to open or close doors.

    A Lever can:
        - Be toggled (activated/deactivated)
        - Trigger specific doors to open/close on activation and deactivation
        - Be marked as "broken" (unusable) after one use if configured
    """

    __slots__ = ('on_activation_close', 'on_activation_open', 'on_deactivation_close', 'on_deactivation_open',
                 'off_deactivate', 'on_deactivate', '__broken', 'activated', )

    def __init__ (self, x: float, y:float) -> None :
        super().__init__(":resources:images/tiles/leverRight.png", constants.SCALE*1)
        self.on_activation_close : list[Door] = []
        self.on_activation_open : list[Door] = []
        self.on_deactivation_close : list[Door] = []
        self.on_deactivation_open : list[Door] = []
        self.off_deactivate = False  
        self.on_deactivate = False  
        self.__broken = False                 #check if the lever is broken or not
        self.activated = False        #the activation status of the lever (on/off)
        self.center_x = x
        self.center_y = y

    def link_doors(self, activation_close : list[Door], activation_open : list[Door], 
                 deactivation_close : list[Door], deactivation_open : list[Door], on_deactivate : bool = False, off_deactivate : bool = False,
                 start_on : bool = False) -> None :
        
        """Configures the lever's behavior: which doors it affects and its initial state."""
        
        self.off_deactivate = off_deactivate
        self.on_deactivate = on_deactivate
        self.activated = start_on
        if self.activated:
            self.texture = arcade.load_texture(":resources:images/tiles/leverRight.png")
        self.on_activation_close = activation_close
        self.on_activation_open = activation_open
        self.on_deactivation_close = deactivation_close
        self.on_deactivation_open = deactivation_open

    @property
    def is_active(self) -> bool :
        return not self.__broken

    def on_action(self) -> None:
        """
        Called when lever is hit with sword or arrow. 
        Could take into account other hit collisions, in the future. 
        Toggles the lever's state and triggers the appropriate door actions.
        """
        if self.__broken :
            return
        
        self.activated = not self.activated

        if self.activated:
            if self.on_deactivate:
                self.__broken = True
                self.alpha =  128
            for door in self.on_activation_open:
                door.open()
            for door in self.on_activation_close:
                door.close()
            self.texture = arcade.load_texture(":resources:images/tiles/leverLeft.png")
                
        else:
            if self.off_deactivate:
                self.__broken = True
                self.alpha =  128
            for door in self.on_deactivation_open:
                door.open()
            for door in self.on_deactivation_close:
                door.close()
            self.texture = arcade.load_texture(":resources:images/tiles/leverRight.png")

        self.sync_hit_box_to_texture()