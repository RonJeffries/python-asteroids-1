import u
from game_over import GameOver
from ship import Ship
from signal import Signal


class SinglePlayerShipProvider:
    def __init__(self, number_of_ships):
        self._ships = number_of_ships

    def add_ship(self, _player):
        self._ships += 1

    def ships_available(self, _player):
        return self._ships

    def provide(self):
        if self._ships:
            self._ships -= 1
            return [Ship(u.CENTER), Signal(u.PLAYER_ZERO)]
        else:
            return []