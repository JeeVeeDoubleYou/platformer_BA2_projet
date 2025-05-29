import arcade
import pytest
from gameview import GameView


def test_plateforme_direction(window: arcade.Window) -> None:
    view = GameView("maps/testing_maps/plateforme_map.txt")
    window.show_view(view)
    start_position_y = view.player_y
    start_position_x = view.player_x
    #verifie que l'épée tue le monstre
    view.on_key_press(arcade.key.LEFT, 0)
    window.test(10)
    view.on_key_release(arcade.key.LEFT, 0)
    plateforme_position = view.player_y
    window.test(10)    
    assert(plateforme_position > view.player_y)
    view.on_key_press(arcade.key.LEFT, 0)
    window.test(30)
    print(view.player_x)
    view.on_key_release(arcade.key.LEFT, 0)
    assert(start_position_y == view.player_y)




    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(10)
    view.on_key_release(arcade.key.RIGHT, 0)
    plateforme_position = view.player_y
    window.test(10)    
    assert(plateforme_position > view.player_y)
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(20)
    view.on_key_release(arcade.key.RIGHT, 0)
    assert(view.won)
    

