from flyer import Flyer


class Score(Flyer):
    def __init__(self, score):
        self.score = score

    @staticmethod
    def are_we_colliding(_position, _radius):
        return False

    def draw(self, screen):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_score(self, fleets)

    def interact_with_scorekeeper(self, scorekeeper, fleets):
        fleets.remove_flyer(self)

    def tick(self, delta_time, _fleet, _fleets):
        pass
