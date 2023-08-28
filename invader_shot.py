import pygame
from pygame import Vector2

import u
from Collider import Collider
from flyer import InvadersFlyer


class InvaderShot(InvadersFlyer):
    def __init__(self, position, maps):
        self.maps = maps
        self.masks = [pygame.mask.from_surface(bitmap) for bitmap in self.maps]
        self._map = maps[0]
        self.map_index = 0
        self._rect = self._map.get_rect()
        self.rect.center = position
        self.count = 0
        self.moves = 0
        self._available = True

    @property
    def available(self):
        return self._available

    @property
    def rect(self):
        return self._rect

    @property
    def mask(self):
        return self.masks[self.map_index]

    @property
    def position(self):
        return Vector2(self.rect.center)

    @position.setter
    def position(self, vector):
        self.rect.center = vector

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
        self.map_index = (self.map_index + 1) % 4
        self._map = self.maps[self.map_index]

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderexplosion(self, explosion, fleets):
        pass

    def interact_with_invaderfleet(self, invader_fleet, fleets):
        pass

    def interact_with_invaderplayer(self, player, fleets):
        self.die_on_collision(player, fleets)

    def die_on_collision(self, flyer, fleets):
        if self.colliding(flyer):
            fleets.remind_me(self, self.die, fleets)

    def interact_with_invadershot(self, shot, fleets):
        pass

    def interact_with_playerexplosion(self, explosion, fleets):
        pass

    def interact_with_playershot(self, shot, fleets):
        self.die_on_collision(shot, fleets)

    def interact_with_shield(self, shield, fleets):
        self.die_on_collision(shield, fleets)

    def interact_with_shotcontroller(self, controller, fleets):
        pass

    def interact_with_shotexplosion(self, explosion, fleets):
        pass

    def interact_with_topbumper(self, top_bumper, fleets):
        pass

    def die(self, fleets):
        self._available = True
        fleets.remove(self)

    def colliding(self, invaders_flyer):
        collider = Collider(self, invaders_flyer)
        return collider.colliding()

    def interact_with(self, other, fleets):
        other.interact_with_invadershot(self, fleets)

    def draw(self, screen):
        screen.blit(self._map, self.rect)

    def tick(self, delta_time, fleets):
        pass
