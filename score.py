from flyer import Flyer

class Score(Flyer):

    @classmethod
    def should_interact_with(cls):
        from scorekeeper import ScoreKeeper
        return [ScoreKeeper]

    def __init__(self, score):
        self.score = score

    def draw(self, screen):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_score(self, fleets)

    def interact_with_asteroid(self, asteroid, fleets):
        pass

    def interact_with_explosion(self, explosion, fleets):
        pass

    def interact_with_fragment(self, fragment, fleets):
        pass

    def interact_with_missile(self, missile, fleets):
        pass

    def interact_with_saucer(self, saucer, fleets):
        pass

    def interact_with_ship(self, ship, fleets):
        pass

    def interact_with_scorekeeper(self, scorekeeper, fleets):
        fleets.remove(self)

    def tick(self, delta_time, fleets):
        pass
