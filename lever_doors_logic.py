from door import Door
from lever import Lever


class LeverDoorsLogic :

    def __init__(self) -> None :
        pass

    def __action_linking(self, switch_on_or_off: list[dict[str,object]],
                        map_doors: list[list[Door|None]]) ->tuple[list[Door],list[Door],bool]:
        """Make door be opened or closed when the coresponding lever is ativated"""
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
                    if   y < 0  or y > len(map_doors) or x > len(map_doors[0]) or  x < 0:
                       raise Exception(f"door given at {(x, y)} is outside of the map")
                    door_in_map = map_doors[y][x]
                    if not isinstance(door_in_map, Door):
                        raise Exception(f"There is no door at (x, y) = {(x, y)}")
                    list_open.append(door_in_map)
                case {'x': int() as x, 'y': int() as y,'action':'close-gate'}:
                    if   y < 0  or y > len(map_doors) or x > len(map_doors[0]) or  x < 0:
                       raise Exception(f"door given at {(x, y)} is outside of the map")
                    door_in_map = map_doors[y][x]
                    if not isinstance(door_in_map, Door):
                        raise Exception(f"There is no door at (x, y) = {(x, y)}")
                    list_close.append(door_in_map)
                case _:
                    raise Exception(f"unknown action")
        return (list_open, list_close, one_time_use)
            
    # ATTENTION : Is *never* used
    def __add_door_to_list(self, map_doors : list[list[Door|None]], x : int, y : int, list : list[Door]) -> None :
        """Takes the [y][x] element in map_doors, checks that it's a door and adds it to the list."""
        if   y < 0  or y > len(map_doors) or x > len(map_doors[0]) or  x < 0:
           raise Exception(f"door given at {(x, y)} is outside of the map")
        door = map_doors[y][x]
        if not isinstance(door, Door):
            raise Exception(f"There is no door at (x, y) = {(x, y)}")
        assert(isinstance(door, Door))
        list.append(door)

    # ATTENTION : Wanted to refactor the switch underneath but i have problems with dict type anotation in function 
    # def set_lever_action(self, dict_key : str, open_list : list[Door], close_list : list[Door], map_doors : list[list[Door|None]]):

    def lever_door_linking(self, ymal_part : dict[str,object],
                            map_doors : list[list[Door|None]],
                            map_levers : list[list[Lever|None]]) -> None:
        """Make the levere able to open their door"""
        try:
            match ymal_part:
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
                                tuple = self.__action_linking(switch_on, map_doors)
                                activation_open = tuple[0] 
                                activation_close = tuple[1] 
                                on_deactivate = tuple[2]
                                #for element in switch_on:
                                #    if not isinstance(element,dict):
                                #        raise Exception("A switch_on action is incorect")
                                #    assert(isinstance(switch,dict))
                                #    match element:
                                #        case {'action':'disable'}:
                                #            one_time_use = True
                                #        case {'x': int() as x, 'y': int() as y,'action':'open-gate'}:
                                #            self.add_door_to_list(map_doors, x, y, activation_open)
                                #        case {'x': int() as x, 'y': int() as y,'action':'close-gate'}:
                                #            self.add_door_to_list(map_doors, x, y, activation_close)
                        match switch:
                            case {'switch_off': list() as switch_off}:
                                        tuple = self.__action_linking(switch_off, map_doors)
                                        deactivation_open = tuple[0] 
                                        deactivation_close = tuple[1] 
                                        off_deactivate = tuple[2]
                        if switch.get('state') == True:
                            start_on = True
                                #for element in switch_off:
                                #    if not isinstance(element,dict):
                                #        raise Exception("A switch_off action is incorect")
                                #    assert(isinstance(switch, dict))
                                #    match element:
                                #        case {'action':'disable'}:
                                #            one_time_use = True
                                #        case {'x': int() as x, 'y': int() as y,'action':'open-gate'}:
                                #            self.add_door_to_list(map_doors, x, y, deactivation_open)    
                                #        case {'x': int() as x, 'y': int() as y,'action':'close-gate'}:
                                #            self.add_door_to_list(map_doors, x, y, deactivation_close)        
                        match switch:
                            case {'x': int() as x, 'y': int() as y}:
                                if  y < 0  or y > len(map_levers) or x > len(map_levers[0]) or  x < 0:
                                    raise Exception(f"lever given at {(x, y)} is outside of the map")
                                lever_in_map = map_levers[y][x]
                                if isinstance(lever_in_map, Lever):
                                    lever : Lever = lever_in_map
                                    lever.link_doors(activation_close ,activation_open, deactivation_close,
                                                      deactivation_open, on_deactivate, off_deactivate, start_on)
                                else: Exception(f"There is no lever at (x, y) = {(x, y)}")
                            case _ :
                                raise Exception("Please, use integer to precise the lever coordinate")
            match ymal_part:
                case {'gates': list() as doors}:
                    for door in doors:
                        if not isinstance(door, dict):
                            raise Exception("A door action is incorect")
                        assert(isinstance(door,dict))
                        match door:
                            case {'x': int() as x, 'y': int() as y,'state':'open'}:
                                if   y < 0  or y > len(map_doors) or x > len(map_doors[0]) or  x < 0:
                                    raise Exception(f"door given at {(x, y)} is outside of the map")
                                door_in_map = map_doors[y][x]
                                if isinstance(door_in_map,Door):
                                    door_in_map.open()
                                else: raise Exception(f"There is no door at (x, y) = {(x, y)}")
                                
        except ValueError :
            pass