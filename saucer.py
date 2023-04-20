# Saucer


class Saucer:
    def __init__(self, position=None):
        if position is not None: self.position = position
        self.score_list = [0, 0, 0]
        self.radius = 20

    def destroyed_by(self, attacker, saucers):
        if self in saucers: saucers.remove(self)

    def score_against(self, _):
        return 0