import arcade
from gameview import GameView
from constants import WINDOW_HEIGHT, WINDOW_WIDTH
import sys

WINDOW_TITLE = "Platformer"


def main() -> None:
    """Main function."""

    # Create the (unique) Window, setup our GameView, and launch
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    if len(sys.argv) > 1 :
        map_name = sys.argv[1]
    else :
        map_name = "maps/level_1.txt"
    game_view = GameView(map_name)
    window.show_view(game_view)
    arcade.run()

    game_view.profiler.dump_stats("profile.prof")


if __name__ == "__main__":
    main()
