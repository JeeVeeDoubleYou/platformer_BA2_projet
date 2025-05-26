import arcade

from gameview import GameView

INITIAL_COIN_COUNT = 5

def test_collect_coins(window: arcade.Window) -> None: 
    view = GameView("maps/testing_maps/default_map.txt")
    window.show_view(view)

    # Make sure we have the amount of coins we expect at the start
    assert view.coin_count == INITIAL_COIN_COUNT

    # Start moving right
    view.on_key_press(arcade.key.RIGHT, 0)

    # Let the game run for one second
    window.test(60)

    # We should have collected the first coin
    assert view.coin_count == INITIAL_COIN_COUNT - 1

    # Jump to get past the first crate
    view.on_key_press(arcade.key.UP, 0)
    view.on_key_release(arcade.key.UP, 0)

    # Let the game run for one more second
    window.test(60)

    # We should have collected the second coin
    assert view.coin_count == INITIAL_COIN_COUNT - 2