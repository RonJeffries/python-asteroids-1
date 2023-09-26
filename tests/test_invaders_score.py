from invaders.bitmap_maker import BitmapMaker
from invaders.invader import Invader
from invaders.invader_score import InvaderScore, InvaderScoreKeeper


class TestInvaderScore:
    def test_exists(self):
        InvaderScore(100)
        InvaderScoreKeeper()

    def test_accumulates(self):
        score = InvaderScore(100)
        keeper = InvaderScoreKeeper()
        assert keeper.total_score == 0
        score.interact_with(keeper, [])
        assert keeper.total_score == 100
        score.interact_with(keeper, [])
        assert keeper.total_score == 200

    def test_score_removes_self(self):
        fleets = []
        score = InvaderScore(100)
        fleets.append(score)
        keeper = InvaderScoreKeeper()
        keeper.interact_with(score, fleets)
        assert not fleets

    def test_invader_scores(self):
        maker = BitmapMaker.instance()
        maps = maker.invaders
        assert Invader(1, 0, maps)._score == 10
        assert Invader(1, 1, maps)._score == 10
        assert Invader(1, 2, maps)._score == 20
        assert Invader(1, 3, maps)._score == 20
        assert Invader(1, 4, maps)._score == 30
