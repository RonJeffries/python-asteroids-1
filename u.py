# U - Universal Constants
import pygame
from pygame import Vector2

SCREEN_SIZE = 1024
SPEED_OF_LIGHT = 500
SCALE_FACTOR = 0.75

ASTEROID_DELAY = 4
ASTEROID_SCORE_LIST = [100, 50, 20]
ASTEROID_SPEED = pygame.Vector2(100, 0)
CENTER = pygame.Vector2(SCREEN_SIZE // 2, SCREEN_SIZE // 2)
FRAGMENT_SPEED = SPEED_OF_LIGHT // 6
FRAGMENT_LIFETIME = 2
FREE_SHIP_SCORE = 3000
MISSILE_LIFETIME = 3
MISSILE_LIMIT = 4
MISSILE_SPEED = SPEED_OF_LIGHT // 3
PLAYER_ZERO = 0
PLAYER_ONE = 1
SAFE_EMERGENCE_DISTANCE = 200
SAUCER_EMERGENCE_TIME = 7
SAUCER_MISSILE_DELAY = 0.5
SAUCER_MISSILE_LIMIT = 2
SAUCER_SCORE_FOR_SMALL = 3000
SAUCER_VELOCITY = pygame.Vector2(150, 0)
SAUCER_ZIG_TIME = 1
SAUCER_TARGETING_FRACTION = 0.25
SHIPS_PER_QUARTER = 4
SHIP_ACCELERATION = pygame.Vector2(120, 0)
SHIP_EMERGENCE_TIME = 3
SHIP_HYPERSPACE_MAX_VELOCITY = SPEED_OF_LIGHT // 6
SHIP_HYPERSPACE_RECHARGE_TIME = 5
SHIP_ROTATION_STEP = 120

# Invaders

"""
;##-AlienStartTable
; Starting Y coordinates for aliens at beginning of rounds. The first round is initialized to $78 at 07EA.
; After that this table is used for 2nd, 3rd, 4th, 5th, 6th, 7th, 8th, and 9th. The 10th starts over at
; 1DA3 (60).
1DA3: 60                                    
1DA4: 50                                    
1DA5: 48                                    
1DA6: 48                                    
1DA7: 48                                    
1DA8: 40                                    
1DA9: 40                                    
1DAA: 40   
"""

BOTTOM_LINE_OFFSET = 50
BUMPER_LEFT = 64
BUMPER_RIGHT = 960
INVADER_HALF_WIDTH = 32
INVADER_PLAYER_Y = SCREEN_SIZE - 128
INVADER_SAUCER_Y = 128
INVADER_SAUCER_HALF_WIDTH = 48
INVADER_SAUCER_SCORE_LIST = [100, 50, 50, 100, 150, 100, 100, 50, 300, 100, 100, 100, 50, 150, 100]
INVADER_SAUCER_X_MIN = BUMPER_LEFT + INVADER_SAUCER_HALF_WIDTH
INVADER_SAUCER_X_MAX = BUMPER_RIGHT - INVADER_SAUCER_HALF_WIDTH
INVADER_SPACING = 64
INVADER_SPEED = 8
INVADER_FIRST_START = 0x40
INVADER_STARTS = 0x60, 0x50, 0x48, 0x48, 0x48, 0x40, 0x40, 0x40
# 8080 values height = 256 = 0x100. Our screen is 4x that size and upside down.
RESERVE_PLAYER_Y = SCREEN_SIZE - 32
SHIELD_OFFSET = 208
SHIELD_Y = SCREEN_SIZE - 208
INVADER_DOWN_STEP_Y = 32
INVADER_TOO_FAR_DOWN_Y = SHIELD_Y
