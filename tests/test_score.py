from fleets import Fleets
from interactor import Interactor
from score import Score
from scorekeeper import ScoreKeeper


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
        fleets.add_flyer(score)
        assert score in fleets.all_objects

    def test_score_removed_on_interaction(self):
        fleets = Fleets()
        keeper = ScoreKeeper()
        fleets.add_flyer(keeper)
        score = Score(20)
        fleets.add_flyer(score)
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        assert keeper.score == 20
        assert score not in fleets.all_objects
        