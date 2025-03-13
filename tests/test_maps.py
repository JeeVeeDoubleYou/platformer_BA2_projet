import arcade
import pytest
from gameview import GameView


def test_bad_maps(window: arcade.Window) -> None: 

    with pytest.raises(Exception, match="Configuration lines on file aren't formated correctly") :
        view = GameView("maps/bad_maps/bad_config.txt")
    
    # ATTENTION : Doesn't work with all bad config


    with pytest.raises(Exception, match="Width and height should be positive numbers") :
        view = GameView("maps/bad_maps/negative_height.txt")

    with pytest.raises(Exception, match="Width and height should be positive numbers") :
        view = GameView("maps/bad_maps/zero_width.txt")

    with pytest.raises(Exception, match="Width and height should be defined in configuration of file") :
        view = GameView("maps/bad_maps/no_height.txt")

    with pytest.raises(Exception, match="Width and height should be defined in configuration of file") :
        view = GameView("maps/bad_maps/no_config.txt")

    with pytest.raises(Exception, match="Player must have a starting point") :
        view = GameView("maps/bad_maps/no_start.txt")

    with pytest.raises(Exception, match="Player can't be placed twice") :
        view = GameView("maps/bad_maps/two_start.txt")

    with pytest.raises(Exception, match=r"There are too many characters on line .* \(counting from after config\)") :
        view = GameView("maps/bad_maps/too_many_char.txt")


    # Test bad path
    with pytest.raises(SystemExit) :
        view = GameView("maps/bad_maps/no_such_map.txt")
        window.show_view(view)


def test_good_maps(window: arcade.Window) -> None :
    
    view = GameView("maps/map1.txt")
    window.show_view(view)
    view = GameView("maps/map2.txt")
    window.show_view(view)
