"""All global constants are defined here. File to be imported as needed."""

"""Lateral speed of the player, in pixels per frame"""
PLAYER_MOVEMENT_SPEED = 5

"""Gravity applied to the player, in pixels per frame"""
PLAYER_GRAVITY = 1

"""Instant vertical speed for jumping, in pixels per frame"""
PLAYER_JUMP_SPEED = 18

"""Scale for all sprites"""
SCALE = 0.5

"""Size in pixels of one block"""
PIXELS_IN_BLOCK = 64

"""Speed of platforms"""
PLATFORM_SPEED = 1

"""Height of the arcade window in pixels"""
WINDOW_HEIGHT = 720

"""Width of the arcade window in pixels"""
WINDOW_WIDTH = 1280

"""Speed of the ghost"""
GHOST_SPEED = -1       # is negative to make the slime move in the direction it is facing (technicality)

"""Makes the ghost spawn at correct distance from floor"""
GHOST_SPAWN_HEIGHT = 10 

"""Max margin between player x coordinate and edges of camera"""
CAMERA_X_MARGIN = 400

"""Max margin between player y coordinate and edges of camera"""
CAMERA_Y_MARGIN = 200

"""Speed of an arrow"""
ARROW_SPEED = 25

"""Gravity felt by an arrow"""
ARROW_GRAVITY = 0.8

"""Speed of bats"""
BAT_SPEED = 2

"""Radius in which a bat can move around it's spawning point"""
BAT_ACTION_RADIUS = 75

"""Number of frames every which we change direction randomly"""
BAT_FRAMES = 2

"""Speed of the blue blobs"""
BLUE_BLOB_SPEED = -2       # is negative to make the slime move in the direction it is facing (technicality)

"""Speed of boss"""
BOSS_SPEED = 3

"""Radius in which boss can move around it's spawning point"""
BOSS_ACTION_RADIUS = 500

"""Number of frames every which we change direction randomly"""
BOSS_FRAMES = 80

"""Speed of the frogs blobs"""
FROG_SPEED = -1       # is negative to make the frog move in the direction it is facing (technicality)

"""Frog jump speed"""
JUMP_SPEED = 10

"""Gravity felt by frogs"""
FROG_GRAVITY = 1

"""Distance between weapon and center of player"""
DISTANCE_ARME_JOUEUR = 25 # ATTENTION : Ça veut dire quoi?

"""Height of weapon compared to player center"""
DELTA_H = 5

"""Number of frames after spawn during which the sword can hit an enemy"""
SWORD_ACTIVE_FRAMES = 7

"""Number of frames necessary after spawn before bow can shoot"""
BOW_TIME_OUT = 15