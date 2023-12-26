from invaders.bitmap_maker import BitmapMaker
from invaders.invader import Invader
from invaders.invader_score import InvaderScore, InvaderScoreKeeper


class TestInvaderScore:
    def test_exists(self):
        InvaderScore(100)
        InvaderScoreKeeper()

    def test_accumulates_only_at_end(self):
        score = InvaderScore(100)
        keeper = InvaderScoreKeeper()
        assert keeper.total_score == 0

        keeper.begin_interactions([])
        score.interact_with(keeper, [])
        assert keeper.total_score == 0
        keeper.end_interactions([])
        assert keeper.total_score == 100

        keeper.begin_interactions([])
        score.interact_with(keeper, [])
        assert keeper.total_score == 100
        keeper.end_interactions([])
        assert keeper.total_score == 200

    def test_can_accumulate_more_than_one(self):
        score = InvaderScore(100)
        keeper = InvaderScoreKeeper()
        assert keeper.total_score == 0
        keeper.begin_interactions([])
        score.interact_with(keeper, [])  # one score
        score.interact_with(keeper, [])  # another score
        assert keeper.total_score == 0
        keeper.end_interactions([])
        assert keeper.total_score == 200

    def test_robot_cannot_score(self):
        score = InvaderScore(100)
        keeper = InvaderScoreKeeper()
        assert keeper.total_score == 0

        keeper.begin_interactions([])
        score.interact_with(keeper, [])
        assert keeper.total_score == 0
        keeper.interact_with_robotplayer(None, [])
        keeper.end_interactions([])
        assert keeper.total_score == 0


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
