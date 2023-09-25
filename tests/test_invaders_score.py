from invader_score import InvaderScore, InvaderScoreKeeper


class TestInvaderScore:
    def test_exists(self):
        InvaderScore(100)
        InvaderScoreKeeper()