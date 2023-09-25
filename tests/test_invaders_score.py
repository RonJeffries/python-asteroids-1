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
