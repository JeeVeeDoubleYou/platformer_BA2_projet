import arcade

"""Lateral speed of the player, in pixels per frame"""
PLAYER_MOVEMENT_SPEED = 5

"""Gravity applied to the player, in pixels per frame"""
PLAYER_GRAVITY = 1

"""Instant vertical speed for jumping, in pixels per frame"""
PLAYER_JUMP_SPEED = 19

"""going left"""
LEFT = False

"""going left"""
RIGHT = False


class GameView(arcade.View):
    """Main in-game view."""

    player_sprite: arcade.Sprite
    player_sprite_list: arcade.SpriteList[arcade.Sprite]
    wall_list: arcade.SpriteList[arcade.Sprite]
    coin_list: arcade.SpriteList[arcade.Sprite]
    

    physics_engine: arcade.PhysicsEnginePlatformer
    camera: arcade.camera.Camera2D

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
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.camera = arcade.camera.Camera2D()
        self.camera.position = self.player_sprite.position #type: ignore


        for x in range(0, 1250, 64) :
            self.wall_list.append(arcade.Sprite(
                ":resources:images/tiles/grassMid.png",
                center_x=x,
                center_y=32,
                scale=0.5
            ))

        for x in [256,512,768] :
            self.wall_list.append(arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png",
                center_x=x,
                center_y=96,
                scale=0.5
            ))

        for x in range (128,1250,256) :
            self.coin_list.append(arcade.Sprite(
                ":resources:images/items/coinGold.png",
                center_x=x,
                center_y=96,
                scale=0.5
            ))

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.wall_list,
            gravity_constant=PLAYER_GRAVITY
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""
        #print(LEFT)
        match key:
            case arcade.key.RIGHT | arcade.key.D:
                # start moving to the right
                self.player_sprite.change_x += PLAYER_MOVEMENT_SPEED
                RIGHT = True
                LEFT = False
        
            case arcade.key.LEFT | arcade.key.A :
                # start moving to the left
                self.player_sprite.change_x -= PLAYER_MOVEMENT_SPEED
                LEFT = True
                RIGHT = False
            
            case arcade.key.UP | arcade.key.W | arcade.key.SPACE:
                # jump by giving an initial vertical speed
                self.player_sprite.center_y -= 20
                print(arcade.check_for_collision_with_list(self.player_sprite, self.wall_list))
                a=len(arcade.check_for_collision_with_list(self.player_sprite, self.wall_list))
                if a != 0:
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
                    arcade.play_sound(arcade.load_sound(":resources:sounds/jump3.wav"))
                self.player_sprite.center_y += 20
                
            
            case arcade.key.ESCAPE:
                # reset game
                self.setup()
    
    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""
        print(LEFT)

        match key:
            case arcade.key.RIGHT | arcade.key.D:
                # stop lateral movement
                if LEFT == False:
                    self.player_sprite.change_x -= PLAYER_MOVEMENT_SPEED
            case arcade.key.LEFT | arcade.key.A:
                if RIGHT == False:
                    self.player_sprite.change_x += PLAYER_MOVEMENT_SPEED

                    

            #pourrait avoir des probleme avec les plateformes qui bouges

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.
        This is where in-world time "advances" or "ticks". """

        self.physics_engine.update()

        camera_x, camera_y = self.camera.position
        if (self.camera.center_right[0] < self.player_sprite.center_x + 400):
            camera_x += 5
        elif (self.camera.center_left[0] > self.player_sprite.center_x - 400):
            camera_x -= 5
        
        if (self.camera.top_center[1] < self.player_sprite.center_y + 150):
            camera_y += 5
        elif (self.camera.bottom_center[1] > self.player_sprite.center_y - 250):
            camera_y -= 5
        # not convinced by recentering of platform, check back later when player must climb platforms

        self.camera.position = arcade.Vec2(camera_x, camera_y)

        for coin in arcade.check_for_collision_with_list(self.player_sprite, self.coin_list) :
            coin.remove_from_sprite_lists()
            arcade.play_sound(arcade.load_sound(":resources:sounds/coin5.wav"))

    def on_draw(self) -> None:
        """Render the screen."""

        self.clear() # always start with self.clear()

        with self.camera.activate():
            self.wall_list.draw()
            self.player_sprite_list.draw()
            self.coin_list.draw()

    
