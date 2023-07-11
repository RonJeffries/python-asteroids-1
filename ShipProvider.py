
class SinglePlayerShipProvider():
    def __init__(self, number_of_ships):
        self._ships = number_of_ships

    def ships_available(self, _player):
        return self._ships
