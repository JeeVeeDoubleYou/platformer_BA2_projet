import os
from typing import Final
import arcade

from bat import Bat
from blob import Blob
import constants
from constants import PIXELS_IN_BLOCK, PLATFORM_SPEED
from monster import Monster

from plateforme import Platform, PlatformArrows, Direction

class Map :

    player_coordinates : tuple[int, int]
    __next_map : str
    __allowed_characters : Final[frozenset[str]] = frozenset({"S", "o", "v", "E", "=", "-", "x", "*", "£", "^", " ", "\n", "\r", "←", "→", "↑", "↓"})
    __hidden_characters : Final[frozenset[str]] = frozenset({" ", "\n", "\r"})
    __arrow_characters : Final[frozenset[str]] = frozenset({"←", "→", "↑", "↓"})
    __platform_sprites = frozenset({"=", "-", "x", "£", "E", "^"})
    __list_of_platforms : list[Platform]
    
    def __init__(self, current_map_name : str, wall_list: arcade.SpriteList[arcade.Sprite], 
                 lava_list: arcade.SpriteList[arcade.Sprite], coin_list: arcade.SpriteList[arcade.Sprite], 
                 monster_list: arcade.SpriteList[Monster], end_list: arcade.SpriteList[arcade.Sprite], platform_list: arcade.SpriteList[arcade.Sprite]) -> None:
    
        self.__current_map_name = current_map_name
        self.__wall_list = wall_list
        self.__lava_list = lava_list
        self.__coin_list = coin_list
        self.__monster_list = monster_list
        self.__end_list = end_list
        self.__next_map = ""
        self.__list_of_platforms = []
        self.__platform_list = platform_list

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

    

    def mini_platform_matrices(self) -> None :

        visited : set[tuple[int, int]] = set()

        for line in range(len(self.__map_matrix)) :
            for column in range(len(self.__map_matrix[line])):
                if self.__map_matrix[line][column] in self.__platform_sprites and (line, column) not in visited :
                    platform = Platform()
                    self.grouping_platform(line, column, platform, visited, None)
                    if platform.movement != (0,0) :
                        self.__list_of_platforms.append(platform)


    def grouping_platform(self, line : int, column : int, platform : Platform, visited : set[tuple[int, int]], valid_arrow : PlatformArrows | None) -> None :

        if line < 0 or column < 0 or line >= len(self.__map_matrix) or column >= len(self.__map_matrix[0]) or (line, column) in visited :
            return
        if self.__map_matrix[line][column] not in self.__platform_sprites | {a.value for a in PlatformArrows} :
            return
        
        visited.add((line, column))

        if (value := self.__map_matrix[line][column]) in {a.value for a in PlatformArrows} :
            arrow_type = self.get_arrow_enum(value)
            if arrow_type == valid_arrow :
                arrows_counted = arrow_type.count_arrows(line, column, 1, visited, self.__map_matrix)
                platform.add_arrow_info(arrow_type, arrows_counted)
            else :
                return
        if self.__map_matrix[line][column] in self.__platform_sprites :
            platform.add_to_sprite_set((self.__height - (line + 1), column)) 
            #ATTENTION : To modify!, weird expression is to match arcade coordinates, could be made into function?
            

        for d_line, d_col, valid_arrow in [(0, -1, PlatformArrows.LEFT), (0, 1, PlatformArrows.RIGHT), (1, 0, PlatformArrows.DOWN), (-1, 0, PlatformArrows.UP)] :
            self.grouping_platform(line + d_line, column + d_col, platform, visited, valid_arrow)

    def get_arrow_enum(self, arrow : str) -> PlatformArrows :
        """Gets an arrow name from it's string representation : example Arrows.LEFT from "←". 
        Should only ever get called with an argument that is an arrow. """
        assert arrow in {a.value for a in PlatformArrows}
        match arrow :
            case "←" :
                return PlatformArrows.LEFT
            case "→" :
                return PlatformArrows.RIGHT 
            case "↑" :
                return PlatformArrows.UP
            case "↓" :
                return PlatformArrows.DOWN
            case _ :
                raise Exception("Invalid arrow ", {arrow})

    def give_movement_to_sprites(self, sprite : arcade.Sprite) -> bool :
        for platform in self.__list_of_platforms :
            if (sprite.center_y, sprite.center_x) in platform.sprite_set :
                assert platform.direction is not None
                match platform.direction :
                    case Direction.VERTICAL :
                        sprite.boundary_top = sprite.center_y + platform.movement[0] * PIXELS_IN_BLOCK
                        sprite.boundary_bottom = sprite.center_y - platform.movement[1] * PIXELS_IN_BLOCK
                        sprite.change_y = PLATFORM_SPEED
                        return True
                    case Direction.HORIZONTAL :
                        sprite.boundary_left = sprite.center_x - platform.movement[0] * PIXELS_IN_BLOCK
                        sprite.boundary_right = sprite.center_x + platform.movement[1] * PIXELS_IN_BLOCK
                        sprite.change_x = PLATFORM_SPEED
                        return True
        return False

    def __create_map(self) -> None : 
        """Creates map from file, raises exceptions in case of errors in map."""

        self.__parse_config()
        self.__file_to_matrix()
        self.mini_platform_matrices()
    
        start_is_placed = False
        end_is_placed = False

        for line_num, line in enumerate(self.__map_matrix) :
            line_number_arcade_coordinates = self.__height - (line_num + 1)
            # To match line number with convention that first line is h-1, last line is 0
            for position_x, sprite_char in enumerate(line) :
                x_coordinate = PIXELS_IN_BLOCK * position_x
                y_coordinate =  PIXELS_IN_BLOCK * line_number_arcade_coordinates
                match sprite_char : 
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
                    case char if char in self.__hidden_characters | self.__arrow_characters :
                        pass
                    case char if char in self.__allowed_characters :
                        match sprite_char :
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
                        sprite = arcade.Sprite(name_and_list[0], center_x= x_coordinate, center_y= y_coordinate, scale=constants.SCALE)
                        if self.give_movement_to_sprites(sprite) :
                            self.__platform_list.append(sprite)
                        else :
                            name_and_list[1].append(sprite)  

        if not start_is_placed :
            raise Exception("Player must have a starting point")
        if self.__has_next_map and not end_is_placed :
            raise Exception("The file sets the next map but no end to the level")
        
    def get_player_coordinates(self) -> tuple[int, int] :
        return self.player_coordinates
    
    def get_next_map(self) -> str :
        return self.__next_map
    