import os
import arcade
import constants
from player import Player
from blob import Blob


class GameView(arcade.View):
    """Main in-game view."""

    player_sprite_list: arcade.SpriteList[arcade.Sprite]
    wall_list: arcade.SpriteList[arcade.Sprite]
    lava_list: arcade.SpriteList[arcade.Sprite]
    coin_list: arcade.SpriteList[arcade.Sprite]
    blob_list: arcade.SpriteList[Blob]
    physics_engine: arcade.PhysicsEnginePlatformer
    __camera: arcade.camera.Camera2D


    def __init__(self, map_name : str = "maps/default_map.txt") -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        if not os.path.exists(map_name) :
            raise SystemExit(1)
        self.__map_name = map_name

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # Setup our game
        self.setup()

        

    def create_map(self) -> None : 
        """Creates map from file"""

        with open(self.__map_name, "r", encoding="utf-8", newline='') as f :
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
                    raise Exception("Configuration lines on file aren't formated correctly")
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
                    raise Exception(f"There are too many characters on line {line_num + 1} (counting from after config)")    
                for position_x, sprite in enumerate(line) :
                    x_coordinate = 64 * position_x
                    y_coordinate =  64 * line_number_arcade_coordinates
                    match sprite : 
                        case "=" :
                            self.wall_list.append(arcade.Sprite(
                            ":resources:images/tiles/grassMid.png",
                            center_x= x_coordinate,
                            center_y= y_coordinate,
                            scale=constants.SCALE
                            ))
                        case "-" :
                            self.wall_list.append(arcade.Sprite(
                            ":resources:/images/tiles/grassHalf_mid.png",
                            center_x= x_coordinate,
                            center_y= y_coordinate,
                            scale=constants.SCALE
                            ))
                        case "x" :
                            self.wall_list.append(arcade.Sprite(
                            ":resources:/images/tiles/boxCrate_double.png",
                            center_x= x_coordinate,
                            center_y= y_coordinate,
                            scale=constants.SCALE
                            ))
                        case "*" :
                            self.coin_list.append(arcade.Sprite(
                            ":resources:images/items/coinGold.png",
                            center_x= x_coordinate,
                            center_y= y_coordinate,
                            scale=constants.SCALE
                            ))
                        case "o" :
                            blob = Blob(x_coordinate, y_coordinate)
                            self.blob_list.append(blob)
                        case "£" :
                            self.lava_list.append(arcade.Sprite(
                            ":resources:/images/tiles/lava.png",
                            center_x= x_coordinate,
                            center_y= y_coordinate,
                            scale=constants.SCALE
                            ))
                        case "S" :
                            if start_is_placed :
                                raise Exception("Player can't be placed twice")
                            start_is_placed = True
                            self.__player = Player(x_coordinate, y_coordinate)
        if not start_is_placed :
            raise Exception("Player must have a starting point")


    def setup(self) -> None:
        """Set up the game here."""

        # Initialisation of all lists
        self.player_sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.lava_list = arcade.SpriteList(use_spatial_hash=True)
        self.blob_list = arcade.SpriteList()

        self.create_map()
                
        self.player_sprite_list.append(self.__player)
        self.__camera = arcade.camera.Camera2D()
        self.__camera.position = self.__player.position #type: ignore

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.__player,
            walls=self.wall_list,
            gravity_constant = constants.PLAYER_GRAVITY
        )

        self.__player.physics_engine = self.physics_engine
        

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""

        self.__player.on_key_press(key, modifiers)

        match key:   
            case arcade.key.ESCAPE:
                # reset game
                self.setup()
    
    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""

        self.__player.on_key_release(key, modifiers)
        

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.
        This is where in-world time "advances" or "ticks". """

        for blob in self.blob_list :
            blob.blob_move(self.wall_list)

        self.physics_engine.update()
        self.__update_camera()
        self.__check_collisions()
            
    def __update_camera(self) -> None :
        """Updates camera position when player moves/dies"""

        camera_x, camera_y = self.__camera.position
        if (self.__camera.center_right.x < self.__player.center_x + 400):
            camera_x += constants.PLAYER_MOVEMENT_SPEED
        elif (self.__camera.center_left.x > self.__player.center_x - 400):
            camera_x -= constants.PLAYER_MOVEMENT_SPEED

        if ((self.__camera.top_center.y < self.__player.center_y + 150) or (self.__camera.bottom_center.y + 250 > self.__player.center_y)):
            camera_y += self.__player.change_y

        self.__camera.position = arcade.Vec2(camera_x, camera_y)

        # not convinced by recentering of platform, check back later when player must climb platforms

    
    def __check_collisions(self) -> None :
        """
        Checks collisions between player and coins : takes coins
        Checks collisions between player and lava or blobs : dies
        """

        for coin in arcade.check_for_collision_with_list(self.__player, self.coin_list) :
            coin.remove_from_sprite_lists()
            arcade.play_sound(arcade.load_sound(":resources:sounds/coin5.wav"))

        if arcade.check_for_collision_with_list(self.__player, self.lava_list) != [] :
            self.setup()
        if arcade.check_for_collision_with_list(self.__player, self.blob_list) != [] :
            self.setup()

    def on_draw(self) -> None:
        """Render the screen."""

        self.clear() # always start with self.clear()

        with self.__camera.activate():
            self.wall_list.draw()
            self.player_sprite_list.draw()
            self.coin_list.draw()
            self.blob_list.draw()
            self.lava_list.draw()

    @property
    def player_x(self) -> float:
        return self.__player.center_x
    
    @property
    def player_y(self) -> float:
        return self.__player.center_y
    
    @property
    def player_speed_x(self) -> float:
        return self.__player.change_x

    @property
    def player_speed_y(self) -> float:
        return self.__player.change_y
    
    @property
    def camera_x(self) -> float:
        return self.__camera.center_left.x
    
    @property
    def camera_y(self) -> float:
        return self.__camera.center_left.y