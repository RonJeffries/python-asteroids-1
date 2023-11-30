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
        self.init_map_mask_rect(shot_count)
        self.init_position_and_speed(shot_count)

    # noinspection PyAttributeOutsideInit
    def init_map_mask_rect(self, shot_count):
        self._player_shot_count = shot_count
        maker = BitmapMaker.instance()
        self._map = maker.saucer
        self.mask = pygame.mask.from_surface(self._map)
        self.rect = self._map.get_rect()

    # noinspection PyAttributeOutsideInit
    def init_position_and_speed(self, shot_count):
        even_or_odd = shot_count % 2
        starting_x_coordinate = (u.INVADER_SAUCER_X_MAX, u.INVADER_SAUCER_X_MIN)[even_or_odd]
        self.position = Vector2(starting_x_coordinate, u.INVADER_SAUCER_Y)
        self._speed = (-u.INVADER_SPEED, u.INVADER_SPEED)[even_or_odd]

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, value):
        self._mask = value

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value

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
            self.explode_scream_and_die(fleets)

    def explode_scream_and_die(self, fleets):
        explosion = InvadersExplosion.saucer_explosion(self.position, 0.5)
        fleets.append(explosion)
        fleets.append(InvaderScore(self._mystery_score()))
        self.play_death_sound()
        self._die(fleets)

    def update(self, delta_time, fleets):
        self._move_along_x()
        self._adjust_stereo_position()
        self._die_if_done(fleets)

    def draw(self, screen):
        screen.blit(self._map, self.rect)

    def _die(self, fleets):
        fleets.remove(self)

    def play_death_sound(self):
        frac = (self.position.x - u.INVADER_SAUCER_X_MIN) / (u.INVADER_SAUCER_X_MAX - u.INVADER_SAUCER_X_MIN)
        player.play_stereo("ufo_highpitch", frac, True)


    def _move_along_x(self):
        self.position = (self.position.x + self._speed, self.position.y)

    def _adjust_stereo_position(self):
        frac = (self.position.x - u.INVADER_SAUCER_X_MIN) / (u.INVADER_SAUCER_X_MAX - u.INVADER_SAUCER_X_MIN)
        player.play_stereo("ufo_lowpitch", frac, False)

    def _die_if_done(self, fleets):
        if self._going_off_screen():
            self._die(fleets)

    def _going_off_screen(self):
        return not u.INVADER_SAUCER_X_MIN <= self.position.x <= u.INVADER_SAUCER_X_MAX

    def _mystery_score(self):
        score_index = self._player_shot_count % len(u.INVADER_SAUCER_SCORE_LIST)
        return u.INVADER_SAUCER_SCORE_LIST[score_index]
