from invaders.generic_explosion import GenericExplosion
from sounds import player
import u


class Exploder():
    @classmethod
    def explode_invader(cls, position, fleets):
        invader_explosion_sound = "invaderkilled"
        explosion = GenericExplosion.invader_explosion(position, 0.125)
        cls.explode(position, invader_explosion_sound, explosion, fleets)

    @classmethod
    def explode_player(cls, position, fleets):
        player_explosion_sound = "explosion"
        explosion = GenericExplosion.player_explosion(position, 1.0)
        cls.explode(position, player_explosion_sound, explosion, fleets)

    @classmethod
    def explode_player_shot(cls, position, fleets):
        shot_sound = ""
        shot_explosion = GenericExplosion.shot_explosion(position, 0.125)
        cls.explode(position, shot_sound, shot_explosion, fleets)

    @classmethod
    def explode_saucer(cls, position, fleets):
        saucer_explosion_sound = "ufo_highpitch"
        explosion = GenericExplosion.saucer_explosion(position, 0.5)
        cls.explode(position, saucer_explosion_sound, explosion, fleets)

    @classmethod
    def explode(cls, position, sound, explosion, fleets):
        frac = u.screen_fraction(position)
        player.play_stereo(sound, frac)
        fleets.append(explosion)
