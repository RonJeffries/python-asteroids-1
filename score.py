from flyer import AsteroidFlyer


class Score(AsteroidFlyer):
    def __init__(self, score):
        self.score = score

    @classmethod
    def should_interact_with(cls):
        from scorekeeper import ScoreKeeper
        return [ScoreKeeper]

    def interact_with(self, other, fleets):
        other.interact_with_score(self, fleets)

    def interact_with_scorekeeper(self, scorekeeper, fleets):
        fleets.remove(self)
