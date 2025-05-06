import os
from typing import Final
import arcade
import yaml

from bat import Bat
from blob import Blob
from lever import Lever
from door import Door
import constants
from monster import Monster

from typing import Any # ATTENTION : chacker si on peut utiliser Any avec le prof, dans la fonction lever_door_linking() 
class Map :

    player_coordinates : tuple[int, int]
    __next_map : str
    __allowed_characters : Final[frozenset[str]] = frozenset({"S", "o", "v", "E", "=", "-", "x", "*", "£", " ", "|", "^", "\n", "\r"})
    __hidden_characters : Final[frozenset[str]] = frozenset({" ", "\n", "\r"})
    
    def __init__(self, current_map_name : str, wall_list: arcade.SpriteList[arcade.Sprite], 
                 lava_list: arcade.SpriteList[arcade.Sprite], coin_list: arcade.SpriteList[arcade.Sprite], 
                 monster_list: arcade.SpriteList[Monster], door_list: arcade.SpriteList[Door], lever_list: arcade.SpriteList[Lever], end_list: arcade.SpriteList[arcade.Sprite]) -> None:
    
        self.__current_map_name = current_map_name
        self.__wall_list = wall_list
        self.__lava_list = lava_list
        self.__coin_list = coin_list
        self.__monster_list = monster_list
        self.__door_list = door_list
        self.__lever_list = lever_list
        self.__end_list = end_list
        self.__next_map = ""

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
        self.__map_matrix = [["" for i in range(self.__width)] for j in range(self.__height)]
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
        map_doors : list[list[Door | None]] = [[None for i in range(self.__width)] for j in range(self.__height)]
        map_levers : list[list[Lever | None]] = [[None for i in range(self.__width)] for j in range(self.__height)]
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
                    case "^" :
                        lever = Lever(x_coordinate, y_coordinate)
                        self.__lever_list.append(lever)
                        map_levers[line_number_arcade_coordinates][position_x] = lever
                        
                    case "|" :
                        door = Door(x_coordinate, y_coordinate)
                        self.__door_list.append(door)
                        map_doors[line_number_arcade_coordinates][position_x] = door

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
        self.lever_door_linking(map_doors,map_levers) 
        
    def get_player_coordinates(self) -> tuple[int, int] :
        return self.player_coordinates
    
    def get_next_map(self) -> str :
        return self.__next_map
    
