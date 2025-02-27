import arcade


class GameView(arcade.View):
    """Main in-game view."""

    player_sprite: arcade.Sprite
    player_sprite_list: arcade.SpriteList[arcade.Sprite]
    wall_list: arcade.SpriteList[arcade.Sprite]

    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # Setup our game
        self.setup()

    def setup(self) -> None:
        """Set up the game here."""

        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
            center_x=64,
            center_y=128
        )
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)
        self.wall_list = arcade.SpriteList()

        for x in range(0, 1250-64, 64) :
            self.wall_list.append(arcade.Sprite(
                ":resources:images/tiles/grassMid.png" ,
                center_x=x ,
                center_y=32 ,
                scale=0.5
            ))

        for x in range(256, 769, 256) :
            self.wall_list.append(arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png" ,
                center_x=x ,
                center_y=96 ,
                scale=0.5
            ))

            



    def on_draw(self) -> None:
        """Render the screen."""

        self.clear() # always start with self.clear()
        self.player_sprite_list.draw()
        self.wall_list.draw()
        
