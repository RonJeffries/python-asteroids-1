from invaders.player_explosion import PlayerExplosion
from invaders.player_shot import PlayerShot
from flyer import InvadersFlyer
from pygame import Vector2
import pygame

from invaders.sprite import Sprite, Spritely
from sounds import player
import u


class InvaderPlayer(Spritely, InvadersFlyer):
    def __init__(self):
        self._sprite = Sprite.player()
        self.step = 4
        half_width = self.rect.width / 2
        self.left = 64 + half_width
        self.right = 960 - half_width
        self.rect.center = Vector2(self.left, u.INVADER_PLAYER_Y)
        self.free_to_fire = True
        self.fire_request_allowed = True
        self.shot_count = 0

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
            self.fire(fleets)

    def fire(self, fleets):
        frac = self.x_fraction()
        player.play_stereo("shoot", frac)
        self.shot_count += 1
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

    def interact_with_invadershot(self, shot, fleets):
        if self.colliding(shot):
            self.hit_by_shot(fleets)

    def hit_by_shot(self, fleets):
        frac = self.x_fraction()
        player.play_stereo("explosion", frac)
        fleets.append(PlayerExplosion(self.position))
        fleets.remove(self)

    def x_fraction(self):
        x = self.rect.centerx - self.left
        denom = self.right - self.left
        return x / denom

    def interact_with_playershot(self, bumper, fleets):
        self.free_to_fire = False
