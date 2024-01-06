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

    def explode_saucer(self, fleets):
        frac = u.screen_fraction(self.position)
        player.play_stereo("ufo_highpitch", frac, True)
        explosion = GenericExplosion.saucer_explosion(self.position, 0.5)
        fleets.append(explosion)
        fleets.remove(self)