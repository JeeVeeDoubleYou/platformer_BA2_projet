from door import Door
from lever import Lever
from custom_exception import CustomException


class LeverDoorsLogic :

    """
    Handles the logic linking levers to doors in the map.
    This includes configuring which doors open or close when a lever is activated or deactivated,
    supporting one-time-use levers, and setting initial door states based on configuration data.
    """

    def __init__(self) -> None :
        pass

    def __action_linking(self, switch_on_or_off: list[dict[str,object]],
                        map_doors: list[list[Door|None]]) ->tuple[list[Door],list[Door],bool]:
        """
        Interprets a list of lever actions and returns which doors to open or close.

        Returns
            - A list of doors to open
            - A list of doors to close
            - A boolean: True if this lever should be disabled after use

        Raises exception: If an action is unknown or refers to an invalid map position.
        """
        
        one_time_use : bool = False
        list_close: list[Door] = []
        list_open: list[Door] = []
        for element in switch_on_or_off:
            if not isinstance(element,dict):
                raise CustomException("A switch_on action is incorect")
            assert(isinstance(element,dict))
            match element:
                case {'action':'disable'}:
                    one_time_use = True
                case {'x': int() as x, 'y': int() as y,'action':'open-gate'}:
                    if   y < 0  or y > len(map_doors) or x > len(map_doors[0]) or  x < 0:
                       raise Exception(f"door given at {(x, y)} is outside of the map")
                    door_in_map = map_doors[y][x]
                    if not isinstance(door_in_map, Door):
                        raise CustomException(f"There is no door at (x, y) = {(x, y)}")
                    list_open.append(door_in_map)
                case {'x': int() as x, 'y': int() as y,'action':'close-gate'}:
                    if   y < 0  or y > len(map_doors) or x > len(map_doors[0]) or  x < 0:
                       raise Exception(f"door given at {(x, y)} is outside of the map")
                    door_in_map = map_doors[y][x]
                    if not isinstance(door_in_map, Door):
                        raise CustomException(f"There is no door at (x, y) = {(x, y)}")
                    list_close.append(door_in_map)
                case _:
                    raise CustomException(f"unknown action")
        return (list_open, list_close, one_time_use)
 

    def lever_door_linking(self, ymal_part : dict[str,object],
                            map_doors : list[list[Door|None]],
                            map_levers : list[list[Lever|None]]) -> None:
        """
        Sets up the links between levers and doors based on the config data.
        Raises Exception: If the config is invalid or references an invalid location.
        """
        try:
            match ymal_part:
                case {'switches': list() as switches}:
                    for switch in switches:
                        if not isinstance(switch,dict):
                            raise CustomException("The switch list is incorect")
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
                                deactivation_open, deactivation_close, off_deactivate = self.__action_linking(switch_off, map_doors)
                        if switch.get('state') == True:
                            start_on = True       
                        match switch:
                            case {'x': int() as x, 'y': int() as y}:
                                if  y < 0  or y > len(map_levers) or x > len(map_levers[0]) or  x < 0:
                                    raise Exception(f"lever given at {(x, y)} is outside of the map")
                                lever_in_map = map_levers[y][x]
                                if isinstance(lever_in_map, Lever):
                                    lever : Lever = lever_in_map
                                    lever.link_doors(activation_close ,activation_open, deactivation_close,
                                                      deactivation_open, on_deactivate, off_deactivate, start_on)
                                else: CustomException(f"There is no lever at (x, y) = {(x, y)}")
                            case _ :
                                raise Exception("Please, use integer to precise the lever coordinate")
            match ymal_part:
                case {'gates': list() as doors}:
                    for door in doors:
                        if not isinstance(door, dict):
                            raise CustomException("A door action is incorect")
                        assert(isinstance(door,dict))
                        match door:
                            case {'x': int() as x, 'y': int() as y,'state':'open'}:
                                if   y < 0  or y > len(map_doors) or x > len(map_doors[0]) or  x < 0:
                                    raise Exception(f"door given at {(x, y)} is outside of the map")
                                door_in_map = map_doors[y][x]
                                if isinstance(door_in_map,Door):
                                    door_in_map.open()
                                else: raise CustomException(f"There is no door at (x, y) = {(x, y)}")
                                
        except ValueError :
            pass