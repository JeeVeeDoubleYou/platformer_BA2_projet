from pathlib import Path
import sys

import pytest
from gameview import GameView
import arcade



def test_levers_maps(window: arcade.Window) -> None :
    """
    Tests that all maps in directory ""maps/levers_testing_maps" 
    raise and exception in GameView 
    """

    for file_path in Path("maps/levers_testing_maps").iterdir():
        if file_path.is_file():
            with pytest.raises(Exception) :
                view = GameView(str(file_path))
                window.show_view(view)
