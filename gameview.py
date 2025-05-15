import os
from typing import Optional
import arcade
import constants
from player import Player
from player import WeaponType
from boss import Boss
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
    __platform_list : arcade.SpriteList[arcade.Sprite] # ATTENTION : Should add collisions with this
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
    physics_engine: arcade.PhysicsEnginePlatformer
    __camera: arcade.camera.Camera2D

    __icon_list: arcade.SpriteList[arcade.Sprite]
    __fixed_camera: arcade.camera.Camera2D

    __player : Player
    __next_map : str



    def __init__(self, map_name : str = "maps/testing_maps/default_map.txt") -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        if not os.path.exists(map_name) :
            raise Exception("The file path for initial level is incorrect")
        self.__initial_map_name = map_name
        self.__current_map_name = self.__initial_map_name

        # Choose a nice comfy background color
        self.background_color = arcade.types.Color(223, 153, 153)
        #arcade.color.LIGHT_CORAL
    
        # Setup our game
        self.setup()



    def setup(self) -> None:
        """Set up the game here."""

        # Initialisation of all lists
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

        self.sprite_tuple = (self.__player_sprite_list, self.__wall_list, self.__platform_list, self.__coin_list, self.__lava_list,
                            self.__monster_list, self.__lever_list, self.__door_list ,self.__weapon_list, 
                            self.__arrow_list, self.__end_list) 
       
        map = Map(self.__current_map_name, self.__wall_list, self.__lava_list, self.__coin_list, 
                  self.__monster_list, self.__boss_list, self.__door_list ,self.__lever_list, self.__end_list, self.__platform_list)
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
        self.__text_win = arcade.Text("", 200 ,200, arcade.color.BLACK, 30)
        self.text_list = [self.__text_score,]
        #self.icon_list = [self.__weapon_icon]
        self.update_user_interface()

        self.solid_block_update() 

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.__player,
            platforms=self.__platform_list,
            walls=self.__solid_block_list, 
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
        """Called when the user presses a mouse button."""

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
                match self.__player.selected_weapon_type:
                    case WeaponType.SWORD:
                        self.__weapon_icon['texture'] = "assets/kenney-voxel-items-png/sword_silver.png" 
                    case WeaponType.BOW:
                        self.__weapon_icon['texture'] = "assets/kenney-voxel-items-png/bow.png"
                
                                  
    def on_mouse_release(self, mouse_x: int, mouse_y: int, button: int, modifiers: int) -> None:
        """Called when the user a mouse button."""

        # ATTENTION : Problème de polymorphisme, cette méthode ne devrait pas devoir choisir si c'est Bow ou pas. 
        # Relire tuto polymorphisme pour voir comment amméliorer.
        match button:
            case arcade.MOUSE_BUTTON_LEFT:
                if self.has_weapon_in_hand :
                    current_weapon = self.__weapon_list[0]
                    if isinstance(current_weapon, Bow) and current_weapon.is_active :
                        self.__arrow_list.append(Arrow(current_weapon))
                self.__weapon_list.clear()

            

    def on_mouse_motion(self, mouse_x: int, mouse_y: int, buttons: int, modifiers: int) -> None:
        """Called when the mouse moves."""

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

        if self.player_y < -500 :
            self.__setup_from_initial()

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
            camera_x += constants.PLAYER_MOVEMENT_SPEED
        elif (self.__camera.center_left.x > self.__player.center_x - CAMERA_X_MARGIN):
            camera_x -= constants.PLAYER_MOVEMENT_SPEED

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
                arrow.remove_from_sprite_lists()
                lever.on_action()
                self.solid_block_update()
                arcade.play_sound(arcade.load_sound(":resources:sounds/rockHit2.wav")) 
            for monster_hit in arcade.check_for_collision_with_list(arrow, self.__monster_list) :
                for monster in arcade.check_for_collision_with_list(arrow, self.__monster_list) :
                    monster.die()
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
                    self.solid_block_update()
                    deactivate = True
                    arcade.play_sound(arcade.load_sound(":resources:sounds/hurt4.wav"))
                for lever in arcade.check_for_collision_with_list(current_weapon, self.__lever_list):
                    lever.on_action()
                    self.solid_block_update()
                    deactivate = True
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

        else:
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
        with self.__camera.activate():
            for list in self.sprite_tuple :
                list.draw()
                list.draw_hit_boxes()

        with self.__fixed_camera.activate(): 
                if 'rect' in self.__weapon_icon and 'texture' in self.__weapon_icon:           
                    rect = self.__weapon_icon['rect']
                    texture = self.__weapon_icon['texture']
                    assert(isinstance(rect, Rect) and isinstance(texture, str))
                    arcade.draw_texture_rect(arcade.load_texture(texture), rect)
                self.__text_score.draw()
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
    