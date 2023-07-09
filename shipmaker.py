import u
from flyer import Flyer
from game_over import GameOver
from ship import Ship
from signal import Signal
from sounds import player
from timer import Timer


class ShipMaker(Flyer):

    def __init__(self, number_of_players):
        self._ships_remaining = []
        for _ in range(0, number_of_players):
            self._ships_remaining.append(u.SHIPS_PER_QUARTER)
        self._current_player_number = 0
        self._timer = Timer(u.SHIP_EMERGENCE_TIME)
        self._game_over = False
        self._need_ship = True
        self._safe_to_emerge = False

    def ships_remaining(self, player_number):
        return self._ships_remaining[player_number]

    def testing_set_ships_remaining(self, ships):
        self._ships_remaining[0] = ships

    def add_ship(self):
        self._ships_remaining[self._current_player_number] += 1
        player.play("extra_ship")

    def begin_interactions(self, fleets):
        self._game_over = False
        self._need_ship = True
        self._safe_to_emerge = True

    def interact_with_asteroid(self, asteroid, fleets):
        if asteroid.position.distance_to(u.CENTER) < u.SAFE_EMERGENCE_DISTANCE:
            self._safe_to_emerge = False

    def interact_with_missile(self, missile, fleets):
        self._safe_to_emerge = False

    def interact_with_saucer(self, saucer, fleets):
        self._safe_to_emerge = False

    def interact_with_ship(self, ship, fleets):
        self._need_ship = False

    def tick(self, delta_time, fleets):
        if self._need_ship and not self._game_over:
            self._timer.tick(delta_time, self.create_ship, fleets)

    def create_ship(self, fleets):
        if not self._safe_to_emerge:
            return False
        if self._ships_remaining[self._current_player_number] > 0:
            self._ships_remaining[self._current_player_number] -= 1
            fleets.append(Ship(u.CENTER))
            fleets.append(Signal(self._current_player_number))
            self._current_player_number = (self._current_player_number + 1) % len(self._ships_remaining)
        else:
            fleets.append(GameOver())
            self._game_over = True
        return True

    def interact_with(self, other, fleets):
        other.interact_with_shipmaker(self, fleets)

    def draw(self, screen):
        pass
