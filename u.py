# U - Universal Constants
import pygame

SCREEN_SIZE = 1024
SPEED_OF_LIGHT = 500

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
