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
    view.on_mouse_press(500, 300, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(5)
    assert(isinstance(view.get_weapon_list[-1],Sword))  #verifie que l'arme est une épée
    view.on_mouse_release(500, 300, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(5)

    assert(len(view.get_weapon_list) == 0)
    assert(len(view.get_monster_list) == 0)

    view.on_mouse_press(500, 300, arcade.MOUSE_BUTTON_RIGHT, 0) #change d'arme
    view.on_mouse_press(500, 300, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(5)
    assert(not isinstance(view.get_weapon_list[-1],Sword))      #verifie que l'arme n'est plus une épée
    view.on_mouse_release(500, 300, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(5)

    view.on_mouse_press(500, 300, arcade.MOUSE_BUTTON_RIGHT, 0) #re-change d'arme
    view.on_mouse_press(500, 300, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(5)
    assert(isinstance(view.get_weapon_list[-1],Sword))      #verifie que l'arme est de nouveau une épée
    view.on_mouse_release(500, 300, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(5)


    
    




