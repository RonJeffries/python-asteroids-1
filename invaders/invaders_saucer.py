import pygame
from pygame import Vector2
import u
from flyer import InvadersFlyer
from invaders.Collider import Collider
from invaders.bitmap_maker import BitmapMaker
from invaders.invader_score import InvaderScore
from invaders.shot_explosion import InvadersExplosion
from invaders.timecapsule import TimeCapsule


class InvadersSaucer(InvadersFlyer):
    def __init__(self, direction=1):
        self.direction = direction
        maker = BitmapMaker.instance()
        self._map = maker.saucer
        self._mask = pygame.mask.from_surface(self._map)
        self._rect = self._map.get_rect()
        half_width = self._rect.width // 2
        self._left = u.BUMPER_LEFT + half_width
        self._right = u.BUMPER_RIGHT - half_width
        self._speed = 0
        self._player = None
        self._score_list = [100, 50, 50, 100, 150, 100, 100, 50, 300, 100, 100, 100, 50, 150, 100]
        self.initialized = False

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
        if invader_fleet.invader_count() < 8:
            self.die(fleets)

    def interact_with_invaderplayer(self, player, fleets):
        self._player = player

    def interact_with_playershot(self, shot, fleets):
        if Collider(self, shot).colliding():
            explosion = InvadersExplosion.saucer_explosion(self.position, 0.5)
            fleets.append(explosion)
            fleets.append(InvaderScore(self.mystery_score()))
            self.die(fleets)

    def end_interactions(self, fleets):
        if not self.initialized and self._player:
            shot_count = self._player.shot_count % 2
            self.init_motion(shot_count)

    def init_motion(self, shot_count):
        self.initialized = True
        speed = 8
        if shot_count == 0:
            self._speed = -speed
            self.rect.center = Vector2(self._right, u.INVADER_SAUCER_Y)
        else:
            self._speed = speed
            self.rect.center = Vector2(self._left, u.INVADER_SAUCER_Y)

    def mystery_score(self):
        if not self._player:
            return 0
        score_index = self._player.shot_count % len(self._score_list)
        return self._score_list[score_index]

    def die(self, fleets):
        fleets.remove(self)
        fleets.append(TimeCapsule(10, InvadersSaucer()))

    def update(self, delta_time, fleets):
        if not self.initialized:
            return
        x = self.position.x + self._speed
        if x > self._right or x < self._left:
            self.die(fleets)
        else:
            self.position = (x, self.position.y)

    def draw(self, screen):
        screen.blit(self._map, self.rect)

