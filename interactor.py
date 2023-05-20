# Collider
import itertools


class Interactor:
    def __init__(self, fleets):
        self.fleets = fleets

    @property
    def score(self):
        return self.fleets.score

    def perform_interactions(self):
        for pair in itertools.combinations(self.fleets.colliding_fleets, 2):
            self.perform_individual_interactions(pair[0], pair[1])
        return self.score

    def perform_individual_interactions(self, attackers, targets):
        for target in targets:
            for attacker in attackers:
                if self.interact_one_pair(target, targets, attacker, attackers):
                    break

    def interact_one_pair(self, target, targets, attacker, attackers):
        attacker.interact_with(target, self.fleets)
        target.interact_with(attacker, self.fleets)
        return self.within_range(target, attacker)

    @staticmethod
    def within_range(target, attacker):
        in_range = target.radius + attacker.radius
        dist = target.position.distance_to(attacker.position)
        return dist <= in_range

    




