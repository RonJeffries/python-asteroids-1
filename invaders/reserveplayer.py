from flyer import InvadersFlyer
from invaders.explosion_mixin import ExplosionMixin
from invaders.sprite import SpritelyMixin, Sprite
from pygame import Vector2
import u


class ReservePlayer(ExplosionMixin, SpritelyMixin, InvadersFlyer):
    @classmethod
    def invalid(cls):
        return cls(-666)

    def __init__(self, reserve_number=0):
        self._sprite = Sprite.player()
        position_in_row = reserve_number * (5 * self.rect.width // 4)
        x = u.INVADER_PLAYER_LEFT + position_in_row
        self.position = Vector2(x, u.RESERVE_PLAYER_Y)
        self.reserve_number = reserve_number

    @property
    def is_valid(self):
        return self.reserve_number >= 0

    # def __gt__(self, other):
    #     return self.reserve_number > other.reserve_number

    def interact_with(self, other, fleets):
        other.interact_with_reserveplayer(self, fleets)

    def interact_with_destructor(self, destructor, fleets):
        self.explode(fleets)

    def rightmost_of(self, other_player):
        return other_player if other_player.reserve_number > self.reserve_number else self
