import arcade
import constants
from player import Player
from gameview import GameView


def test_lave(window: arcade.Window) -> None:
    view = GameView("maps/testing_maps/lava_test_map.txt")
    window.show_view(view)
    start_position_x = view.player_x    # take the starting player position
    start_position_y = view.player_y 
    view.on_key_press(arcade.key.RIGHT, 0)       #stat moving into the lava
    window.test(60)
    assert(start_position_x == view.player_x )          # normaly the player is suposed to die and go back to its starting point
    assert(start_position_y == view.player_y )
        