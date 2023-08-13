import pygame
from pygame import Vector2

import u
from bitmap_maker import BitmapMaker
from flyer import InvadersFlyer
from player_shot import PlayerShot


class InvaderPlayer(InvadersFlyer):

    def __init__(self):
        maker = BitmapMaker.instance()
        self.players = maker.players  # one turret, two explosions
        self.player = self.players[0]
        self.rect = self.player.get_rect()
        self.rect.center = Vector2(u.SCREEN_SIZE/2, u.SCREEN_SIZE - 5*32 - 16)
        self.step = 4
        half_width = self.rect.width / 2
        self.left = 64 + half_width
        self.right = 960 - half_width
        self.free_to_fire = True

    def begin_interactions(self, fleets):
        self.free_to_fire = True

    def interact_with_playershot(self, bumper, fleets):
        self.free_to_fire = False

    def attempt_firing(self, fleets):
        if self.free_to_fire:
            fleets.append(PlayerShot())

    def update(self, _delta_time, _fleets):
        if not pygame.get_init():
            return
        keys = pygame.key.get_pressed()
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

    def interact_with_invaderfleet(self, bumper, fleets):
        pass

    def interact_with_invaderplayer(self, bumper, fleets):
        pass

    def draw(self, screen):
        screen.blit(self.player, self.rect)

    def tick(self, delta_time, fleets):
        pass