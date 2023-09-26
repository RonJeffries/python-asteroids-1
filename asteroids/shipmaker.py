from asteroids.game_over import GameOver
from asteroids.shipprovider import SinglePlayerShipProvider, TwoPlayerShipProvider
from flyer import AsteroidFlyer
from sounds import player
from core.timer import Timer
import u


class ShipMaker(AsteroidFlyer):

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

    def __init__(self, number_of_players):
        if number_of_players == 1:
            self._provider = SinglePlayerShipProvider(u.SHIPS_PER_QUARTER)
        else:
            self._provider = TwoPlayerShipProvider(u.SHIPS_PER_QUARTER)
        self._current_player = number_of_players - 1  # trust me
        self._timer = Timer(u.SHIP_EMERGENCE_TIME)
        self._game_over = False
        self._need_ship = True
        self._safe_to_emerge = False

    def ships_remaining(self, player_number):
        return self._provider.ships_remaining(player_number)

    def testing_set_ships_remaining(self, ships):
        self._provider.testing_set_ships_remaining(ships)

    def add_ship(self, player_identifier):
        self._provider.add_ship(player_identifier)
        player.play("extra_ship")

    def begin_interactions(self, fleets):
        self._game_over = False
        self._need_ship = True
        self._safe_to_emerge = True

    def interact_with_asteroid(self, asteroid, fleets):
        self._safe_to_emerge = self._safe_to_emerge and asteroid.is_safe_for_emergence()

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
        self.rez_available_ship(fleets)
        return True

    def rez_available_ship(self, fleets):
        to_append = self._provider.provide()
        if to_append:
            for flyer in to_append:
                fleets.append(flyer)
        else:
            fleets.append(GameOver())
            self._game_over = True

    def interact_with(self, other, fleets):
        other.interact_with_shipmaker(self, fleets)

    def draw(self, screen):
        pass
