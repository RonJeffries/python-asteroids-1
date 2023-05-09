# Collider
import itertools


class Collider:
    def __init__(self, fleets):
        self.fleets = fleets
        self.score = 0

    def check_collisions(self):
        for pair in itertools.combinations(self.fleets.colliding_fleets, 2):
            self.check_individual_collisions(pair[0], pair[1])
        return self.score

    def check_individual_collisions(self, attackers, targets):
        for target in targets.flyers.copy():
            for attacker in attackers.flyers.copy():
                if self.mutual_destruction(target, targets, attacker, attackers):
                    break

    def mutual_destruction(self, target, targets, attacker, attackers):
        if self.within_range(target, attacker):
            self.score += target.score_for_hitting(attacker)
            self.score += attacker.score_for_hitting(target)
            attacker.destroyed_by(target, attackers, self.fleets)
            target.destroyed_by(attacker, targets, self.fleets)
            return True
        else:
            return False

    @staticmethod
    def within_range(target, attacker):
        in_range = target.radius + attacker.radius
        dist = target.position.distance_to(attacker.position)
        return dist <= in_range

    




