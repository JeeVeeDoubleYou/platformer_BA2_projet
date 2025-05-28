analyse de complexite de setup de plateforme avec n nombred de blocks dans la plateforme



def find_platforms_in_map_matrix(self, map_matrix : list[list[str]]) -> None :
        """Goes to each position in self.__map_matrix and checks if the sprite there could be part of
        a moving platform. If so, it calls function self.grouping_platform(), passing an empty platform instance, 
        which becomes a full platform. 
        This platform gets added to self.__list_of_platforms if it's movement is not zero.
        """
        visited : set[tuple[int, int]] = set()     # θ(1)

        for line in range(len(map_matrix)) :   
            for column in range(len(map_matrix[line])): 
                if map_matrix[line][column] in self.__platform_characters and (line, column) not in visited :      # θ(1)
                    platform = Platform()      # θ(1)
                    self.__grouping_platform(map_matrix, line, column, platform, visited, None) # θ(f)
                    if platform.moves : # θ(1)
                        self.__list_of_platforms.append(platform)   # θ(1)





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
            return  # θ(1)
        if map_matrix[line][column] not in self.__platform_characters | {a.value for a in PlatformArrows} :
            return  # θ(1)

        if (value := map_matrix[line][column]) in {a.value for a in PlatformArrows} :
            arrow_type = PlatformArrows.get_arrow_enum(value)   # θ(1)
            if arrow_type == valid_arrow :  # θ(1)
                visited.add((line, column)) # add dans un set est θ(1)
                arrows_counted = arrow_type.count_arrows(line, column, 1, visited, map_matrix)  # θ(1)
                platform.add_arrow_info(arrow_type, arrows_counted) # θ(1)
            else :
                return  # θ(1)
        else :
            visited.add((line, column)) # add dans un set est θ(1)
            if map_matrix[line][column] in self.__platform_characters : # θ(1)
                arcade_line = matrix_line_num_to_arcade(line, len(map_matrix))  # θ(1)
                platform.add_sprite((arcade_line, column))  # θ(1)

            for d_line, d_col, direction_arrow in [(0, -1, PlatformArrows.LEFT), (0, 1, PlatformArrows.RIGHT), (1, 0, PlatformArrows.DOWN), (-1, 0, PlatformArrows.UP)] :
                self.__grouping_platform(map_matrix, line + d_line, column + d_col, platform, visited, direction_arrow)

On cree 4 instances de self.grouping_plateforme et un appel a self.grouping_plateforme est en O(1). 
On pourrait donc penser que self.grouping_plateforme est en θ(4^n).
Or, pour une case aux coordonnees x, y, on ne peut avoir que 4 appels a
self.__grouping_platform(map_matrix, x, y, visited, direction_arrow).
En effet, on ne peut acceder a une case que par 4 chemins differents, sinon cela veut dire que l'on a accede a une case deja contenue dans visited.
Donc, pour chaque case comprise dans notre plateforme et sa frontiere, on ne peut avoir que 4 appels.
Et on sait aussi que la frontiere est au plus de 2n + 2 (cas ou l'on prend une plateforme allongee).

Donc, on en conclut que dans le pire cas possible, la complexite est de O(9n) = O(n)





















Arrow on updade tourne en θ(n²) ou n est le nombre d'arrow

les deux fonction qui utilisent les arrow sont:



for arrow in list(self.__arrow_list) : #on repete n donc θ(n²)

            for lever in arcade.check_for_collision_with_list(arrow, self.__lever_list):# on repete c fois (c=cst) donc θ(n)
                if not lever.broken:
                    lever.on_action()   # θ(1)
                    self.solid_block_update()   # θ(1)
                    arcade.play_sound(arcade.load_sound(":resources:sounds/rockHit2.wav")) 
                    arrow.remove_from_sprite_lists()    # θ(1)
                break
                

            for monster in arcade.check_for_collision_with_list(arrow, self.__monster_list) : on repete c fois(c=cst) donc θ(n)
                self.__on_monster_death(monster)    # θ(1)
                arrow.remove_from_sprite_lists()    # θ(1)
                break   # θ(1)

            for _ in arcade.check_for_collision_with_lists(arrow, ( self.__solid_block_list,
                                                                    self__list_of_sprites_in_platforms, 
                                                                    self.__lava_list)):# θ(c) on repete c fois(c=cst) donc θ(n)

                arcade.play_sound(arcade.load_sound(":resources:sounds/rockHit2.wav"))  # θ(1)
                arrow.remove_from_sprite_lists()    # θ(1)
                break   # θ(1)

for arrow in self.__arrow_list :   on repete n donc #   θ(n)
            arrow.move()    #  θ(1)
            if (arrow.center_y < self.__camera.bottom_left.y):  #  θ(1)
                arrow.remove_from_sprite_lists()    #  θ(1)


def move(self) -> None : # donc θ(1)
        """Defines the movement of an arrow."""
        
        self.change_y -= constants.ARROW_GRAVITY    #  θ(1)
        self.center_x += self.change_x  #  θ(1)
        self.center_y += self.change_y  #  θ(1)
        self.angle = atan2_deg(self.change_x,self.change_y) - 45    #  θ(1)






arrow.remove_from_sprite_lists()    # θ(1)
Apparament  arrow.remove from spritelist est en θ(1) voici quelques hypotheses sur pourquoi ce serait le cas:
1)Arcade remarque quand plusieurs sprites sont retires en meme temps et supprime directement la liste au lieu de supprimer les sprites un par un