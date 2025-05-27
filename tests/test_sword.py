import arcade
import constants
from blob import *
from gameview import GameView
from player import Player
from sword import Sword

# Same tests, with swords pointing in different directions. Answers week 4, question 2.

def test_sword(window: arcade.Window) -> None:
    view = GameView("maps/testing_maps/sword_test_map.txt")
    window.show_view(view)
    #verifie que l'épée tue le monstre
    view.on_mouse_press(1000, 300, arcade.MOUSE_BUTTON_LEFT, 0)
    assert(len(view.get_weapon_list) == 1)
    window.test(35)
    assert(isinstance(view.get_weapon_list[-1], Sword))  #verifie que l'arme est une épée
    view.on_mouse_release(128, 64, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(1)    
    assert(len(view.get_weapon_list) == 0)
    assert(len(view.get_monster_list) == 0)

def test_wrong(window: arcade.Window) -> None:
    view = GameView("maps/testing_maps/sword_test_map.txt")
    window.show_view(view)
    #verifie que l'épée ne tue pas le monstre
    view.on_mouse_press(0, 0, arcade.MOUSE_BUTTON_LEFT, 0)
    assert(len(view.get_weapon_list) == 1)
    window.test(35)
    assert(isinstance(view.get_weapon_list[-1], Sword))  #verifie que l'arme est une épée
    view.on_mouse_release(0, 0, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(1)    
    assert(len(view.get_weapon_list) == 0)
    assert(len(view.get_monster_list) == 1)