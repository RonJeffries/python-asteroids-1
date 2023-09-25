from fleets import Fleets
from invader_score import InvaderScore, InvaderScoreKeeper


class TestInvaderScore:
    def test_exists(self):
        InvaderScore(100)
        InvaderScoreKeeper()

    def test_accumulates(self):
        score = InvaderScore(100)
        keeper = InvaderScoreKeeper()
        assert keeper.total_score == 0
        keeper.interact_with_invaderscore(score, [])
        assert keeper.total_score == 100
        keeper.interact_with_invaderscore(score,[])
        assert keeper.total_score == 200

    def test_score_removes_self(self):
        fleets = []
        score = InvaderScore(100)
        fleets.append(score)
        keeper = InvaderScoreKeeper()
        score.interact_with_invaderscorekeeper(keeper, fleets)
        assert not fleets
