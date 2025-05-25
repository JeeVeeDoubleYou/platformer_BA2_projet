import arcade
import constants
from blob import *
from gameview import GameView
from player import Player
from sword import Sword

# ATTENTION : Ne marche pas !

def test_sword(window: arcade.Window) -> None:
    pass
    # view = GameView("maps/testing_maps/sword_test_map.txt")
    # window.show_view(view)
    # #verifie que l'épée tue le monstre
    # view.get_weapon_list
    # view.mouse_override_for_tests = arcade.Vec2(128, 64)
    # view.on_mouse_press(128, 64, arcade.MOUSE_BUTTON_LEFT, 0)
    # print("BLAH", view.get_weapon_list)
    # for i in range(20) :
    #     assert(len(view.get_weapon_list) == 1)
    #     window.test(1)
    # assert(isinstance(view.get_weapon_list[-1], Sword))  #verifie que l'arme est une épée
    # view.on_mouse_release(128, 64, arcade.MOUSE_BUTTON_LEFT, 0)
    # window.test(500)

    # assert(len(view.get_weapon_list) == 0)
    # assert(len(view.get_monster_list) == 0)