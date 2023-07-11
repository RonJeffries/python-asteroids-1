import u
from ship import Ship
from signal import Signal
from abc import ABC, abstractmethod


class ShipProvider(ABC):
    @abstractmethod
    def add_ship(self, _player: int):
        pass

    @abstractmethod
    def provide(self) -> list[Ship|Signal]:
        pass

    @abstractmethod
    def ships_available(self, _player:int) -> int:
        pass

    @abstractmethod
    def testing_set_ships_remaining(self, counts: list[int]):
        pass


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

    def testing_set_ships_remaining(self, counts):
        self._ships = counts[0]


class TwoPlayerShipProvider:
    def __init__(self, number_of_ships):
        self._current_player = 1
        self._ships = [number_of_ships, number_of_ships]

    def add_ship(self, player):
        self._ships[player] += 1

    def ships_available(self, player):
        return self._ships[player]

    def provide(self):
        self.switch_players()
        if self._ships[self._current_player]:
            return self.ship_for_player(self._current_player)
        else:
            self.switch_players()
            if self._ships[self._current_player]:
                return self.ship_for_player(self._current_player)
            else:
                return []

    def ship_for_player(self, player):
        self._ships[player] -= 1
        return [Ship(u.CENTER), Signal(player)]

    def switch_players(self):
        self._current_player = (self._current_player + 1) % 2

    def testing_set_ships_remaining(self, counts):
        self._ships = counts
