import pygame
from pygame import Vector2
import u
from flyer import InvadersFlyer
from invaders.invader_score import InvaderScore
from invaders.shot_explosion import InvadersExplosion
from invaders.sprite import Sprite, Spritely
from sounds import player


class InvadersSaucer(Spritely, InvadersFlyer):
    def __init__(self, shot_count=0):
        self.init_sprite()
        self.init_position_and_speed(shot_count)

    # noinspection PyAttributeOutsideInit
    def init_sprite(self):
        self._sprite = Sprite.saucer()

    # noinspection PyAttributeOutsideInit
    def init_position_and_speed(self, shot_count):
        self._player_shot_count = shot_count
        even_or_odd = shot_count % 2
        starting_x_coordinate = (u.INVADER_SAUCER_X_MAX, u.INVADER_SAUCER_X_MIN)[even_or_odd]
        self.position = Vector2(starting_x_coordinate, u.INVADER_SAUCER_Y)
        self._speed = (-u.INVADER_SPEED, u.INVADER_SPEED)[even_or_odd]

    def interact_with(self, other, fleets):
        other.interact_with_invaderssaucer(self, fleets)

    def interact_with_playershot(self, shot, fleets):
        if self.colliding(shot):
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
