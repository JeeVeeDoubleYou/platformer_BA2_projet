import arcade
import constants
from blob import *
from gameview import GameView
from player import Player
from sword import Sword


def test_sword(window: arcade.Window) -> None:
    view = GameView("maps/testing_maps/sword_test_map.txt")
    window.show_view(view)
    #verifie que l'épée tue le monstre
    view.on_mouse_press(1000, 300, arcade.MOUSE_BUTTON_LEFT, 0)
    assert(len(view.get_weapon_list) == 1)
    window.test(150)
    assert(isinstance(view.get_weapon_list[-1], Sword))  #verifie que l'arme est une épée
    view.on_mouse_release(128, 64, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(50)    
    assert(len(view.get_weapon_list) == 0)
    assert(len(view.get_monster_list) == 0)