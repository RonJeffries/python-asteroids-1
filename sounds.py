
from asteroids.movable_location import MovableLocation
import pygame.mixer


class Sounds:
    def __init__(self):
        self.catalog = {}
        self.channels = {}

    def init_sounds(self):
        self.add_sound("accelerate", "sounds/thrust.wav", 0.5)
        self.add_sound("bang_large", "sounds/bangLarge.wav", 0.5)
        self.add_sound("bang_medium", "sounds/bangMedium.wav", 0.5)
        self.add_sound("bang_small", "sounds/bangSmall.wav", 0.5)
        self.add_sound("beat1", "sounds/beat1.wav", 0.5)
        self.add_sound("beat2", "sounds/beat2.wav", 0.5)
        self.add_sound("extra_ship", "sounds/extraShip.wav", 0.5)
        self.add_sound("fire", "sounds/fire.wav", 0.5)
        self.add_sound("saucer_big", "sounds/saucerBig.wav", 0.3)
        self.add_sound("saucer_small", "sounds/saucerSmall.wav", 0.3)

        self.add_sound("explosion", "sounds/explosion.wav", 0.1)
        self.add_sound("fastinvader1", "sounds/fastinvader1.wav", 0.1)
        self.add_sound("fastinvader2", "sounds/fastinvader2.wav", 0.1)
        self.add_sound("fastinvader3", "sounds/fastinvader3.wav", 0.1)
        self.add_sound("fastinvader4", "sounds/fastinvader4.wav", 0.1)
        self.add_sound("invaderkilled", "sounds/invaderkilled.wav", 0.1)
        self.add_sound("ufo_highpitch", "sounds/ufo_highpitch.wav", 0.1)
        self.add_sound("ufo_lowpitch", "sounds/ufo_lowpitch.wav", 0.1)
        self.add_sound("shoot", "sounds/shoot.wav", 0.1)

    def add_sound(self, name, file, volume=1.0):
        if not pygame.mixer.get_init():
            return
        sound = pygame.mixer.Sound(file)
        sound.set_volume(volume)
        print(name, sound.get_length())
        self.catalog[name] = sound

    def play(self, name, location=None, multi_channel=True):
        frac_right = self.get_stereo_fraction(location)
        self.play_stereo(name, frac_right, multi_channel)

    def play_stereo(self, name, stereo_fraction_right, multi_channel=True):
        try:
            sound = self.catalog[name]
        except KeyError:
            return
        if multi_channel or sound.get_num_channels() == 0:
            self.channels[name] = sound.play()
        try:
            channel = self.channels[name]
            if channel:
                channel.set_volume(1 - stereo_fraction_right, stereo_fraction_right)
        except KeyError:
            pass

    @staticmethod
    def get_stereo_fraction(location: MovableLocation):
        return location.stereo_right() if location else 0.5


player = Sounds()
