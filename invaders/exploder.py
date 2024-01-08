from invaders.generic_explosion import GenericExplosion
from sounds import player
import u


class Exploder():
    @classmethod
    def explode_invader(self, position, fleets):
        invader_explosion_sound = "invaderkilled"
        explosion = GenericExplosion.invader_explosion(position, 0.125)
        Exploder().explode(position, invader_explosion_sound, explosion, fleets)

    @classmethod
    def explode_player(self, position, fleets):
        player_explosion_sound = "explosion"
        explosion = GenericExplosion.player_explosion(position, 1.0)
        Exploder().explode(position, player_explosion_sound, explosion, fleets)

    @classmethod
    def explode_saucer(self, position, fleets):
        saucer_explosion_sound = "ufo_highpitch"
        explosion = GenericExplosion.saucer_explosion(position, 0.5)
        Exploder().explode(position, saucer_explosion_sound, explosion, fleets)

    @staticmethod
    def explode(position, sound, explosion, fleets):
        frac = u.screen_fraction(position)
        player.play_stereo(sound, frac)
        fleets.append(explosion)
