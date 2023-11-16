
from asteroids.movable_location import MovableLocation
import pygame.mixer


class Sounds:
    def __init__(self):
        self.catalog = {}

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
        # print(name, sound.get_length())
        self.catalog[name] = sound

    def play(self, name, location=None, multi_channel=True):
        if name in self.catalog:
            sound = self.catalog[name]
            count = sound.get_num_channels()
            if multi_channel or count == 0:
                chan = self.catalog[name].play()
                if chan:
                    self.set_volume(chan, location)
                # else:
                    # print("channel came back None")
        else:
            print("missing sound", name)

    @staticmethod
    def set_volume(chan, location: MovableLocation):
        if location is None:
            return
        frac_right = location.stereo_right() if location else 0.5
        chan.set_volume(1-frac_right, frac_right)


player = Sounds()
