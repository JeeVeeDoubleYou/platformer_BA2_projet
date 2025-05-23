import os
import sys
from typing import Optional
import arcade
import constants
from platforms import Direction
from non_platform_moving_blocks import NonPlatformMovingBlocks
from player import Player
from player import WeaponType
from boss import Boss
from boss import Attack
from monster import Monster
from weapon import Weapon
from sword import Sword
from bow import Bow
from arrow import Arrow
from lever import Lever
from door import Door
from map import Map



from arcade import Rect

CAMERA_X_MARGIN = 400
CAMERA_Y_MARGIN = 200


class GameView(arcade.View):
    """Main in-game view."""

    __player_sprite_list: arcade.SpriteList[arcade.Sprite]
    __wall_list: arcade.SpriteList[arcade.Sprite]
    __platform_list : arcade.SpriteList[arcade.Sprite]
    __lava_list: arcade.SpriteList[arcade.Sprite]
    __coin_list: arcade.SpriteList[arcade.Sprite]
    __weapon_list: arcade.SpriteList[Weapon]
    __arrow_list: arcade.SpriteList[Arrow]
    __monster_list: arcade.SpriteList[Monster]
    __boss_list: arcade.SpriteList[Boss]
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
        self.__won = False

        # Choose a nice comfy background color
        self.background_color = arcade.types.Color(223, 153, 153)
        self.__is_test = 'pytest' in sys.argv[0]

        try :
            if not os.path.exists(map_name) :
                raise Exception("The file path for initial level is incorrect")
            self.__initial_map_name = map_name
            self.__current_map_name = self.__initial_map_name
            # Setup our game
            self.setup()

        except Exception as e :
            self.__make_error_text(str(e))
            if self.__is_test : 
                raise e


    def setup(self) -> None:
        """Set up the game here."""

        self.__reset_sprite_lists()

        self.__won = False
        self.__win_text = arcade.Text(
                        "Congratulations, you've won !",
                        color = arcade.color.BLACK,
                        font_size= 54,
                        font_name="Impact",
                        x = constants.WINDOW_WIDTH/2,
                        y = constants.WINDOW_HEIGHT/2,
                        anchor_x="center",
                        anchor_y="center"
                        )


        self.sprite_tuple = (self.__wall_list, self.__platform_list, self.__coin_list, self.__lava_list,
                             self.__lever_list, self.__door_list , self.__arrow_list, self.__end_list,
                               self.__monster_list, self.__player_sprite_list, self.__weapon_list) 
        self.__player_sprite_list, 
        map = Map(self.__current_map_name, self.__wall_list, self.__lava_list, self.__coin_list, 
                  self.__monster_list,  self.__boss_list, self.__door_list, self.__lever_list, self.__end_list, 
                  self.__platform_list, self.__non_platform_moving_sprites_list)
        
        self.__player = Player(map.get_player_coordinates()[0], map.get_player_coordinates()[1])
        self.__next_map = map.get_next_map()
        
        self.__player_sprite_list.append(self.__player)
        self.__camera = arcade.camera.Camera2D()
        self.__fixed_camera = arcade.camera.Camera2D()
        self.__camera.position = self.__player.position #type: ignore
        self. __fixed_camera.position = arcade.Vec2(0, 0)

        
        weapon_rect = Rect(0, 0, 0, 0, 50, 50, 
                            self.__fixed_camera.top_left.x+30,
                            self.__fixed_camera.top_left.y-30,)
        self.__weapon_icon : dict[str, Rect | str] = {'rect' : weapon_rect, 
                                               'texture' : 'assets/kenney-voxel-items-png/sword_silver.png' }
        self.__text_score = arcade.Text("", self.__fixed_camera.bottom_left.x+10, self.__fixed_camera.bottom_left.y+10, arcade.color.BLACK, 12)
        self.__text_boss_life = arcade.Text("", self.__fixed_camera.bottom_left.x+200, self.__fixed_camera.bottom_left.y+10, arcade.color.RED, 12)

        for boss in self.__monster_list:
            if isinstance(boss,Boss):
                string_score ="malenia blade of miquela:  "
                for i in range (boss.hit_points):
                    string_score += " <3 "
                self.__text_boss_life.text = string_score

        self.__text_win = arcade.Text("", 200 ,200, arcade.color.BLACK, 30)
        self.text_list = [self.__text_score,]
        self.update_user_interface()

        self.solid_block_update() 

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.__player,
            platforms=self.__platform_list,
            walls=self.__solid_block_list, 
            gravity_constant = constants.PLAYER_GRAVITY
        )
        self.__player.physics_engine = self.physics_engine

        
    def __reset_sprite_lists(self) -> None :
        """Sets all sprite lists to their initial empty values"""
        self.__player_sprite_list = arcade.SpriteList()
        self.__wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.__platform_list = arcade.SpriteList()
        self.__coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.__lava_list = arcade.SpriteList(use_spatial_hash=True)
        self.__lever_list = arcade.SpriteList(use_spatial_hash=True)
        self.__door_list = arcade.SpriteList(use_spatial_hash=True)
        self.__monster_list = arcade.SpriteList()
        self.__boss_list = arcade.SpriteList()
        self.__weapon_list = arcade.SpriteList()
        self.__arrow_list = arcade.SpriteList()
        self.__end_list = arcade.SpriteList(use_spatial_hash=True)
        self.__solid_block_list = arcade.SpriteList(use_spatial_hash=True)
        self.__non_platform_moving_sprites_list = []

    #def __make_error_text(self, error : str) -> None :
    #    self.__error_text = arcade.Text(
    #            text=f"ERROR : {error}",
    #            color = arcade.color.RED_BROWN,
    #            font_size= 40,
    #            font_name="Impact",
    #            x = constants.WINDOW_WIDTH/2,
    #            y = constants.WINDOW_HEIGHT/2,
    #            anchor_x="center",
    #            anchor_y="center"
    #            )
    #    self.background_color = arcade.color.ALMOND
    #    self.__error = True
    #    self.__reset_sprite_lists()

    
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
                self.__player.reset_coin_counter()
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
                
                match self.__player.selected_weapon_type:
                    case WeaponType.SWORD:
                        self.__weapon_list.append(Sword(arcade.Vec2(mouse_x, mouse_y), arcade.Vec2(self.player_x, self.player_y), self.__camera.bottom_left))
                    case WeaponType.BOW:
                        self.__weapon_list.append(Bow(arcade.Vec2(mouse_x, mouse_y), arcade.Vec2(self.player_x, self.player_y), self.__camera.bottom_left))
                        for boss in self.__boss_list:       #to make the boss attack when drawing an arrow
                            boss.choice = Attack.RUSH
            case arcade.MOUSE_BUTTON_RIGHT:
                self.__weapon_list.clear()
                self.__player.change_weapon()
                match self.__player.selected_weapon_type:
                    case WeaponType.SWORD:
                        self.__weapon_icon['texture'] = "assets/kenney-voxel-items-png/sword_silver.png" 
                    case WeaponType.BOW:
                        self.__weapon_icon['texture'] = "assets/kenney-voxel-items-png/bow.png"
                
                                  
    def on_mouse_release(self, mouse_x: int, mouse_y: int, button: int, modifiers: int) -> None:
        """Called when the user a mouse button."""

        if not self.can_play :
            return

        # ATTENTION : Problème de polymorphisme, cette méthode ne devrait pas devoir choisir si c'est Bow ou pas. 
        # Relire tuto polymorphisme pour voir comment amméliorer.

        match button:
            case arcade.MOUSE_BUTTON_LEFT:
                if self.has_weapon_in_hand :
                    current_weapon = self.__weapon_list[0]
                    if isinstance(current_weapon, Bow) and current_weapon.is_active :
                        self.__arrow_list.append(Arrow(current_weapon))
                        for boss in self.__boss_list:       #to make the boss dodge arrows
                            boss.frame_until_action = 1
                            boss.choice = Attack.DASH
                self.__weapon_list.clear()

            

    def on_mouse_motion(self, mouse_x: int, mouse_y: int, buttons: int, modifiers: int) -> None:
        """Called when the mouse moves."""

        if not self.can_play :
            return

        # ATTENTION : Problem if player moves but not mouse for weapons.

        for weapon in self.__weapon_list:
            weapon.update_angle(arcade.Vec2(mouse_x, mouse_y), arcade.Vec2(self.player_x, self.player_y), self.__camera.bottom_left)
    
    def solid_block_update(self) -> None:
        self.__solid_block_list.clear()
        for wall in self.__wall_list:
            self.__solid_block_list.append(wall)
        for door in self.__door_list:
            if door.is_closed:
                self.__solid_block_list.append(door)



    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.
        This is where in-world time "advances" or "ticks"."""

        if not self.can_play: 
            return

        if self.player_y < -500 :
            self.__setup_from_initial()

        for non_platform in self.__non_platform_moving_sprites_list :
            non_platform.move()

        if self.physics_engine is not None :
            self.physics_engine.update()

        for boss in self.__boss_list :
            boss.ia(self.player_x,self.player_y)

        for monster in self.__monster_list :
            monster.move(self.__wall_list)

        for weapon in self.__weapon_list :
            weapon.update_position(arcade.Vec2(self.player_x, self.player_y))

        for arrow in self.__arrow_list :
            arrow.move()
            if (arrow.center_x < self.__camera.bottom_left.x):
                arrow.remove_from_sprite_lists()

        self.__update_camera()
        self.__check_collisions()
        
            
    def __update_camera(self) -> None :
        """Updates camera position when player moves/dies"""

        camera_x, camera_y = self.__camera.position
        if (self.__camera.center_right.x < self.__player.center_x + CAMERA_X_MARGIN):
            camera_x += max(abs(self.player_speed_x), constants.PLATFORM_SPEED)
        elif (self.__camera.center_left.x > self.__player.center_x - CAMERA_X_MARGIN):
            camera_x -= max(abs(self.player_speed_x), constants.PLATFORM_SPEED)

        if (self.__camera.top_center.y < self.__player.center_y + CAMERA_Y_MARGIN) :
            if self.__player.change_y != 0 :
                camera_y += self.__player.change_y
            else :
                camera_y += constants.PLATFORM_SPEED
        elif (self.__camera.bottom_center.y + CAMERA_Y_MARGIN > self.__player.center_y) :
            if self.__player.change_y != 0 :
                camera_y += self.__player.change_y
            else :
                camera_y -= constants.PLATFORM_SPEED

        self.__camera.position = arcade.Vec2(camera_x, camera_y)
        
        
    
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
            for lever in arcade.check_for_collision_with_list(arrow, self.__lever_list):
                if not lever.broken:
                    arrow.remove_from_sprite_lists()
                    lever.on_action()
                    self.solid_block_update()
                    arcade.play_sound(arcade.load_sound(":resources:sounds/rockHit2.wav")) 
            for monster_hit in arcade.check_for_collision_with_list(arrow, self.__monster_list) :
                for monster in arcade.check_for_collision_with_list(arrow, self.__monster_list) :
                    monster.die()
                    if isinstance(monster,Boss):
                        string_score : str
                        if monster.hit_points == 0:
                            string_score =""
                        else : 
                            string_score ="malenia blade of miquela:  "
                            for i in range (monster.hit_points):
                                string_score += " <3 "
                        self.__text_boss_life.text = string_score
                    self.solid_block_update()
                    arrow.remove_from_sprite_lists()
                    arcade.play_sound(arcade.load_sound(":resources:sounds/hurt4.wav")) 
            for wall_hit in arcade.check_for_collision_with_lists(arrow, (self.__solid_block_list, self.__platform_list)):
                arrow.remove_from_sprite_lists()
                arcade.play_sound(arcade.load_sound(":resources:sounds/rockHit2.wav"))
            for lava_hit in arcade.check_for_collision_with_list(arrow, self.__lava_list) :
                arrow.remove_from_sprite_lists()

               

           
        if self.has_weapon_in_hand and self.__player.selected_weapon_type == WeaponType.SWORD :
            current_weapon = self.__weapon_list[0]
            if current_weapon.is_active :
                deactivate = False
                for monster in arcade.check_for_collision_with_list(current_weapon, self.__monster_list) :
                    monster.die()
                    if isinstance(monster,Boss):
                        if monster.hit_points == 0:
                            string_score =""
                        else : 
                            string_score ="malenia blade of miquela:  "
                            for i in range (monster.hit_points):
                                string_score += " <3 "
                        self.__text_boss_life.text = string_score
                    self.solid_block_update()
                    deactivate = True
                    arcade.play_sound(arcade.load_sound(":resources:sounds/hurt4.wav"))
                for lever in arcade.check_for_collision_with_list(current_weapon, self.__lever_list):
                    if not lever.broken:
                        deactivate = True
                        lever.on_action()
                        self.solid_block_update()
                        arcade.play_sound(arcade.load_sound(":resources:sounds/rockHit2.wav"))
                if deactivate :
                    for weapon in self.__weapon_list:
                        assert(isinstance(weapon,Sword))
                        weapon.deactivate()

        if arcade.check_for_collision_with_list(self.__player, self.__lava_list) != [] :
            self.__setup_from_initial()
        if arcade.check_for_collision_with_list(self.__player, self.__monster_list) != [] :
            self.__setup_from_initial()
        if arcade.check_for_collision_with_list(self.__player, self.__end_list) != [] :
            self.__load_next_map()


    def __load_next_map(self) -> None :
        """Load next_map of file. Should only be called if the file has a valid next map."""
        if self.__next_map is None:
            self.__text_win.text = "you won "
            self.__text_win.draw()

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
        self.__current_map_name = self.__initial_map_name
        self.setup()

    def update_user_interface(self) -> None :
        """"geres les compteur et icones sur l'ecran"""
        string_score ="Coin score = " + str(self.__player.coin_score)
        self.__text_score.text = string_score



    def on_draw(self) -> None:
        """Render the screen."""

        self.clear() # always start with self.clear()

        if self.__won :
            self.__win_text.draw()
        elif self.__error :
            self.__error_text.draw()
        else :
            with self.__camera.activate():
                for list in self.sprite_tuple :
                    list.draw()

            with self.__fixed_camera.activate(): 
                if 'rect' in self.__weapon_icon and 'texture' in self.__weapon_icon:           
                    rect = self.__weapon_icon['rect']
                    texture = self.__weapon_icon['texture']
                    assert(isinstance(rect, Rect) and isinstance(texture, str))
                    arcade.draw_texture_rect(arcade.load_texture(texture), rect)
                self.__text_score.draw()
                self.__text_boss_life.draw()
                self.__text_win.draw()
            
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
    
    @property
    def can_play(self) -> bool :
        return not (self.__error or self.__won)
    
    @property
    def __won(self) -> bool :
        return self.__has_won

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
    def get_monster_list(self) -> arcade.SpriteList[Monster]:
        return self.__monster_list
    
    @property
    def get_weapon_list(self) -> arcade.SpriteList[Weapon]:
        return self.__weapon_list
    
    @property
    def get_arrow_list(self) -> arcade.SpriteList[Arrow]:
        return self.__arrow_list

    