import os
import sys
import arcade
import constants
from non_platform_moving_blocks import NonPlatformMovingBlocks
from player import Player
from monster import Monster
from weapon import Weapon
from arrow import Arrow
from lever import Lever
from door import Door
from map import Map
from UI import UI
from custom_exception import CustomException

from map_movement import MapMovement

import cProfile


class GameView(arcade.View):
    """Main in-game view."""
    
    profiler: cProfile.Profile
    

    __player_sprite_list: arcade.SpriteList[arcade.Sprite]
    __wall_list: arcade.SpriteList[arcade.Sprite]
    __list_of_sprites_in_platforms : arcade.SpriteList[arcade.Sprite]
    __lava_list: arcade.SpriteList[arcade.Sprite]
    __coin_list: arcade.SpriteList[arcade.Sprite]
    __weapon_list: arcade.SpriteList[Weapon]
    __arrow_list: arcade.SpriteList[Arrow]
    __monster_list: arcade.SpriteList[Monster]
    __lever_list: arcade.SpriteList[Lever]
    __door_list: arcade.SpriteList[Door]
    __solid_block_list: arcade.SpriteList[arcade.Sprite]
    __end_list: arcade.SpriteList[arcade.Sprite]
    __non_platform_moving_sprites_list : list[NonPlatformMovingBlocks]
    physics_engine: arcade.PhysicsEnginePlatformer | None
    __camera: arcade.camera.Camera2D

    __fixed_camera: arcade.camera.Camera2D

    __player : Player
    __next_map : str | None

    __has_won : bool # Internal variable for __won property
    __has_error : bool # Internal variable for __error property


    def __init__(self, map_name : str = "maps/testing_maps/default_map.txt") -> None:


        # Magical incantion: initialize the Arcade view
        super().__init__()

        self.__error = False
        self.__has_won = False


        # Choose a nice comfy background color
        self.background_color = arcade.types.Color(223, 153, 153)
        self.__is_test = 'pytest' in sys.argv[0]

        try :
            if not os.path.exists(map_name) :
                raise CustomException("The file path for initial level is incorrect")

            self.__initial_map_name = map_name
            self.__current_map_name = self.__initial_map_name

            # Setup our game
            self.create_new_player()
            self.setup()
        except CustomException as e :
            self.__make_error_text(str(e))
            if self.__is_test : 
                raise e
        except Exception as e :
            self.__make_error_text("An unknow error has occured")
            if self.__is_test : 
                raise e
           


    def setup(self) -> None:
        """Set up the game here."""

        self.__reset_sprite_lists()

        self.__won = False

        self.sprite_tuple = (self.__wall_list, self.__list_of_sprites_in_platforms, self.__coin_list, self.__lava_list,
                             self.__lever_list, self.__door_list , self.__arrow_list, self.__end_list,
                               self.__monster_list, self.__player_sprite_list, self.__weapon_list) 
        map = Map(self.__current_map_name, self.__wall_list, self.__lava_list, self.__coin_list, 
                  self.__monster_list, self.__door_list, self.__lever_list, self.__end_list, 
                  self.__list_of_sprites_in_platforms, self.__non_platform_moving_sprites_list)
        
        self.__player.set_position(map.get_player_coordinates()[0], map.get_player_coordinates()[1])
        
        self.__next_map = map.get_next_map()
        
        self.__player_sprite_list.append(self.__player)
        self.__camera = arcade.camera.Camera2D()
        self.__fixed_camera = arcade.camera.Camera2D()
        self.__camera.position = self.__player.position #type: ignore
        self. __fixed_camera.position = arcade.Vec2(0, 0)

        self.__ui = UI(self.__fixed_camera, self.__monster_list, self.__player.coin_score)
        self.__ui.update_weapon_icon(self.__player.selected_weapon_type)

        self.solid_block_update() 

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.__player,
            platforms=self.__list_of_sprites_in_platforms,
            walls=self.__solid_block_list, 
            gravity_constant = constants.PLAYER_GRAVITY
        )
        self.__player.physics_engine = self.physics_engine

    def create_new_player(self) -> None :
        """Creates a new player instance."""
        self.__player = Player(0, 0)
        
    def __reset_sprite_lists(self) -> None :
        """Sets all sprite lists to their initial empty values"""
        self.__player_sprite_list = arcade.SpriteList()
        self.__wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.__list_of_sprites_in_platforms = arcade.SpriteList()
        self.__coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.__lava_list = arcade.SpriteList(use_spatial_hash=True)
        self.__lever_list = arcade.SpriteList(use_spatial_hash=True)
        self.__door_list = arcade.SpriteList(use_spatial_hash=True)
        self.__monster_list = arcade.SpriteList()
        self.__weapon_list = arcade.SpriteList()
        self.__arrow_list = arcade.SpriteList()
        self.__end_list = arcade.SpriteList(use_spatial_hash=True)
        self.__solid_block_list = arcade.SpriteList(use_spatial_hash=True)
        self.__non_platform_moving_sprites_list = []

    def __make_error_text(self, error : str) -> None :
        """Creates the personalised error text, based on the particular error that has occured."""
        self.__error_text = arcade.Text(
                text=f"ERROR : {error}",
                color = arcade.color.RED_BROWN,
                font_size= 40,
                font_name="Impact",
                x = constants.WINDOW_WIDTH/2,
                y = constants.WINDOW_HEIGHT/2,
                anchor_x="center",
                anchor_y="center"
                )
        self.background_color = arcade.color.ALMOND
        self.__error = True

    
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""

        if not self.can_play :
            return

        self.__player.on_key_press(key, modifiers)

        match key:   
            case arcade.key.ESCAPE if modifiers & arcade.key.MOD_SHIFT :
                # reset game from start
                self.__setup_from_initial()
            case arcade.key.ESCAPE:
                # reset level
                self.create_new_player()
                self.setup()

    
    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""
        if not self.can_play :
            return

        self.__player.on_key_release(key, modifiers)
        

    def on_mouse_press(self, mouse_x: int, mouse_y: int, button: int, modifiers: int) -> None:
        """Called when the user presses a mouse button."""

        if not self.can_play :
            return

        match button:
            case arcade.MOUSE_BUTTON_LEFT:
                self.__weapon_list.append(self.__player.create_weapon(arcade.Vec2(mouse_x, mouse_y), self.__camera.bottom_left))
            case arcade.MOUSE_BUTTON_RIGHT:
                self.__weapon_list.clear()
                self.__player.change_weapon()
                self.__ui.update_weapon_icon(self.__player.selected_weapon_type)
                
                                  
    def on_mouse_release(self, mouse_x: int, mouse_y: int, button: int, modifiers: int) -> None:
        """Called when the user releases a mouse button."""

        if not self.can_play :
            return

        match button:
            case arcade.MOUSE_BUTTON_LEFT:
                if (weapon := self.current_weapon) is not None :
                    if (arrow := weapon.on_mouse_release()) is not None :
                        self.__arrow_list.append(arrow)
                self.__weapon_list.clear()

    def solid_block_update(self) -> None:
        """Updates the list consisting of wall_list and the closed doors in door_list"""
        self.__solid_block_list.clear()
        self.__solid_block_list.extend(self.__wall_list)
        open_doors = [door for door in self.__door_list if door.is_closed]
        self.__solid_block_list.extend(open_doors)

    def test_compexite_plateformes(self) -> None:
        """Called once per frame, before drawing.
        This is where in-world time "advances" or "ticks"."""

        
        map_test : list[list[str]] = []
        for i in range (5):
            line = []
            for j in range (5):
                line.append("=")
            map_test.append(line)
        map_mouvement = MapMovement(self.__non_platform_moving_sprites_list)
        map_mouvement.find_platforms_in_map_matrix(map_test)

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.
        This is where in-world time "advances" or "ticks"."""

        self.do_on_update(delta_time)

    def do_on_update(self, delta_time: float) -> None :
        """Only called in on_update, what actually happens when updates."""
        
        if not self.can_play: 
            return

        if self.player_y < -500 :
            self.__setup_from_initial()

        for non_platform in self.__non_platform_moving_sprites_list :
            non_platform.move()

        if self.physics_engine is not None :
            self.physics_engine.update()

        for monster in self.__monster_list :
            monster.move(self.__wall_list, arcade.Vec2(self.player_x, self.player_y))

        try :
            for weapon in self.__weapon_list :
                if not self.__is_test :         # Pour que l'on ne puisse pas bouger la souris pendant les tests
                    mouse_position = self.__get_mouse_position()
                    weapon.update_angle(mouse_position, arcade.Vec2(self.player_x, self.player_y), self.__camera.bottom_left)
                weapon.update_weapon(arcade.Vec2(self.player_x, self.player_y))
        except KeyError :
            # Sometimes getting the mouse position from acade throws an exception, but not often. 
            # The program should just ignore this and not update weapon angle in that frame.
            pass


        for arrow in self.__arrow_list :
            arrow.move()
            if (arrow.center_y < self.__camera.bottom_left.y):
                arrow.remove_from_sprite_lists()
        

        self.__update_camera()
        self.__check_collisions()
        
    def __update_camera(self) -> None :
        """Updates camera position when player moves/dies. 
        The camera in question is that moving one, not the static UI one."""

        camera_x, camera_y = self.__camera.position
        if (self.__camera.center_right.x < self.__player.center_x + constants.CAMERA_X_MARGIN):
            camera_x += max(abs(self.player_speed_x), constants.PLATFORM_SPEED)
        elif (self.__camera.center_left.x > self.__player.center_x - constants.CAMERA_X_MARGIN):
            camera_x -= max(abs(self.player_speed_x), constants.PLATFORM_SPEED)

        if (self.__camera.top_center.y < self.__player.center_y + constants.CAMERA_Y_MARGIN) :
            if self.__player.change_y != 0 :
                camera_y += self.__player.change_y
            else :
                camera_y += constants.PLATFORM_SPEED
        elif (self.__camera.bottom_center.y + constants.CAMERA_Y_MARGIN > self.__player.center_y) :
            if self.__player.change_y != 0 :
                camera_y += self.__player.change_y
            else :
                camera_y -= constants.PLATFORM_SPEED

        self.__camera.position = arcade.Vec2(camera_x, camera_y)

    def __on_monster_death(self, monster : Monster) -> None :
        """Called when a monster dies"""
        monster.die()
        self.__ui.update_boss_life(monster)
        self.solid_block_update() # Because some monsters, like bosses, can affect doors
        
    def __coin_collisions(self) -> None :
        """Handles collisions between coins and player"""
        for coin in arcade.check_for_collision_with_list(self.__player, self.__coin_list) :
            coin.remove_from_sprite_lists()
            self.__player.coin_score_update()
            self.__ui.update_coin_score(self.__player.coin_score)
            arcade.play_sound(arcade.load_sound(":resources:sounds/coin5.wav"))

    def __arrow_collisions(self) -> None :
        """Handles collisions between arrows and everything else"""

        for arrow in list(self.__arrow_list) : # To prevent bugs from modifying list while looping through it

            for lever in arcade.check_for_collision_with_list(arrow, self.__lever_list):
                if not lever.broken:
                    lever.on_action()
                    self.solid_block_update()
                    arcade.play_sound(arcade.load_sound(":resources:sounds/rockHit2.wav")) 
                    arrow.remove_from_sprite_lists()
                break

                

            for monster in arcade.check_for_collision_with_list(arrow, self.__monster_list) :
                self.__on_monster_death(monster)
                arrow.remove_from_sprite_lists()
                break

            for _ in arcade.check_for_collision_with_lists(arrow, (self.__solid_block_list, self.__list_of_sprites_in_platforms, self.__lava_list)):
                arcade.play_sound(arcade.load_sound(":resources:sounds/rockHit2.wav"))
                arrow.remove_from_sprite_lists()
                break

    
    def __check_collisions(self) -> None :
        """Handles all game collisions: player, weapons, arrows, monsters, coins, levers, lava, end."""

        self.__coin_collisions()
        self.__arrow_collisions()

        if (weapon := self.current_weapon) is not None :
            weapon.check_collision(self.__monster_list, self.__lever_list, self.__ui)
            self.solid_block_update()

        if arcade.check_for_collision_with_lists(self.__player, (self.__lava_list, self.__monster_list)) != [] :
            self.__setup_from_initial()
        if arcade.check_for_collision_with_list(self.__player, self.__end_list) != [] :
            self.__load_next_map()


    def __load_next_map(self) -> None :
        """Load next_map of file. Should only be called if the file has a valid next map."""

        if self.__next_map is None :
            self.__won = True
            self.__reset_sprite_lists()
        else :
            assert os.path.exists(self.__next_map)
            self.__current_map_name = self.__next_map
            self.setup()

    def __setup_from_initial(self) -> None :
        """Setup the game from the initial map."""
        assert os.path.exists(self.__initial_map_name)
        arcade.play_sound(arcade.load_sound(":resources:/sounds/lose2.wav"))
        self.__current_map_name = self.__initial_map_name
        self.create_new_player()
        self.setup()



    def on_draw(self) -> None:
        """Render the screen."""

        self.clear() # always start with self.clear()

        if self.__won :
            self.__ui.draw_winning_text()
        elif self.__error :
            self.__error_text.draw()
        else :
            with self.__camera.activate():
                for list in self.sprite_tuple :
                    list.draw()
            self.__ui.draw_in_game()

    def __get_mouse_position(self) -> arcade.Vec2 :
        """Returns mouse position. If mouse doesn't exist, returns player position as safe value."""
        if self.window.mouse is not None :
            return arcade.Vec2(self.window.mouse.data['x'], self.window.mouse.data['y'])
        else :
            return arcade.Vec2(self.player_x, self.player_speed_y)
    
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
    def current_weapon(self) -> Weapon | None :
        """ Returns the currently in hand weapon, or None if the player isn't holding a weapon."""
        if len(self.__weapon_list) == 0 :
            return None
        return self.__weapon_list[0]
    
    @property
    def can_play(self) -> bool :
        return not (self.__error or self.__won)
    
    # This property is needed for the tests
    @property
    def won(self) -> bool : 
        return self.__has_won
    
    # This property is needed to match the private setter
    @property
    def __won(self) -> bool : 
        return self.__has_won

    # This setter is private because it should not be modified outside GameView
    @__won.setter
    def __won(self, value : bool) -> None :
        if value == True :
            self.__reset_sprite_lists()
        self.__has_won = value

    @property
    def __error(self) -> bool :
        return self.__has_error

    @__error.setter
    def __error(self, value : bool) -> None :
        if value == True :
            self.__reset_sprite_lists()
        self.__has_error = value

    @property
    def get_wall_list(self) -> arcade.SpriteList[arcade.Sprite]:
        return self.__wall_list
    
    @property
    def get_lava_list(self) -> arcade.SpriteList[arcade.Sprite]:
        return self.__lava_list
    
    @property
    def get_monster_list(self) -> arcade.SpriteList[Monster]:
        return self.__monster_list
    
    @property
    def get_weapon_list(self) -> arcade.SpriteList[Weapon]:
        return self.__weapon_list
    
    @property
    def get_arrow_list(self) -> arcade.SpriteList[Arrow]:
        return self.__arrow_list

    