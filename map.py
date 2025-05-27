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
from constants import PIXELS_IN_BLOCK
from monster import Monster
from boss import Boss
from ghost import Ghost
from frog import Frog
from non_platform_moving_blocks import NonPlatformMovingBlocks
from map_movement import MapMovement
from helper import matrix_line_num_to_arcade
from lever_doors_logic import LeverDoorsLogic
from custom_exception import CustomException

section_split = re.compile(r'---\s*\r?\n?')

class Map :

    player_coordinates : tuple[int, int]
    __next_map : str | None
    __allowed_characters : Final[frozenset[str]] = frozenset({"S", "o", "v", "E", "=", "-", 
                                                              "x", "*", "£", "^", "B", "f", "g", " ", "|", "^", "\n", 
                                                              "\r", "←", "→", "↑", "↓"})
    __hidden_characters : Final[frozenset[str]] = frozenset({" ",  "\n","\r"})
    __arrow_characters : Final[frozenset[str]] = frozenset({"←", "→", "↑", "↓"})
    __ymal_part : dict[str,object]
    
    def __init__(self, current_map_name : str, wall_list: arcade.SpriteList[arcade.Sprite], 
                 lava_list: arcade.SpriteList[arcade.Sprite], coin_list: arcade.SpriteList[arcade.Sprite], 
                 monster_list: arcade.SpriteList[Monster], door_list: arcade.SpriteList[Door], 
                 lever_list: arcade.SpriteList[Lever], end_list: arcade.SpriteList[arcade.Sprite], 
                 list_of_sprites_in_platforms: arcade.SpriteList[arcade.Sprite],
                 non_platform_moving_sprites_list : list[NonPlatformMovingBlocks]
                 ) -> None:

        self.__current_map_name = current_map_name
        self.__wall_list = wall_list
        self.__lava_list = lava_list
        self.__coin_list = coin_list
        self.__monster_list = monster_list
        self.__door_list = door_list
        self.__lever_list = lever_list
        self.__end_list = end_list
        self.__next_map = None
        self.__list_of_sprites_in_platforms = list_of_sprites_in_platforms
        self.__non_platform_moving_sprites_list = non_platform_moving_sprites_list
        self.__map_movement = MapMovement(self.__non_platform_moving_sprites_list)

        self.__create_map()
    
    def __partition_file(self) -> None :
        with open(self.__current_map_name, "r", encoding="utf-8", newline='') as file:
            level = file.read()
            partition = section_split.split(level, 1)
        self.partition = partition

    def get_ymal(self) -> None: 
        """Get the dict part of the file that contain the height, width, next map, levers and door"""
        try : 
            self.__partition_file()
            yaml_return : object = yaml.safe_load(self.partition[0])
            if (isinstance(yaml_return,dict)):
                self.__ymal_part = yaml_return
            else : raise CustomException("Configuration lines on file aren't formated correctly")
        except ValueError :
            raise CustomException("Configuration lines on file aren't formated correctly")

    def __parse_config(self) -> None:
        """Extract from the dict the height, width and next map of the file, and possibly other configuration attributes in the future."""
        self.get_ymal()
        self.__width = 0
        self.__height = 0
        try : 
            match self.__ymal_part:
                case {"width":width,"height":height}:
                    if isinstance(width, int):
                        self.__width = width
                    else: raise CustomException("The width must be an integer")
                    if isinstance(height, int):
                        self.__height = height
                    else: raise CustomException("The height must be an integer")
            if "next-map" in self.__ymal_part:
                if isinstance(self.__ymal_part["next-map"],str) and os.path.exists(self.__ymal_part["next-map"]) :
                    self.__next_map = self.__ymal_part["next-map"]
                else: raise CustomException("The next map path is incorrect")                                                                                                                                                                                                           
        except ValueError :
            raise CustomException("Configuration lines on file aren't formated correctly")    #je check 2 fois pas sur que c'est necessaire
        if (self.__width == 0 or self.__height == 0) :
            raise CustomException(f"Width and height should be defined and non-zero in configuration of file {self.__current_map_name}")
        if (self.__width < 0 or self.__height < 0) :
            raise CustomException("Width and height should be positive numbers")

    def __file_to_matrix(self) -> None :
        """Turns map file into a matrix"""
        self.__map_matrix = [["" for _ in range(self.__width)] for _ in range(self.__height)]
        with open(self.__current_map_name, "r", encoding="utf-8", newline='') as f :
            while not section_split.fullmatch(f.readline()):
                # Skips the configuration for of the file, taken care of by function self.__parse_config
                continue
            for j in range(self.__height) :
                line = f.readline().rstrip("\n").ljust(self.__width)
                if len(line) > self.__width :
                    raise CustomException(f"There is a line with more characters than {self.__width}") 
                for i in range(self.__width) :
                    char = line[i]
                    if char not in self.__allowed_characters :
                        raise CustomException("The map contains an unknown character")
                    if char  in self.__hidden_characters :
                        continue
                    self.__map_matrix[j][i] = char
            if not section_split.fullmatch(f.readline()) :
                raise CustomException(f"The map isn't exactly {self.__height} lines long")

    def __create_map(self) -> None : 
        """Creates map from file, raises exceptions in case of errors in map."""
        self.__parse_config()
        self.__file_to_matrix()
        self.__map_movement.find_platforms_in_map_matrix(self.__map_matrix)
        
    
        map_doors : list[list[Door | None]] = [[None for i in range(self.__width)] for j in range(self.__height)]
        map_levers : list[list[Lever | None]] = [[None for i in range(self.__width)] for j in range(self.__height)]
        start_is_placed = False
        end_is_placed = False

        for line_num, line in enumerate(self.__map_matrix) :
            line_num_arcade = matrix_line_num_to_arcade(line_num, self.__height)
            for position_x, sprite_char in enumerate(line) :
                x_coordinate = PIXELS_IN_BLOCK * position_x
                y_coordinate =  PIXELS_IN_BLOCK * line_num_arcade
                sprite : arcade.Sprite | None = None
                match sprite_char : 
                    case "S" :
                        if start_is_placed :
                            raise CustomException("Player can't be placed twice")
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
                                    raise CustomException("There can't be two ending points to a level")
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
                        if (self.__map_movement.give_movement_to_platform_sprites(sprite, sprite_char)) :
                            self.__list_of_sprites_in_platforms.append(sprite)
                        else :
                            name_and_list[1].append(sprite)  
                self.__map_movement.give_movement_to_non_platform_sprites(sprite, sprite_char)

        if not start_is_placed :
            raise CustomException("Player must have a starting point")
        if self.__next_map is not None and not end_is_placed :
            raise CustomException("The file sets the next map but no end to the level")
        LeverDoorsLogic().lever_door_linking(self.__ymal_part, map_doors, map_levers) 
        
    def get_player_coordinates(self) -> tuple[int, int] :
        return self.player_coordinates
    
    def get_next_map(self) -> str | None :
        return self.__next_map
