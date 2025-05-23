import os
from typing import Final
import arcade
import yaml
import re

from bat import Bat
from blob import Blob
from lever import Lever
from door import Door
import constants
from constants import PIXELS_IN_BLOCK, PLATFORM_SPEED
from monster import Monster
from boss import Boss
from ghost import Ghost
from frog import Frog



from platforms import Platform, Direction
from non_platform_moving_blocks import NonPlatformMovingBlocks
from platform_arrows import PlatformArrows

section_split = re.compile(r'---\s*\r?\n?')

class Map :

    player_coordinates : tuple[int, int]
    __next_map : str | None
    __allowed_characters : Final[frozenset[str]] = frozenset({"S", "o", "v", "E", "=", "-", 
                                                              "x", "*", "£", "^", "B", "f", "g", " ", "|", "^", "\n", 
                                                              "\r", "←", "→", "↑", "↓"})
    __hidden_characters : Final[frozenset[str]] = frozenset({" ",  "\n","\r"})
    __arrow_characters : Final[frozenset[str]] = frozenset({"←", "→", "↑", "↓"})
    __platform_characters = frozenset({"=", "-", "x", "£", "E", "^"})
    __non_wall_platform_characters = frozenset({"£", "E", "^"})
    __list_of_platforms : list[Platform]
    __ymal_part : dict[str,object]
    
    def __init__(self, current_map_name : str, wall_list: arcade.SpriteList[arcade.Sprite], 
                 lava_list: arcade.SpriteList[arcade.Sprite], coin_list: arcade.SpriteList[arcade.Sprite], 
                 monster_list: arcade.SpriteList[Monster], boss_list: arcade.SpriteList[Boss], door_list: arcade.SpriteList[Door], 
                 lever_list: arcade.SpriteList[Lever], end_list: arcade.SpriteList[arcade.Sprite], 
                 platform_list: arcade.SpriteList[arcade.Sprite],
                 non_platform_moving_sprites_list : list[NonPlatformMovingBlocks]
                 ) -> None:

        self.__current_map_name = current_map_name
        self.__wall_list = wall_list
        self.__lava_list = lava_list
        self.__coin_list = coin_list
        self.__monster_list = monster_list
        self.__boss_list = boss_list
        self.__door_list = door_list
        self.__lever_list = lever_list
        self.__end_list = end_list
        self.__next_map = None
        self.__list_of_platforms = []
        self.__platform_list = platform_list
        self.__non_platform_moving_sprites_list = non_platform_moving_sprites_list

        self.__create_map()
    
    # def partition_file(self) -> list[str] :
    #     with open(self.__current_map_name, "r", encoding="utf-8", newline='') as file:
    #         level = file.read()
    #         partition = section_split.split(level, 1)
    #     return partition

    def get_ymal(self) -> None: 

        try : 
            with open(self.__current_map_name, "r", encoding="utf-8", newline='') as file:
                level = file.read()
                partition = section_split.split(level, 1)
                yaml_return : object = yaml.safe_load(partition[0])
                if (isinstance(yaml_return,dict)):
                    self.__ymal_part = yaml_return
                else : raise Exception("Configuration lines on file aren't formated correctly")
        except ValueError :
            raise Exception("Configuration lines on file aren't formated correctly")

    def __parse_config_2(self) -> None:
        self.get_ymal()
        self.__width = 0
        self.__height = 0
        try : 
            match self.__ymal_part:
                case {"width":width,"height":height}:
                    if isinstance(width, int):
                        self.__width = width
                    else: raise Exception("The width must be an integer")
                    if isinstance(height, int):
                        self.__height = height
                    else: raise Exception("The height must be an integer")
            if "next-map" in self.__ymal_part:
                if isinstance(self.__ymal_part["next-map"],str) and os.path.exists(self.__ymal_part["next-map"]) :
                    self.__next_map = self.__ymal_part["next-map"]
                else: raise Exception("The next map path is incorrect")                                                                                                                                                                                                           
        except ValueError :
            raise Exception("Configuration lines on file aren't formated correctly")    #je check 2 fois pas sur que c'est necessaire
        if (self.__width == 0 or self.__height == 0) :
            raise Exception(f"Width and height should be defined and non-zero in configuration of file {self.__current_map_name}")
        if (self.__width < 0 or self.__height < 0) :
            raise Exception("Width and height should be positive numbers")

    def action_linking(self, switch_on_or_off: list[dict[str,object]],
                        map_doors: list[list[Door|None]]) ->tuple[list[Door],list[Door],bool]:
        one_time_use : bool = False
        list_close: list[Door] = []
        list_open: list[Door] = []
        for element in switch_on_or_off:
            if not isinstance(element,dict):
                raise Exception("A switch_on action is incorect")
            assert(isinstance(element,dict))
            match element:
                case {'action':'disable'}:
                    one_time_use = True
                case {'x': int() as x, 'y': int() as y,'action':'open-gate'}:
                    door_in_map = map_doors[y][x]
                    if not isinstance(door_in_map,Door):
                        raise Exception("There is no door at x= ",x," y= ",y)
                    list_open.append(door_in_map)
                case {'x': int() as x, 'y': int() as y,'action':'close-gate'}:
                    door_in_map = map_doors[y][x]
                    if not isinstance(door_in_map,Door):
                        raise Exception("There is no door at x= ",x," y= ",y)
                    list_close.append(door_in_map)
        return (list_open, list_close, one_time_use)
            
     

    def add_door_to_list(self, map_doors : list[list[Door|None]], x : int, y : int, list : list[Door]) -> None :
        """Takes the [y][x] element in map_doors, checks that it's a door and adds it to the list."""
        door = map_doors[y][x]
        if not isinstance(door, Door):
            raise Exception(f"There is no door at (x, y) = {(x, y)}")
        assert(isinstance(door, Door))
        list.append(door)

    # ATTENTION : Wanted to refactor the switch underneath but i have problems with dict type anotation in function 
    # def set_lever_action(self, dict_key : str, open_list : list[Door], close_list : list[Door], map_doors : list[list[Door|None]]):

    def lever_door_linking_2(self, map_doors : list[list[Door|None]], map_levers : list[list[Lever|None]]) -> None:
        """"""
        try:
            match self.__ymal_part:
                case {'switches': list() as switches}:
                    for switch in switches:
                        if not isinstance(switch,dict):
                            raise Exception("the switch list is incorect")
                        assert(isinstance(switch,dict))
                        activation_close : list[Door] = [] 
                        activation_open : list[Door] = []  
                        deactivation_close : list[Door] = [] 
                        deactivation_open : list[Door] = [] 
                        start_on : bool = False
                        on_deactivate : bool = False
                        off_deactivate : bool = False
                        match switch:
                            case {'switch_on': list() as switch_on}:
                                # tuple = self.action_linking(switch_on, map_doors)
                                # activation_open = tuple[0] 
                                # activation_close = tuple[1] 
                                # on_deactivate = tuple[2]
                                for element in switch_on:
                                    if not isinstance(element,dict):
                                        raise Exception("A switch_on action is incorect")
                                    assert(isinstance(switch,dict))
                                    match element:
                                        case {'action':'disable'}:
                                            one_time_use = True
                                        case {'x': int() as x, 'y': int() as y,'action':'open-gate'}:
                                            self.add_door_to_list(map_doors, x, y, activation_open)
                                        case {'x': int() as x, 'y': int() as y,'action':'close-gate'}:
                                            self.add_door_to_list(map_doors, x, y, activation_close)
                        match switch:
                            case {'switch_off': list() as switch_off}:
                                #         tuple = self.action_linking(switch_off, map_doors)
                                #         deactivation_open = tuple[0] 
                                #         deactivation_close = tuple[1] 
                                #         off_deactivate = tuple[2]
                                # if switch.get('state') == True:
                                #     start_on = True
                                for element in switch_off:
                                    if not isinstance(element,dict):
                                        raise Exception("A switch_off action is incorect")
                                    assert(isinstance(switch, dict))
                                    match element:
                                        case {'action':'disable'}:
                                            one_time_use = True
                                        case {'x': int() as x, 'y': int() as y,'action':'open-gate'}:
                                            self.add_door_to_list(map_doors, x, y, deactivation_open)    
                                        case {'x': int() as x, 'y': int() as y,'action':'close-gate'}:
                                            self.add_door_to_list(map_doors, x, y, deactivation_close)        
                        match switch:
                            case {'x': int() as x, 'y': int() as y}:
                                lever_in_map = map_levers[y][x]
                                if isinstance(lever_in_map, Lever):
                                    lever : Lever = lever_in_map
                                    lever.link_doors(activation_close ,activation_open, deactivation_close,
                                                      deactivation_open, on_deactivate, off_deactivate, start_on)
                                else: Exception(f"There is no lever at (x, y) = {(x, y)}")
                            case _ :
                                raise Exception("Please precise where the lever is suposed to be with integer coordinate")
            match self.__ymal_part:
                case {'gates': list() as doors}:
                    for door in doors:
                        if not isinstance(door, dict):
                            raise Exception("A door action is incorect")
                        assert(isinstance(door,dict))
                        match door:
                            case {'x': int() as x, 'y': int() as y,'state':'open'}:
                                door_in_map = map_doors[y][x]
                                if isinstance(door_in_map,Door):
                                    door_in_map.open()
                                else: raise Exception(f"There is no door at (x, y) = {(x, y)}")
                                
        except ValueError :
            pass

    def __file_to_matrix(self) -> None :
        """Turns map file into a matrix"""
        self.__map_matrix = [["" for i in range(self.__width)] for j in range(self.__height)]
        # Matrice[Lines][Colonne]
        with open(self.__current_map_name, "r", encoding="utf-8", newline='') as f :
            while not section_split.fullmatch(f.readline()):
                # ATTENTION : Function should probably only take second half of broken up file, so we can skip this
                # Skips the configuration for of the file, taken care of by function self.__parse_config
                continue
            for j in range(self.__height) :
                line = f.readline().rstrip("\n").ljust(self.__width)
                if len(line) > self.__width :
                    raise Exception(f"There is a line with more characters than {self.__width}") 
                for i in range(self.__width) :
                    char = line[i]
                    if char not in self.__allowed_characters :
                        raise Exception("The map contains an unknown character")
                    if char  in self.__hidden_characters :
                        continue
                    self.__map_matrix[j][i] = char
            if not section_split.fullmatch(f.readline()) :
                raise Exception(f"The map isn't exactly {self.__height} lines long")

    

    def find_platforms_in_map_matrix(self) -> None :
        """Goes to each position in self.__map_matrix and checks if the sprite there could be part of
        a moving platform. If so, it calls function self.grouping_platform(), passing an empty platform instance, 
        which becomes a full platform. 
        This platform gets added to self.__list_of_platforms if it's movement is not zero.
        """
        visited : set[tuple[int, int]] = set()

        for line in range(len(self.__map_matrix)) :
            for column in range(len(self.__map_matrix[line])):
                if self.__map_matrix[line][column] in self.__platform_characters and (line, column) not in visited :
                    platform = Platform()
                    self.grouping_platform(line, column, platform, visited, None)
                    if platform.moves :
                        self.__list_of_platforms.append(platform)

        
    def grouping_platform(self, line : int, column : int, platform : Platform, visited : set[tuple[int, int]], valid_arrow : PlatformArrows | None) -> None :
        """Recursive function taking as arguments :
            - line, column
                The lines and column numbers of possible platform sprites       
            - platform
                The platform it is creating                                     
            - visited
                A set of already visited positions, which are positions of sprites that can't be currently added to the platform. 
                They could either belong to another platform, not be the correct type of sprite or already belong to this platform.       
            - valid_arrow
                The only arrow type that could affect the platform, if the current sprite is an arrow.
        """

        if line < 0 or column < 0 or line >= len(self.__map_matrix) or column >= len(self.__map_matrix[0]) or (line, column) in visited :
            return
        if self.__map_matrix[line][column] not in self.__platform_characters | {a.value for a in PlatformArrows} :
            return

        if (value := self.__map_matrix[line][column]) in {a.value for a in PlatformArrows} :
            arrow_type = PlatformArrows.get_arrow_enum(value)
            if arrow_type == valid_arrow :
                visited.add((line, column))
                arrows_counted = arrow_type.count_arrows(line, column, 1, visited, self.__map_matrix)
                platform.add_arrow_info(arrow_type, arrows_counted)
            else :
                return
        else :
            visited.add((line, column))
            if self.__map_matrix[line][column] in self.__platform_characters : 
                arcade_line = self.__matrix_line_num_to_arcade(line)
                platform.add_sprite((arcade_line, column))
            
            for d_line, d_col, direction_arrow in [(0, -1, PlatformArrows.LEFT), (0, 1, PlatformArrows.RIGHT), (1, 0, PlatformArrows.DOWN), (-1, 0, PlatformArrows.UP)] :
                self.grouping_platform(line + d_line, column + d_col, platform, visited, direction_arrow)

    def __matrix_line_num_to_arcade(self, line : int) -> int :
        """Tranforms a line number taken from looping through the map matrix to the line number considered by arcade.
        Arcade convention is top line is height - 1, last line is 0."""
        assert (line < self.__height)
        return self.__height - (line + 1)

    def get_sprite_boundaries(self, sprite : arcade.Sprite) -> tuple[Direction | None, tuple[int, int]] :
        """Returns the movement and direction a platform sprite should move, 
        with direction being None if and only if the sprite doesn't move.
        Should *only* be called to sprites that haven't started moved yet.
        """
        for platform in self.__list_of_platforms :
            if platform.contains(sprite) :
                assert platform.movement is not None
                return (platform.direction, platform.movement)
        return (None, (0, 0))

    def give_movement_to_non_platform_sprites(self, sprite : arcade.Sprite | None, sprite_char : str) -> bool :
        """Takes an arcade.Sprite as argument, as well as it's character. Checks if it is a non-platform moving sprite.
        If it is, checks if it belongs to some platform. 
        If it does, gives the platform movement to the individual sprite and returns True. 
        Otherwise, return False.
        Should *only* be called to sprites that haven't started moved yet.
        """
        if sprite is None : 
            return False
        assert(sprite is not None)
        if not sprite_char in self.__non_wall_platform_characters :
            return False
        direction, movement = self.get_sprite_boundaries(sprite)
        if direction is None :
            return False
        self.__non_platform_moving_sprites_list.append(NonPlatformMovingBlocks(sprite, direction, movement, arcade.Vec2(sprite.center_x, sprite.center_y))) 
        return True

    def give_movement_to_platform_sprites(self, sprite : arcade.Sprite, sprite_char : str) -> bool :
        """Takes an arcade.Sprite as argument. Checks that it is a platform character.
        Checks if it belongs to some platform. 
        If it does, gives the platform movement to the individual sprite and returns True. 
        Otherwise, return False.
        Should *only* be called to sprites that haven't started moved yet.
        """
        if not (sprite_char in self.__platform_characters - self.__non_wall_platform_characters) :
            return False
        
        direction, movement = self.get_sprite_boundaries(sprite)
        
        match direction :
            case Direction.VERTICAL :
                sprite.boundary_top = sprite.top + movement[0] 
                sprite.boundary_bottom = sprite.bottom - movement[1] 
                sprite.change_y = PLATFORM_SPEED
                return True
            case Direction.HORIZONTAL :
                sprite.boundary_left = sprite.left - movement[0] 
                sprite.boundary_right = sprite.right + movement[1] 
                sprite.change_x = PLATFORM_SPEED
                return True
            case None :
                return False

    def __create_map(self) -> None : 
        """Creates map from file, raises exceptions in case of errors in map."""
        self.__parse_config_2()
        #self.__parse_config()
        self.__file_to_matrix()
        self.find_platforms_in_map_matrix()
        
    
        map_doors : list[list[Door | None]] = [[None for i in range(self.__width)] for j in range(self.__height)]
        map_levers : list[list[Lever | None]] = [[None for i in range(self.__width)] for j in range(self.__height)]
        start_is_placed = False
        end_is_placed = False

        for line_num, line in enumerate(self.__map_matrix) :
            line_num_arcade = self.__matrix_line_num_to_arcade(line_num)
            for position_x, sprite_char in enumerate(line) :
                x_coordinate = PIXELS_IN_BLOCK * position_x
                y_coordinate =  PIXELS_IN_BLOCK * line_num_arcade
                sprite : arcade.Sprite | None = None
                match sprite_char : 
                    case "S" :
                        if start_is_placed :
                            raise Exception("Player can't be placed twice")
                        start_is_placed = True
                        self.player_coordinates = (x_coordinate, y_coordinate)
                    case "o" :
                        blob = Blob(x_coordinate, y_coordinate)
                        self.__monster_list.append(blob)
                    case "g" :
                        ghost = Ghost(x_coordinate, y_coordinate)
                        self.__monster_list.append(ghost)
                    case "f" :
                        frog = Frog(x_coordinate, y_coordinate)
                        self.__monster_list.append(frog)
                    case "B" :
                        boss = Boss(x_coordinate, y_coordinate)
                        map_levers[line_num_arcade][position_x] = boss
                        self.__monster_list.append(boss)
                        self.__boss_list.append(boss)
                    case "v" :
                        bat = Bat(x_coordinate, y_coordinate)
                        self.__monster_list.append(bat)   
                    case "|" :
                        door = Door(x_coordinate, y_coordinate)
                        self.__door_list.append(door)
                        map_doors[line_num_arcade][position_x] = door
                    case "^" :
                        lever = Lever(x_coordinate, y_coordinate)
                        self.__lever_list.append(lever)
                        map_levers[line_num_arcade][position_x] = lever
                        sprite = lever
                    case char if char in self.__hidden_characters | self.__arrow_characters :
                        pass
                    case char if char in self.__allowed_characters :
                        match sprite_char :
                            case "E" :
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
                        sprite = arcade.Sprite(name_and_list[0], center_x= x_coordinate, center_y= y_coordinate, scale=constants.SCALE)
                        if (self.give_movement_to_platform_sprites(sprite, sprite_char)) :
                            self.__platform_list.append(sprite)
                        else :
                            name_and_list[1].append(sprite)  
                self.give_movement_to_non_platform_sprites(sprite, sprite_char)

        if not start_is_placed :
            raise Exception("Player must have a starting point")
        if self.__next_map is not None and not end_is_placed :
            raise Exception("The file sets the next map but no end to the level")
        self.lever_door_linking_2(map_doors,map_levers) 
        
    # ATTENTION : Should be a property?
    def get_player_coordinates(self) -> tuple[int, int] :
        return self.player_coordinates
    
    # ATTENTION : Should be a property?
    def get_next_map(self) -> str | None :
        return self.__next_map
    
    def valid_dict(self,dict: dict[str,object], key: str, type_in_dict: type ) -> bool:
        """Return true if the dict have the key and the correct value type associated with that key """
        if key in dict:
            if isinstance(dict[key],type_in_dict):
                return True
        return False
