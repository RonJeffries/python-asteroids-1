import pygame
from pygame import Vector2
import u
from flyer import InvadersFlyer
from invaders.Collider import Collider
from invaders.bitmap_maker import BitmapMaker
from invaders.invader_score import InvaderScore
from invaders.shot_explosion import InvadersExplosion
from invaders.timecapsule import TimeCapsule
from sounds import player


# noinspection PyProtectedMember
class Unready:
    def __init__(self, saucer):
        self._saucer = saucer

    def die_if_lonely(self, invader_fleet, fleets):
        self._saucer._die_if_lonely(invader_fleet, fleets)

    def finish_initializing(self, shot_count):
        self._saucer._finish_initializing(shot_count)

    def just_draw(self, screen):
        pass

    def move_or_die(self, fleets):
        pass


class Ready:
    def __init__(self, saucer):
        self._saucer = saucer

    def die_if_lonely(self, _invader_fleet, _fleets):
        pass

    def finish_initializing(self, shot_count):
        pass

    # noinspection PyProtectedMember
    def just_draw(self, screen):
        self._saucer._just_draw(screen)

    # noinspection PyProtectedMember
    def move_or_die(self, fleets):
        self._saucer._move_or_die(fleets)


class InvadersSaucer(InvadersFlyer):
    def __init__(self):
        maker = BitmapMaker.instance()
        self._map = maker.saucer
        self._mask = pygame.mask.from_surface(self._map)
        self._rect = self._map.get_rect()
        half_width = self._rect.width // 2
        self._left = u.BUMPER_LEFT + half_width
        self._right = u.BUMPER_RIGHT - half_width
        self._speed = 0
        self._player_shot_count = 0
        self._score_list = [100, 50, 50, 100, 150, 100, 100, 50, 300, 100, 100, 100, 50, 150, 100]
        self._readiness = Unready(self)

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

    def interact_with_invaderfleet(self, invader_fleet, fleets):
        self._readiness.die_if_lonely(invader_fleet, fleets)

    def interact_with_invaderplayer(self, player, fleets):
        self._player_shot_count = player.shot_count
        self._readiness.finish_initializing(self._player_shot_count)

    def interact_with_playershot(self, shot, fleets):
        if Collider(self, shot).colliding():
            explosion = InvadersExplosion.saucer_explosion(self.position, 0.5)
            fleets.append(explosion)
            fleets.append(InvaderScore(self._mystery_score()))
            self._die(fleets)

    def update(self, delta_time, fleets):
        self._readiness.move_or_die(fleets)

    def draw(self, screen):
        self._readiness.just_draw(screen)

    def _die(self, fleets):
        fleets.remove(self)
        fleets.append(TimeCapsule(10, InvadersSaucer()))

    def _die_if_lonely(self, invader_fleet, fleets):
        if invader_fleet.invader_count() < 8:
            self._die(fleets)

    def _finish_initializing(self, shot_count):
        self._readiness = Ready(self)
        speed = 8
        even_or_odd = shot_count % 2
        self._speed = (-speed, speed)[even_or_odd]
        left_or_right = (self._right, self._left)[even_or_odd]
        self.rect.center = Vector2(left_or_right, u.INVADER_SAUCER_Y)

    def _just_draw(self, screen):
        screen.blit(self._map, self.rect)

    def _move_or_die(self, fleets):
        x = self.position.x + self._speed
        if x > self._right or x < self._left:
            self._die(fleets)
        else:
            frac = (x - self._left)/(self._right - self._left)
            player.play_stereo("ufo_lowpitch", frac, False)
            self.position = (x, self.position.y)

    def _mystery_score(self):
        score_index = self._player_shot_count % len(self._score_list)
        return self._score_list[score_index]

