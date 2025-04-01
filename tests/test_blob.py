import arcade
import constants
from blob import *
from gameview import GameView


#le test marche principalement car il n'y a aucun blob sur la map 

# def test_key(window: arcade.Window) -> None:
#     view = GameView()
#     window.show_view(view)

#     for x in range (0, 128)  :
#         for blob in view.blob_list :
#             assert arcade.check_for_collision_with_list(blob, view.wall_list) == []
#             blob.center_y -= 10
#             assert arcade.check_for_collision_with_list(blob, view.wall_list) != []
#             blob.center_y += 10
#             window.test(1)


# BAD TEST, TO REWRITE