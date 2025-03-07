import arcade

"""Lateral speed of the player, in pixels per frame"""
PLAYER_MOVEMENT_SPEED = 5

"""Gravity applied to the player, in pixels per frame"""
PLAYER_GRAVITY = 1

"""Instant vertical speed for jumping, in pixels per frame"""
PLAYER_JUMP_SPEED = 18

"""Scale for all sprites"""
SCALE = 0.5

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

        self.player_sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        map_name = "maps/broken_map.txt"

        with open(map_name, "r", encoding="utf-8", newline='') as f:
     
            try :
                map_width = None
                map_height = None
                for line in f :
                    if line == "---\n" or line == "---" :
                        break
                    line.split()
                    try : 
                        if line.startswith("width") :
                            map_width = int(line.split()[-1])
                        if line.startswith("height") :
                            map_height = int(line.split()[-1])
                    except ValueError :
                        raise Exception("Configuration lines one file aren't formated correctly")
                    # What to do with other parameters?
                if (map_width == None or map_height == None) :
                    raise Exception("Width and height should be defined in configuration of file")
                if (map_width <= 0 or map_height <= 0) :
                    raise Exception("Width and height should be positive numbers")
                
                start_is_placed = False
                # Starts looping from where last loop stopped
                for line_num, line in enumerate(f) :
                    line_number_arcade_coordinates = map_height - (line_num + 1)
                    # To match line number with convention that first line is h-1, last line is 0
                    if line_number_arcade_coordinates < 0 :
                        break
                    if len(line) > map_width + 1 :
                        raise Exception(f"There are too many characters on line {line_num + 1}")    
                    for position_x, sprite in enumerate(line) :
                        x_coordinate = 64 * position_x
                        y_coordinate =  64 * line_number_arcade_coordinates
                        match sprite : 
                            case "=" :
                                self.wall_list.append(arcade.Sprite(
                                ":resources:images/tiles/grassMid.png",
                                center_x= x_coordinate,
                                center_y= y_coordinate,
                                scale=SCALE
                                ))
                            case "-" :
                                self.wall_list.append(arcade.Sprite(
                                ":resources:/images/tiles/grassHalf_mid.png",
                                center_x= x_coordinate,
                                center_y= y_coordinate,
                                scale=SCALE
                                ))
                            case "x" :
                                self.wall_list.append(arcade.Sprite(
                                ":resources:/images/tiles/boxCrate_double.png",
                                center_x= x_coordinate,
                                center_y= y_coordinate,
                                scale=SCALE
                                ))
                            case "*" :
                                self.coin_list.append(arcade.Sprite(
                                ":resources:images/items/coinGold.png",
                                center_x= x_coordinate,
                                center_y= y_coordinate,
                                scale=SCALE
                                ))
                            case "o" :
                                self.coin_list.append(arcade.Sprite(
                                ":resources:/images/enemies/slimeBlue.png",
                                center_x= x_coordinate,
                                center_y= y_coordinate,
                                scale=SCALE
                                ))
                                # Needs to be implemented first (change "coin type, cause incorrect")
                            case "£" :
                                self.wall_list.append(arcade.Sprite(
                                ":resources:/images/tiles/lava.png",
                                center_x= x_coordinate,
                                center_y= y_coordinate,
                                scale=SCALE
                                ))
                                # Needs to be implemented first (change "wall type, cause incorrect")
                            case "S" :
                                if start_is_placed :
                                    raise Exception("Player can't be placed twice")
                                else : 
                                    start_is_placed = True
                                    self.player_sprite = arcade.Sprite(
                                    ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
                                    center_x= x_coordinate,
                                    center_y= y_coordinate,
                                    scale=SCALE
                                    )
            except Exception as e:
                print("ERROR : ", e)
                raise SystemExit(1)


        # Il faut mettre des else apres raise exception? À checker
        # Dans case, répétition de code...
                

        self.player_sprite_list.append(self.player_sprite)
        self.camera = arcade.camera.Camera2D()
        self.camera.position = self.player_sprite.position #type: ignore

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.wall_list,
            gravity_constant=PLAYER_GRAVITY
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""

        match key:
            case arcade.key.RIGHT | arcade.key.D:
                # start moving to the right
                self.player_sprite.change_x = +PLAYER_MOVEMENT_SPEED
        
            case arcade.key.LEFT | arcade.key.A :
                # start moving to the left
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            
            case arcade.key.UP | arcade.key.W | arcade.key.SPACE:
                # jump by giving an initial vertical speed
                self.player_sprite.center_y -= 20
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

        match key:
            case arcade.key.RIGHT | arcade.key.D:
                # stop lateral movement
                if self.player_sprite.change_x > 0:
                    self.player_sprite.change_x = 0
            case arcade.key.LEFT | arcade.key.A:
                if self.player_sprite.change_x < 0:
                    self.player_sprite.change_x = 0

            #pourrait avoire probleme avec plateformes qui bouges

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.
        This is where in-world time "advances" or "ticks". """

        self.physics_engine.update()

        camera_x, camera_y = self.camera.position
        if (self.camera.center_right.x < self.player_sprite.center_x + 400):
            camera_x += PLAYER_MOVEMENT_SPEED
        elif (self.camera.center_left.x > self.player_sprite.center_x - 400):
            camera_x -= PLAYER_MOVEMENT_SPEED
        
        if ((self.camera.top_center[1] < self.player_sprite.center_y + 150) or (self.camera.bottom_center[1] + 250 > self.player_sprite.center_y)):
            camera_y += self.player_sprite.change_y

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

    
