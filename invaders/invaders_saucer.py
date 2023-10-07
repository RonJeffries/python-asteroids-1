import pygame
from pygame import Vector2
import u
from flyer import InvadersFlyer
from invaders.Collider import Collider
from invaders.bitmap_maker import BitmapMaker
from invaders.invader_score import InvaderScore
from invaders.timecapsule import TimeCapsule


class InvadersSaucer(InvadersFlyer):
    def __init__(self, direction=1):
        self.direction = direction
        maker = BitmapMaker.instance()
        self.saucers = maker.saucers  # one turret, two explosions
        self._map = self.saucers[0]
        self._mask = pygame.mask.from_surface(self._map)
        self._rect = self._map.get_rect()
        half_width = self._rect.width // 2
        self._left = u.BUMPER_LEFT + half_width
        self._right = u.BUMPER_RIGHT - half_width
        self.rect.center = Vector2(self._left, u.INVADER_SAUCER_Y)
        self._speed = 8
        self._player = None
        self._score_list = [100, 50, 50, 100, 150, 100, 100, 50, 300, 100, 100, 100, 50, 150, 100]

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
            fleets.append(InvaderScore(self.mystery_score()))
            self.die(fleets)

    def mystery_score(self):
        if not self._player:
            return 0
        score_index = self._player.shot_count % len(self._score_list)
        return self._score_list[score_index]

    def die(self, fleets):
        fleets.remove(self)
        fleets.append(TimeCapsule(10, InvadersSaucer()))

    def update(self, delta_time, fleets):
        x = self.position.x + self._speed
        if x > self._right:
            self.die(fleets)
        else:
            self.position = (x, self.position.y)

    def draw(self, screen):
        screen.blit(self._map, self.rect)

