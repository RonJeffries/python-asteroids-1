from fleets import Fleets
from interactor import Interactor
from score import Score


class ScoreKeeper:
    def __init__(self):
        self.score = 0

    def are_we_colliding(self, position, radius):
        return False

    def interact_with(self, other, fleets):
        other.interact_with_scorekeeper(self, fleets)

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_score(self, score, fleets):
        self.score += score.score

    def interact_with_scorekeeper(self, scorekeeper, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass


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
        fleets.add_score(score)
        assert score in fleets.all_objects

    def test_score_removed_on_interaction(self):
        fleets = Fleets()
        keeper = ScoreKeeper()
        fleets.add_scorekeeper(keeper)
        score = Score(20)
        fleets.add_score(score)
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        assert keeper.score == 20
        assert score not in fleets.all_objects
        