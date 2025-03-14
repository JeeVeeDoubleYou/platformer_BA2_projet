import arcade
import constants
from player import Player
from gameview import GameView


def test_jump(window: arcade.Window) -> None:
    view = GameView()
    window.show_view(view)
    
    view.on_key_press(arcade.key.UP, 0)
    assert view.player_speed_y == constants.PLAYER_JUMP_SPEED
    
    #we wait one frame and try to jump while in the air each frame while in the air 
    # window.test(1)
    #using math we deduce that the jump should last 19*2 - 2 frame of landing and jumping so 36 frames
    while view.physics_engine.can_jump(5) == False :
        window.test(1)
        view.on_key_press(arcade.key.UP, 0)
        assert view.player_speed_y < constants.PLAYER_JUMP_SPEED
    
    

