from pygame import Vector2

import u
from bitmap_maker import BitmapMaker
from flyer import InvadersFlyer


class ReservePlayer(InvadersFlyer):
    def __init__(self, reserve_number):
        self.reserve_number = reserve_number
        maker = BitmapMaker.instance()
        players = maker.players  # one turret, two explosions
        self.player = players[0]
        self._rect = self.player.get_rect()
        half_width = self.rect.width / 2
        left = 64 + half_width
        self.rect.center = Vector2(left, u.SCREEN_SIZE - 16)

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return self._rect

    def draw(self, screen):
        pass

    def interact_with(self, other, fleets):
        pass

    def interact_with_bumper(self, bumper, fleets):
        pass

    def interact_with_invaderfleet(self, fleet, fleets):
        pass

    def interact_with_invaderplayer(self, player, fleets):
        pass

    def interact_with_invadershot(self, shot, fleets):
        pass

    def interact_with_playerexplosion(self, explosion, fleets):
        pass

    def interact_with_playershot(self, shot, fleets):
        pass

    def interact_with_invaderexplosion(self, explosion, fleets):
        pass

    def interact_with_shield(self, shield, fleets):
        pass

    def interact_with_shotcontroller(self, controller, fleets):
        pass

    def interact_with_shotexplosion(self, bumper, fleets):
        pass

    def interact_with_topbumper(self, top_bumper, fleets):
        pass

    def tick(self, delta_time, fleets):
        pass
