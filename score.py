from flyer import AsteroidFlyer

class Score(AsteroidFlyer):

    def interact_with_fragment(self, fragment, fleets):
        pass

    def interact_with_gameover(self, game_over, fleets):
        pass

    def interact_with_saucermaker(self, saucermaker, fleets):
        pass

    def interact_with_score(self, score, fleets):
        pass

    def interact_with_shipmaker(self, shipmaker, fleets):
        pass

    def interact_with_signal(self, signal, fleets):
        pass

    def interact_with_thumper(self, thumper, fleets):
        pass

    def interact_with_wavemaker(self, wavemaker, fleets):
        pass

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
