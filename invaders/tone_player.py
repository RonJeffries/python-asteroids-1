

class TonePlayer:
    _invader_count = [0x32, 0x2B, 0x24, 0x1C, 0x16, 0x11, 0x0D, 0x0A, 0x08, 0x07, 0x06, 0x05, 0x04, 0x03, 0x02, 0x01]
    _delays = [0x34, 0x2E, 0x27, 0x22, 0x1C, 0x18, 0x15, 0x13, 0x10, 0x0E, 0x0D, 0x0C, 0x0B, 0x09, 0x07, 0x05]

    def __init__(self):
        self._tones = ("fastinvader4", "fastinvader1", "fastinvader2", "fastinvader3")
        self._tone_index = 3

    def next_tone(self):
        self._tone_index = (self._tone_index + 1) % 4
        return self._tones[self._tone_index]

    def delay(self, number_of_aliens):
        for invaders, delay in zip(self._invader_count, self._delays):
            if invaders <= number_of_aliens:
                return delay
        return 0x05
