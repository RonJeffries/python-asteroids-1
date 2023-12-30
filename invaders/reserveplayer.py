from flyer import InvadersFlyer
from invaders.bitmap_maker import BitmapMaker
from pygame import Vector2
import u
from invaders.player_explosion import PlayerExplosion
from invaders.sprite import Spritely, Sprite


class ReservePlayer(Spritely, InvadersFlyer):
    def __init__(self, reserve_number):
        self._sprite = Sprite.player()
        self.reserve_number = reserve_number
        half_width = self.rect.width / 2
        left = 64 + half_width
        x = left + reserve_number*(5*self.rect.width//4)
        self.rect.center = Vector2(x, u.RESERVE_PLAYER_Y)

    def __gt__(self, other):
        return self.reserve_number > other.reserve_number

    def rightmost_of(self, another_reserve_player):
        return max(self, another_reserve_player)

    def interact_with(self, other, fleets):
        other.interact_with_reserveplayer(self, fleets)

    def interact_with_destructor(self, destructor, fleets):
        fleets.remove(self)
        fleets.append(PlayerExplosion(self.rect.center))

    def tick(self, delta_time, fleets):
        pass

