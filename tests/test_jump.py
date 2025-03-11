import arcade

from gameview import *


def test_jump(window: arcade.Window) -> None:
    view = GameView()
    window.show_view(view)
    
   
    view.on_key_press(arcade.key.UP, 0)
    assert view.player_sprite.change_y == PLAYER_JUMP_SPEED
    
    #we wait one frame and try to jump while in the air each frame while in the air 
    # window.test(1)
    #using math we deduce that the jump should last 19*2 - 2 frame of landing and jumping so 36 frame
    while view.physics_engine.can_jump(5) == False :
        window.test(1)
        view.on_key_press(arcade.key.UP, 0)
        assert view.player_sprite.change_y < PLAYER_JUMP_SPEED
    

   # NO CODING TEST THAT FAIL WHILE PROGRAM WORKS AS INTENDED
    

