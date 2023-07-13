from abc import ABC, abstractmethod
from ship import Ship
from signal import Signal
import u


class ShipProvider(ABC):
    @abstractmethod
    def add_ship(self, _player: int):
        pass

    @abstractmethod
    def provide(self) -> list[Ship | Signal]:
        pass

    @abstractmethod
    def ships_remaining(self, _player: int) -> int:
        pass

    @abstractmethod
    def testing_set_ships_remaining(self, counts: list[int]):
        pass


class SinglePlayerShipProvider:
    def __init__(self, number_of_ships):
        self._ships = number_of_ships

    def add_ship(self, _player):
        self._ships += 1

    def ships_remaining(self, _player):
        return self._ships

    def provide(self):
        if self._ships:
            self._ships -= 1
            return [Ship(u.CENTER), Signal(u.PLAYER_ZERO)]
        else:
            return []

    def testing_set_ships_remaining(self, counts):
        self._ships = counts[0]


class TwoPlayerShipProvider:
    def __init__(self, number_of_ships):
        self._current_player_token = u.PLAYER_ONE
        self._ships = {u.PLAYER_ZERO: number_of_ships, u.PLAYER_ONE: number_of_ships}

    def add_ship(self, player_token):
        self._ships[player_token] += 1

    def ships_remaining(self, player_token):
        return self._ships[player_token]

    def provide(self):
        self._switch_players()
        if self._ships[self._current_player_token]:
            return self._ship_for_player(self._current_player_token)
        else:
            self._switch_players()
            if self._ships[self._current_player_token]:
                return self._ship_for_player(self._current_player_token)
            else:
                return []

    def _ship_for_player(self, player_token):
        self._ships[player_token] -= 1
        return [Ship(u.CENTER), Signal(player_token)]

    def _switch_players(self):
        self._current_player_token = u.PLAYER_ONE if self._current_player_token == u.PLAYER_ZERO else u.PLAYER_ZERO

    def testing_set_ships_remaining(self, counts):
        self._ships[u.PLAYER_ZERO] = counts[0]
        self._ships[u.PLAYER_ONE] = counts[1]
