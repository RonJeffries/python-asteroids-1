# Collider
import itertools


class Interactor:
    def __init__(self, fleets):
        self.fleets = fleets

    def perform_interactions(self):
        self.fleets.begin_interactions()
        self.interact_all_pairs()
        self.fleets.end_interactions()

    def interact_all_pairs(self):
        for target, attacker in self.all_pairs():
            self.interact_one_pair(target, attacker)

    def all_pairs(self):
        return itertools.combinations(self.fleets.all_objects, 2)

    def interact_one_pair(self, target, attacker):
        attacker.interact_with(target, self.fleets)
        target.interact_with(attacker, self.fleets)
