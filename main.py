import arcade
from gameview import GameView
# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"


def main() -> None:
    """Main function."""

    try :
        # Create the (unique) Window, setup our GameView, and launch
        window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        game_view = GameView("maps/level_1.txt")
        window.show_view(game_view)
        arcade.run()
    except Exception as e :
        print("ERROR : ", e)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
