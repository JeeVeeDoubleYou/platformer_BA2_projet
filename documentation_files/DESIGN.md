# Liste de Modules et leurs Classes 

## Central
| Module        | Classes | Description                  |
|---------------|-------------------------------|------------------------------|
| `main.py`         | -        | Lancement du programme             |
| `gameview.py`     | `GameView`      | Classe principale du jeu        |
## Ennemis

| Module        | Classes | Description                  |
|---------------|-------------------------------|------------------------------|
| `monster.py`  | `Monster`                     | Classe abstraite de base des ennemis. Elle étend arcade.Sprite |
| `bat.py`      | `Bat`                         | Monstre qui vole aléatoirement, dans un rayon d'action. N'est pas affecté par les murs.                             |
| `blob.py`     | `Blob`                        | Monstre qui bouge sur le sol, faisant des aller-retours.                             |
| `frog.py`     | `Frog`                        | Monstre qui bouge comme un blob, mais qui saute verticalement parfois, aléatoirement.                          |
| `ghost.py`    | `Ghost`                       | Monstre qui bouge comme un blob, mais qui n'est pas affecté par les murs. Il devient peu à peu transparent, jusqu'à qu'il soit presque invisible.            |
| `boss.py`     | `Boss` `Attack`      |  Monstre spécial, ayant ses propres attaques, définies dans l'enum `Attack`. Il choisit ses attaques aléatoirement, sauf dans certaines situations spécifiques. Il étend aussi la classe `Lever`. Il peut alors ouvrir des portes, à sa mort. Il est doté de plusieurs vies.   |

```
Monster
├── Blob
│    ├── Frog
│    └── Ghost
├── Bat
└── Boss → Lever
```

## Armes

| Module           | Classes | Description                  |
|------------------|---------------------------------|------------------------------|
| `weapon.py`      | `Weapon`                       | Classe abstraite de base des armes. Elle étend arcade.Sprite. |
| `bow.py`         | `Bow`                         | Classe représentant l'arc     |
| `sword.py`       | `Sword`                       | Classe représentant l'épée  |
| `arrow.py`       | `Arrow`                       | Classe représentant les flèches tirées par l'arc |
| `weapon_type.py` | `WeaponType` | Enum des types d'armes : Bow et Sword, pour l'instant. Pour référencer une arme sans en créer une instance.  |

