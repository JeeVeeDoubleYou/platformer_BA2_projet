import arcade
import pytest
from gameview import GameView
import re


def test_bad_maps(window: arcade.Window) -> None: 

    # Test bad path
    with pytest.raises(Exception, match="The file path for initial level is incorrect") :
        view = GameView("maps/bad_maps/no_such_map.txt")

    with pytest.raises(Exception, match="Configuration lines on file aren't formated correctly") :
        view = GameView("maps/bad_maps/no_config.txt")

    with pytest.raises(Exception, match="The width must be an integer") :
        view = GameView("maps/bad_maps/non_int_width.txt")

    with pytest.raises(Exception, match="Width and height should be positive numbers") :
        view = GameView("maps/bad_maps/negative_height.txt")

    with pytest.raises(Exception, match="Width and height should be defined and non-zero in configuration of file") :
        view = GameView("maps/bad_maps/zero_width.txt")

    with pytest.raises(Exception, match="Width and height should be defined and non-zero in configuration of file") :
        view = GameView("maps/bad_maps/no_height.txt")

    with pytest.raises(Exception, match="Player must have a starting point") :
        view = GameView("maps/bad_maps/no_start.txt")

    with pytest.raises(Exception, match="Player can't be placed twice") :
        view = GameView("maps/bad_maps/two_start.txt")

    with pytest.raises(Exception, match="There is a line with more characters than 20") :
        view = GameView("maps/bad_maps/too_many_char.txt")

    with pytest.raises(Exception, match="The map contains an unknown character") :
        view = GameView("maps/bad_maps/bad_character.txt")

    with pytest.raises(Exception, match="The map isn't exactly 8 lines long") :
        view = GameView("maps/bad_maps/too_long_map.txt")

    with pytest.raises(Exception, match=re.escape(f"There is no lever at (x, y) = {(4, 1)}")) :
        view = GameView("maps/bad_maps/bad_lever_door_map/wrong_lever_placement.txt")

    with pytest.raises(Exception, match="Please, use integer to precise the lever coordinate") :
        view = GameView("maps/bad_maps/bad_lever_door_map/bad_lever_coordinates.txt")

    with pytest.raises(Exception, match=re.escape(f"lever given at {(1000, 1)} is outside of the map")) :
        view = GameView("maps/bad_maps/bad_lever_door_map/lever_oustide_the_map.txt")
    
    with pytest.raises(Exception, match=re.escape(f"door given at {(1000, 1)} is outside of the map")) :
        view = GameView("maps/bad_maps/bad_lever_door_map/door_outside_the_map.txt")

    with pytest.raises(Exception, match=re.escape(f"There is no door at (x, y) = {(3, 1)}")) :
        view = GameView("maps/bad_maps/bad_lever_door_map/bad_door_palcement.txt")

    with pytest.raises(Exception, match=re.escape(f"unknown action")) :
        view = GameView("maps/bad_maps/bad_lever_door_map/bad_lever_action.txt")

        

def test_good_maps(window: arcade.Window) -> None :
    
    view = GameView("maps/map1.txt")
    window.show_view(view)
    view = GameView("maps/map2.txt")
    window.show_view(view)

    # File with next-map
    view = GameView("maps/testing_maps/easy_next_level1.txt")
    window.show_view(view)

def test_chaining_levels(window: arcade.Window) -> None :

    with pytest.raises(Exception, match="The next map path is incorrect") :
        view = GameView("maps/bad_maps/bad_next-map_name.txt")
        window.show_view(view)

    with pytest.raises(Exception, match="There can't be two ending points to a level") :
        view = GameView("maps/bad_maps/two_exits.txt")
        window.show_view(view)
    
    with pytest.raises(Exception, match="The file sets the next map but no end to the level") :
        view = GameView("maps/bad_maps/next-map_and_no_exit.txt")
        window.show_view(view)