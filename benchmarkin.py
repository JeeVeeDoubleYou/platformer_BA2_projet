import timeit
import arcade
import constants
import cProfile
from player import Player
from gameview import GameView

def test_collision_check(window: arcade.Window):
    player_sprite = Player(0, 0)
    view = GameView("maps/testing_maps/bat_test_map.txt")
    window.show_view(view)
    lava_list = arcade.SpriteList(use_spatial_hash=True)
    for x in range(10000):
        lava = arcade.Sprite(":resources:/images/tiles/lava.png", center_x = x*64, center_y = 0 , scale = constants.SCALE)
        lava_list.append(lava)
    number = 1000
    res = timeit.timeit(lambda: view.on_update(), number = number)
    print(res,'ms')


if __name__ == "__benchmarking__":
    profiler = cProfile.Profile()
    profiler.enable()
    test_collision_check()
    profiler.disable()
    profiler.dump_stats("profile.prof")
    print("sauvgarder dans profile.prof")