```
Weapon
├── Bow
└── Sword

Arrow
WeaponType
````

## Joueur

| Module           | Classes | Description                  |
|------------------|---------------------------------|------------------------------|
| `player.py`      | `Player`                       | Classe représentant le joueur. Elle étend arcade.Sprite. |

## Map

| Module                   | Classes    | Description                  |
|--------------------------|-------------------------------|------------------------------|
| `platforms.py`           | `Platform`, `Direction(Enum)`   | `Platform` représente une ensemble de blocs qui bougent ensemble. Ici, les blocs sont représentés par leur position initiale, par leur type. `Direction` représente les directions dans lesquelles peut bouger un platforme, VERTICAL ou HORIZONTAL. |
| `platform_arrows.py`     | `PlatformArrows`| Une classe étendant `Enum`, permettant de transformer une flèche en caractère spécial, par exemple "←", en type de donné facilement manipulable par le code. |
| `non_platform_moving_blocks.py` | `NonPlatformMovingBlocks` | Cette classe représente un bloc en mouvement, d'un type dont le mouvement n'est pas géré directement par Arcade, tel que la lave, ou les interrupteurs. |
| `lever.py`               | `Lever`                     | Classe représentant un interrupteur, qui peut agir sur des `Door` |
| `door.py`                | `Door`                      | Classe représentant une porte, qui peut-être être ouverte ou fermée.   |
| `map.py`          | `Map` | Classe gérant la création des cartes. |
| `map_mouvement.py`| `MapMovement` | Classe gérant le mouvement des platformes dans la carte.  |
| `lever_doors_logic.py`   | `LeverDoorsLogic`          | Classe gérant l'association entre les `Lever` et les `Door`, à la création de la carte.  |

## Utilitaires

*Ces modules sont importées presque partout, elles sont faites pour ça. Ce sont des modules qui nous 
permettent de simplifier les calculs, de centraliser les constantes, et d'éviter la duplication de code pour des outils qui sont utilisés dans plusieurs classes
différentes.*

| Module            | Classes | Description                  |
|-------------------|----------------------------|------------------------------|
| `constants.py`    | -                  | Contient toutes les constantes du projet. Permet à celles-ci d'être facilement accessibles. |
| `helper.py`       | `Disk`, fonctions utilitaires | `Disk` permet de créer le rayon d'action de la chauve-souris et du boss. |
| `math_personal.py`| -               | Fonctions mathématiques simples mais non-présentes directement dans le module `math`. |
| `custom_exception.py` | `CustomException` | Type d'Exception lancé par notre code, afin de s'assure que le message d'erreur à destination de l'utilisateur soit lisible. Tout autre type d'exception imprime simplement "An unknow error has occured".

# Intéraction des classes entre elles


La classe principale du projet est la classe `GameView.` Celle-ci importe les 
classes principales des autres sous-groupes de classes, telles que `Monster` 
ou `Weapon`. Cependant, elle n'importe pas les classes comme `Blob` ou 
`Sword`, qui étendent ces classes principales, grâce au polymorphisme. En effet, `GameView` travaille essentiellement 
sur des listes — plus précisément des SpriteList — contenant des `Monster`. 
Grâce au polymorphisme de ces classes abstraites, il n'est pas nécessaire 
de différencier les types de `Monster` pour les faire se déplacer, attaquer ou mourir.  

  
Une partie importante du travail de `GameView` consiste à créer une instance de la 
classe `Map`. Celle-ci importe tous les différents types de Sprites, notamment les 
sous-classes de `Monster`, et lit le fichier de carte que le joueur a sélectionné. 
Pour cela, elle remplit les listes de `Monster`, `Lava`, etc., que `GameView` lui 
a fournies, avec les sprites correspondants, en se basant sur le fichier texte fourni.  

En plus des sprites `Monster` et des blocs immobiles, la carte est aussi constituée 
de plateformes mobiles, ainsi que d'interrupteurs. Afin de produire une carte complète 
comprenant ces éléments, la classe `Map` se sert des classes `MapMovement` 
(qui permet de gérer les blocs mobiles) et `LeverDoorsLogic` (qui s'occupe des liens 
entre les `Lever` et les `Door`). 

Un autre groupe de classes sont celles qui étendent `Monster`, comme mentionné 
précédemment. `Monster` est une classe abstraite définissant les méthodes publiques move() 
et die(). Pour satisfaire au principe de polymorphisme nécessaire dans `GameView`, ainsi qu'à 
l'encapsulation, les sous-classes de `Monster` ne définissent aucune méthode publique 
supplémentaire. Ainsi, une fois la carte créée, il n'est jamais nécessaire de connaître 
le type exact de `Monster` pour le faire évoluer. Une particularité est qu'une de ses 
sous-classes, `Boss`, étend également Lever en plus d’étendre `Monster`. Ici, le LSP est respecté.
En effet, toute sous classe de `Monster` peut-être remplacée là où un un `Monster` est attendu.

Nous avons aussi l’ensemble des classes relatives aux armes. `Weapon`, une classe 
abstraite, suit les mêmes principes que `Monster` avec ses sous-classes. Ainsi, 
`Weapon` et ses sous-classes gèrent elles-mêmes leurs collisions, leurs déplacements, etc. 
Pour cette raison, `Weapon` importe la classe `Lever`. Liées logiquement à Weapon, 
nous avons les classes `Arrow` et `WeaponType`. La première est simplement le sprite lancé 
par un `Bow`. Elle est séparée de la classe `Bow`, car une fois lancée, le mouvement de 
l’arc n’a plus aucun impact sur celui de la flèche. 
La seconde classe, `WeaponType`, est une énumération des types d’armes, 
permettant de représenter le type d'arme accessible au joueur sans en instancier une.  

`Player` est la classe représentant notre joueuse. Elle gère le mouvement, 
le score (les pièces ramassées), ainsi que l’arme sélectionnée, 
qui est différente de l’arme active. En effet, il y a toujours 
une arme sélectionnée, mais pas nécessairement une arme équipée. 

Enfin, la dernière classe importante est la classe `UI`. 
Une instance de `UI` est créée dans `GameView` et s’occupe de toute l’interface 
graphique annexe du jeu. Par exemple, elle affiche la vie restante du boss, 
s’il y en a un. En revanche, l’affichage principal, tel que celui de la 
joueuse, est géré directement dans `GameView`.

Nous avons aussi plusieurs autres classes utilitaires et 
énumérations, que vous pouvez retrouver dans les tableaux ci-dessus 
mais dont l’utilité ne sera pas détaillée ici.

# Méthodes intéressantes

La méthode create_weapon() de `WeaponType` est un exemple du principe encapsulation. 
En effet, cette méthode crée directement un `Weapon` du type voulu, sans que `GameView` ou 
`Player` ait besoin de connaître le type de l'arme. Il y a même une encapsulation double, si l'on prend en compte la 
méthode du même nom appartenant à `Player`. Grâce à cette méthode, et donc au principe d'encapsulation, 
`GameView`, qui appelle Player().create_weapon() n'a même pas besoin de savoir que la classe `WeaponType` existe, 
alors que c'est elle qui fait le travail derrière l'appel de la fonction.
Pour prouver que `WeaponType` n'existe pas au yeux de `GameView`, il suffit de remarquer que `GameView` n'importe pas la classe `WeaponType`. 
Ainsi, pour `GameView`, toute la classe `WeaponType` est relégué au status de détail d'implémentation.

Nous avons beaucoup utilisé les propriétés dans ce projet, en conjonction avec les méthodes et les attributs privés, 
afin de protéger nos classes d'interférences externes. Un exemple est dans `Platform`, où nous avons l'attribut privé
__direction, ainsi qu'un getter et un setter publiques pour cet attribut, afin de pouvoir lire et écrire l'attribut sans casser 
la logique de __direction, qui est que chaque platforme ne peut bouger que dans une direction. Ainsi, dans le setter de direction,
nous nous assurons que self.__horizontal_movement soit None, avant d'autorister l'attribut à être mis-à-jour en Direction.VERTICAL.

La méthode __partition_file() de `Map` utilise les expressions régulières, afin de permettre à notre code de lire une map créée 
aussi bien sur Mac, Linux et Windows.

#Analyse complexite

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
1:Arcade remarque quand plusieurs sprites sont retires en meme temps et supprime directement la liste au lieu de supprimer les sprites un par un