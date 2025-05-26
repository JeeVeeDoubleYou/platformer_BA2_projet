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
                    door_in_map = map_doors[y][x]
                    if not isinstance(door_in_map, Door):
                        raise Exception(f"There is no door at (x, y) = {(x, y)}")
                    list_open.append(door_in_map)
                case {'x': int() as x, 'y': int() as y,'action':'close-gate'}:
                    door_in_map = map_doors[y][x]
                    if not isinstance(door_in_map, Door):
                        raise Exception(f"There is no door at (x, y) = {(x, y)}")
                    list_close.append(door_in_map)
                case _:
                    raise Exception(f"unknown action")
        return (list_open, list_close, one_time_use)

    def lever_door_linking(self, ymal_part : dict[str,object], map_doors : list[list[Door|None]], map_levers : list[list[Lever|None]]) -> None:
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
                                activation_open, activation_close, on_deactivate = self.__action_linking(switch_on, map_doors)
                        match switch:
                            case {'switch_off': list() as switch_off}:
                                        tuple = self.__action_linking(switch_off, map_doors)
                                        deactivation_open = tuple[0] 
                                        deactivation_close = tuple[1] 
                                        off_deactivate = tuple[2]
                        if switch.get('state') == True:
                            start_on = True       
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
            match ymal_part:
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