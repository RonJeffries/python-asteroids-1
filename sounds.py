import pygame.mixer


class Sounds:
    def __init__(self):
        self.catalog = {}

    def init_sounds(self):
        self.add_sound("accelerate", "sounds/thrust.wav", 0.5)

    def add_sound(self, name, file, volume=1.0):
        if not pygame.mixer.get_init():
            return
        sound = pygame.mixer.Sound(file)
        sound.set_volume(volume)
        # sound.fadeout(150)
        print(name, sound.get_length())
        self.catalog[name] = sound

    def play(self, name):
        if name in self.catalog:
            sound = self.catalog[name]
            count = sound.get_num_channels()
            if count == 0:
                self.catalog[name].play()



player = Sounds()