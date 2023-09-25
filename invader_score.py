from flyer import InvadersFlyer


class InvaderScore(InvadersFlyer):
    def __init__(self, score):
        self.score = score

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def interact_with(self, other, fleets):
        other.interact_with_invaderscore(self, fleets)

    def interact_with_invaderscorekeeper(self, keeper, fleets):
        fleets.remove(self)


class InvaderScoreKeeper(InvadersFlyer):
    def __init__(self):
        self.total_score = 0

    @property
    def mask(self):
        return None

    @property
    def rect(self):
        return None

    def interact_with(self, other, fleets):
        other.interact_with_invaderscorekeeper(self, fleets)

    def interact_with_invaderscore(self, score, fleets):
        self.total_score += score.score
        print("Score:", self.total_score)
