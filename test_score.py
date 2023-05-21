from fleets import Fleets
from score import Score


class ScoreKeeper:
    def __init__(self):
        self.score = 0

    def interact_with_score(self, score, fleets):
        self.score += score.score


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
        