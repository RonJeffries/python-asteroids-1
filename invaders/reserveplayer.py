from flyer import InvadersFlyer
from invaders.bitmap_maker import BitmapMaker
from pygame import Vector2
import u
from invaders.player_explosion import PlayerExplosion
from invaders.sprite import Spritely, Sprite
from sounds import player


class ReservePlayer(Spritely, InvadersFlyer):
    def __init__(self, reserve_number=0):
        self._sprite = Sprite.player()
        x = u.INVADER_PLAYER_LEFT + reserve_number*(5*self.rect.width//4)
        self.position = Vector2(x, u.RESERVE_PLAYER_Y)
        self.reserve_number = reserve_number

    def __gt__(self, other):
        return self.reserve_number > other.reserve_number

    def rightmost_of(self, another_reserve_player):
        return max(self, another_reserve_player)

    def interact_with(self, other, fleets):
        other.interact_with_reserveplayer(self, fleets)

# COMMON ELEMENTS

    def interact_with_destructor(self, destructor, fleets):
        self.hit_by_something(fleets)

    def hit_by_something(self, fleets):
        frac = self.x_fraction()
        player.play_stereo("explosion", frac)
        fleets.append(PlayerExplosion(self.position))
        fleets.remove(self)

    def x_fraction(self):
        x = self.position.x - u.INVADER_PLAYER_LEFT
        total_width = u.INVADER_PLAYER_RIGHT - u.INVADER_PLAYER_LEFT
        return x / total_width
