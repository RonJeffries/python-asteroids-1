from pygame import Vector2

import u
from flyer import InvadersFlyer


class InvaderShot(InvadersFlyer):
    def __init__(self, position, maps):
        self.maps = maps
        self.map = maps[0]
        self.map_index = 0
        self.rect = self.map.get_rect()
        self.rect.center = position
        self.count = 0

    @property
    def position(self):
        return Vector2(self.rect.center)

    @position.setter
    def position(self, vector):
        self.rect.center = vector

    def update(self, _dt, fleets):
        self.count = (self.count + 1) % 3
        if self.count == 0:
            self.move(fleets)

    def move(self, fleets):
        self.update_map()
        self.position = self.position + Vector2(0, 16)
        if self.position.y >= u.SCREEN_SIZE:
            fleets.remove(self)

    def update_map(self):
        self.map_index = (self.map_index + 1) % 4
        self.map = self.maps[self.map_index]

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderfleet(self, bumper, fleets):
        pass

    def interact_with_invaderplayer(self, bumper, fleets):
        pass

    def interact_with_playershot(self, bumper, fleets):
        pass

    def interact_with(self, other, fleets):
        pass

    def draw(self, screen):
        screen.blit(self.map, self.rect)

    def tick(self, delta_time, fleets):
        pass
