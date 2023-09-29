import pygame

from invaders.bitmap_maker import BitmapMaker
from flyer import InvadersFlyer


class ShotExplosion(InvadersFlyer):
    def interact_with_playermaker(self, maker, fleets):
        pass

    def interact_with_timecapsule(self, capsule, fleets):
        pass

    def __init__(self, position):
        self.position = position
        maker = BitmapMaker()
        self.image = maker.player_shot_explosion
        self._mask = pygame.mask.from_surface(self.image)
        self._rect = self.image.get_rect()
        self.time = 0.125

    @property
    def mask(self):
        return self._mask

    @property
    def rect(self):
        return self._rect

    def tick(self, delta_time, fleets):
        self.time -= delta_time
        if self.time < 0:
            fleets.remove(self)

    def draw(self, screen):
        self.rect.center = self.position
        screen.blit(self.image, self.rect)

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderexplosion(self, explosion, fleets):
        pass

    def interact_with_invaderfleet(self, bumper, fleets):
        pass

    def interact_with_invaderplayer(self, bumper, fleets):
        pass

    def interact_with_invadershot(self, shot, fleets):
        pass

    def interact_with_playerexplosion(self, _explosion, _fleets):
        pass

    def interact_with_playershot(self, bumper, fleets):
        pass

    def interact_with_roadfurniture(self, shield, fleets):
        pass

    def interact_with_shotcontroller(self, controller, fleets):
        pass

    def interact_with_shotexplosion(self, bumper, fleets):
        pass

    def interact_with_topbumper(self, top_bumper, fleets):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_shotexplosion(self, fleets)
