from flyer import Flyer


class Score(Flyer):
    def __init__(self, score):
        self.score = score

    def are_we_colliding(self, position, radius):
        return False

    def draw(self, screen):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_score(self, fleets)

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_score(self, score, fleets):
        pass

    def interact_with_scorekeeper(self, scorekeeper, fleets):
        fleets.remove_score(self)

    def interact_with_ship(self, ship, fleets):
        pass

    def tick(self, delta_time, _fleet, _fleets):
        pass
