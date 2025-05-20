import os
from typing import Final
import arcade
import yaml

from bat import Bat
from blob import Blob
from lever import Lever
from door import Door
import constants
from constants import PIXELS_IN_BLOCK, PLATFORM_SPEED
from monster import Monster

from platforms import Platform, Direction
from non_platform_moving_blocks import NonPlatformMovingBlocks
from platform_arrows import PlatformArrows

class Map :

    player_coordinates : tuple[int, int]
    __next_map : str | None
    __allowed_characters : Final[frozenset[str]] = frozenset({"S", "o", "v", "E", "=", "-", 
                                                              "x", "*", "£", "^", " ", "|", "^", "\n", 
                                                              "\r", "←", "→", "↑", "↓"})
    __hidden_characters : Final[frozenset[str]] = frozenset({" ",  "\n","\r"})
    __arrow_characters : Final[frozenset[str]] = frozenset({"←", "→", "↑", "↓"})
    __platform_characters = frozenset({"=", "-", "x", "£", "E", "^"})
    __non_wall_platform_characters = frozenset({"£", "E", "^"})
    __list_of_platforms : list[Platform]
    
    def __init__(self, current_map_name : str, wall_list: arcade.SpriteList[arcade.Sprite], 
                 lava_list: arcade.SpriteList[arcade.Sprite], coin_list: arcade.SpriteList[arcade.Sprite], 
                 monster_list: arcade.SpriteList[Monster], door_list: arcade.SpriteList[Door], 
                 lever_list: arcade.SpriteList[Lever], end_list: arcade.SpriteList[arcade.Sprite], 
                 platform_list: arcade.SpriteList[arcade.Sprite],
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
        self.__list_of_platforms = []
        self.__platform_list = platform_list
        self.__non_platform_moving_sprites_list = non_platform_moving_sprites_list

        self.__create_map()
    
    def lever_door_linking(self, map_doors : list[list[Door|None]], map_levers : list[list[Lever|None]]) -> None:
        """relie les portes au levier
        ATTENTION cette fonction marche mais n'est pas securiser
        """
        
        
        with open(self.__current_map_name, "r", encoding="utf-8", newline='') as file:
            level = file.read()
            partition = level.split('---\n',1)
            yaml_return : object = yaml.safe_load(partition[0])
            assert(isinstance(yaml_return,dict))
            if not ('switches' in yaml_return):
                return
            if ('gates' in yaml_return):
                for door in yaml_return['gates']:
                    if 'state' and 'x' and 'y' in door:
                        element = map_doors[door['y']][door['x']]
                        if door['state'] =='open'  and isinstance(element,Door): 
                            element.open()
            lever_list = yaml_return['switches']
            for switch in lever_list:
                activation_close : list[Door] = [] 
                activation_open : list[Door] = []  
                deactivation_close : list[Door] = [] 
                deactivation_open : list[Door] = [] 
                start_on : bool = False
                one_time_use : bool = False
                if 'state' in switch:
                    if isinstance(switch['state'],bool):
                            start_on = switch['state']
                if 'switch_on' in switch:
                    for element in switch['switch_on']:
                        #element : dict[str:str]
                        #x_position : int = int(element['x'])
                        #y_position : int = int(element['y'])
                        if 'action' in element: 
                            match element['action']:
                                case 'disable':
                                    one_time_use = True
                                case 'open-gate':
                                    if 'x' and 'y' in element:
                                        activation_open.append(map_doors[element['y']][element['x']])
                                case 'close-gate':
                                    if 'x' and 'y' in element:
                                        activation_close.append(map_doors[element['y']][element['x']])
                if 'switch_off' in switch:
                    for element in switch['switch_off']:
                        if 'action' in element: 
                            match element['action']:
                                case 'disable':
                                    one_time_use = True
                                case 'open-gate':
                                    deactivation_open.append(map_doors[element['y']][element['x']])
                                case 'close-gate':
                                    deactivation_close.append(map_doors[element['y']][element['x']])
                if 'x' and 'y' in switch:
                    lever : Lever = map_levers[switch['y']][switch['x']]
                    lever.link_doors(activation_close ,activation_open, deactivation_close, deactivation_open, one_time_use,start_on)
            

    def __parse_config(self) -> None :
        """Parses the configuration part of the map file."""
        with open(self.__current_map_name, "r", encoding="utf-8", newline='') as f :
            self.__width = 0
            self.__height = 0

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
        """Turns map file into a matrix"""
        self.__map_matrix = [["" for i in range(self.__width)] for j in range(self.__height)]
        # Matrice[Lines][Colonne]
        with open(self.__current_map_name, "r", encoding="utf-8", newline='') as f :
            while not f.readline() == "---\n" :
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
            if not f.readline().rstrip("\n") == "---" :
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
        Arcadem convention is top line is height - 1, last line is 0."""
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

    def give_movement_to_non_platform_sprites(self, sprite : arcade.Sprite) -> bool :
        """Takes an arcade.Sprite as argument. Checks if it belongs to some platform. 
        If it does, gives the platform movement to the individual sprite and returns True. 
        Otherwise, return False.
        Should *only* be called to sprites that haven't started moved yet.
        Should be called on sprites that *are* in self.__non_wall_platform_characters."""
        direction, movement = self.get_sprite_boundaries(sprite)
        if direction is None :
            return False
        self.__non_platform_moving_sprites_list.append(NonPlatformMovingBlocks(sprite, direction, movement, arcade.Vec2(sprite.center_x, sprite.center_y))) 
        return True

    def give_movement_to_platform_sprites(self, sprite : arcade.Sprite) -> bool :
        """Takes an arcade.Sprite as argument. Checks if it belongs to some platform. 
        If it does, gives the platform movement to the individual sprite and returns True. 
        Otherwise, return False.
        Should *only* be called to sprites that haven't started moved yet.
        Should be called on sprites that *are not* in self.__non_wall_platform_characters.
        """
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

        self.__parse_config()
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
                    case "|" :
                        door = Door(x_coordinate, y_coordinate)
                        self.__door_list.append(door)
                        map_doors[line_num_arcade][position_x] = door
                    case "^" :
                        lever = Lever(x_coordinate, y_coordinate)
                        self.__lever_list.append(lever)
                        map_levers[line_num_arcade][position_x] = lever
                        self.give_movement_to_non_platform_sprites(lever) # ATTENTION : Cas spécial, mais devrait généraliser avec fonction peutetre
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
                        if char in self.__non_wall_platform_characters :
                            self.give_movement_to_non_platform_sprites(sprite)
                        if (char in self.__platform_characters - self.__non_wall_platform_characters) and (self.give_movement_to_platform_sprites(sprite)) :
                            self.__platform_list.append(sprite)
                        else : # This else only applies to the last if. This condition is met as long as the sprite didn't go into the platform list.
                            name_and_list[1].append(sprite)  

        if not start_is_placed :
            raise Exception("Player must have a starting point")
        if self.__next_map is not None and not end_is_placed :
            raise Exception("The file sets the next map but no end to the level")
        self.lever_door_linking(map_doors,map_levers) 
        
    def get_player_coordinates(self) -> tuple[int, int] :
        return self.player_coordinates
    
    def get_next_map(self) -> str | None :
        return self.__next_map
    
