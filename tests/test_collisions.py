import arcade
from gameview import GameView


def test_key(window: arcade.Window) -> None:
    view = GameView("maps/testing_maps/default_map.txt")
    window.show_view(view)

    # Check position of player doesn't change when against a crate. Also checks that player doesn't fall through the floor.
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(30)
    position_before_box_x, position_before_box_y = view.player_x, view.player_y
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(30)
    view.on_key_release(arcade.key.RIGHT, 0)
    assert position_before_box_x == view.player_x
    assert position_before_box_y  == view.player_y

    # Player falls when not on ground
    view.on_key_press(arcade.key.ESCAPE, 0)
    starting_y = view.player_y
    view.on_key_press(arcade.key.LEFT, 0)
    window.test(40)
    assert starting_y != view.player_y