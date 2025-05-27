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
classes principales des sous-groupes d'autres classes, telles que `Monster` 
ou `Weapon`. Cependant, elle n'importe pas d'autres classes comme `Blob` ou 
`Sword`, qui étendent ces classes principales, grâce au polymorphisme. En effet, `GameView` travaille essentiellement 
sur des listes — plus précisément des SpriteList — contenant des `Monster` ou des 
`Weapon`. Grâce au polymorphisme de ces classes abstraites, il n'est pas nécessaire 
de différencier les types de `Monster` pour les faire se déplacer, attaquer ou mourir.  

  
Une partie importante du travail de `GameView` consiste à créer une instance de la 
classe `Map`. Celle-ci importe tous les différents types de Sprites, notamment les 
sous-classes de `Monster`, et lit le fichier de carte que le joueur a sélectionné. 
Pour cela, elle remplit les listes de `Monster`, `Lava`, etc., que `GameView` lui 
a fournies, avec les sprites correspondants, en se basant sur le fichier texte fourni.  

En plus des sprites `Monster` et des blocs immobiles, la carte est aussi constituée 
de plateformes mobiles, ainsi que de interrupteurs. Afin de produire une carte complète 
comprenant ces éléments, la classe `Map` s’appuie sur les classes `MapMovement` 
(qui permet de gérer les blocs mobiles) et `LeverDoorsLogic` (qui s'occupe des liens 
entre les `Lever` et les `Door`). 

Séparément, nous avons l’ensemble des classes qui étendent `Monster`, comme mentionné 
précédemment. `Monster` est une classe abstraite définissant les méthodes publiques move() 
et die(). Pour satisfaire aux principes de polymorphisme et d'encapsulation nécessaires 
dans `GameView`, les sous-classes de `Monster` ne définissent aucune méthode publique 
supplémentaire. Ainsi, une fois la carte créée, il n'est jamais nécessaire de connaître 
le type exact de `Monster` pour le faire évoluer. Une particularité est qu'une de ses 
sous-classes, `Boss`, étend également Lever en plus d’étendre `Monster`. 


Nous avons aussi l’ensemble des classes relatives aux armes. `Weapon`, une classe 
abstraite, suit les mêmes principes que `Monster` avec ses sous-classes. Ainsi, 
`Weapon` et ses sous-classes gèrent elles-mêmes leurs collisions, leurs déplacements, etc. 
Pour cette raison, `Weapon` importe la classe `Lever`. Liées logiquement à Weapon, 
nous avons les classes `Arrow` et `WeaponType`. La première est simplement le sprite lancé 
par un `Bow`. Elle est séparée de la classe `Bow`, car une fois lancée, le mouvement de 
l’arc n’a plus aucun impact sur celui de la flèche. La seconde classe, `WeaponType`, 
est une énumération des types d’armes, permettant de représenter le type d'arme 
accessible au joueur sans en instancier une.  

`Player` est la classe représentant notre joueuse. Elle gère le mouvement, 
le score (les pièces ramassées), ainsi que l’arme sélectionnée, 
qui est différente de l’arme active. En effet, il y a toujours 
une arme sélectionnée, mais pas nécessairement une arme équipée. 


Enfin, la dernière classe (hors classes utilitaires et autres 
énumérations que vous pouvez retrouver dans les tableaux ci-dessus 
mais dont l’utilité ne sera pas détaillée ici) est la classe `UI`. 
Une instance de `UI` est créée dans `GameView` et s’occupe de toute l’interface 
graphique annexe du jeu. Par exemple, elle affiche la vie restante du boss, 
s’il y en a un. En revanche, l’affichage principal, tel que celui de la 
joueuse, est géré directement dans `GameView`.