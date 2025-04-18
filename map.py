import os
from typing import Final
import arcade

from bat import Bat
from blob import Blob
import constants
from monster import Monster


class Map :

    player_coordinates : tuple[int, int]
    __next_map : str
    __allowed_characters : Final[frozenset[str]] = frozenset({"S", "o", "v", "E", "=", "-", "x", "*", "£", " ", "\n", "\r"})
    __hidden_characters : Final[frozenset[str]] = frozenset({" ", "\n", "\r"})
    
    def __init__(self, current_map_name : str, wall_list: arcade.SpriteList[arcade.Sprite], 
                 lava_list: arcade.SpriteList[arcade.Sprite], coin_list: arcade.SpriteList[arcade.Sprite], 
                 monster_list: arcade.SpriteList[Monster], end_list: arcade.SpriteList[arcade.Sprite]) -> None:
    
        self.__current_map_name = current_map_name
        self.__wall_list = wall_list
        self.__lava_list = lava_list
        self.__coin_list = coin_list
        self.__monster_list = monster_list
        self.__end_list = end_list
        self.__next_map = ""

        self.__create_map()
    
    def __parse_config(self) -> None :
        with open(self.__current_map_name, "r", encoding="utf-8", newline='') as f :
            self.__width = 0
            self.__height = 0
            self.__has_next_map = False
            for line in f :
                if line == "---\n" or line == "---" :
                    break
                line.split()
                if line.startswith("next-map") :
                    if self.__has_next_map :
                        raise Exception("You can't set the next map twice")
                    self.__next_map = line.split()[-1]
                    self.__has_next_map = True
                    if not os.path.exists(self.__next_map) :
                        raise Exception("The next map path is incorrect")
                try : 
                    if line.startswith("width") :
                        if not self.__width == 0 :
                            raise Exception("You can't set the width twice")
                        self.__width = int(line.split()[-1])
                    if line.startswith("height") :
                        if not self.__height == 0 :
                            raise Exception("You can't set the height twice")
                        self.__height = int(line.split()[-1])
                except ValueError :
                    raise Exception("Configuration lines on file aren't formated correctly")
            if (self.__width == 0 or self.__height == 0) :
                raise Exception(f"Width and height should be defined and non-zero in configuration of file {self.__current_map_name}")
            if (self.__width < 0 or self.__height < 0) :
                raise Exception("Width and height should be positive numbers")

    def __file_to_matrix(self) -> None :
        """Turns map file into matrix"""
        self.__map_matrix = [['' for i in range(self.__width)] for j in range(self.__height)]
        # Matrice[Lines][Colonne]
        with open(self.__current_map_name, "r", encoding="utf-8", newline='') as f :
            while not f.readline() == "---\n" :
                continue
            for j in range(self.__height) :
                line = f.readline().rstrip("\n").ljust(self.__width)
                if len(line) > self.__width :
                    raise Exception(f"There is a line with more characters than {self.__width}") 
                for i in range(self.__width) :
                    char = line[i]
                    if char not in self.__allowed_characters :
                        raise Exception("The map contains an unknown character")
                    if char not in self.__hidden_characters :
                        self.__map_matrix[j][i] = char
            if not f.readline().rstrip("\n") == "---" :
                raise Exception(f"The map isn't exactly {self.__height} lines long")
        # for lst in self.__map_matrix:
        #     print(*lst) 
        # ATTENTION : Juste pour test, à enlever

    def __create_map(self) -> None : 
        """Creates map from file, raises exceptions in case of errors in map."""

        self.__parse_config()
        self.__file_to_matrix()
           
    
        start_is_placed = False
        end_is_placed = False

        for line_num, line in enumerate(self.__map_matrix) :
            line_number_arcade_coordinates = self.__height - (line_num + 1)
            # To match line number with convention that first line is h-1, last line is 0
            for position_x, sprite in enumerate(line) :
                x_coordinate = 64 * position_x
                y_coordinate =  64 * line_number_arcade_coordinates
                match sprite : 
                    case "S" :
                        if start_is_placed :
                            raise Exception("Player can't be placed twice")
                        start_is_placed = True
                        self.player_coordinates = (x_coordinate, y_coordinate)
                    case "o" :
                        blob = Blob(x_coordinate, y_coordinate)
                        self.__monster_list.append(blob)
                    case "v" :
                        bat = Bat(x_coordinate, y_coordinate)
                        self.__monster_list.append(bat)
                    case char if char in self.__hidden_characters :
                        pass
                    case char if char in self.__allowed_characters :
                        match sprite :
                            case "E" :
                                if not self.__has_next_map :
                                    raise Exception("There is no next map, but there is an exit") 
                                    # ATTENTION : Question : accepter end of map même sans prochain niveau?
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
        if self.__has_next_map and not end_is_placed :
            raise Exception("The file sets the next map but no end to the level")
        
    def get_player_coordinates(self) -> tuple[int, int] :
        return self.player_coordinates
    
    def get_next_map(self) -> str :
        return self.__next_map
    