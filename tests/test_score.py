import u
from fleets import Fleets
from interactor import Interactor
from score import Score
from scorekeeper import ScoreKeeper
from shipmaker import ShipMaker
from signal import Signal


class TestScore:

    def test_keeper_accumulates_score(self):
        fleets = Fleets()
        keeper = ScoreKeeper()
        assert keeper.score == 0
        score = Score(20)
        keeper.interact_with_score(score, fleets)
        assert keeper.score == 20
        score = Score(50)
        keeper.interact_with_score(score, fleets)
        assert keeper.score == 70

    def test_score_saved_in_fleets(self):
        fleets = Fleets()
        score = Score(20)
        fleets.append(score)
        assert score in fleets.all_objects

    def test_score_removed_on_interaction(self):
        fleets = Fleets()
        keeper = ScoreKeeper()
        fleets.append(keeper)
        score = Score(20)
        fleets.append(score)
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        assert keeper.score == 20
        assert score not in fleets.all_objects

    def test_free_ship_every_N_points(self):
        fleets, maker, keeper = self.set_up_free_ship_test()
        free = u.FREE_SHIP_SCORE
        keeper.interact_with_shipmaker(maker, fleets)
        assert keeper.score == 0
        keeper.interact_with_score(Score(100), fleets)
        assert maker.ships_remaining(0) == 0
        assert keeper.score == 100
        keeper.interact_with_score(Score(free), fleets)
        assert keeper.score == 100 + free
        assert maker.ships_remaining(0) == 1

    def test_two_player_free_ship_goes_to_right_ship(self):
        fleets = Fleets()
        fleets.append(keeper := ScoreKeeper())
        fleets.append(maker := ShipMaker(2))
        maker.rez_available_ship(fleets)
        maker.testing_set_ships_remaining(0)
        keeper.interact_with_signal(Signal(0), fleets)
        free = u.FREE_SHIP_SCORE
        keeper.interact_with_shipmaker(maker, fleets)
        assert keeper.score == 0
        keeper.interact_with_score(Score(100), fleets)
        assert maker.ships_remaining(0) == 0
        assert keeper.score == 100
        keeper.interact_with_score(Score(free), fleets)
        assert keeper.score == 100 + free
        assert maker.ships_remaining(0) == 1
        assert maker.ships_remaining(1) == u.SHIPS_PER_QUARTER

    def test_free_ship_moves_fence(self):
        fleets, maker, keeper = self.set_up_free_ship_test()
        free = u.FREE_SHIP_SCORE
        keeper.interact_with_shipmaker(maker, fleets)
        assert keeper.score == 0
        keeper.interact_with_score(Score(100), fleets)
        assert maker.ships_remaining(0) == 0
        keeper.interact_with_score(Score(free - 100), fleets)
        assert maker.ships_remaining(0) == 1
        keeper.interact_with_score(Score(50), fleets)
        assert maker.ships_remaining(0) == 1
        keeper.interact_with_score(Score(free - 50), fleets)
        assert maker.ships_remaining(0) == 2

    def test_free_ship_on_exact_score(self):
        fleets, maker, keeper = self.set_up_free_ship_test()
        free = u.FREE_SHIP_SCORE
        keeper.interact_with_shipmaker(maker, fleets)
        assert keeper.score == 0
        assert maker.ships_remaining(0) == 0
        keeper.interact_with_score(Score(free), fleets)
        assert maker.ships_remaining(0) == 1

    @staticmethod
    def set_up_free_ship_test():
        fleets = Fleets()
        fleets.append(keeper := ScoreKeeper())
        fleets.append(maker := ShipMaker(1))
        maker.testing_set_ships_remaining(0)
        return fleets, maker, keeper
