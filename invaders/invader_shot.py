import pygame
from pygame import Vector2

import u
from invaders.Collider import Collider
from invaders.bitmap_maker import BitmapMaker
from flyer import InvadersFlyer


class InvaderShot(InvadersFlyer):
    def __init__(self, position, sprite):
        self._sprite = sprite
        self.position = position
        self.count = 0
        self.moves = 0
        self._available = True
        explosion = BitmapMaker.instance().invader_shot_explosion
        self.explosion_mask = pygame.mask.from_surface(explosion)

    @property
    def available(self):
        return self._available

    @property
    def mask(self):
        return self._sprite.mask

    @property
    def rect(self):
        return self._sprite.rectangle

    @property
    def position(self):
        return self._sprite.position

    @position.setter
    def position(self, vector):
        self._sprite.position = vector

    def fire_from(self, position, fleets):
        self._available = False
        self.position = position
        fleets.append(self)

    def update(self, _dt, fleets):
        self.count = (self.count + 1) % 3
        if self.count == 0:
            self.move(fleets)

    def move(self, fleets):
        self.moves += 1
        self.update_map()
        self.position = self.position + Vector2(0, 16)
        if self.position.y >= u.SCREEN_SIZE:
            self.die(fleets)

    def update_map(self):
        self._sprite.next_frame()

    def interact_with_bottomline(self, line, fleets):
        self.die_on_collision(line, fleets)

    def interact_with_invaderplayer(self, player, fleets):
        self.die_on_collision(player, fleets)

    def interact_with_playershot(self, shot, fleets):
        self.die_on_collision(shot, fleets)

    def interact_with_roadfurniture(self, shield, fleets):
        self.die_on_collision(shield, fleets)

    def die_on_collision(self, flyer, fleets):
        if self.colliding(flyer):
            self.die(fleets)

    def die(self, fleets):
        self._available = True
        fleets.remove(self)

    def colliding(self, invaders_flyer):
        collider = Collider(self, invaders_flyer)
        return collider.colliding()

    def interact_with(self, other, fleets):
        other.interact_with_invadershot(self, fleets)

    def draw(self, screen):
        self._sprite.draw(screen)
