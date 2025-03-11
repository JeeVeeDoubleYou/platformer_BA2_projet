import arcade

from gameview import GameView
from gameview import *


def test_key(window: arcade.Window) -> None:
    view = GameView()
    window.show_view(view)

    #start of the basic test

    # Check initial velocity
    assert view.player_sprite.change_x == 0
    # Let the game run for 0.1 second between each press
    
    # Start moving right (the player should moove to the right)
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(6)
    assert view.player_sprite.change_x == PLAYER_MOVEMENT_SPEED

    # stop moving right (the player should stop moving)
    view.on_key_release(arcade.key.RIGHT, 0)
    window.test(6)
    assert view.player_sprite.change_x == 0

    # Start moving left (the player should moove to the left)
    view.on_key_press(arcade.key.LEFT, 0)
    window.test(6)
    assert view.player_sprite.change_x == -PLAYER_MOVEMENT_SPEED

    
     # stop moving left (the player should stop moving)
    view.on_key_release(arcade.key.LEFT, 0)
    window.test(6)
    assert view.player_sprite.change_x == 0

    #end of the basic test


    # Start moving right
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(6)
     # Start moving left (the player should move to the left)
    view.on_key_press(arcade.key.LEFT, 0)
    window.test(6)
    assert view.player_sprite.change_x == -PLAYER_MOVEMENT_SPEED
    # stop moving right (the player should stil move to the left)
    view.on_key_release(arcade.key.RIGHT, 0)
    window.test(6)
    assert view.player_sprite.change_x == -PLAYER_MOVEMENT_SPEED
    # stop moving left (the player should stop moving)
    view.on_key_release(arcade.key.LEFT, 0)
    window.test(6)
    assert view.player_sprite.change_x == 0

    # Start moving left
    view.on_key_press(arcade.key.LEFT, 0)
    window.test(6)
    # Start moving right (the player should move to the right)
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(6)
    assert view.player_sprite.change_x == PLAYER_MOVEMENT_SPEED
    # stop moving left (the player should stil move to the right)
    view.on_key_release(arcade.key.LEFT, 0)
    window.test(6)
    assert view.player_sprite.change_x == PLAYER_MOVEMENT_SPEED
    # stop moving right (the player should stop moving)
    view.on_key_release(arcade.key.RIGHT, 0)
    window.test(6)
    assert view.player_sprite.change_x == 0


    # Start moving right
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(6)
    # Start moving left
    view.on_key_press(arcade.key.LEFT, 0)
    window.test(6)
    # stop moving left (the player should resume moving to the right)
    view.on_key_release(arcade.key.LEFT, 0)
    window.test(6)
    assert view.player_sprite.change_x == PLAYER_MOVEMENT_SPEED
    # stop moving right (the player should stop moving)
    view.on_key_release(arcade.key.RIGHT, 0)
    window.test(6)
    assert view.player_sprite.change_x == 0

    # Start moving left
    view.on_key_press(arcade.key.LEFT, 0)
    window.test(6)
    # Start moving right
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(6)
    # stop moving right (the player should resume moving to the left)
    view.on_key_release(arcade.key.RIGHT, 0)
    window.test(6)
    assert view.player_sprite.change_x == -PLAYER_MOVEMENT_SPEED
    # stop moving left (the player should stop moving)
    view.on_key_release(arcade.key.LEFT, 0)
    window.test(6)
    assert view.player_sprite.change_x == 0


    







