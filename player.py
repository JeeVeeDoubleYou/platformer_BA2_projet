import arcade
import constants
from weapon import Weapon
from weapon_type import WeaponType


class Player(arcade.Sprite):
    """
    Represents the player sprite in the game.

    Manages its movements, animations and interactions with the world.
    """
    

    __slots__ = ('physics_engine', 'coin_score', 'is_going_left', 
                 'is_going_right', 'allow_multi_jump', 'allowed_jumps', 'selected_weapon_type', )

    def __init__(self, x: float, y: float) -> None :
        super().__init__(":resources:/images/animated_characters/female_adventurer/femaleAdventurer_idle.png", constants.SCALE)
        self.physics_engine : arcade.PhysicsEnginePlatformer | None = None
        self.set_position(x, y)
        self.coin_score = 0
        self.is_going_left = False
        self.is_going_right = False
        self.allow_multi_jump : bool = False
        self.allowed_jumps : int = 1

        self.selected_weapon_type : WeaponType = WeaponType.SWORD

    def __repr__(self) -> str :
        return f"Player({self.position})"

    def coin_score_update (self) -> None:
        """Updates coin score by one."""
        self.coin_score += 1

    def change_weapon(self) -> None:
        """
        Switches the available weapon in hand. Calls to this function should always be preceded by clearing the
        weapon list in order to fully correlate the selected_weapon_type, which is the type of weapon a player could have in hand,
        with the type of weapon that the player really has in hand, if it has one.
        """
        self.selected_weapon_type = WeaponType((self.selected_weapon_type + 1) % len(WeaponType))

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
                    if self.physics_engine.can_jump(5):
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

    def set_position(self, new_x : float, new_y : float) -> None :
        """Sets new position for player without creating new instance of Player."""
        self.center_x = new_x
        self.center_y = new_y

    def create_weapon(self, mouse_position : arcade.Vec2, camera_bottom_left : arcade.Vec2) -> Weapon :
        """Create a weapon instance based on player's selected weapon and mouse position."""
        self_position = arcade.Vec2(self.center_x, self.center_y)
        return self.selected_weapon_type.create_weapon(mouse_position, self_position, camera_bottom_left)

