# Collider
import itertools


class Interactor:
    def __init__(self, fleets):
        self.fleets = fleets

    @property
    def score(self):
        return self.fleets.score

    def perform_interactions(self):
        for target, attacker in itertools.combinations(self.fleets.all_objects, 2):
            self.interact_one_pair(target, attacker)
        return self.fleets.score

    def interact_one_pair(self, target, attacker):
        attacker.interact_with(target, self.fleets)
        target.interact_with(attacker, self.fleets)


    




