# Collider
import itertools


class Interactor:
    def __init__(self, fleets):
        self.fleets = fleets

    @property
    def testing_only_score(self):
        return self.fleets.testing_only_score

    def perform_interactions(self):
        self.fleets.begin_interactions()
        for target, attacker in itertools.combinations(self.fleets.all_objects, 2):
            self.interact_one_pair(target, attacker)
        self.fleets.end_interactions()

    def interact_one_pair(self, target, attacker):
        attacker.interact_with(target, self.fleets)
        target.interact_with(attacker, self.fleets)
