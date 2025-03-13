import arcade
import constants

class Player():
    """
    Represents the player sprite in the game.

    Manages its movements, animations and interactions with the world.
    """

    physics_engine : arcade.PhysicsEnginePlatformer | None
    player_sprite: arcade.Sprite

    def __init__(self) -> None :

        self.physics_engine = None

    


    is_going_left = False
    is_going_right = False

    allow_multi_jump: bool
    allowed_jumps: int
    allow_multi_jump = False
    allowed_jumps = 1

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        Called by gameview when the user presses a key on the keyboard.
        Makes the player move. 
        """

        match key:
            case arcade.key.RIGHT | arcade.key.D:
                # start moving to the right
                self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED
                self.is_going_right = True
        
            case arcade.key.LEFT | arcade.key.A :
                # start moving to the left
                self.player_sprite.change_x = -constants.PLAYER_MOVEMENT_SPEED
                self.is_going_left = True
            

            
            case arcade.key.UP | arcade.key.W | arcade.key.SPACE:
                # jump by giving an initial vertical speed
                if self.physics_engine is not None : 
                    if self.physics_engine.can_jump(5) :
                        self.player_sprite.change_y = constants.PLAYER_JUMP_SPEED
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
                    self.player_sprite.change_x = 0
                    
                else :
                    self.player_sprite.change_x = -constants.PLAYER_MOVEMENT_SPEED

            case arcade.key.LEFT | arcade.key.A:
                self.is_going_left = False
                if self.is_going_right == False:
                    self.player_sprite.change_x = 0
                else :
                    self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED