from invaders.generic_explosion import GenericExplosion
from sounds import player
import u


class ExplosionMixin:
    def explode_player(self, fleets):
        player_explosion_sound = "explosion"
        explosion = GenericExplosion.player_explosion(self.position, 1.0)
        self.make_the_explosion(player_explosion_sound, explosion, fleets)

    def explode_saucer(self, fleets):
        saucer_explosion_sound = "ufo_highpitch"
        explosion = GenericExplosion.saucer_explosion(self.position, 0.5)
        self.make_the_explosion(saucer_explosion_sound, explosion, fleets)

    def make_the_explosion(self, player_explosion_sound, explosion, fleets):
        frac = u.screen_fraction(self.position)
        player.play_stereo(player_explosion_sound, frac)
        fleets.append(explosion)
        fleets.remove(self)