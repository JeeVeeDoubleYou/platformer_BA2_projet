import arcade
import constants
from non_platform_moving_blocks import NonPlatformMovingBlocks
from platform_arrows import PlatformArrows
from platforms import Direction, Platform
from helper import matrix_line_num_to_arcade


class MapMovement :

    __platform_characters = frozenset({"=", "-", "x", "£", "E", "^"})
    __non_wall_platform_characters = frozenset({"£", "E", "^"})
    __list_of_platforms : list[Platform]

    def __init__(self, non_platform_moving_sprites_list : list[NonPlatformMovingBlocks]) -> None :
        self.__non_platform_moving_sprites_list = non_platform_moving_sprites_list
        self.__list_of_platforms = []

    def find_platforms_in_map_matrix(self, map_matrix : list[list[str]]) -> None :
        """Goes to each position in self.__map_matrix and checks if the sprite there could be part of
        a moving platform. If so, it calls function self.grouping_platform(), passing an empty platform instance, 
        which becomes a full platform. 
        This platform gets added to self.__list_of_platforms if it's movement is not zero.
        """
        visited : set[tuple[int, int]] = set()

        for line in range(len(map_matrix)) :
            for column in range(len(map_matrix[line])):
                if map_matrix[line][column] in self.__platform_characters and (line, column) not in visited :
                    platform = Platform()
                    self.__grouping_platform(map_matrix, line, column, platform, visited, None)
                    if platform.moves :
                        self.__list_of_platforms.append(platform)


    def __grouping_platform(self, map_matrix : list[list[str]], line : int, column : int, platform : Platform, visited : set[tuple[int, int]], valid_arrow : PlatformArrows | None) -> None :
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

        if line < 0 or column < 0 or line >= len(map_matrix) or column >= len(map_matrix[0]) or (line, column) in visited :
            return
        if map_matrix[line][column] not in self.__platform_characters | {a.value for a in PlatformArrows} :
            return

        if (value := map_matrix[line][column]) in {a.value for a in PlatformArrows} :
            arrow_type = PlatformArrows.get_arrow_enum(value)
            if arrow_type == valid_arrow :
                visited.add((line, column))
                arrows_counted = arrow_type.count_arrows(line, column, 1, visited, map_matrix)
                platform.add_arrow_info(arrow_type, arrows_counted)
            else :
                return
        else :
            visited.add((line, column))
            if map_matrix[line][column] in self.__platform_characters : 
                arcade_line = matrix_line_num_to_arcade(line, len(map_matrix))
                platform.add_sprite((arcade_line, column))
            
            for d_line, d_col, direction_arrow in [(0, -1, PlatformArrows.LEFT), (0, 1, PlatformArrows.RIGHT), (1, 0, PlatformArrows.DOWN), (-1, 0, PlatformArrows.UP)] :
                self.__grouping_platform(map_matrix, line + d_line, column + d_col, platform, visited, direction_arrow)

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
                sprite.change_y = constants.PLATFORM_SPEED
                return True
            case Direction.HORIZONTAL :
                sprite.boundary_left = sprite.left - movement[0] 
                sprite.boundary_right = sprite.right + movement[1] 
                sprite.change_x = constants.PLATFORM_SPEED
                return True
            case None :
                return False
            
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