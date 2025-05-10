import arcade
import sys
from gameview import GameView
from constants import WINDOW_HEIGHT, WINDOW_WIDTH
# Constants

WINDOW_TITLE = "Platformer"

def main() -> None:
    """Main function."""

    try :
        # Create the (unique) Window, setup our GameView, and launch
        window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        if len(sys.argv) > 1 :
            map_name = sys.argv[1]
        else :
            map_name = "maps/moving_map.txt"
        game_view = GameView(map_name)
        window.show_view(game_view)
        arcade.run()
    except Exception as e :
        print(f"ERROR in {map_name} : {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
