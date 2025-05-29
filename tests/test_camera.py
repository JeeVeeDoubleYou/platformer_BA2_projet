import arcade
from gameview import GameView
from constants import WINDOW_HEIGHT, WINDOW_WIDTH, CAMERA_Y_MARGIN, CAMERA_X_MARGIN


def test_camera(window: arcade.Window) -> None: 
    view = GameView("maps/testing_maps/camera_test_map.txt")
    window.show_view(view)

    view.on_key_press(arcade.key.LEFT, 0)

    for i in range(0, 30) :
        window.test(5)
        assert(x_is_in_range(view))

    view.on_key_release(arcade.key.LEFT, 0)

    view.on_key_press(arcade.key.RIGHT, 0)

    for i in range(0, 30) :
        window.test(10)
        assert(x_is_in_range(view))

    view.on_key_press(arcade.key.UP, 0)
    window.test(25)
    view.on_key_release(arcade.key.RIGHT, 0)

    for i in range(0, 10) :
        window.test(10)
        assert(y_is_in_range(view))

def test_camera_avec_platformes(window: arcade.Window) -> None: 
    view = GameView("maps/testing_maps/vertical_camera_platform_map.txt")
    window.show_view(view)


    for i in range(0, 30) :
        window.test(5)
        assert(x_is_in_range(view))
        assert(y_is_in_range(view))

def x_is_in_range(view : GameView) -> bool :
    return abs(calculate_delta_x(view)) <= (WINDOW_WIDTH/2) - CAMERA_X_MARGIN + 10 
    # The test conditions make the camera vibrate when the player colides with a box, 
    # which alters the position slightly. In order to account for that, we add a small buffer area

def y_is_in_range(view : GameView) -> bool :
    return abs(calculate_delta_y(view)) <= (WINDOW_HEIGHT/2) - CAMERA_Y_MARGIN + 10


def calculate_delta_x(view : GameView) -> float :

    camera_left_x = view.camera_x
    camera_center_x = camera_left_x + WINDOW_WIDTH/2

    player_x = view.player_x

    return player_x - camera_center_x

def calculate_delta_y(view : GameView) -> float :

    camera_center_y = view.camera_y

    player_y = view.player_y

    return player_y - camera_center_y