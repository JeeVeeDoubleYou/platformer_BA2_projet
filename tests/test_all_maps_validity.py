from pathlib import Path

import pytest
from gameview import GameView
import arcade


def test_all_valid_maps(window: arcade.Window) -> None :
    """
    Tests that all maps in directories "maps" 
    (not including subdirectories) and in "maps/testing maps"
    don't raise any exception in GameView 
    """

    for file_path in Path("maps").iterdir():
        if file_path.is_file():
            view = GameView(str(file_path))
            window.show_view(view)

    for file_path in Path("maps/testing_maps").iterdir():
        if file_path.is_file():
            view = GameView(str(file_path))
            window.show_view(view)

def test_all_bad_maps(window: arcade.Window) -> None :
    """
    Tests that all maps in directory "maps/bad_maps" 
    raise and exception in GameView 
    """

    for file_path in Path("maps/bad_maps").iterdir():
        if file_path.is_file():
            with pytest.raises(Exception) :
                view = GameView(str(file_path))
                window.show_view(view)