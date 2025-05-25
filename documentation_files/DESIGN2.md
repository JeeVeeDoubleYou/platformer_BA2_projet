# Liste de Modules et leurs Classes 

## Central
| Module        | Classes | Description                  |
|---------------|-------------------------------|------------------------------|
| `main.py`         | -        | Lancement du programme             |
| `gameview.py`     | `GameView`      | Classe principale du jeu        |
## Ennemis

| Module        | Classes | Description                  |
|---------------|-------------------------------|------------------------------|
| `monster.py`  | `Monster`                     | Classe de base des ennemis   |
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
| `weapon.py`      | `Weapon`                       | Classe de base des armes      |
| `bow.py`         | `Bow`                         |                              |
| `sword.py`       | `Sword`                       |                              |
| `arrow.py`       | `Arrow`                       |                              |
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
| `player.py`      | `Player`                       |                              |

## Map

| Module                   | Classes    | Description                  |
|--------------------------|-------------------------------|------------------------------|
| `platforms.py`           | `Platform`                   |                              |
| `platform_arrows.py`     | (probablement `PlatformArrow`)|                              |
| `non_platform_moving_blocks.py` | (probablement `NonPlatformBlock`) |                        |
| `lever.py`               | `Lever`                     |                              |
| `lever_doors_logic.py`   | (logique/gestion)            |                              |
| `door.py`                | `Door`                      |                              |
| `map.py`          | `Map` (ou classe associée) | Gestion de la carte          |
| `map_mouvement.py`| (classes déplacement ?)    | Mouvement sur la carte       |

## Utilitaires

| Module            | Classes | Description                  |
|-------------------|----------------------------|------------------------------|
| `constants.py`    | (aucune)                  | Constantes globales          |
| `helper.py`       | `Disk`, fonctions utilitaires | Fonctions math et géométrie |
| `math_personal.py`| (fonctions)                | Fonctions math personnalisées|