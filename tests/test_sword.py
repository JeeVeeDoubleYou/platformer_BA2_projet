import arcade
from blob import *
from gameview import GameView
from sword import Sword

# Same tests, with swords pointing in different directions. Answers week 4, question 2.

def test_sword_right(window: arcade.Window) -> None:
    view = GameView("maps/testing_maps/sword_test_map.txt")
    window.show_view(view)
    #verifie que l'épée tue le monstre
    for i in range(10):
        view.on_mouse_press(1000, 300, arcade.MOUSE_BUTTON_LEFT, 0)
        window.test(10)
        view.on_mouse_release(1000, 300, arcade.MOUSE_BUTTON_LEFT, 0) 
    window.test(1)    
    assert(len(view.get_weapon_list) == 0)
    assert(len(view.get_monster_list) == 0)

def test_sword_wrong(window: arcade.Window) -> None:
    view = GameView("maps/testing_maps/sword_test_map.txt")
    window.show_view(view)
    #verifie que l'épée ne tue pas le monstre
    for i in range(10):
        view.on_mouse_press(0, 0, arcade.MOUSE_BUTTON_LEFT, 0)
        window.test(10)
        view.on_mouse_release(0, 0, arcade.MOUSE_BUTTON_LEFT, 0) 
    window.test(1)    
    assert(len(view.get_weapon_list) == 0)
    assert(len(view.get_monster_list) == 1)