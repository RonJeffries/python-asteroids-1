import pygame
from pygame import Vector2
import u
from flyer import InvadersFlyer
from invaders.Collider import Collider
from invaders.bitmap_maker import BitmapMaker
from invaders.invader_score import InvaderScore
from invaders.shot_explosion import InvadersExplosion
from sounds import player


class InvadersSaucer(InvadersFlyer):
    def __init__(self, shot_count=0):
        self.init_map_mask_rect()
        self.init_for_scoring(shot_count)
        self.init_motion_limits()
        self.init_start_and_direction(shot_count)

    def init_for_scoring(self, shot_count):
        self._player_shot_count = shot_count
        self._score_list = [100, 50, 50, 100, 150, 100, 100, 50, 300, 100, 100, 100, 50, 150, 100]

    # noinspection PyAttributeOutsideInit
    def init_motion_limits(self):
        half_width = self._rect.width // 2
        self._x_minimum = u.BUMPER_LEFT + half_width
        self._x_maximum = u.BUMPER_RIGHT - half_width

    # noinspection PyAttributeOutsideInit
    def init_start_and_direction(self, shot_count):
        even_or_odd = shot_count % 2
        starting_x_coordinate = (self._x_maximum, self._x_minimum)[even_or_odd]
        self.rect.center = Vector2(starting_x_coordinate, u.INVADER_SAUCER_Y)
        self._speed = (-u.INVADER_SPEED, u.INVADER_SPEED)[even_or_odd]

    # noinspection PyAttributeOutsideInit
    def init_map_mask_rect(self):
        maker = BitmapMaker.instance()
        self._map = maker.saucer
        self._mask = pygame.mask.from_surface(self._map)
        self._rect = self._map.get_rect()

    @property
    def mask(self):
        return self._mask

    @property
    def rect(self):
        return self._rect

    @property
    def position(self):
        return Vector2(self.rect.center)

    @position.setter
    def position(self, value):
        self.rect.center = value

    def interact_with(self, other, fleets):
        other.interact_with_invaderssaucer(self, fleets)

    def interact_with_playershot(self, shot, fleets):
        if Collider(self, shot).colliding():
            explosion = InvadersExplosion.saucer_explosion(self.position, 0.5)
            fleets.append(explosion)
            fleets.append(InvaderScore(self._mystery_score()))
            self._die(fleets)

    def update(self, delta_time, fleets):
        self._move_along_x()
        self._adjust_stereo_position()
        self._die_if_done(fleets)

    def draw(self, screen):
        screen.blit(self._map, self.rect)

    def _die(self, fleets):
        fleets.remove(self)

    def _move_along_x(self):
        self.position = (self.position.x + self._speed, self.position.y)

    def _adjust_stereo_position(self):
        frac = (self.position.x - self._x_minimum) / (self._x_maximum - self._x_minimum)
        player.play_stereo("ufo_lowpitch", frac, False)

    def _die_if_done(self, fleets):
        if self._going_off_screen():
            self._die(fleets)

    def _going_off_screen(self):
        return not self._x_minimum <= self.position.x <= self._x_maximum

    def _mystery_score(self):
        score_index = self._player_shot_count % len(self._score_list)
        return self._score_list[score_index]
