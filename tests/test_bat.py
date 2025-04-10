import math
import arcade
from bat import ACTION_RADIUS
from gameview import GameView


def test_bat(window: arcade.Window) -> None: 
    view = GameView("maps/testing_maps/bat_test_map.txt")
    window.show_view(view)

    monster_list = view.get_monster_list
    bat = monster_list[0] # Only one monster in this map
    
    initial_bat_x = bat.center_x
    initial_bat_y = bat.center_y

    for i in range(0, 200) :
        window.test(1)
        current_bat_x = bat.center_x
        current_bat_y = bat.center_y
        assert(math.sqrt((current_bat_x - initial_bat_x)**2 + (current_bat_y - initial_bat_y)**2) <= ACTION_RADIUS)