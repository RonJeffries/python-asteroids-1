import random

import pygame
from pygame import Vector2

import u
from Collider import Collider
from bitmap_maker import BitmapMaker
from flyer import InvadersFlyer
from invader_shot import InvaderShot
from player_explosion import PlayerExplosion
from player_shot import PlayerShot
from timecapsule import TimeCapsule


class InvaderPlayer(InvadersFlyer):

    def interact_with_playermaker(self, maker, fleets):
        pass

    def interact_with_timecapsule(self, capsule, fleets):
        pass

    def __init__(self):
        maker = BitmapMaker.instance()
        self.players = maker.players  # one turret, two explosions
        self.player = self.players[0]
        self._mask = pygame.mask.from_surface(self.player)
        self._rect = self.player.get_rect()
        self.step = 4
        half_width = self.rect.width / 2
        self.left = 64 + half_width
        self.right = 960 - half_width
        self.rect.center = Vector2(self.left, u.SCREEN_SIZE - 5*32 - 16)
        self.free_to_fire = True
        self.fire_request_allowed = True

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

    def begin_interactions(self, fleets):
        self.free_to_fire = True

    def trigger_pulled(self, fleets):
        if self.fire_request_allowed:
            self.attempt_firing(fleets)
        self.fire_request_allowed = False

    def trigger_released(self):
        self.fire_request_allowed = True

    def attempt_firing(self, fleets):
        if self.free_to_fire:
            fleets.append(PlayerShot(self.rect.center))

    def update(self, _delta_time, fleets):
        if not pygame.get_init():
            return
        keys = pygame.key.get_pressed()
        self.check_motion(keys)
        self.check_firing(fleets, keys)

    def check_firing(self, fleets, keys):
        if keys[pygame.K_k]:
            self.trigger_pulled(fleets)
        else:
            self.trigger_released()

    def check_motion(self, keys):
        if keys[pygame.K_f]:
            self.move(self.step)
        elif keys[pygame.K_d]:
            self.move(-self.step)

    def move(self, amount):
        self.rect.centerx = max(self.left, min(self.rect.centerx + amount, self.right))

    def interact_with(self, other, fleets):
        other.interact_with_invaderplayer(self, fleets)

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderexplosion(self, explosion, fleets):
        pass

    def interact_with_invaderfleet(self, fleet, fleets):
        pass

    def interact_with_invaderplayer(self, player, fleets):
        pass

    def interact_with_invadershot(self, shot, fleets):
        collider = Collider(self, shot)
        if collider.colliding():
            self.hit_by_shot(fleets)

    def hit_by_shot(self, fleets):
        fleets.append(PlayerExplosion(self.position))
        fleets.remove(self)

    def interact_with_playerexplosion(self, _explosion, _fleets):
        pass

    def interact_with_playershot(self, bumper, fleets):
        self.free_to_fire = False

    def interact_with_shield(self, shield, fleets):
        pass

    def interact_with_shotcontroller(self, controller, fleets):
        pass

    def interact_with_shotexplosion(self, bumper, fleets):
        pass

    def interact_with_topbumper(self, top_bumper, fleets):
        pass

    def draw(self, screen):
        screen.blit(self.player, self.rect)

    def tick(self, delta_time, fleets):
        pass