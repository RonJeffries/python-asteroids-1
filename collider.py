# Collider

class Collider:
    def __init__(self, asteroids, missiles, saucers, ships, game):
        self.asteroids = asteroids
        self.missiles = missiles
        self.saucers = saucers
        self.ships = ships
        self.game = game

    def check_collisions(self):
        self.check_individual_collisions(self.ships, self.asteroids)
        self.check_individual_collisions(self.asteroids, self.missiles)
        self.check_individual_collisions(self.ships, self.missiles)
        return self.game.score

    def check_individual_collisions(self, attackers, targets):
        for target in targets.copy():
            for attacker in attackers.copy():
                if self.mutual_destruction(target, targets, attacker, attackers):
                    break

    def mutual_destruction(self, target, targets, attacker, attackers):
        return self.game.mutual_destruction(target, targets, attacker, attackers)

    




