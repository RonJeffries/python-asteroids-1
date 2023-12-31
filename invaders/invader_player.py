from invaders.player_explosion import PlayerExplosion
from invaders.player_shot import PlayerShot
from flyer import InvadersFlyer
from pygame import Vector2
import pygame

from invaders.sprite import Sprite, Spritely
from sounds import player
import u


class InvaderPlayer(Spritely, InvadersFlyer):
    def __init__(self, reserve_number=0):
        self._sprite = Sprite.player()
        x = u.INVADER_PLAYER_LEFT + reserve_number*(5*self.rect.width//4)
        self.position = Vector2(x, u.INVADER_PLAYER_Y)
        self.reserve_number = reserve_number

        self._free_to_fire = True
        self.fire_request_allowed = True
        self.shot_count = 0

    def begin_interactions(self, fleets):
        self._free_to_fire = True

    def interact_with_playershot(self, bumper, fleets):
        self._free_to_fire = False

    def trigger_pulled(self, fleets):
        if self.fire_request_allowed:
            self.attempt_firing(fleets)
        self.fire_request_allowed = False

    def trigger_released(self):
        self.fire_request_allowed = True

    def attempt_firing(self, fleets):
        if self._free_to_fire:
            self.fire(fleets)

    def fire(self, fleets):
        frac = self.x_fraction()
        player.play_stereo("shoot", frac)
        self.shot_count += 1
        fleets.append(PlayerShot(self._sprite.center))

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
            self.move(u.INVADER_STEP)
        elif keys[pygame.K_d]:
            self.move(-u.INVADER_STEP)

    def move(self, amount):
        centerx = max(u.INVADER_PLAYER_LEFT, min(self.position.x + amount, u.INVADER_PLAYER_RIGHT))
        self.position = Vector2(centerx, self.position.y)

    def interact_with(self, other, fleets):
        other.interact_with_invaderplayer(self, fleets)

    def interact_with_destructor(self, destructor, fleets):
        self.hit_by_something(fleets)

    def interact_with_invadershot(self, shot, fleets):
        if self.colliding(shot):
            self.hit_by_something(fleets)

    def hit_by_something(self, fleets):
        frac = self.x_fraction()
        player.play_stereo("explosion", frac)
        fleets.append(PlayerExplosion(self.position))
        fleets.remove(self)

    def hit_invader(self, invader, fleets):
        self.hit_by_something(fleets)

    def x_fraction(self):
        x = self.position.x - u.INVADER_PLAYER_LEFT
        denom = u.INVADER_PLAYER_RIGHT - u.INVADER_PLAYER_LEFT
        return x / denom
