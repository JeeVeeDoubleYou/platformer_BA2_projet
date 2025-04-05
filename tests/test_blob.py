import arcade
import constants
from blob import *
from gameview import GameView


def test_blob(window: arcade.Window) -> None:
    view = GameView("maps/testing_maps/blob_test_map.txt")
    window.show_view(view)
    for x in range (0, 60)  :
        for blob in view.get_monster_list :
            if isinstance(blob,Blob):
                assert arcade.check_for_collision_with_list(blob, view.get_wall_list) == []
                blob.center_y -= 10
                assert arcade.check_for_collision_with_list(blob, view.get_wall_list) != []
                blob.center_y += 10
                window.test(1)
    start_position_x = view.player_x    # take the starting player position
    start_position_y = view.player_y 
    view.on_key_press(arcade.key.RIGHT, 0)       #stat moving into the lava
    window.test(60)
    assert(start_position_x == view.player_x )          # normaly the player is suposed to die and go back to its starting point
    assert(start_position_y == view.player_y )


# BAD TEST, TO REWRITE

