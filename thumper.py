from flyer import AsteroidFlyer
from sounds import player


class Thumper(AsteroidFlyer):

    def interact_with_fragment(self, fragment, fleets):
        pass

    def interact_with_gameover(self, game_over, fleets):
        pass

    def interact_with_saucermaker(self, saucermaker, fleets):
        pass

    def interact_with_score(self, score, fleets):
        pass

    def interact_with_scorekeeper(self, scorekeeper, fleets):
        pass

    def interact_with_shipmaker(self, shipmaker, fleets):
        pass

    def interact_with_signal(self, signal, fleets):
        pass

    def interact_with_thumper(self, thumper, fleets):
        pass

    def interact_with_wavemaker(self, wavemaker, fleets):
        pass

    def __init__(self, first_action=None, second_action=None):
        self._longest_time_between_beats = 30 / 60
        self._shortest_time_between_beats = 8 / 60
        self._delay_before_shortening_beat_time = 127 / 60
        self._amount_to_shorten_beat_time = 1 / 60
        self._time_between_beats = 0
        self._time_since_last_beat = 0
        self._time_since_last_decrement = 0
        self.current_action = first_action if first_action else self.play_beat_1
        self.next_action = second_action if second_action else self.play_beat_2
        self._saw_ship = False
        self._saw_asteroids = False
        self.reset()

    @staticmethod
    def play_beat_1():
        player.play("beat1")

    @staticmethod
    def play_beat_2():
        player.play("beat2")

    def begin_interactions(self, fleets):
        self._saw_ship = False
        self._saw_asteroids = False

    def draw(self, screen):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_thumper(self, fleets)

    def interact_with_asteroid(self, asteroid, fleets):
        self._saw_asteroids = True

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        self._saw_ship = True

    def reset(self):
        self._time_between_beats = self._longest_time_between_beats
        self._time_since_last_decrement = 0
        self._time_since_last_beat = 0

    def tick(self, delta_time, fleets):
        if self._saw_ship and self._saw_asteroids:
            if self.it_is_time_to_beat(delta_time):
                self.play_and_reset_beat()
            if self.it_is_time_to_speed_up_beats(delta_time):
                self.speed_up_beats()
        else:
            self.reset()

    def it_is_time_to_beat(self, delta_time):
        self._time_since_last_beat += delta_time
        return self._time_since_last_beat >= self._time_between_beats

    def play_and_reset_beat(self):
        self._time_since_last_beat = 0
        self.current_action()
        self.current_action, self.next_action = self.next_action, self.current_action

    def it_is_time_to_speed_up_beats(self, delta_time):
        self._time_since_last_decrement += delta_time
        return self._time_since_last_decrement >= self._delay_before_shortening_beat_time

    def speed_up_beats(self):
        self._time_since_last_decrement = 0
        self._time_between_beats = max(
            self._time_between_beats - self._amount_to_shorten_beat_time,
            self._shortest_time_between_beats)
