

class TonePlayer:
    def __init__(self):
        self._tones = ("fastinvader4", "fastinvader1", "fastinvader2", "fastinvader3")
        self._tone_index = 3
        
    def next_tone(self):
        self._tone_index = (self._tone_index + 1) % 4
        return self._tones[self._tone_index]
