from bitmap_maker import BitmapMaker
from fleets import Fleets
from invader import Invader
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

    def test_invader_scores(self):
        maker = BitmapMaker.instance()
        maps = maker.invaders
        assert Invader(1, 0, maps)._score == 100
        assert Invader(1, 1, maps)._score == 100
        assert Invader(1, 2, maps)._score == 200
        assert Invader(1, 3, maps)._score == 200
        assert Invader(1, 4, maps)._score == 300
