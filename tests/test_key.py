import arcade
import constants
from player import Player
from gameview import GameView


def test_key(window: arcade.Window) -> None:
    view = GameView()
    window.show_view(view)

    #start of the basic test

    # Check initial velocity
    assert view.player_speed_x == 0
    # Let the game run for 0.1 second between each press
    
    # Start moving right (the player should moove to the right)
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(6)
    assert view.player_speed_x == constants.PLAYER_MOVEMENT_SPEED

    # stop moving right (the player should stop moving)
    view.on_key_release(arcade.key.RIGHT, 0)
    window.test(6)
    assert view.player_speed_x == 0

    # Start moving left (the player should moove to the left)
    view.on_key_press(arcade.key.LEFT, 0)
    window.test(6)
    assert view.player_speed_x == -constants.PLAYER_MOVEMENT_SPEED

    
     # stop moving left (the player should stop moving)
    view.on_key_release(arcade.key.LEFT, 0)
    window.test(6)
    assert view.player_speed_x == 0

    #end of the basic test


    # Start moving right
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(6)
     # Start moving left (the player should move to the left)
    view.on_key_press(arcade.key.LEFT, 0)
    window.test(6)
    assert view.player_speed_x == -constants.PLAYER_MOVEMENT_SPEED
    # stop moving right (the player should stil move to the left)
    view.on_key_release(arcade.key.RIGHT, 0)
    window.test(6)
    assert view.player_speed_x == -constants.PLAYER_MOVEMENT_SPEED
    # stop moving left (the player should stop moving)
    view.on_key_release(arcade.key.LEFT, 0)
    window.test(6)
    assert view.player_speed_x == 0

    # Start moving left
    view.on_key_press(arcade.key.LEFT, 0)
    window.test(6)
    # Start moving right (the player should move to the right)
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(6)
    assert view.player_speed_x == constants.PLAYER_MOVEMENT_SPEED
    # stop moving left (the player should stil move to the right)
    view.on_key_release(arcade.key.LEFT, 0)
    window.test(6)
    assert view.player_speed_x == constants.PLAYER_MOVEMENT_SPEED
    # stop moving right (the player should stop moving)
    view.on_key_release(arcade.key.RIGHT, 0)
    window.test(6)
    assert view.player_speed_x == 0


    # Start moving right
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(6)
    # Start moving left
    view.on_key_press(arcade.key.LEFT, 0)
    window.test(6)
    # stop moving left (the player should resume moving to the right)
    view.on_key_release(arcade.key.LEFT, 0)
    window.test(6)
    assert view.player_speed_x == constants.PLAYER_MOVEMENT_SPEED
    # stop moving right (the player should stop moving)
    view.on_key_release(arcade.key.RIGHT, 0)
    window.test(6)
    assert view.player_speed_x == 0

    # Start moving left
    view.on_key_press(arcade.key.LEFT, 0)
    window.test(6)
    # Start moving right
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(6)
    # stop moving right (the player should resume moving to the left)
    view.on_key_release(arcade.key.RIGHT, 0)
    window.test(6)
    assert view.player_speed_x == -constants.PLAYER_MOVEMENT_SPEED
    # stop moving left (the player should stop moving)
    view.on_key_release(arcade.key.LEFT, 0)
    window.test(6)
    assert view.player_speed_x == 0

def test_reset(window: arcade.Window) -> None :

    view = GameView("maps/testing_maps/easy_next_level1.txt")
    window.show_view(view)

    assert view.current_map == "maps/testing_maps/easy_next_level1.txt"
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(100)
    assert view.current_map == "maps/testing_maps/easy_next_level2.txt"
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(10)
    view.on_key_press(arcade.key.ESCAPE, 0)
    assert view.current_map == "maps/testing_maps/easy_next_level2.txt"
    view.on_key_press(arcade.key.ESCAPE, arcade.key.MOD_SHIFT)
    assert view.current_map == "maps/testing_maps/easy_next_level1.txt"
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(10)
    assert view.current_map == "maps/testing_maps/easy_next_level1.txt"










