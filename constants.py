"""All global constants are defined here. File to be imported as needed."""

PLAYER_MOVEMENT_SPEED = 5
"""Lateral speed of the player, in pixels per frame"""

PLAYER_GRAVITY = 1
"""Gravity applied to the player, in pixels per frame"""

PLAYER_JUMP_SPEED = 18
"""Instant vertical speed for jumping, in pixels per frame"""

SCALE = 0.5
"""Scale for all sprites"""

PIXELS_IN_BLOCK = 64
"""Size in pixels of one block"""

PLATFORM_SPEED = 1
"""Speed of platforms"""

WINDOW_HEIGHT = 720
"""Height of the arcade window in pixels"""

WINDOW_WIDTH = 1280
"""Width of the arcade window in pixels"""

GHOST_SPEED = -1       # is negative to make the slime move in the direction it is facing (technicality)
"""Speed of the ghost"""

GHOST_SPAWN_HEIGHT = 10 
"""Makes the ghost spawn at correct distance from floor"""

CAMERA_X_MARGIN = 400
"""Max margin between player x coordinate and edges of camera"""

CAMERA_Y_MARGIN = 200
"""Max margin between player y coordinate and edges of camera"""

ARROW_SPEED = 25
"""Speed of an arrow"""

ARROW_GRAVITY = 0.8
"""Gravity felt by an arrow"""

BAT_SPEED = 2
"""Speed of bats"""

BAT_ACTION_RADIUS = 75
"""Radius in which a bat can move around it's spawning point"""

BAT_FRAMES = 2
"""Number of frames every which we change direction randomly"""

BLUE_BLOB_SPEED = -2       # is negative to make the slime move in the direction it is facing (technicality)
"""Speed of the blue blobs"""

BOSS_SPEED = 3
"""Speed of boss"""

BOSS_ACTION_RADIUS = 500
"""Radius in which boss can move around it's spawning point"""

BOSS_FRAMES = 80
"""Number of frames every which we change direction randomly"""

FROG_SPEED = -1       # is negative to make the frog move in the direction it is facing (technicality)
"""Speed of the frogs blobs"""

FROG_JUMP_SPEED = 10
"""Frog jump speed"""

FROG_GRAVITY = 1
"""Gravity felt by frogs"""

DISTANCE_ARME_JOUEUR = 25 # ATTENTION : Ça veut dire quoi?
"""Distance between weapon and center of player"""

DELTA_H = 5
"""Height of weapon compared to player center"""

SWORD_ACTIVE_FRAMES = 7
"""Number of frames after spawn during which the sword can hit an enemy"""

BOW_TIME_OUT = 15
"""Number of frames necessary after spawn before bow can shoot"""