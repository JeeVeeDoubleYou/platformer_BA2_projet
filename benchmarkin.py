import timeit
import arcade
import constants
import cProfile
from player import Player

def test_collision_check():
    player_sprite = Player(0, 0)
    lava_list = arcade.SpriteList(use_spatial_hash=True)
    for x in range(10000):
        lava = arcade.Sprite(":resources:/images/tiles/lava.png", center_x = x*64, center_y = 0 , scale = constants.SCALE)
        lava_list.append(lava)
    number = 1000
    res = timeit.timeit(lambda: arcade.check_for_collision_with_list(player_sprite, lava_list), number = number)
    print(res,'ms')


if __name__ == "__benchmarking__":
    profiler = cProfile.Profile()
    profiler.enable()
    test_collision_check()
    profiler.disable()
    profiler.dump_stats("profile.prof")
    print("Profil sauvegardé dans profile.prof")
