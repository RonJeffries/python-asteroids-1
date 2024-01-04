from invaders.generic_explosion import GenericExplosion
from sounds import player
import u


class ExplosionMixin:
    def explode(self, fleets):
        frac = u.screen_fraction(self.position)
        player.play_stereo("explosion", frac)
        explosion = GenericExplosion.player_explosion(self.position, 1.0)
        fleets.append(explosion)
        fleets.remove(self)