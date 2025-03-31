import os
from typing import Optional
import arcade
import constants
from player import Player
from blob import Blob
from monster import Monster
from weapon import Weapon
from pyglet.graphics import Batch
from bat import Bat


class GameView(arcade.View):
    """Main in-game view."""

    player_sprite_list: arcade.SpriteList[arcade.Sprite]
    __wall_list: arcade.SpriteList[arcade.Sprite]
    __lava_list: arcade.SpriteList[arcade.Sprite]
    __coin_list: arcade.SpriteList[arcade.Sprite]
    __weapon_list: arcade.SpriteList[Weapon]
    __monster_list: arcade.SpriteList[Monster]
    __end_list: arcade.SpriteList[arcade.Sprite]
    physics_engine: arcade.PhysicsEnginePlatformer
    __camera: arcade.camera.Camera2D
    __fixed_camera: arcade.camera.Camera2D



    __next_map : Optional[str]

    def __init__(self, map_name : str = "maps/testing_maps/default_map.txt") -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        if not os.path.exists(map_name) :
            raise Exception("The file path for initial level is incorrect")
        self.__initial_map_name = map_name
        self.__current_map_name = self.__initial_map_name
        self.__next_map = None

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
    
        # Setup our game
        self.setup()

        

    def __create_map(self) -> None : 
        """Creates map from file"""

        with open(self.__current_map_name, "r", encoding="utf-8", newline='') as f :
            map_width = None
            map_height = None
            self.__next_map = None
            for line in f :
                if line == "---\n" or line == "---" :
                    break
                line.split()
                if line.startswith("next-map") :
                    if self.__next_map is not None :
                        raise Exception("You can't set the next map twice")
                    self.__next_map = line.split()[-1]
                    if not os.path.exists(self.__next_map) :
                        raise Exception("The next map path is incorrect")
                try : 
                    if line.startswith("width") :
                        if map_width is not None :
                            raise Exception("You can't set the width twice")
                        map_width = int(line.split()[-1])
                    if line.startswith("height") :
                        if map_height is not None :
                            raise Exception("You can't set the height twice")
                        map_height = int(line.split()[-1])
                except ValueError :
                    raise Exception("Configuration lines on file aren't formated correctly")
                # What to do with other parameters?
            if (map_width == None or map_height == None) :
                raise Exception("Width and height should be defined in configuration of file")
            if (map_width <= 0 or map_height <= 0) :
                raise Exception("Width and height should be positive numbers")
            
            start_is_placed = False
            has_next_map = self.__next_map is not None
            end_is_placed = False

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
                        case "S" :
                            if start_is_placed :
                                raise Exception("Player can't be placed twice")
                            start_is_placed = True
                            self.__player = Player(x_coordinate, y_coordinate)
                        case "o" :
                            blob = Blob(x_coordinate, y_coordinate)
                            self.__monster_list.append(blob)
                        case "v" :
                            bat = Bat(x_coordinate, y_coordinate)
                            self.__monster_list.append(bat)
                        case " " | "\n" :
                            # Pour que les espaces et retours à la ligne
                            # ne soient pas gérés dans l'autre 'match', où tout caractère est mis dans une sprite list
                            pass
                        case _ :
                            match sprite :
                                case "E" :
                                    if not has_next_map :
                                        raise Exception("There is no next map, but there is an exit") 
                                        # Question : accepter end of map même sans prochain niveau?
                                    if end_is_placed :
                                        raise Exception("There can't be two ending points to a level")
                                    end_is_placed = True
                                    name_and_list = (":resources:/images/tiles/signExit.png", self.__end_list)
                                case "=" :
                                    name_and_list = (":resources:images/tiles/grassMid.png", self.__wall_list)
                                case "-" :
                                    name_and_list = (":resources:/images/tiles/grassHalf_mid.png", self.__wall_list)
                                case "x" :
                                    name_and_list = (":resources:/images/tiles/boxCrate_double.png", self.__wall_list)
                                case "*" :
                                    name_and_list = (":resources:images/items/coinGold.png", self.__coin_list)
                                case "£" :
                                    name_and_list = (":resources:/images/tiles/lava.png", self.__lava_list)
                            name_and_list[1].append(arcade.Sprite(name_and_list[0], center_x= x_coordinate, 
                                                    center_y= y_coordinate, scale=constants.SCALE))             
        if not start_is_placed :
            raise Exception("Player must have a starting point")
        if has_next_map and not end_is_placed :
            raise Exception("The file sets the next map but no end to the level")


    def setup(self) -> None:
        """Set up the game here."""

        # Initialisation of all lists
        self.player_sprite_list = arcade.SpriteList()
        self.__wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.__coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.__lava_list = arcade.SpriteList(use_spatial_hash=True)
        self.__monster_list = arcade.SpriteList()
        self.__weapon_list = arcade.SpriteList()
        self.__end_list = arcade.SpriteList(use_spatial_hash=True)

        self.sprite_tuple = (self.player_sprite_list, self.__wall_list, self.__coin_list, self.__lava_list,
                            self.__monster_list, self.__weapon_list, self.__end_list) 

        self.__create_map()
                
        self.player_sprite_list.append(self.__player)
        self.__camera = arcade.camera.Camera2D()
        self.__fixed_camera = arcade.camera.Camera2D()
        self.__camera.position = self.__player.position #type: ignore
        self. __fixed_camera.position = arcade.Vec2(0, 0)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.__player,
            walls=self.__wall_list,
            gravity_constant = constants.PLAYER_GRAVITY
        )

        self.__player.physics_engine = self.physics_engine
        

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""

        self.__player.on_key_press(key, modifiers)

        match key:   
            case arcade.key.ESCAPE if modifiers & arcade.key.MOD_SHIFT :
                # reset game from start
                self.__setup_from_initial()
            case arcade.key.ESCAPE:
                # reset level
                self.setup()

    
    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""

        self.__player.on_key_release(key, modifiers)
        

    def on_mouse_press(self, mouse_x: int, mouse_y: int, button: int, modifiers: int) -> None:
            match button:
                case arcade.MOUSE_BUTTON_LEFT:
                    """calclule la difference x et y entre la souris et le joueur"""
                    delta_x=mouse_x+self.__camera.bottom_left.x-self.__player.center_x
                    delta_y=mouse_y+self.__camera.bottom_left.y-self.__player.center_y-5
                    weapon = Weapon(delta_x, delta_y, self.__player.center_x ,self.__player.center_y)
                    self.__weapon_list.append(weapon)
                    #weapon = Weapon.__init__(angle)
                    #self.__weapon_list.append(weapon)
                                  
    def on_mouse_release(self, mouse_x: int, mouse_y: int, button: int, modifiers: int) -> None:
        match button:
            case arcade.MOUSE_BUTTON_LEFT:
                for weapon in self.__weapon_list:
                        weapon.remove_from_sprite_lists()

    def on_mouse_motion(self, mouse_x: int, mouse_y: int, _buttons: int, _modifiers: int) -> None:
        """calclule la difference x et y entre la souris et le joueur"""
        delta_x=mouse_x+self.__camera.bottom_left.x-self.__player.center_x
        delta_y=mouse_y+self.__camera.bottom_left.y-self.__player.center_y-5
        for weapon in self.__weapon_list:
            Weapon.set_angle(weapon, delta_x, delta_y)

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.
        This is where in-world time "advances" or "ticks". """

        for monster in self.__monster_list :
            monster.move(self.__wall_list)
        
        for weapon in self.__weapon_list:
            Weapon.move(weapon, self.__player.center_x ,self.__player.center_y)
        
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
        Checks collisions between player and lava or monster : dies
        Checks collisions between weapon and monster : monster dies
        """

        for coin in arcade.check_for_collision_with_list(self.__player, self.__coin_list) :
            coin.remove_from_sprite_lists()
            Player.coin_score_update(self.__player, 1)
            arcade.play_sound(arcade.load_sound(":resources:sounds/coin5.wav"))

        for weapon in self.__weapon_list:
           if Weapon.hit_frame(weapon, 5):
                for monster in arcade.check_for_collision_with_list(weapon, self.__monster_list) :
                    monster.die()
                    arcade.play_sound(arcade.load_sound(":resources:sounds/hurt4.wav"))

        if arcade.check_for_collision_with_list(self.__player, self.__lava_list) != [] :
            self.__setup_from_initial()
        if arcade.check_for_collision_with_list(self.__player, self.__monster_list) != [] :
            self.__setup_from_initial()
        if arcade.check_for_collision_with_list(self.__player, self.__end_list) != [] :
            self.__load_next_map()

    def __load_next_map(self) -> None :
        assert self.__next_map is not None
        assert os.path.exists(self.__next_map)
        self.__current_map_name = self.__next_map
        self.__next_map = None
        self.setup()

    def __setup_from_initial(self) -> None :
        assert os.path.exists(self.__initial_map_name)
        self.__current_map_name = self.__initial_map_name
        self.setup()


    def on_draw(self) -> None:
        """Render the screen."""

        self.clear() # always start with self.clear()
        with self.__camera.activate():
            for list in self.sprite_tuple :
                list.draw()
        string_score ="coin score = " + str(self.__player.coin_score)
        text = arcade.Text(string_score, self.__fixed_camera.bottom_left.x+10, self.__fixed_camera.bottom_left.y+10, arcade.color.BLACK, 12)
        with self.__fixed_camera.activate():
                text.draw()
            #text.draw()
            

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
    
    @property
    def current_map(self) -> str:
        return self.__current_map_name
    
    @property
    def coin_count(self) -> int:
        return len(self.__coin_list)
    