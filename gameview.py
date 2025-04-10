import os
from typing import Optional
import arcade
import constants
from player import Player
from player import WeaponType
from blob import Blob
from monster import Monster
from weapon import Weapon
from sword import Sword
from bow import Bow
from pyglet.graphics import Batch
from bat import Bat
from arrow import Arrow


class GameView(arcade.View):
    """Main in-game view."""

    player_sprite_list: arcade.SpriteList[arcade.Sprite]
    __wall_list: arcade.SpriteList[arcade.Sprite]
    __lava_list: arcade.SpriteList[arcade.Sprite]
    __coin_list: arcade.SpriteList[arcade.Sprite]
    __sword_list: arcade.SpriteList[Sword]
    __weapon_list: arcade.SpriteList[Weapon]
    __bow_list: arcade.SpriteList[Bow]
    __arrow_list: arcade.SpriteList[Arrow]
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
                            if self.__current_map_name == self.__initial_map_name :
                                self.__player = Player(x_coordinate, y_coordinate)
                            else :
                                self.__player.set_position(x_coordinate, y_coordinate)
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
                                case _ :
                                    raise Exception("The map contains an unknown character")
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
        self.__sword_list = arcade.SpriteList()
        self.__bow_list = arcade.SpriteList()
        self.__arrow_list = arcade.SpriteList()
        self.__end_list = arcade.SpriteList(use_spatial_hash=True)

        self.sprite_tuple = (self.player_sprite_list, self.__wall_list, self.__coin_list, self.__lava_list,
                            self.__monster_list, self.__weapon_list, self.__sword_list, self.__bow_list, self.__arrow_list, self.__end_list) 

       

        self.__create_map()
                
        self.player_sprite_list.append(self.__player)
        self.__camera = arcade.camera.Camera2D()
        self.__fixed_camera = arcade.camera.Camera2D()
        self.__camera.position = self.__player.position #type: ignore
        self. __fixed_camera.position = arcade.Vec2(0, 0)

        self.icon = arcade.Sprite()
        self.text_score = arcade.Text("!", self.__fixed_camera.bottom_left.x+10, self.__fixed_camera.bottom_left.y+10, arcade.color.BLACK, 12)
        self.ui_element = (self.icon,self.text_score)
        self.update_user_interface()

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
                self.__player.reset_coin_counter()
                self.setup()

    
    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""

        self.__player.on_key_release(key, modifiers)
        

    def on_mouse_press(self, mouse_x: int, mouse_y: int, button: int, modifiers: int) -> None:
            match button:
                case arcade.MOUSE_BUTTON_LEFT:
                   
                    match self.__player.selected_weapon_type:
                        case WeaponType.SWORD:
                            self.__weapon_list.append(Sword(arcade.Vec2(mouse_x, mouse_y), arcade.Vec2(self.player_x, self.player_y), self.__camera.bottom_left))
                        case WeaponType.BOW:
                            self.__weapon_list.append(Bow(arcade.Vec2(mouse_x, mouse_y), arcade.Vec2(self.player_x, self.player_y), self.__camera.bottom_left))

                case arcade.MOUSE_BUTTON_RIGHT:
                    self.__weapon_list.clear()
                    self.__player.change_weapon()
                                  
    def on_mouse_release(self, mouse_x: int, mouse_y: int, button: int, modifiers: int) -> None:
        match button:
            case arcade.MOUSE_BUTTON_LEFT:
                if self.has_weapon_in_hand and self.__player.selected_weapon_type == WeaponType.BOW :
                    current_weapon = self.__weapon_list[0]
                    if current_weapon.is_active :
                        assert(type(current_weapon) == Bow)
                        self.__arrow_list.append(Arrow(current_weapon))
                self.__weapon_list.clear()

            

    def on_mouse_motion(self, mouse_x: int, mouse_y: int, buttons: int, modifiers: int) -> None:
        for weapon in self.__weapon_list:
            weapon.update_angle(arcade.Vec2(mouse_x, mouse_y), arcade.Vec2(self.player_x, self.player_y), self.__camera.bottom_left)

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.
        This is where in-world time "advances" or "ticks". """

        if self.player_y < -500 :
            self.__setup_from_initial()

        self.physics_engine.update()

        for monster in self.__monster_list :
            monster.move(self.__wall_list)

        for weapon in self.__weapon_list :
            weapon.update_position(arcade.Vec2(self.player_x, self.player_y))

        for arrow in self.__arrow_list :
            arrow.move()

        
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
            self.__player.coin_score_update()
            self.update_user_interface()
            arcade.play_sound(arcade.load_sound(":resources:sounds/coin5.wav"))            
                                                                            
        for arrow in self.__arrow_list :
            for monster_hit in arcade.check_for_collision_with_list(arrow, self.__monster_list) :
                for monster in arcade.check_for_collision_with_list(arrow, self.__monster_list) :
                    monster.die()
                    arrow.remove_from_sprite_lists()
                    arcade.play_sound(arcade.load_sound(":resources:sounds/hurt4.wav")) 
                #arrow.remove_from_sprite_lists()
            for wall_hit in arcade.check_for_collision_with_list(arrow, self.__wall_list) :
                arrow.remove_from_sprite_lists()
                arcade.play_sound(arcade.load_sound(":resources:sounds/rockHit2.ogg"))

           
        if self.has_weapon_in_hand and self.__player.selected_weapon_type == WeaponType.SWORD :
            current_weapon = self.__weapon_list[0]
            if current_weapon.is_active :
                for monster in arcade.check_for_collision_with_list(current_weapon, self.__monster_list) :
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

    def update_user_interface(self) -> None :
        """"geres les compteur et icones sur l'ecran"""
        string_score ="Coin score = " + str(self.__player.coin_score)
        self.text_score.text = string_score

    def on_draw(self) -> None:
        """Render the screen."""

        self.clear() # always start with self.clear()
        with self.__camera.activate():
            for list in self.sprite_tuple :
                list.draw()

        with self.__fixed_camera.activate(): 
                self.text_score.draw()
            
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
    
    @property
    def has_weapon_in_hand(self) -> bool :
        if len(self.__weapon_list) == 0 :
            return False
        return True
    
    #needed for the tests

    @property
    def get_wall_list(self) -> arcade.SpriteList[arcade.Sprite]:
        return self.__wall_list
    
    @property
    def get_monster_list(self) -> arcade.SpriteList[Monster]:
        return self.__monster_list
    
    @property
    def get_weapon_list(self) -> arcade.SpriteList[Weapon]:
        return self.__weapon_list
    
    @property
    def get_arrow_list(self) -> arcade.SpriteList[Arrow]:
        return self.__arrow_list
    

    