import arcade
from blob import *
from gameview import GameView
from sword import Sword
from weapon import Weapon
from bow import Bow
from arrow import Arrow


def test_bow(window: arcade.Window) -> None:

    view = GameView("maps/testing_maps/camera_test_map.txt")
    window.show_view(view)
    #verifie que l'épée tue le monstre
    view.on_mouse_press(1000, 300, arcade.MOUSE_BUTTON_RIGHT, 0)

    view.on_mouse_press(1000, 300, arcade.MOUSE_BUTTON_LEFT, 0)
    assert(len(view.get_weapon_list) == 1)
    assert(isinstance(view.get_weapon_list[-1], Bow))  #verifie que l'arme est un arc
    window.test(10)
    view.on_mouse_release(128, 64, arcade.MOUSE_BUTTON_LEFT, 0)
    assert(len(view.get_arrow_list) == 0)
    assert(len(view.get_weapon_list) == 0) 
    view.on_mouse_press(1000, 300, arcade.MOUSE_BUTTON_LEFT, 0)
    assert(len(view.get_weapon_list) == 1)
    assert(isinstance(view.get_weapon_list[-1], Bow))  #verifie que l'arme est un arc 
    window.test(50)
    view.on_mouse_release(10, 1000, arcade.MOUSE_BUTTON_LEFT, 0) 
    assert(len(view.get_arrow_list) == 1)
    assert(len(view.get_weapon_list) == 0)