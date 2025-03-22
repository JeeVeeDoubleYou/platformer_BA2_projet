import arcade
import constants
import math

class Player(arcade.Sprite):
    """
    Represents the player sprite in the game.

    Manages its movements, animations and interactions with the world.
    """

    physics_engine : arcade.PhysicsEnginePlatformer | None

    def __init__(self, x: float, y: float) -> None :
        super().__init__(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png", constants.SCALE)
        self.physics_engine = None

        self.center_x = x
        self.center_y = y
        self.coin_score=0

    is_going_left = False
    is_going_right = False

    allow_multi_jump: bool
    allowed_jumps: int
    allow_multi_jump = False
    allowed_jumps = 1

    def coin_score_update (self, coin :int) -> None:
        self.coin_score += coin

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        Called by gameview when the user presses a key on the keyboard.
        Makes the player move. 
        """

        match key:
            case arcade.key.RIGHT | arcade.key.D :
                # start moving to the right
                self.change_x = constants.PLAYER_MOVEMENT_SPEED
                self.is_going_right = True
        
            case arcade.key.LEFT | arcade.key.A :
                # start moving to the left
                self.change_x = -constants.PLAYER_MOVEMENT_SPEED
                self.is_going_left = True
            
            case arcade.key.UP | arcade.key.W | arcade.key.SPACE:
                # jump by giving an initial vertical speed
                if self.physics_engine is not None : 
                    if self.physics_engine.can_jump(5) :
                        self.change_y = constants.PLAYER_JUMP_SPEED
                        arcade.play_sound(arcade.load_sound(":resources:sounds/jump3.wav"))

           

    def on_key_release(self, key: int, modifiers: int) -> None:
        """
        Called by gameview when the user releases a key on the keyboard.
        Makes the player stop moving or change directions.
        """
        match key:
            # stop lateral movement
            case arcade.key.RIGHT | arcade.key.D:
                self.is_going_right = False
                if self.is_going_left == False:
                    self.change_x = 0
                    
                else :
                    self.change_x = -constants.PLAYER_MOVEMENT_SPEED

            case arcade.key.LEFT | arcade.key.A:
                self.is_going_left = False
                if self.is_going_right == False:
                    self.change_x = 0
                else :
                    self.change_x = constants.PLAYER_MOVEMENT_SPEED

    