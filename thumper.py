

class Thumper:
    def __init__(self, b1, b2):
        self._longest_time_between_beats = 30 / 60
        self._shortest_time_between_beats = 8 / 60
        self._delay_before_shortening_beat_time = 127 / 60
        self._amount_to_shorten_beat_time = 1 / 60
        self._time_between_beats = 0
        self._time_since_last_beat = 0
        self._time_since_last_decrement = 0
        self.b1 = b1
        self.b2 = b2
        self.reset()

    def reset(self):
        self._time_between_beats = self._longest_time_between_beats
        self._time_since_last_decrement = 0
        self._time_since_last_beat = 0

    def tick(self, delta_time):
        if self.it_is_time_to_beat(delta_time):
            self.play_and_reset_beat()
        if self.it_is_time_to_speed_up_beats(delta_time):
            self.speed_up_beats()

    def it_is_time_to_beat(self, delta_time):
        self._time_since_last_beat += delta_time
        return self._time_since_last_beat >= self._time_between_beats

    def play_and_reset_beat(self):
        self._time_since_last_beat = 0
        self.b1()
        self.b1, self.b2 = self.b2, self.b1

    def it_is_time_to_speed_up_beats(self, delta_time):
        self._time_since_last_decrement += delta_time
        return self._time_since_last_decrement >= self._delay_before_shortening_beat_time

    def speed_up_beats(self):
        self._time_since_last_decrement = 0
        self._time_between_beats = max(
            self._time_between_beats - self._amount_to_shorten_beat_time,
            self._shortest_time_between_beats)
