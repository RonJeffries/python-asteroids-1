from flyer import InvadersFlyer
from invaders.bitmap_maker import BitmapMaker
from pygame import Vector2
import u


class ReservePlayer(InvadersFlyer):
    def __init__(self, reserve_number):
        self.reserve_number = reserve_number
        maker = BitmapMaker.instance()
        players = maker.players  # one turret, two explosions
        self.player = players[0]
        self._rect = self.player.get_rect()
        half_width = self.rect.width / 2
        left = 64 + half_width
        x = left + reserve_number*(5*self._rect.width//4)
        self.rect.center = Vector2(x, u.RESERVE_PLAYER_Y)

    def __gt__(self, other):
        return self.reserve_number > other.reserve_number

    def rightmost_of(self, another_reserve_player):
        return max(self, another_reserve_player)

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return self._rect

    def draw(self, screen):
        screen.blit(self.player, self.rect)

    def interact_with(self, other, fleets):
        other.interact_with_reserveplayer(self, fleets)

    def interact_with_destructor(self, destructor, fleets):
        fleets.remove(self)

    def tick(self, delta_time, fleets):
        pass

